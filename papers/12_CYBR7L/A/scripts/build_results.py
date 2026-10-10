"""Build results.json for 12_CYBR7L agent A from files in outputs/ and the frozen targets.json."""
import os, json, csv, math

A = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(A)))
OUT = os.path.join(A, 'outputs')
targets = json.load(open(os.path.join(REPO, 'papers', '12_CYBR7L', 'targets.json')))
ex = {r['key']: r for r in csv.DictReader(open(os.path.join(OUT, 'targets_extracted.csv')))}
v = lambda k: float(ex[k]['value'])
rob = json.load(open(os.path.join(OUT, 'robustness.json')))
cc = json.load(open(os.path.join(OUT, 'code_checks.json')))

def rnd(x, d):  # round half up at d decimals, on the decimal string the code printed
    return math.floor(x * 10 ** d + 0.5 + 1e-9) / 10 ** d

concl = {
    'T1': (v('T1') < v('table1_2021_african_all_pct'), f"top {v('T1')} < complete {v('table1_2021_african_all_pct')}"),
    'T2': (v('T2') < v('table1_2021_based_all_pct'), f"top {v('T2')} < complete {v('table1_2021_based_all_pct')}"),
    'T3': (v('T3') > v('table1_2010_african_all_pct') and v('T3') > v('table1_2000_african_top_pct'),
           f"top2010 {v('T3')} > complete2010 {v('table1_2010_african_all_pct')} and > top2000 {v('table1_2000_african_top_pct')}"),
    'T4': (v('T4') > 50 and v('T4') > v('table2_nonafr_2010'), f"{v('T4')} > 50 and > 1956-2010 {v('table2_nonafr_2010')}"),
    'T5': (v('T5') > v('table2_afr_2010'), f"{v('T5')} > 1956-2010 {v('table2_afr_2010')} (above 50: {v('T5') > 50})"),
    'T6': (abs(v('T6') - 903) <= 5, f"N {v('T6')} within 5 of 903; cell 3 nb_authors {v('cell3_nb_authors')}, nb_papers {v('cell3_nb_papers')}, top-5% size {v('table1_2021_top_n')}"),
}
counts = {'T1': ('table1_2021_african_top_count', 4), 'T2': ('table1_2021_based_top_count', 2), 'T3': ('table1_2010_african_top_count', 6)}
tout = []
for t in targets:
    r = v(t['id']); p = t['paper_value']; d = t['paper_rounding_decimals']
    note = 'same_conclusion rule: ' + concl[t['id']][1]
    if t['id'] in counts:
        k, pc = counts[t['id']]; note += f"; count reproduced {int(v(k))} vs paper {pc}"
    tout.append({'id': t['id'], 'description': t['description'], 'paper_value': p, 'paper_rounding_decimals': d,
                 'reproduced_value': r, 'source_file': ex[t['id']]['source_file'],
                 'abs_diff': round(r - p, 6), 'rel_diff': round((r - p) / p, 6),
                 'match_to_rounding': rnd(r, d) == p, 'within_5pct': abs((r - p) / p) <= 0.05,
                 'same_conclusion': bool(concl[t['id']][0]), 'note': note})

def robrow(id_, desc, d, extra):
    return {'id': id_, 'description': desc, 'ran': True, 'estimate': d['african_top_share_pct'],
            'se_or_ci': 'none (paper reports no test); complete-set African share %.4f%%' % d['african_complete_share_pct'],
            'p_value': d['african_hypergeom_p_lower'],
            'same_direction_and_significance_as_paper': bool(d['same_direction_african']),
            'source_file': 'outputs/robustness.json',
            'note': 'paper reports no significance test; direction only. p_value = one-sided hypergeometric P(X<=k), information only. '
                    + 'African top count %d of %d. Secondary T2 (Africa-based): top %.4f%% vs complete %.4f%%, p=%.4f. ' % (
                        d['african_top_count'], d['top_size'], d['based_top_share_pct'], d['based_complete_share_pct'], d['based_hypergeom_p_lower']) + extra}

