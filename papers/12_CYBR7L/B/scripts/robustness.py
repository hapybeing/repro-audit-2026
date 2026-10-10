"""Agent B, 12_CYBR7L: pre-registered robustness checks R_a, R_b, R_c (PREREG.md section 3).
Uses G_citation[2021] pickled from the main notebook run right after the Table 1 cell, and the deposited Data.csv.
Writes outputs/robustness.json and outputs/R_a_seeds.csv."""
import os, json, pickle
import numpy as np, pandas as pd, networkx as nx
from scipy.stats import hypergeom

P = '/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/12_CYBR7L/B'
OUT = os.path.join(P, 'outputs')
RUN = '/workspace/audit_runs/12_CYBR7L/B/run'
PRIMARY = 20261010

obj = pickle.load(open(os.path.join(RUN, 'audit_table1_objects.pkl'), 'rb'))
G = obj['G_citation'][2021]
main_top_ids = set(obj['df_auth_cit_net_2021_table1'].iloc[:45]['AuthorID'])
df = pd.read_csv(os.path.join(RUN, 'SciSciNet_AfricanPolitics_Data.csv'))
df2 = df[df['Year'] <= 2021].drop_duplicates(subset='AuthorID', keep='first')
num_authors = len(df2)


def node_table(Gx, scores):
    ent = []
    for node, data in Gx.nodes(data=True):
        ent.append((node, data.get('Author_is_African', 0), data.get('Author_based_in_Africa', 0), scores[node]))
    return pd.DataFrame(ent, columns=['AuthorID', 'Author_is_African', 'Author_based_in_Africa', 'Score'])


def summarise(top, d2, M):
    k_af = int((top['Author_is_African'] == 1).sum())
    k_ba = int((top['Author_based_in_Africa'] == 1).sum())
    n_af = int((d2['Author_is_African'] == 1).sum())
    n_ba = int((d2['Author_based_in_Africa'] == 1).sum())
    N = len(top)
    return {
        'top_size': N, 'complete_size': M,
        'african_top_count': k_af, 'african_top_pct': 100 * k_af / N,
        'african_complete_count': n_af, 'african_complete_pct': 100 * n_af / M,
        'african_hypergeom_p_le': float(hypergeom.cdf(k_af, M, n_af, N)),
        'based_top_count': k_ba, 'based_top_pct': 100 * k_ba / N,
        'based_complete_count': n_ba, 'based_complete_pct': 100 * n_ba / M,
        'based_hypergeom_p_le': float(hypergeom.cdf(k_ba, M, n_ba, N)),
        'direction_african_lower': bool(100 * k_af / N < 100 * n_af / M),
        'direction_based_lower': bool(100 * k_ba / N < 100 * n_ba / M),
    }


def seeded_hits(Gx, s):
    rng = np.random.default_rng(s)
    nstart = dict(zip(Gx, rng.standard_normal(len(Gx))))
    h, a = nx.hits(Gx, nstart=nstart)
    return a


def top_by_cell8(Gx, a, M):
    t = node_table(Gx, a)
    t.sort_values(by='Score', ascending=False, inplace=True)
    return t.iloc[:round(5 * M / 100)]

res = {'num_authors': num_authors, 'network_nodes_2021': G.number_of_nodes()}

# R_a
top = top_by_cell8(G, seeded_hits(G, PRIMARY), num_authors)
ra = summarise(top, df2, num_authors)
ra['seed'] = PRIMARY
ra['top_set_differs_from_main_run'] = bool(set(top['AuthorID']) != main_top_ids)
seed_rows = []
for s in range(1, 21):
    t = top_by_cell8(G, seeded_hits(G, s), num_authors)
    sm = summarise(t, df2, num_authors)
    seed_rows.append({'seed': s, 'african_top_pct': sm['african_top_pct'], 'based_top_pct': sm['based_top_pct'],
                      'african_top_count': sm['african_top_count'], 'based_top_count': sm['based_top_count'],
                      'direction_african_lower': sm['direction_african_lower'],
                      'top_set_differs_from_main_run': bool(set(t['AuthorID']) != main_top_ids)})
sd = pd.DataFrame(seed_rows); sd.to_csv(os.path.join(OUT, 'R_a_seeds.csv'), index=False)
ra['seeds_1_20'] = {'african_pct_min': float(sd.african_top_pct.min()), 'african_pct_max': float(sd.african_top_pct.max()),
                    'based_pct_min': float(sd.based_top_pct.min()), 'based_pct_max': float(sd.based_top_pct.max()),
                    'n_top_set_differs_from_main': int(sd.top_set_differs_from_main_run.sum()),
                    'n_keep_direction': int(sd.direction_african_lower.sum())}
res['R_a'] = ra

# R_b
a = seeded_hits(G, PRIMARY)
nodes = list(G.nodes)
v = np.array([a[n] for n in nodes])
z = (v - v.mean()) / v.std(ddof=0)
drop = [n for n, zz in zip(nodes, z) if abs(zz) > 3]
Gr = G.copy(); Gr.remove_nodes_from(drop)
d2r = df2[~df2['AuthorID'].isin(drop)]
M_r = num_authors - len(drop)
ar = seeded_hits(Gr, PRIMARY)
topr = top_by_cell8(Gr, ar, M_r)
rb = summarise(topr, d2r, M_r)
rb['n_dropped'] = len(drop)
rb['n_dropped_african_or_based'] = int(sum(1 for n in drop if G.nodes[n].get('Author_is_African') == 1 or G.nodes[n].get('Author_based_in_Africa') == 1))
rb['n_dropped_african'] = int(sum(1 for n in drop if G.nodes[n].get('Author_is_African') == 1))
rb['reduced_df2_rows'] = len(d2r)
res['R_b'] = rb

# R_c
indeg = dict(G.in_degree(weight='weight'))
t = node_table(G, indeg)
ts = t.sort_values(by='Score', ascending=False)
k = round(5 * num_authors / 100)
cut = ts['Score'].iloc[k - 1]
topc = t[t['Score'] >= cut]
rc = summarise(topc, df2, num_authors)
rc['cutoff_weighted_indegree'] = float(cut)
strict = t.sort_values(by='Score', kind='mergesort', ascending=False).iloc[:k]
rc['strict_first45'] = summarise(strict, df2, num_authors)
res['R_c'] = rc

json.dump(res, open(os.path.join(OUT, 'robustness.json'), 'w'), indent=1)
print(json.dumps(res, indent=1))
