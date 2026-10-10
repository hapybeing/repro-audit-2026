#!/usr/bin/env python3
"""Agent B, 09_4U8CTG: build results.json from files in outputs/ (no hand-typed numbers)."""
import csv, json, os, re
B = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO_P = os.path.dirname(B)
O = lambda f: os.path.join(B, 'outputs', f)
targets_def = json.load(open(os.path.join(REPO_P, 'targets.json')))
rows = list(csv.DictReader(open(O('targets_extracted.csv'))))
def get(model, term, col):
    for r in rows:
        if r['model'] == model and r['term'] == term:
            return float(r[col])
    raise KeyError((model, term))
TERM = 'treatmentwin_mainstream'
t1, t1p = get('model_1_ez', TERM, 'estimate'), get('model_1_ez', TERM, 'p')
t1se = get('model_1_ez', TERM, 'se')
t2 = int(float(get('model_1_ez', TERM, 'nobs')))
t3, t3p = get('model_1_ez_lrem', TERM, 'estimate'), get('model_1_ez_lrem', TERM, 'p')
t3se = get('model_1_ez_lrem', TERM, 'se')
t4 = int(float(get('model_1_ez_lrem', TERM, 'nobs')))
repro = {'T1': (t1, f'SE {t1se:.6f}, classical p {t1p:.6f}', t1 < 0 and t1p < 0.05),
         'T2': (t2, '', None), 'T3': (t3, f'SE {t3se:.6f}, classical p {t3p:.6f}', t3 < 0 and t3p >= 0.05),
         'T4': (t4, '', None)}
targets = []
for t in targets_def:
    d = {'id': t['id'], 'description': t['description'], 'paper_value': t['paper_value'],
         'paper_rounding_decimals': t['paper_rounding_decimals']}
    if t['id'] in repro:
        v, note, concl = repro[t['id']]
        pv = t['paper_value']
        ad = v - pv; rd = ad / abs(pv)
        dec = t['paper_rounding_decimals']
        if concl is None:
            concl = abs(v - pv) <= 5
        d.update(reproduced_value=v, source_file='outputs/targets_extracted.csv', abs_diff=ad, rel_diff=rd,
                 match_to_rounding=(round(v, dec) == pv), within_5pct=(abs(rd) <= 0.05), same_conclusion=bool(concl),
                 note=note)
    else:
        d.update(reproduced_value=None, source_file='', abs_diff=None, rel_diff=None, match_to_rounding=None,
                 within_5pct=None, same_conclusion=None,
                 note='FES 2022 microdata restricted at ELIPSS; registration not permitted under audit rules (DATA_STATEMENT.md). Not run.')
    targets.append(d)
# deposited-table comparison
cmp = json.load(open(O('table_compare.json')))
# robustness
rb = list(csv.DictReader(open(O('robustness.csv'))))
def R(check, outcome):
    return next(r for r in rb if r['check'] == check and r['outcome'] == outcome)
f = lambda x: None if x in ('', 'NA') else float(x)
ra, ra2 = R('R_a', 'swd_ch'), R('R_a', 'affect_LREM_ch')
rbb, rbb2 = R('R_b', 'swd_ch'), R('R_b', 'affect_LREM_ch')
rc, rc2 = R('R_c', 'swd_w2'), R('R_c', 'affect_LREM_w2')
robust = [
 {'id': 'R_a', 'description': 'Stratified (within-arm) case bootstrap, seed 20261010, B=2000, model_1_ez Out-group Government coefficient; percentile 95% CI',
  'ran': True, 'estimate': f(ra['estimate']), 'se_or_ci': f"boot SE {f(ra['se']):.4f}; 95% percentile CI [{f(ra['ci_low']):.4f}, {f(ra['ci_high']):.4f}]",
  'p_value': f(ra['p_value']), 'same_direction_and_significance_as_paper': f(ra['estimate']) < 0 and f(ra['ci_high']) < 0,
  'source_file': 'outputs/robustness.csv',
  'note': f"Secondary (LREM, n={ra2['n']}): est {f(ra2['estimate']):.4f}, boot SE {f(ra2['se']):.4f}, CI [{f(ra2['ci_low']):.4f}, {f(ra2['ci_high']):.4f}], p {f(ra2['p_value']):.4f}; same as paper (neg, p>=0.05): {f(ra2['estimate'])<0 and f(ra2['p_value'])>=0.05}. {ra['note']}"},
 {'id': 'R_b', 'description': 'Drop rows with |z|>3 on swd_ch within the 123-row sample, refit lm(swd_ch ~ treatment), classical SE',
  'ran': True, 'estimate': f(rbb['estimate']), 'se_or_ci': f"SE {f(rbb['se']):.4f}", 'p_value': f(rbb['p_value']),
  'same_direction_and_significance_as_paper': f(rbb['estimate']) < 0 and f(rbb['p_value']) < 0.05,
  'source_file': 'outputs/robustness.csv',
  'note': f"N after = {rbb['n']}; {rbb['note']}. Secondary (LREM): est {f(rbb2['estimate']):.4f}, SE {f(rbb2['se']):.4f}, p {f(rbb2['p_value']):.4f}, N {rbb2['n']}; {rbb2['note']}; same as paper: {f(rbb2['estimate'])<0 and f(rbb2['p_value'])>=0.05}"},
 {'id': 'R_c', 'description': 'ANCOVA: lm(swd_w2 ~ treatment + swd_w1), classical SE',
  'ran': True, 'estimate': f(rc['estimate']), 'se_or_ci': f"SE {f(rc['se']):.4f}", 'p_value': f(rc['p_value']),
  'same_direction_and_significance_as_paper': f(rc['estimate']) < 0 and f(rc['p_value']) < 0.05,
  'source_file': 'outputs/robustness.csv',
  'note': f"N = {rc['n']}; {rc['note']}. Secondary (LREM ANCOVA): est {f(rc2['estimate']):.4f}, SE {f(rc2['se']):.4f}, p {f(rc2['p_value']):.4f}, N {rc2['n']}; {rc2['note']}; same as paper: {f(rc2['estimate'])<0 and f(rc2['p_value'])>=0.05}"},
]
extra = json.load(open(O('extra_checks.json')))
res = json.load(open(os.path.join(B, 'scripts', 'results_static.json')))
open_ok = all(t['match_to_rounding'] for t in targets if t['reproduced_value'] is not None)
res.update({'paper_id': '09_4U8CTG', 'agent': 'B', 'targets': targets, 'robustness': robust,
            'table_comparison': cmp, 'extra_checks': extra,
            'alternative_class_open_targets_only': 'A' if open_ok else ('B' if all(t['within_5pct'] and t['same_conclusion'] for t in targets if t['reproduced_value'] is not None) else 'see targets')})
json.dump(res, open(os.path.join(B, 'results.json'), 'w'), indent=1, ensure_ascii=False)
print(json.dumps({k: res[k] for k in ('proposed_class', 'alternative_class_open_targets_only')}, indent=1))
for t in targets: print(t['id'], t['paper_value'], t['reproduced_value'], t['match_to_rounding'], t['same_conclusion'])
for r in robust: print(r['id'], r['estimate'], r['p_value'], r['same_direction_and_significance_as_paper'])
