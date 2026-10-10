# Builds results.json for 16_QZNVZ0 agent B from files in outputs/ and the read-only targets.json.
import json, csv, os, math
B = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.dirname(B)
def rd(p): return list(csv.DictReader(open(os.path.join(B, p))))
targets = json.load(open(os.path.join(P, 'targets.json')))
est = {(r['model'], r['variable']): r for r in rd('outputs/regression_estimates.csv')}
src = {'T1': ('results_1', 'FA_Female', 'params', 1), 'T2': ('results_1', 'FA_Hispanic/Latino', 'params', -1),
       'T3': ('results_1', 'FA_South', 'params', -1), 'T4': ('results_1', 'International', 'params', 1),
       'T5': ('results_4', 'FA_African', 'params', -1), 'T6': ('results_1', 'Const', 'nobs', None)}
def rround(x, d):  # round half away from zero
    q = 10 ** d; return math.floor(abs(x) * q + 0.5) / q * (1 if x >= 0 else -1)
out_t = []
for t in targets:
    m, v, f, sign = src[t['id']]; r = est[(m, v)]
    val = float(r[f]); pv = t['paper_value']; dec = t['paper_rounding_decimals']
    if f == 'nobs':
        val = int(round(val)); match = (val == pv); same = abs(val - pv) <= 0.01 * pv
        note = 'statsmodels nobs of results_1'
    else:
        match = rround(val, dec) == pv; p = float(r['pvalues'])
        same = (val * sign > 0) and p < 0.001
        note = f"t = {float(r['tvalues']):.3f}, nonrobust SE = {float(r['bse']):.4f}, p = {p:.3g}"
    ad = val - pv
    out_t.append(dict(id=t['id'], description=t['description'], paper_value=pv, paper_rounding_decimals=dec,
                      reproduced_value=val, source_file='outputs/regression_estimates.csv', abs_diff=ad,
                      rel_diff=ad / abs(pv), match_to_rounding=bool(match), within_5pct=bool(abs(ad / pv) <= 0.05),
                      same_conclusion=bool(same), note=note))
# robustness
ra = {r['variable']: r for r in rd('outputs/R_a_bootstrap_summary.csv')}
p = ra['FA_Hispanic/Latino']
sec = '; '.join(f"{k}: B {float(ra[k]['full_sample_B']):.4f}, CI [{float(ra[k]['ci_lo']):.4f}, {float(ra[k]['ci_hi']):.4f}], crossings {ra[k]['n_cross_zero']}" for k in ['FA_Female','FA_South','International'])
Ra = dict(id='R_a', description='Case bootstrap of Model 1 estimation rows, 1,000 resamples, numpy default_rng(20261010), primary FA_Hispanic/Latino',
          ran=True, estimate=float(p['full_sample_B']),
          se_or_ci=f"bootstrap SE {float(p['boot_se']):.5f}; percentile 95% CI [{float(p['ci_lo']):.5f}, {float(p['ci_hi']):.5f}]",
          p_value=float(p['p_boot']),
          same_direction_and_significance_as_paper=bool(float(p['full_sample_B']) < 0 and float(p['ci_hi']) < 0 and int(p['n_cross_zero']) == 0),
          source_file='outputs/R_a_bootstrap_summary.csv',
          note=f"{p['n_cross_zero']} of 1000 bootstrap B >= 0, so p reported as < 0.001 (p_value field = 2 x share = {p['p_boot']}); rank-deficient resamples {p['n_rank_deficient']}. Secondaries: {sec}. Draws in outputs/R_a_bootstrap_draws.csv.")
rb = rd('outputs/R_b_outliers.csv'); rbm = {(r['check'], r['variable']): r for r in rb}
q = rbm[('R_b_model1', 'FA_Hispanic/Latino')]
secb = '; '.join(f"{k}: B {float(rbm[('R_b_model1',k)]['estimate']):.4f}, p {float(rbm[('R_b_model1',k)]['p_value']):.3g}" for k in ['FA_Female','FA_South','International'])
m4 = rbm[('R_b_model4', 'FA_African')]
Rb = dict(id='R_b', description='Drop |z| > 3 on log10(citations+1) within Model 1 estimation rows, refit Model 1; secondary same within Model 4 for T5',
          ran=True, estimate=float(q['estimate']), se_or_ci=f"nonrobust SE {float(q['se']):.5f}", p_value=float(q['p_value']),
          same_direction_and_significance_as_paper=bool(float(q['estimate']) < 0 and float(q['p_value']) < 0.001),
          source_file='outputs/R_b_outliers.csv',
          note=f"Model 1: {q['n_dropped']} of {q['n_before']} rows dropped (all z > 3; z range {float(q['z_min']):.3f} to {float(q['z_max']):.3f}). Secondaries: {secb}. Model 4 FA_African: B {float(m4['estimate']):.4f}, SE {float(m4['se']):.4f}, p {float(m4['p_value']):.3g}, {m4['n_dropped']} of {m4['n_before']} rows dropped.")
