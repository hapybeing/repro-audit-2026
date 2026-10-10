"""Checks behind the code-review observations (not targets). Writes outputs/code_checks.json.
1. Location coding: authors whose Author_based_in_Africa rows are all blank get mode() == empty array,
   which cells 6/9 set to 1 (Africa-based). Count them and whether any is in the 2021 / 2010 top 5% (unseeded hits as cell 8).
2. Complete-set Africa-based count in cell 8 uses each author's first row (df2), the top-5% count uses the mode-based node
   attribute. Recompute the complete-set count with the mode-based value for comparison.
3. Cell 4 chained assignment under pandas 3.0.0: does df_tmp['Author_based_in_Africa'][mask] = value change df_tmp?
"""
import os, json, pickle
import numpy as np, pandas as pd, networkx as nx

A = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(A, 'outputs'); RUN = '/workspace/audit_runs/12_CYBR7L/A/run'
df = pd.read_csv(os.path.join(RUN, 'SciSciNet_AfricanPolitics_Data.csv'))
G = pickle.load(open(os.path.join(RUN, 'audit_G_citation_cell6.pkl'), 'rb'))['G_citation']
res = {'pandas_version': pd.__version__}

for year in [2010, 2021]:
    sub = df[df['Year'] <= year]
    allblank = sub.groupby('AuthorID')['Author_based_in_Africa'].apply(lambda s: s.isna().all())
    ab_ids = set(allblank[allblank].index)
    loc = sub.groupby('AuthorID')['Author_based_in_Africa'].agg(lambda x: x.mode()).to_dict()
    n_tie = 0
    for k, v in loc.items():
        if isinstance(v, (list, np.ndarray)):
            if k not in ab_ids: n_tie += 1
            loc[k] = 1.
    _, auth = nx.hits(G[year])
    order = sorted(auth, key=lambda n: -auth[n])
    N = sub['AuthorID'].nunique(); top = set(order[:round(5 * N / 100)])
    df2 = sub.drop_duplicates(subset='AuthorID', keep='first')
    res[str(year)] = {
        'n_authors': int(N),
        'authors_all_location_blank': len(ab_ids),
        'authors_all_location_blank_in_graph': len(ab_ids & set(G[year].nodes)),
        'authors_all_location_blank_in_top5pct': len(ab_ids & top),
        'authors_location_tie_coded_1': n_tie,
        'complete_set_based_count_first_row_as_cell8': int((df2['Author_based_in_Africa'] == 1).sum()),
        'complete_set_based_count_mode_based': int(sum(1 for k in df2['AuthorID'] if loc.get(k) == 1)),
        'top5pct_based_count_mode_based': int(sum(1 for k in top if loc.get(k) == 1)),
        'top5pct_based_count_first_row': int(df2[df2['AuthorID'].isin(top)]['Author_based_in_Africa'].eq(1).sum()),
    }

# 3. chained assignment
df_tmp = df[df['Year'] <= 2021]
before = df_tmp['Author_based_in_Africa'].copy()
key = df_tmp['AuthorID'].iloc[0]
import warnings
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter('always')
    df_tmp['Author_based_in_Africa'][df_tmp['AuthorID'] == key] = 99.0
    msgs = [str(x.message)[:200] for x in w]
res['cell4_chained_assignment'] = {'value_written_99_present_after': bool((df_tmp['Author_based_in_Africa'] == 99.0).any()),
                                   'warnings': msgs}
json.dump(res, open(os.path.join(OUT, 'code_checks.json'), 'w'), indent=1)
print(json.dumps(res, indent=1))
