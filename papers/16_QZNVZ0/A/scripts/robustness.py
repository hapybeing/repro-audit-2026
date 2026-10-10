"""Pre-registered robustness checks R_a, R_b, R_c for 16_QZNVZ0 (PREREG.md section 3). Agent A.

Usage: python robustness.py {rb|rc|ra} ; run from the data directory. Writes to $AUDIT_OUT (outputs/).
Estimation sample = the rows results_1 (and results_4) actually used, read from outputs/model1_row_labels.csv
(and model4_row_labels.csv), written by the extraction block appended to the authors' notebook code.
"""
import os, sys, json, time
import numpy as np
import pandas as pd
import statsmodels.api as sm

OUT = os.environ.get("AUDIT_OUT", "outputs")
TOPICS = ['T' + str(i) for i in range(1, 50)]
# Column lists copied from Regression.ipynb cell 4 (Model 1) and cell 7 (Model 4), same order.
M1_COLS = ['Const', 'FA_Female', 'FA_European', 'FA_Asian', 'FA_Slavic', 'FA_Hispanic/Latino', 'FA_African', 'FA_Jewish',
           'FA_Other', 'FA_South', 'Mixed_Gender', 'Cross_Ethnic', 'Cross_Regional', 'International', 'Cited_Outgroup',
           'Team_Size', 'Cited_References', 'FA_Author_Reputation', 'FA_Author_Publication', 'Article_Age',
           'Journal_Prestige', 'FA_Affliation_Weight'] + TOPICS
M4_COLS = ['Const', 'FA_Female', 'FA_European', 'FA_Asian', 'FA_Slavic', 'FA_Hispanic/Latino', 'FA_African', 'FA_Jewish',
           'FA_Other', 'FA_South', 'Mixed_Gender', 'Cross_Ethnic', 'Cross_Regional', 'International', 'Cited_Outgroup',
           'Team_Size', 'Cited_References', 'Article_Age', 'Journal_Prestige', 'FA_Author_Publication',
           'FA_Author_Reputation', 'FA_Affliation_Weight'] + TOPICS
PRIMARY = 'FA_Hispanic/Latino'
SECONDARY = ['FA_Female', 'FA_South', 'International']
EXPECTED_SIGN = {'FA_Hispanic/Latino': -1, 'FA_Female': 1, 'FA_South': -1, 'International': 1, 'FA_African': -1}


def load(cols_needed):
    rt = pd.read_csv('regression_table_anonymous_final.csv', index_col=0,
                     usecols=None)  # same read as the notebook; only the needed columns are kept afterwards
    assert rt.index.is_unique, "index not unique"
    return rt[cols_needed]


def sample(rt, cols, label_file):
    labels = pd.read_csv(os.path.join(OUT, label_file))['row_label']
    sub = rt.loc[labels.values]
    X = sub[cols].astype(float)
    y = np.log10(sub['Citations_Received'].astype(float) + 1)
    assert not X.isna().any().any() and not y.isna().any()
    return sub, X, y


def coef_rows(res, vars_, check, extra=None):
    rows = []
    for v in vars_:
        rows.append(dict(check=check, variable=v, B=float(res.params[v]), SE=float(res.bse[v]),
                         t_or_z=float(res.tvalues[v]), p=float(res.pvalues[v]), nobs=int(res.nobs),
                         **(extra or {})))
    return rows


def run_rb():
    rt = load(list(dict.fromkeys(M1_COLS + M4_COLS + ['Citations_Received'])))
    rows = []
    for model, cols, lf, vars_ in [('model_1', M1_COLS, 'model1_row_labels.csv', [PRIMARY] + SECONDARY),
                                   ('model_4', M4_COLS, 'model4_row_labels.csv', ['FA_African'])]:
        sub, X, y = sample(rt, cols, lf)
        z = (y - y.mean()) / y.std(ddof=1)
        keep = z.abs() <= 3
        res = sm.OLS(y[keep], X[keep]).fit()
        rows += coef_rows(res, vars_, 'R_b_' + model, dict(n_before=len(y), n_dropped=int((~keep).sum()),
                                                            z_min=float(z.min()), z_max=float(z.max())))
    pd.DataFrame(rows).to_csv(os.path.join(OUT, 'R_b_outlier_exclusion.csv'), index=False)
    print(pd.DataFrame(rows).to_string())


