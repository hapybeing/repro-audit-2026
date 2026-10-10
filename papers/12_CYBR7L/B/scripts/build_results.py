"""Agent B, 12_CYBR7L: build results.json from files in outputs/. Paper values are read from PREREG-derived targets.json."""
import os, json, csv

P = '/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/12_CYBR7L/B'
OUT = os.path.join(P, 'outputs')
targets_def = json.load(open(os.path.join(P, '..', 'targets.json')))
ex = {r['key']: float(r['value']) for r in csv.DictReader(open(os.path.join(OUT, 'targets_extracted.csv')))}
rob = json.load(open(os.path.join(OUT, 'robustness.json')))
loc = json.load(open(os.path.join(OUT, 'location_coding_check.json')))

T1F = 'outputs/output_for_table_1.txt'; T2F = 'outputs/output_for_table_2.txt'
spec = {
    'T1': ('african_top_pct_2021', T1F, lambda: ex['african_top_pct_2021'] < ex['african_complete_pct_2021'],
           f"count {int(ex['african_top_count_2021'])} of {int(ex['top_size_2021'])} (paper 4 of 45); complete-set {ex['african_complete_pct_2021']}% (paper 17%)"),
    'T2': ('based_top_pct_2021', T1F, lambda: ex['based_top_pct_2021'] < ex['based_complete_pct_2021'],
           f"count {int(ex['based_top_count_2021'])} of {int(ex['top_size_2021'])} (paper 2 of 45); complete-set {ex['based_complete_pct_2021']}% (paper 13%)"),
    'T3': ('african_top_pct_2010', T1F, lambda: ex['african_top_pct_2010'] > ex['african_complete_pct_2010'] and ex['african_top_pct_2010'] > ex['african_top_pct_2000'],
           f"count {int(ex['african_top_count_2010'])} of {int(ex['top_size_2010'])} (paper 6 of 22); complete-set 2010 {ex['african_complete_pct_2010']}% (paper 23%); 2000 top share {ex['african_top_pct_2000']}% (paper 17%)"),
    'T4': ('t2_nonafr_2021', T2F, lambda: ex['t2_nonafr_2021'] > 50 and ex['t2_nonafr_2021'] > ex['t2_nonafr_2010'],
           f"1956-2010 value {ex['t2_nonafr_2010']}% (paper 64.3%)"),
    'T5': ('t2_afr_2021', T2F, lambda: ex['t2_afr_2021'] > ex['t2_afr_2010'],
           f"1956-2010 value {ex['t2_afr_2010']}% (paper 40.7%; text p. 708 says 42%)"),
    'T6': ('num_authors_2021', T1F, lambda: abs(ex['num_authors_2021'] - 903) <= 5,
           f"cell 3 nb_authors {int(ex['cell3_nb_authors'])}, nb_papers {int(ex['cell3_nb_papers'])} (paper 903, 923); top-5% size {int(ex['top_size_2021'])} (paper 45)"),
}
targets = []
for t in targets_def:
    key, src, crit, note = spec[t['id']]
    rv = ex[key]; pv = t['paper_value']; d = t['paper_rounding_decimals']
    ad = rv - pv; rd = ad / pv
    m = round(rv, d) == pv if d > 0 else int(round(rv)) == pv
    targets.append({'id': t['id'], 'description': t['description'], 'paper_value': pv, 'paper_rounding_decimals': d,
                    'reproduced_value': rv, 'source_file': src, 'abs_diff': round(ad, 6), 'rel_diff': round(rd, 6),
                    'match_to_rounding': bool(m), 'within_5pct': bool(abs(rd) <= 0.05), 'same_conclusion': bool(crit()),
                    'note': note + '. Main run unseeded as deposited; primary-seed (20261010) run gives the same top-45 set (outputs/robustness.json).' if t['id'] in ('T1', 'T2') else note})