ra, rb, rc = rob['R_a'], rob['R_b'], rob['R_c']
robust = [
    robrow('R_a', 'nx.hits on G_citation[2021] with nstart from default_rng(20261010); cell 8 ranking and top-5% rule; spread over seeds 1-20', ra,
           'Seeds 1-20: African share min %.4f max %.4f, Africa-based min %.4f max %.4f; %d of 20 seeds give a top-5%% set different from the reference unseeded call; %d of 20 keep the direction. Primary-seed set differs from reference: %s. Reference = an unseeded nx.hits call in robustness.py (the notebook does not save its own top set); its counts equal the notebook output. Per-seed: outputs/R_a_seeds.csv.' % (
               ra['seeds_1_20_african_share_min'], ra['seeds_1_20_african_share_max'], ra['seeds_1_20_based_share_min'], ra['seeds_1_20_based_share_max'],
               ra['seeds_1_20_n_top_set_differs_from_reference'], ra['seeds_1_20_n_same_direction_african'], ra['primary_top_set_differs_from_reference_unseeded'])),
    robrow('R_b', 'drop authors with |z|>3 on 2021 authority score (ddof=0), recompute hits on reduced graph, top round(5*N_reduced/100), compare with reduced complete set', rb,
           'Dropped %d authors (%d African, %d Africa-based); reduced N %d; top size %d.' % (rb['n_dropped'], rb['dropped_african'], rb['dropped_based_in_africa'], rb['complete_size'], rb['top_size'])),
    robrow('R_c', 'rank by weighted in-degree in G_citation[2021]; ties-included top set at rank round(5*N/100)', rc,
           'Threshold weighted in-degree %.0f, ties-included set size %d. Secondary strict first-45 (mergesort): African %d (%.4f%%), p=%.4f.' % (
               rc['threshold_weighted_indegree'], rc['top_size'], rc['strict_first_k_mergesort']['african_top_count'],
               rc['strict_first_k_mergesort']['african_top_share_pct'], rc['strict_first_k_mergesort']['african_hypergeom_p_lower'])),
]

c21 = cc['2021']; c10 = cc['2010']
bugs = [{
    'file': 'replication_code.ipynb', 'line': 77,
    'description': "Cell 4 (Figure 1), line 15 of the cell: df_tmp['Author_based_in_Africa'][df_tmp['AuthorID']==key] = value is a chained assignment. Under pandas 3.0.0 (the README version, Copy-on-Write) it does not modify df_tmp, so Figure 1's Africa-based series uses each author's first row rather than the mode-based location the loop computes. Affects Figure 1 only; no target.",
    'evidence': "outputs/code_checks.json cell4_chained_assignment: value written was present after assignment = %s; pandas %s warning: '%s...'. Line 77 is the line in the notebook JSON file; warnings are silenced in cell 1 (warnings.simplefilter('ignore'))." % (
        cc['cell4_chained_assignment']['value_written_99_present_after'], cc['pandas_version'], cc['cell4_chained_assignment']['warnings'][0][:90].replace('\n', ' '))}]

unc = [
    "Python 3.12.15 used instead of README Python 3.14.2; all five README package versions installed exactly (numpy 2.4.1, pandas 3.0.0, scipy 1.17.0, matplotlib 3.10.8, networkx 2.8.8). No version pin change was needed.",
    "nx.hits in the notebook is unseeded (svds start vector). The main run is one unseeded run. Boundary check outputs/boundary_authority_scores.csv: 2021 rank 45 authority %s vs rank 46 %s; 2010 rank 22 %s vs rank 23 %s (no tie at either boundary). R_a: all 20 seeds and the primary seed give the identical 2021 top-5%% set." % (
        None, None, None, None),
    "Code observation (confirmed by run, judged a design inconsistency rather than a bug): cell 8 complete-set Africa-based counts use each author's first row (notebook JSON line 318, df2 = ...drop_duplicates(keep='first')), while the top-5%% counts use the mode-based node attribute. With the mode-based value the 2021 complete-set count would be %d instead of %d, 2010 %d instead of %d (outputs/code_checks.json). Top-5%% counts are the same either way (2021: %d vs %d; 2010: %d vs %d). Not a target value; T2's comparison direction is unaffected." % (
        c21['complete_set_based_count_mode_based'], c21['complete_set_based_count_first_row_as_cell8'], c10['complete_set_based_count_mode_based'], c10['complete_set_based_count_first_row_as_cell8'],
        c21['top5pct_based_count_mode_based'], c21['top5pct_based_count_first_row'], c10['top5pct_based_count_mode_based'], c10['top5pct_based_count_first_row']),
    "Code observation (confirmed by run): authors whose location rows are all blank get an empty mode, which cells 6 and 9 set to 1 (Africa-based), while the appendix says undetermined values were set to missing. Count of such authors: 2021 %d, 2010 %d (in 2010 top 5%%: %d). Ties coded 1 (as the appendix states): 2021 %d, 2010 %d. outputs/code_checks.json." % (
        c21['authors_all_location_blank'], c10['authors_all_location_blank'], c10['authors_all_location_blank_in_top5pct'], c21['authors_location_tie_coded_1'], c10['authors_location_tie_coded_1']),
    "R_a 'main run top set' comparison uses a reference unseeded nx.hits call in robustness.py, because the notebook does not save its top-5% AuthorIDs; its counts (4 African, 2 Africa-based of 45) equal the notebook output.",
    "PREREG section 2 says the G_citation pickle cell is an 'added final cell'. Cell 9 reassigns G_citation (graphs with isolated nodes), so a final cell alone would not save the cell 6 objects the checks name. A save-only cell was inserted after cell 8 (cell 6 graphs, used for boundary scores and all robustness checks) and a second save-only cell was added at the end. Both only pickle objects (diffs/replication_code_audit_cells.diff).",
    "Paper text p. 708 says 42 percent for the African or Africa-based 1956-2010 cell; the run gives " + ex['table2_afr_2010']['value'] + ", matching Table 2's 40.7 (not a target).",
]
import pandas as pd
b = pd.read_csv(os.path.join(OUT, 'boundary_authority_scores.csv'))
g = lambda y, r: b[(b.year == y) & (b['rank'] == r)]['Authority'].iloc[0]
unc[1] = unc[1].replace('None vs rank 46 None', '%s vs rank 46 %s' % (g(2021, 45), g(2021, 46)), 1).replace('None vs rank 23 None', '%s vs rank 23 %s' % (g(2010, 22), g(2010, 23)), 1)