rc = {r['variable']: r for r in rd('outputs/R_c_poisson.csv')}
c = rc['FA_Hispanic/Latino']
secc = '; '.join(f"{k}: {float(rc[k]['estimate']):.4f}, p {float(rc[k]['p_value']):.3g}" for k in ['FA_Female','FA_South','International'])
Rc = dict(id='R_c', description='Poisson PML (sm.GLM Poisson, HC1) of raw Citations_Received on Model 1 regressors, Model 1 estimation rows',
          ran=True, estimate=float(c['estimate']), se_or_ci=f"HC1 SE {float(c['se']):.5f}", p_value=float(c['p_value']),
          same_direction_and_significance_as_paper=bool(float(c['estimate']) < 0 and float(c['p_value']) < 0.001),
          source_file='outputs/R_c_poisson.csv',
          note=f"Converged with statsmodels defaults ({c['iterations']} iterations), n {c['nobs']}. Primary is negative but p is above the pre-registered .001 threshold (p < .01). Secondaries (log scale): {secc}. Scale not comparable with Table 2.")
sv = rd('outputs/saved_notebook_vs_run.csv')
res = dict(paper_id='16_QZNVZ0', agent='B', run_date_ist='2026-10-11', ran=True, could_not_run_reason='',
           targets=out_t, robustness=[Ra, Rb, Rc], bugs=[],
           env_fixes=['diffs/regression_verbatim_extraction_block.diff: the 13 notebook cells were run verbatim as a script (PREREG section 2 step 3, alternative to nbconvert) with an appended block that only writes params, SE, t, p, nobs, adj R2 and summaries to outputs/; no authors line changed. No package version change, no path change (CSV in working directory under its deposited name).'],
           proposed_class='', class_reason='', confidence='', confidence_reason='', time_minutes=None,
           uncertainties=[])
allmatch = all(t['match_to_rounding'] for t in out_t)
res['proposed_class'] = 'A' if allmatch else ('B' if all(t['within_5pct'] and t['same_conclusion'] for t in out_t) else 'D')
res['class_reason'] = ('All six pre-registered Table 2 targets (five coefficients and Model 1 N) are reproduced to the printed rounding by the deposited notebook code run unchanged on deposit version 2.0, with the same sign and p < .001 for every coefficient.'
                       if allmatch else 'See targets.')
res['confidence'] = 'high'
res['confidence_reason'] = (f"Deterministic OLS with no seed; every coefficient, t and N in the authors' saved notebook output matches this run ({sum(r['coef_match']=='True' for r in sv)} of {len(sv)} coefficient rows at 4 decimals, t at 3), so version drift has no effect; A's agreement not seen by B.")
log = open(os.path.join(B, 'LOG.md')).read()
import re
ts = re.findall(r'(\d{2}):(\d{2}) IST', log)
mins = [int(h) * 60 + int(m) for h, m in ts]
res['time_minutes'] = (max(mins) - min(mins)) if mins else None
res['uncertainties'] = [
 'Packages are current releases (pandas 3.0.6, numpy 2.5.3, statsmodels 0.15.0, Python 3.12) rather than the authors 2024 environment (Python 3.11.9, versions not recorded); outputs still match the saved notebook outputs exactly (outputs/saved_notebook_vs_run.csv), so no version effect was seen.',
 'R_c (Poisson PML) gives the primary FA_Hispanic/Latino coefficient negative but with p = %.4f, above the pre-registered .001 threshold, so R_c is recorded as not the same significance; robustness does not change the class.' % float(c['p_value']),
 'Pre-registered inconsistencies confirmed by this run (not targets): Model 2 N is 39,690 in this run (outputs/summary_results_2.txt) against 68,558 printed in Table 2 for Model 2; Model 3 regressor list has no FA_South (Regression.ipynb cell 6). Other printed-vs-saved star and SE differences listed in PREREG were not re-checked against the PDF by B (B did not re-read the paper table; PREREG copy used).',
 'The regression CSV itself cannot be rebuilt from raw Web of Science records (construction code not deposited, as PREREG and DATA_STATEMENT state); the reproduction is of the analysis step only.',
 'The first full run (scripts/regression_verbatim.py) was killed (exit 137) after all outputs and the final print had been written; peak RSS reported 608 MB, machine had about 0.5 to 2.5 GB available at the time (shared). The outputs were checked complete (568 lines of estimates for 8 models, all summaries).',
 'Visualizations.ipynb (figures) was not run; it produces no pre-registered target.',
]
json.dump(res, open(os.path.join(B, 'results.json'), 'w'), indent=1)
print(json.dumps({k: res[k] for k in ['proposed_class','time_minutes']}), [(t['id'], t['paper_value'], t['reproduced_value'], t['match_to_rounding']) for t in out_t])
print([(r['id'], r['estimate'], r['p_value'], r['same_direction_and_significance_as_paper']) for r in res['robustness']])