def run_rc():
    rt = load(list(dict.fromkeys(M1_COLS + ['Citations_Received'])))
    sub, X, y = sample(rt, M1_COLS, 'model1_row_labels.csv')
    count = sub['Citations_Received'].astype(float)
    note = 'default maxiter'
    try:
        res = sm.GLM(count, X, family=sm.families.Poisson()).fit(cov_type="HC1")
        conv = bool(res.converged)
    except Exception as e:  # pragma: no cover
        conv = False; note = 'default fit raised: %r' % e
    if not conv:
        note += '; not converged, rerun with maxiter=300'
        res = sm.GLM(count, X, family=sm.families.Poisson()).fit(cov_type="HC1", maxiter=300)
        conv = bool(res.converged)
    rows = coef_rows(res, [PRIMARY] + SECONDARY, 'R_c_poisson_pml_HC1',
                     dict(converged=conv, iterations=int(getattr(res, 'fit_history', {}).get('iteration', -1)), note=note))
    pd.DataFrame(rows).to_csv(os.path.join(OUT, 'R_c_poisson.csv'), index=False)
    print(pd.DataFrame(rows).to_string())


def run_ra():
    """Case bootstrap, 1,000 resamples, rng = default_rng(20261010), idx = rng.integers(0, n, n). Resumable."""
    draws_file = os.path.join(OUT, 'R_a_bootstrap_draws.csv')
    rt = load(list(dict.fromkeys(M1_COLS + ['Citations_Received'])))
    sub, X, y = sample(rt, M1_COLS, 'model1_row_labels.csv')
    Xa = X.to_numpy(); ya = y.to_numpy(); n, k = Xa.shape
    ci = {v: M1_COLS.index(v) for v in [PRIMARY] + SECONDARY}
    rng = np.random.default_rng(20261010)
    done = pd.read_csv(draws_file) if os.path.exists(draws_file) else pd.DataFrame()
    start = len(done)
    rows = []
    t0 = time.time()
    for b in range(1000):
        idx = rng.integers(0, n, n)  # always drawn, so the stream is identical on resume
        if b < start:
            continue
        Xb = Xa[idx]; yb = ya[idx]
        beta, _, rank, _ = np.linalg.lstsq(Xb, yb, rcond=None)
        r = dict(draw=b + 1, rank=int(rank), rank_deficient=bool(rank < k))
        for v, j in ci.items():
            r[v] = float(beta[j])
        rows.append(r)
        if len(rows) % 50 == 0 or time.time() - t0 > float(os.environ.get('RA_MAXSEC', '1e9')):
            pd.concat([done, pd.DataFrame(rows)]).to_csv(draws_file, index=False)
            if time.time() - t0 > float(os.environ.get('RA_MAXSEC', '1e9')):
                print('paused at draw', b + 1); return
    pd.concat([done, pd.DataFrame(rows)]).to_csv(draws_file, index=False)
    # full-sample estimate (same sm.OLS as the authors)
    full = sm.OLS(y, X).fit()
    d = pd.read_csv(draws_file)
    assert len(d) == 1000 and list(d['draw']) == list(range(1, 1001))
    summ = []
    for v in [PRIMARY] + SECONDARY:
        s = EXPECTED_SIGN[v]
        bv = d[v].to_numpy()
        n_cross = int((bv >= 0).sum()) if s < 0 else int((bv <= 0).sum())
        summ.append(dict(variable=v, full_sample_B=float(full.params[v]), boot_se=float(bv.std(ddof=1)),
                         ci_lo=float(np.percentile(bv, 2.5)), ci_hi=float(np.percentile(bv, 97.5)),
                         n_cross_zero=n_cross, boot_p=min(2 * n_cross / 1000, 1.0),
                         n_draws=len(d), n_rank_deficient=int(d['rank_deficient'].sum()), seed=20261010))
    pd.DataFrame(summ).to_csv(os.path.join(OUT, 'R_a_bootstrap_summary.csv'), index=False)
    print(pd.DataFrame(summ).to_string())


if __name__ == '__main__':
    {'rb': run_rb, 'rc': run_rc, 'ra': run_ra}[sys.argv[1]]()
