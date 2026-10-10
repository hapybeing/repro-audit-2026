# Pre-registered robustness checks R_a, R_b, R_c for 16_QZNVZ0 (PREREG.md section 3). Agent B.
# Usage: robustness.py <O> <S> rb|rc|ra [max_new_draws]
import numpy as np, pandas as pd, statsmodels.api as sm, sys, os, json, time
O, S, mode = sys.argv[1], sys.argv[2], sys.argv[3]
OUT = os.path.join(O, 'outputs')
d1 = np.load(os.path.join(S, 'design_m1.npz')); X, y, cnt = d1['X'], d1['y'], d1['count']; cols = list(d1['cols'])
PRIM = 'FA_Hispanic/Latino'; SEC = ['FA_Female', 'FA_South', 'International']
ix = {c: cols.index(c) for c in [PRIM] + SEC + ['FA_African']}

def rows_from(res, model, names, extra):
    out = []
    for c in names:
        j = ix[c]
        out.append(dict(check=model, variable=c, estimate=float(res.params[j]), se=float(res.bse[j]),
                        stat=float(res.tvalues[j]), p_value=float(res.pvalues[j]), nobs=int(res.nobs), **extra))
    return out

if mode == 'rb':
    res_rows = []
    for k, label in [(1, 'R_b_model1'), (4, 'R_b_model4')]:
        d = np.load(os.path.join(S, 'design_m%d.npz' % k)); Xk, yk = d['X'], d['y']
        z = (yk - yk.mean()) / yk.std(ddof=1)
        keep = np.abs(z) <= 3
        r = sm.OLS(yk[keep], Xk[keep]).fit()
        names = [PRIM] + SEC if k == 1 else ['FA_African']
        res_rows += rows_from(r, label, names, dict(n_before=int(len(yk)), n_dropped=int((~keep).sum()),
                                                    z_min=float(z.min()), z_max=float(z.max())))
    pd.DataFrame(res_rows).to_csv(os.path.join(OUT, 'R_b_outliers.csv'), index=False, float_format='%.10g')
    print(pd.DataFrame(res_rows).to_string())

elif mode == 'rc':
    note = ''
    try:
        r = sm.GLM(cnt, X, family=sm.families.Poisson()).fit(cov_type='HC1')
        conv = bool(r.converged)
        if not conv:
            note = 'not converged with defaults; rerun maxiter=300'
            r = sm.GLM(cnt, X, family=sm.families.Poisson()).fit(cov_type='HC1', maxiter=300); conv = bool(r.converged)
        rows = []
        for c in [PRIM] + SEC:
            j = ix[c]
            rows.append(dict(check='R_c_poisson_pml_HC1', variable=c, estimate=float(r.params[j]), se=float(r.bse[j]),
                             stat=float(r.tvalues[j]), p_value=float(r.pvalues[j]), nobs=int(r.nobs), converged=conv,
                             iterations=int(r.fit_history['iteration']), note=note))
        pd.DataFrame(rows).to_csv(os.path.join(OUT, 'R_c_poisson.csv'), index=False, float_format='%.10g')
        print(pd.DataFrame(rows).to_string())
    except Exception as e:
        open(os.path.join(OUT, 'R_c_poisson_error.txt'), 'w').write(repr(e)); raise

elif mode == 'ra':
    maxnew = int(sys.argv[4]) if len(sys.argv) > 4 else 1000
    path = os.path.join(OUT, 'R_a_bootstrap_draws.csv')
    done = pd.read_csv(path) if os.path.exists(path) else pd.DataFrame()
    ndone = len(done)
    rng = np.random.default_rng(20261010); n = len(y)
    new = []; t0 = time.time()
    for b in range(1000):
        idx = rng.integers(0, n, n)          # every draw generated in order, so resuming keeps the same stream
        if b < ndone: continue
        if len(new) >= maxnew or time.time() - t0 > 70: break
        r = sm.OLS(y[idx], X[idx]).fit()
        rec = dict(draw=b + 1, rank=int(r.model.rank), rank_deficient=bool(r.model.rank < X.shape[1]))
        for c in [PRIM] + SEC: rec[c] = float(r.params[ix[c]])
        new.append(rec)
        if len(new) % 10 == 0:
            pd.concat([done, pd.DataFrame(new)], ignore_index=True).to_csv(path, index=False, float_format='%.12g')
    allr = pd.concat([done, pd.DataFrame(new)], ignore_index=True)
    allr.to_csv(path, index=False, float_format='%.12g')
    print('draws now', len(allr), 'added', len(new), 'secs', round(time.time() - t0, 1))
    if len(allr) == 1000:
        full = sm.OLS(y, X).fit()
        summ = []
        for c in [PRIM] + SEC:
            v = allr[c].values; est = float(full.params[ix[c]])
            cross = int((v >= 0).sum()) if est < 0 else int((v <= 0).sum())
            summ.append(dict(variable=c, full_sample_B=est, boot_se=float(v.std(ddof=1)), ci_lo=float(np.percentile(v, 2.5)),
                             ci_hi=float(np.percentile(v, 97.5)), n_cross_zero=cross, p_boot=min(2 * cross / 1000, 1.0),
                             n_draws=1000, n_rank_deficient=int(allr['rank_deficient'].sum()), seed=20261010))
        pd.DataFrame(summ).to_csv(os.path.join(OUT, 'R_a_bootstrap_summary.csv'), index=False, float_format='%.10g')
        print(pd.DataFrame(summ).to_string())