ra, rb, rc = rob['R_a'], rob['R_b'], rob['R_c']
nsd = 'paper reports no significance test; same_direction set from direction only (top share < complete-set share). p is one-sided hypergeometric P(X<=k), information only.'
robustness = [
    {'id': 'R_a', 'description': 'nx.hits on G_citation[2021] with nstart from np.random.default_rng(s).standard_normal, s=20261010 primary, s=1..20 spread; cell 8 ranking and top-5% rule',
     'ran': True, 'estimate': ra['african_top_pct'], 'se_or_ci': f"seeds 1-20 African share range {ra['seeds_1_20']['african_pct_min']:.2f} to {ra['seeds_1_20']['african_pct_max']:.2f}; Africa-based {ra['seeds_1_20']['based_pct_min']:.2f} to {ra['seeds_1_20']['based_pct_max']:.2f}",
     'p_value': ra['african_hypergeom_p_le'], 'same_direction_and_significance_as_paper': ra['direction_african_lower'], 'source_file': 'outputs/robustness.json',
     'note': f"primary seed: {ra['african_top_count']}/{ra['top_size']} African vs complete-set {ra['african_complete_pct']:.2f}%; Africa-based {ra['based_top_count']}/{ra['top_size']} ({ra['based_top_pct']:.2f}%, p {ra['based_hypergeom_p_le']:.4f}) vs {ra['based_complete_pct']:.2f}%; primary top set differs from main run: {ra['top_set_differs_from_main_run']}; seeds 1-20 with a different top set: {ra['seeds_1_20']['n_top_set_differs_from_main']}; seeds keeping direction: {ra['seeds_1_20']['n_keep_direction']}/20 (outputs/R_a_seeds.csv). " + nsd},
    {'id': 'R_b', 'description': 'drop authors with |z|>3 on authority score (seed 20261010, ddof=0) from graph and df2, recompute hits, top round(5*(903-dropped)/100)',
     'ran': True, 'estimate': rb['african_top_pct'], 'se_or_ci': 'not applicable',
     'p_value': rb['african_hypergeom_p_le'], 'same_direction_and_significance_as_paper': rb['direction_african_lower'], 'source_file': 'outputs/robustness.json',
     'note': f"dropped {rb['n_dropped']} authors ({rb['n_dropped_african_or_based']} African or Africa-based); top {rb['top_size']} of {rb['complete_size']}: {rb['african_top_count']} African vs reduced complete-set {rb['african_complete_pct']:.2f}%; Africa-based {rb['based_top_count']} ({rb['based_top_pct']:.2f}%, p {rb['based_hypergeom_p_le']:.4f}) vs {rb['based_complete_pct']:.2f}%. " + nsd},
    {'id': 'R_c', 'description': 'rank by weighted in-degree on G_citation[2021]; top set = all with in-degree >= value at rank 45 (ties included)',
     'ran': True, 'estimate': rc['african_top_pct'], 'se_or_ci': 'not applicable',
     'p_value': rc['african_hypergeom_p_le'], 'same_direction_and_significance_as_paper': rc['direction_african_lower'], 'source_file': 'outputs/robustness.json',
     'note': f"cutoff in-degree {rc['cutoff_weighted_indegree']}, set size {rc['top_size']}: {rc['african_top_count']} African vs {rc['african_complete_pct']:.2f}%; Africa-based {rc['based_top_count']} ({rc['based_top_pct']:.2f}%, p {rc['based_hypergeom_p_le']:.4f}); strict first-45 (mergesort): {rc['strict_first45']['african_top_count']} African ({rc['strict_first45']['african_top_pct']:.2f}%, p {rc['strict_first45']['african_hypergeom_p_le']:.4f}), {rc['strict_first45']['based_top_count']} Africa-based. " + nsd},
]

all_match = all(t['match_to_rounding'] for t in targets)
all_b = all(t['within_5pct'] and t['same_conclusion'] for t in targets)
cls = 'A' if all_match else ('B' if all_b else 'D')
res = {
    'paper_id': '12_CYBR7L', 'agent': 'B', 'run_date_ist': '2026-10-10', 'ran': True, 'could_not_run_reason': '',
    'targets': targets, 'robustness': robustness,
    'bugs': [],
    'env_fixes': ['diffs/replication_code_audit.ipynb.diff (and readable cell view diffs/replication_code_audit_cells.diff): two added cells that only pickle objects (G_citation after Table 1, G_citation after Table 2); no computation changed. No package or path fix was needed.'],
    'proposed_class': cls,
    'class_reason': ('All six targets match the paper at its printed rounding from a clean run of the deposited notebook with the README package versions.' if cls == 'A' else 'See targets.'),
    'confidence': 'medium',
    'confidence_reason': 'Exact match by script with README package versions, but Python 3.12 instead of 3.14.2, HITS is unseeded, and agreement with agent A is not yet known.',
    'time_minutes': 25,
    'code_review': f"none found. Read all 10 notebook cells in full. Observations (not bugs): Table 1 complete-set shares use first-row raw location while top-5% counts use mode-based location; for 2021 the complete-set Africa-based count is {loc['complete_set_based_count_first_row_raw']} first-row vs {loc['complete_set_based_count_mode_rule']} mode-based ({loc['complete_set_based_pct_first_row_raw']:.2f}% vs {loc['complete_set_based_pct_mode_rule']:.2f}%, both round to 13%); {loc['n_authors_all_blank_location']} authors have all-blank location; {loc['n_authors_tied_location']} have tied location (none in the top 45) (outputs/location_coding_check.json).",
    'uncertainties': [
        'Python 3.12.15 used instead of README 3.14.2; all five README package versions installed exactly.',
        'Main run unseeded as deposited (svds start vector). Boundary gaps (outputs/boundary_authority_scores.csv): 2021 rank 45 vs 46 authority 0.004664 vs 0.004616 in the main run; 2010 rank 22 vs 23 from a fresh unseeded hits call 0.012089 vs 0.011833. No tie at either boundary; 2010 ranks 24 and 25 are tied but outside the top 22.',
        'PREREG says the pickle comes from an added final cell; a final cell would hold the Table 2 networks (cell 9 rebuilds G_citation with isolates), so the Table 1 networks were pickled by a cell inserted right after the Table 1 cell, and a second pickle cell was added at the end. Only saving, no computation changed.',
        'Figure claims not checked (not pre-registered as targets); figures are saved in outputs/ for inspection.',
        'Batch 3 decision 3: class from the primary-seed run; the primary-seed (20261010) top-45 set equals the main run top-45 set, so T1 and T2 are the same either way. T3 (2010) was not rerun with a seed (not pre-registered).',
        'While checking that a pip install had finished, a `ps aux` listing briefly showed an agent A process command line (a pandas reinstall in A\'s venv). No A file was opened, listed or read.',
    ],
}
json.dump(res, open(os.path.join(P, 'results.json'), 'w'), indent=1)
print(json.dumps({'class': cls, 'targets': [(t['id'], t['paper_value'], t['reproduced_value'], t['match_to_rounding'], t['same_conclusion']) for t in targets]}, indent=1))
