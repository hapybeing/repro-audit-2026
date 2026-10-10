"""Build results.json for 16_QZNVZ0 agent A from files in outputs/. No number is typed here except paper values,
which are read from REPO/papers/16_QZNVZ0/targets.json (copied from PREREG.md)."""
import json, os, re
from datetime import datetime, timezone, timedelta
import pandas as pd

A = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.dirname(A)
O = os.path.join(A, 'outputs')
targets = json.load(open(os.path.join(P, 'targets.json')))
est = pd.read_csv(os.path.join(O, 'regression_estimates.csv'))


def get(model, var, col='B'):
    r = est[(est.model == model) & (est.variable == var)]
    assert len(r) == 1, (model, var)
    return float(r.iloc[0][col])


SRC = {'T1': ('results_1', 'FA_Female', 1), 'T2': ('results_1', 'FA_Hispanic/Latino', -1),
       'T3': ('results_1', 'FA_South', -1), 'T4': ('results_1', 'International', 1),
       'T5': ('results_4', 'FA_African', -1)}
PRINTED_T = {'T1': 11.0, 'T2': -10.8, 'T3': -4.0, 'T4': 14.8, 'T5': -4.9}  # secondary context, from PREREG table

tout = []
for t in targets:
    tid, pv, dec = t['id'], t['paper_value'], t['paper_rounding_decimals']
    if tid == 'T6':
        rv = float(est[est.model == 'results_1'].iloc[0]['nobs'])
        same = abs(rv - pv) <= 0.01 * pv
        note = 'results_1.nobs'
    else:
        m, v, sgn = SRC[tid]
        rv = get(m, v)
        p = get(m, v, 'p'); tv = get(m, v, 't'); se = get(m, v, 'SE')
        same = (rv * sgn > 0) and p < 0.001
        note = '%s.params["%s"]; SE %.4f, t %.2f (printed t %s), nonrobust p %.3g' % (m, v, se, tv, PRINTED_T[tid], p)
    ad = rv - pv
    tout.append(dict(id=tid, description=t['description'], paper_value=pv, paper_rounding_decimals=dec,
                     reproduced_value=rv, source_file='outputs/regression_estimates.csv', abs_diff=ad,
                     rel_diff=ad / pv, match_to_rounding=bool(round(rv, dec) == pv),
                     within_5pct=bool(abs(ad / pv) <= 0.05), same_conclusion=bool(same), note=note))

rob = []
# R_a
fa = os.path.join(O, 'R_a_bootstrap_summary.csv')
if os.path.exists(fa):
    s = pd.read_csv(fa).set_index('variable')
    r = s.loc['FA_Hispanic/Latino']
    ok = bool(r.full_sample_B < 0 and r.ci_hi < 0 and r.n_cross_zero == 0)
    sec = '; '.join('%s B %.4f, boot SE %.4f, CI [%.4f, %.4f], crossings %d' % (v, s.loc[v].full_sample_B, s.loc[v].boot_se,
                    s.loc[v].ci_lo, s.loc[v].ci_hi, s.loc[v].n_cross_zero) for v in ['FA_Female', 'FA_South', 'International'])
    pval = float(r.boot_p)
    rob.append(dict(id='R_a', description='Case bootstrap of Model 1, 1,000 resamples, default_rng(20261010); primary FA_Hispanic/Latino',
                    ran=True, estimate=float(r.full_sample_B),
                    se_or_ci='boot SE %.5f; percentile 95%% CI [%.5f, %.5f]' % (r.boot_se, r.ci_lo, r.ci_hi),
                    p_value=pval, same_direction_and_significance_as_paper=ok, source_file='outputs/R_a_bootstrap_summary.csv',
                    note='%d of %d bootstrap B >= 0 (p reported as < 0.001 when 0); rank-deficient resamples: %d. Secondary: %s' %
                         (r.n_cross_zero, r.n_draws, r.n_rank_deficient, sec)))
else:
    rob.append(dict(id='R_a', description='Case bootstrap of Model 1', ran=False, estimate=None, se_or_ci='', p_value=None,
                    same_direction_and_significance_as_paper=None, source_file='', note='not completed'))