allmatch = all(t['match_to_rounding'] for t in tout)
allwithin = all(t['within_5pct'] and t['same_conclusion'] for t in tout)
cls = 'A' if allmatch else ('B' if allwithin else 'D')
log = open(os.path.join(A, 'LOG.md')).read()
import re
ts = re.findall(r'(\d{2}):(\d{2}) IST', log)
mins = None
if ts:
    t0 = int(ts[0][0]) * 60 + int(ts[0][1]); t1 = int(ts[-1][0]) * 60 + int(ts[-1][1]); mins = t1 - t0
res = {
    'paper_id': '12_CYBR7L', 'agent': 'A', 'run_date_ist': '2026-10-10', 'ran': True, 'could_not_run_reason': '',
    'targets': tout, 'robustness': robust, 'bugs': bugs,
    'env_fixes': ['diffs/replication_code_audit_cells.diff (and the full-JSON form diffs/replication_code_audit.ipynb.diff): two save-only cells that pickle G_citation and author_attributes, as PREREG section 2 allows; no analysis change. No package, path or backend change to the code was needed (MPLBACKEND=Agg set in the environment only).'],
    'proposed_class': cls,
    'class_reason': ('All six targets reproduced to the paper\'s printed precision by running the deposited notebook as is with the README package versions.' if cls == 'A'
                     else 'Not all targets matched to rounding; see targets.'),
    'confidence': 'high' if cls == 'A' else 'medium',
    'confidence_reason': 'Exact README package versions, single deposited notebook run unchanged, values parsed by script; HITS randomness shown not to move the top-5% sets (20 seeds). Agent B comparison pending.',
    'time_minutes': mins,
    'uncertainties': unc,
    'secondary_context': {
        'cell3_nb_papers': v('cell3_nb_papers'), 'cell3_nb_authors': v('cell3_nb_authors'),
        'table1_2021_top_n': v('table1_2021_top_n'), 'table1_2010_top_n': v('table1_2010_top_n'),
        'table1_2000_african_top_pct': v('table1_2000_african_top_pct'),
        'table2_nonafr_2010': v('table2_nonafr_2010'), 'table2_afr_2010': v('table2_afr_2010'),
        'source_files': ['outputs/targets_extracted.csv', 'outputs/output_for_table_1.txt', 'outputs/output_for_table_2.txt', 'outputs/executed.ipynb']},
}
json.dump(res, open(os.path.join(A, 'results.json'), 'w'), indent=1)
print(json.dumps({k: res[k] for k in ['proposed_class', 'time_minutes']}), [(t['id'], t['paper_value'], t['reproduced_value'], t['match_to_rounding'], t['same_conclusion']) for t in tout])
