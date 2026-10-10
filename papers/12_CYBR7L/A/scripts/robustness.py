"""Pre-registered robustness checks R_a, R_b, R_c (PREREG.md section 3) for 12_CYBR7L.
Uses G_citation[2021] from notebook cell 6 (pickled by the audit-added cell) and df, with the notebook's
own definitions (cell 6 node attributes; cell 8 ranking, top-5% rule and df2 complete-set shares).
Writes outputs/robustness.json and outputs/R_a_seeds.csv. Run with the audit venv python."""
import os, json, pickle
import numpy as np
import pandas as pd
import networkx as nx
from scipy.stats import hypergeom

A = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(A, 'outputs')
RUN = '/workspace/audit_runs/12_CYBR7L/A/run'
YEAR = 2021
PRIMARY = 20261010

df = pd.read_csv(os.path.join(RUN, 'SciSciNet_AfricanPolitics_Data.csv'))
G0 = pickle.load(open(os.path.join(RUN, 'audit_G_citation_cell6.pkl'), 'rb'))['G_citation'][YEAR]
df2 = df[df['Year'] <= YEAR].drop_duplicates(subset='AuthorID', keep='first')
N = len(df2)


def table_from_scores(G, scores):
    rows = []
    for node, d in G.nodes(data=True):
        rows.append((node, d.get('Author_is_African', 0), d.get('Author_based_in_Africa', 0), scores[node]))
    return pd.DataFrame(rows, columns=['AuthorID', 'Author_is_African', 'Author_based_in_Africa', 'Score'])


def top_stats(t, n_complete, d2, kind=None):
    t = t.sort_values(by='Score', ascending=False, **({'kind': kind} if kind else {}))
    stop = round(5 * n_complete / 100)
    top = t.iloc[:stop]
    return top, summarize(top, n_complete, d2)


def summarize(top, n_complete, d2):
    k_af = int((top['Author_is_African'] == 1).sum()); k_b = int((top['Author_based_in_Africa'] == 1).sum())
    n_af = int((d2['Author_is_African'] == 1).sum()); n_b = int((d2['Author_based_in_Africa'] == 1).sum())
    sz = len(top)
    return {
        'top_size': sz, 'complete_size': n_complete,
        'african_top_count': k_af, 'african_top_share_pct': 100 * k_af / sz,
        'african_complete_count': n_af, 'african_complete_share_pct': 100 * n_af / n_complete,
        'african_hypergeom_p_lower': float(hypergeom.cdf(k_af, n_complete, n_af, sz)),
        'based_top_count': k_b, 'based_top_share_pct': 100 * k_b / sz,
        'based_complete_count': n_b, 'based_complete_share_pct': 100 * n_b / n_complete,
        'based_hypergeom_p_lower': float(hypergeom.cdf(k_b, n_complete, n_b, sz)),
        'same_direction_african': (100 * k_af / sz) < (100 * n_af / n_complete),
        'same_direction_based': (100 * k_b / sz) < (100 * n_b / n_complete),
    }


def hits_seeded(G, s):
    nstart = dict(zip(G, np.random.default_rng(s).standard_normal(len(G))))
    return nx.hits(G, nstart=nstart)[1]


res = {'year': YEAR, 'N_complete': N, 'graph_nodes': G0.number_of_nodes(), 'graph_edges': G0.number_of_edges()}

# Reference: unseeded call as in cell 8 (the notebook run's own top set is not saved by the notebook)
ref_top, ref = top_stats(table_from_scores(G0, nx.hits(G0)[1]), N, df2)
ref_set = set(ref_top['AuthorID'])
res['reference_unseeded'] = ref

# R_a
top_p, ra = top_stats(table_from_scores(G0, hits_seeded(G0, PRIMARY)), N, df2)
seed_rows = []
for s in range(1, 21):
    tp, st = top_stats(table_from_scores(G0, hits_seeded(G0, s)), N, df2)
    seed_rows.append({'seed': s, 'african_top_share_pct': st['african_top_share_pct'], 'african_top_count': st['african_top_count'],
                      'based_top_share_pct': st['based_top_share_pct'], 'based_top_count': st['based_top_count'],
                      'same_direction_african': st['same_direction_african'],
                      'top_set_differs_from_reference_unseeded': set(tp['AuthorID']) != ref_set})
sd = pd.DataFrame(seed_rows); sd.to_csv(os.path.join(OUT, 'R_a_seeds.csv'), index=False)
ra.update({
    'primary_seed': PRIMARY,
    'primary_top_set_differs_from_reference_unseeded': set(top_p['AuthorID']) != ref_set,
    'seeds_1_20_african_share_min': float(sd.african_top_share_pct.min()), 'seeds_1_20_african_share_max': float(sd.african_top_share_pct.max()),
    'seeds_1_20_based_share_min': float(sd.based_top_share_pct.min()), 'seeds_1_20_based_share_max': float(sd.based_top_share_pct.max()),
    'seeds_1_20_n_top_set_differs_from_reference': int(sd.top_set_differs_from_reference_unseeded.sum()),
    'seeds_1_20_n_same_direction_african': int(sd.same_direction_african.sum()),
})
res['R_a'] = ra

# R_b
a = hits_seeded(G0, PRIMARY)
nodes = list(G0)
vals = np.array([a[n] for n in nodes])
z = (vals - vals.mean()) / vals.std(ddof=0)
drop = [n for n, zz in zip(nodes, z) if abs(zz) > 3]
G1 = G0.copy(); G1.remove_nodes_from(drop)
d2r = df2[~df2['AuthorID'].isin(drop)]
n_red = N - len(drop)
a1 = hits_seeded(G1, PRIMARY)
_, rb = top_stats(table_from_scores(G1, a1), n_red, d2r)
rb.update({'n_dropped': len(drop), 'dropped_in_df2': int(df2['AuthorID'].isin(drop).sum()),
           'dropped_african': int(sum(G0.nodes[n].get('Author_is_African', 0) == 1 for n in drop)),
           'dropped_based_in_africa': int(sum(G0.nodes[n].get('Author_based_in_Africa', 0) == 1 for n in drop)),
           'dropped_african_or_based': int(sum((G0.nodes[n].get('Author_is_African', 0) == 1) or (G0.nodes[n].get('Author_based_in_Africa', 0) == 1) for n in drop)),
           'reduced_complete_size_from_df2': len(d2r)})
res['R_b'] = rb

# R_c
indeg = dict(G0.in_degree(weight='weight'))
t = table_from_scores(G0, indeg).sort_values(by='Score', ascending=False, kind='mergesort')
k = round(5 * N / 100)
thr = t['Score'].iloc[k - 1]
top_ties = t[t['Score'] >= thr]
rc = summarize(top_ties, N, df2)
rc['threshold_weighted_indegree'] = float(thr)
_, strict = top_stats(table_from_scores(G0, indeg), N, df2, kind='mergesort')
rc['strict_first_k_mergesort'] = strict
res['R_c'] = rc

json.dump(res, open(os.path.join(OUT, 'robustness.json'), 'w'), indent=1, default=lambda o: bool(o) if isinstance(o, np.bool_) else int(o) if isinstance(o, np.integer) else float(o))
print(json.dumps(res, indent=1, default=str))