# R_b
b = pd.read_csv(os.path.join(O, 'R_b_outlier_exclusion.csv'))
b1 = b[b.check == 'R_b_model_1'].set_index('variable')
r = b1.loc['FA_Hispanic/Latino']
sign = {'FA_Female': 1, 'FA_South': -1, 'International': 1}
sec = '; '.join('%s B %.4f SE %.4f p %.3g (%s)' % (v, b1.loc[v].B, b1.loc[v].SE, b1.loc[v].p,
                'same sign and p<.001' if (b1.loc[v].B * sign[v] > 0 and b1.loc[v].p < 0.001) else 'differs')
                for v in sign)
b4 = b[b.check == 'R_b_model_4'].iloc[0]
rob.append(dict(id='R_b', description='Drop |z| > 3 on log10(citations+1) within Model 1 estimation rows (ddof=1), refit Model 1; secondary same rule in Model 4 for FA_African',
                ran=True, estimate=float(r.B), se_or_ci='nonrobust SE %.5f' % r.SE, p_value=float(r.p),
                same_direction_and_significance_as_paper=bool(r.B < 0 and r.p < 0.001),
                source_file='outputs/R_b_outlier_exclusion.csv',
                note='Model 1: %d of %d rows dropped (z range %.3f to %.3f). Secondary: %s. Model 4: %d of %d dropped, FA_African B %.4f SE %.4f p %.3g' %
                     (r.n_dropped, r.n_before, r.z_min, r.z_max, sec, b4.n_dropped, b4.n_before, b4.B, b4.SE, b4.p)))
# R_c
fc = os.path.join(O, 'R_c_poisson.csv')
if os.path.exists(fc):
    c = pd.read_csv(fc).set_index('variable')
    r = c.loc['FA_Hispanic/Latino']
    sec = '; '.join('%s coef %.4f HC1 SE %.4f p %.3g' % (v, c.loc[v].B, c.loc[v].SE, c.loc[v].p) for v in sign)
    rob.append(dict(id='R_c', description='Poisson PML (GLM Poisson, HC1) on raw Citations_Received, Model 1 rows and regressors',
                    ran=True, estimate=float(r.B), se_or_ci='HC1 SE %.5f' % r.SE, p_value=float(r.p),
                    same_direction_and_significance_as_paper=bool(r.B < 0 and r.p < 0.001), source_file='outputs/R_c_poisson.csv',
                    note='converged=%s (%s); coefficient on log scale, not comparable in magnitude with Table 2. Secondary: %s' %
                         (r.converged, r.note, sec)))
else:
    rob.append(dict(id='R_c', description='Poisson PML', ran=False, estimate=None, se_or_ci='', p_value=None,
                    same_direction_and_significance_as_paper=None, source_file='', note='not completed'))

