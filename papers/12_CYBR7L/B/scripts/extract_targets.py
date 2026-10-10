"""Agent B, 12_CYBR7L: parse the authors' output files into outputs/targets_extracted.csv.
Also writes authority scores near the top-5% boundary (2021 ranks 40-50 from the main run's own scores;
2010 ranks 18-26 from a fresh nx.hits call on the pickled G_citation[2010]).
Run with the audit venv python from anywhere."""
import json, re, csv, pickle, sys, os
import numpy as np, pandas as pd, networkx as nx

P = '/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/12_CYBR7L/B'
OUT = os.path.join(P, 'outputs')
RUN = '/workspace/audit_runs/12_CYBR7L/B/run'

rows = []
def add(key, value, source, note=''):
    rows.append({'key': key, 'value': value, 'source_file': source, 'note': note})

# ---- Table 1
t1 = open(os.path.join(OUT, 'output_for_table_1.txt')).read()
blocks = re.split(r'Years 1956-(\d{4})\n', t1)
# blocks: ['', '1980', text, '1990', text, ...]
tab1 = {}
for k in range(1, len(blocks), 2):
    tab1[int(blocks[k])] = blocks[k + 1]
for year, txt in tab1.items():
    m = re.search(r'Top (\d+) out of (\d+)', txt)
    add(f'top_size_{year}', int(m.group(1)), 'outputs/output_for_table_1.txt')
    add(f'num_authors_{year}', int(m.group(2)), 'outputs/output_for_table_1.txt')
    for label, tag in [('Africans', 'african'), ('based in Africa', 'based')]:
        mm = re.search(r'^(\d+) \(i\.e\., ([0-9.]+)%\) ' + re.escape(label) + r' \((\d+) i\.e\. ([0-9.]+)% in the complete set\)', txt, re.M)
        add(f'{tag}_top_count_{year}', int(mm.group(1)), 'outputs/output_for_table_1.txt')
        add(f'{tag}_top_pct_{year}', float(mm.group(2)), 'outputs/output_for_table_1.txt')
        add(f'{tag}_complete_count_{year}', int(mm.group(3)), 'outputs/output_for_table_1.txt')
        add(f'{tag}_complete_pct_{year}', float(mm.group(4)), 'outputs/output_for_table_1.txt')

# ---- Table 2
t2 = open(os.path.join(OUT, 'output_for_table_2.txt')).read()
parts = t2.split('Citing authors: African or Africa-based')
for tag, txt in [('nonafr', parts[0]), ('afr', parts[1])]:
    for m in re.finditer(r'1956 - (\d{4}) : ([0-9.]+) %', txt):
        add(f't2_{tag}_{m.group(1)}', float(m.group(2)), 'outputs/output_for_table_2.txt')

# ---- cell 3 (counts) from executed notebook
nb = json.load(open(os.path.join(OUT, 'executed.ipynb')))
for c in nb['cells']:
    src = ''.join(c.get('source', ''))
    if src.startswith('# Number of seed papers'):
        txt = ''.join(''.join(o.get('text', '')) for o in c['outputs'])
        add('cell3_nb_papers', int(re.search(r'Number of seed papers: (\d+)', txt).group(1)), 'outputs/executed.ipynb')
        add('cell3_nb_authors', int(re.search(r'Number of associated authors: (\d+)', txt).group(1)), 'outputs/executed.ipynb')

with open(os.path.join(OUT, 'targets_extracted.csv'), 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['key', 'value', 'source_file', 'note'])
    w.writeheader(); w.writerows(rows)

# ---- boundary scores
obj = pickle.load(open(os.path.join(RUN, 'audit_table1_objects.pkl'), 'rb'))
d21 = obj['df_auth_cit_net_2021_table1'].reset_index(drop=True)
d21['rank'] = np.arange(1, len(d21) + 1)
b21 = d21[(d21['rank'] >= 40) & (d21['rank'] <= 50)].copy(); b21['year'] = 2021
b21['source'] = 'main notebook run (Table 1 cell authorities, pickled)'
G10 = obj['G_citation'][2010]
h, a = nx.hits(G10)
ent = [(n, d.get('Author_Name'), d.get('Author_is_African', 0), d.get('Author_based_in_Africa', 0), d.get('Author_is_female', 0), a[n]) for n, d in G10.nodes(data=True)]
d10 = pd.DataFrame(ent, columns=['AuthorID', 'Author_Name', 'Author_is_African', 'Author_based_in_Africa', 'Author_is_female', 'Authority'])
d10.sort_values(by='Authority', ascending=False, inplace=True)
d10 = d10.reset_index(drop=True); d10['rank'] = np.arange(1, len(d10) + 1)
b10 = d10[(d10['rank'] >= 18) & (d10['rank'] <= 26)].copy(); b10['year'] = 2010
b10['source'] = 'fresh unseeded nx.hits on pickled G_citation[2010] (agent script)'
cols = ['year', 'rank', 'AuthorID', 'Author_is_African', 'Author_based_in_Africa', 'Authority', 'source']
pd.concat([b21[cols], b10[cols]]).to_csv(os.path.join(OUT, 'boundary_authority_scores.csv'), index=False, float_format='%.12g')
print(open(os.path.join(OUT, 'targets_extracted.csv')).read())
print(pd.concat([b21[cols], b10[cols]]).to_string())