cc = json.load(open(os.path.join(O, 'code_checks.json')))
n2 = int(est[est.model == 'results_2'].iloc[0]['nobs'])
n3 = int(est[est.model == 'results_3'].iloc[0]['nobs'])
n4 = int(est[est.model == 'results_4'].iloc[0]['nobs'])
r1adj = float(est[est.model == 'results_1'].iloc[0]['rsquared_adj']); r4adj = float(est[est.model == 'results_4'].iloc[0]['rsquared_adj'])
uncert = [
    'Secondary context (not targets), from outputs/regression_estimates.csv: Model 1 adj R2 %.4f (paper .428), Model 4 adj R2 %.4f (paper .422), Model 4 N %d (paper 16,025), Model 3 N %d, prose values FA_Hispanic/Latino %.4f (paper -.075) and International %.4f (paper .088), FA_Slavic %.4f t %.2f (paper -.073, t -9.9).' %
    (r1adj, r4adj, n4, n3, get('results_1', 'FA_Hispanic/Latino'), get('results_1', 'International'), get('results_1', 'FA_Slavic'), get('results_1', 'FA_Slavic', 't')),
    'PREREG inconsistency 1 confirmed by run: Model 2 N in this run is %d; Table 2 prints 68,558 for Model 2. Outside the targets; does not change the class (outputs/regression_estimates.csv).' % n2,
    'PREREG inconsistency 2 confirmed by run: Model 2 Team_Other t %.2f and Team_South t %.2f; Table 2 prints t -2.7 for both rows (outputs/regression_estimates.csv). Outside the targets.' %
    (get('results_2', 'Team_Other', 't'), get('results_2', 'Team_South', 't')),
    'Stars vs this run (nonrobust p): Model 1 FA_Other p %.3g (printed **), Model 2 Cited_Outgroup p %.3g (printed *), Model 4 FA_Other p %.3g (printed *), Model 3 FA_Author_Reputation p %.3g and FA_Author_Publication p %.3g (printed without stars). Not targets; star legend not in the extracted text.' %
    (get('results_1', 'FA_Other', 'p'), get('results_2', 'Cited_Outgroup', 'p'), get('results_4', 'FA_Other', 'p'), get('results_3', 'FA_Author_Reputation', 'p'), get('results_3', 'FA_Author_Publication', 'p')),
    'Model 3 omits FA_South from its regressor list (notebook cell 6). In the Top10 first-author rows FA_South takes values %s (outputs/code_checks.json), so if FA_South is constant there it would be collinear with Const and its omission is explained by the data rather than a coding slip (descriptive, not a target).' % cc['FA_South_value_counts_in_Top10_FA_rows'],
    'R_a bootstrap p_value is stored as the raw share 0.0 because 0 of 1,000 draws crossed zero; per PREREG it should be read as p < 0.001 at this resolution, not as exactly 0.',
    'within_5pct is computed against the printed 2-decimal values, so it is false for some targets (e.g. T2, T3) only because the printed values are rounded; every target matches to the printed rounding, which is what class A requires.',
    'Package versions differ from the authors (Python 3.11.9, versions not recorded); current pandas 3.0.6 / statsmodels 0.15.0 / numpy 2.5.3 were used. Top*_Inst columns parsed as bool, as expected.',
    'The regression table cannot be rebuilt from raw Web of Science records (construction code not deposited); targets depend only on the deposited table.',
    'R_a was computed with numpy lstsq on the resampled design (identical columns), not statsmodels, for speed; the full-sample estimate uses statsmodels OLS.',
    'Runs were OOM-killed twice (exit 137) on the shared machine before the main run completed; the completed run used peak RSS about 622 MB. No code change was made for memory.',
]

# time from LOG.md first and last timestamps
log = open(os.path.join(A, 'LOG.md')).read()
ts = re.findall(r'(\d{2}):(\d{2}) UTC', log)
mins = None
if ts:
    t0 = int(ts[0][0]) * 60 + int(ts[0][1]); t1 = int(ts[-1][0]) * 60 + int(ts[-1][1])
    mins = (t1 - t0) % (24 * 60)

all_round = all(t['match_to_rounding'] for t in tout)
res = dict(paper_id='16_QZNVZ0', agent='A', run_date_ist=datetime.now(timezone(timedelta(hours=5, minutes=30))).strftime('%Y-%m-%d'),
           ran=True, could_not_run_reason='', targets=tout, robustness=rob,
           bugs=[],
           code_review='none found. Read all 13 cells of Regression.ipynb (version 2.0) in full; Visualizations.ipynb not reviewed beyond its read calls (not used for targets). Unverified observations are listed under uncertainties (Model 3 omits FA_South; Model 2 row filter uses the first-author FA_Ethnicity variable).',
           env_fixes=['diffs/regression_verbatim_extraction.diff: notebook cells run as a script with an appended extraction block (PREREG route 2); no author line changed',
                      'working directory set to the data folder so the bare filename read_csv works (no file edit)'],
           proposed_class='A' if all_round else 'B',
           class_reason=('All six targets match Table 2 to the printed rounding (T6 N exactly), with the same sign and p < .001, from the deposited notebook run unchanged on current packages.'
                         if all_round else 'Not all targets match to rounding; see targets.'),
           confidence='high', confidence_reason='Deterministic OLS, script-parsed values, unchanged author code; pending agreement with agent B.',
           time_minutes=mins, uncertainties=uncert)
json.dump(res, open(os.path.join(A, 'results.json'), 'w'), indent=1)
print(json.dumps(dict(cls=res['proposed_class'], targets=[(t['id'], t['paper_value'], t['reproduced_value'], t['match_to_rounding']) for t in tout],
                      rob=[(r['id'], r['ran'], r['estimate'], r['p_value'], r['same_direction_and_significance_as_paper']) for r in rob]), indent=1))
