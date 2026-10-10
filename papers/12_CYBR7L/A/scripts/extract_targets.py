"""Parse output_for_table_1.txt, output_for_table_2.txt and executed.ipynb (all copied to outputs/)
and write outputs/targets_extracted.csv. Also write the authority scores near the top-5% boundary
(ranks 40-50 for 2021, 18-26 for 2010) from the pickled cell-6 G_citation, as PREREG section 2 asks.
Run with the audit venv python from the A/ directory."""
import re, json, csv, os, pickle, sys
import pandas as pd
import networkx as nx

A = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(A, 'outputs')
RUN = '/workspace/audit_runs/12_CYBR7L/A/run'

rows = []
def add(key, value, source, note=''):
    rows.append({'key': key, 'value': value, 'source_file': source, 'note': note})

# Table 1
t1 = open(os.path.join(OUT, 'output_for_table_1.txt')).read()
blocks = re.split(r'Years 1956-(\d{4})\n', t1)
tab1 = {}
for i in range(1, len(blocks), 2):
    yr = int(blocks[i]); b = blocks[i + 1]
    m = re.search(r'Top (\d+) out of (\d+)', b)
    d = {'top_n': int(m.group(1)), 'N': int(m.group(2))}
    for label, key in [('Africans', 'african'), ('based in Africa', 'based')]:
        mm = re.search(r'^(\d+) \(i\.e\., ([\d.]+)%\) ' + re.escape(label) + r' \((\d+) i\.e\. ([\d.]+)% in the complete set\)', b, re.M)
        d[key + '_top_count'] = int(mm.group(1)); d[key + '_top_pct'] = float(mm.group(2))
        d[key + '_all_count'] = int(mm.group(3)); d[key + '_all_pct'] = float(mm.group(4))
    tab1[yr] = d
src1 = 'outputs/output_for_table_1.txt'
for yr in sorted(tab1):
    for k, v in tab1[yr].items():
        add(f'table1_{yr}_{k}', v, src1)
add('T1', tab1[2021]['african_top_pct'], src1, 'cell 8 year 2021 Africans first pct')
add('T2', tab1[2021]['based_top_pct'], src1, 'cell 8 year 2021 based in Africa first pct')
add('T3', tab1[2010]['african_top_pct'], src1, 'cell 8 year 2010 Africans first pct')
add('T6', tab1[2021]['N'], src1, 'cell 8 year 2021 num_authors')

# Table 2
t2 = open(os.path.join(OUT, 'output_for_table_2.txt')).read()
parts = t2.split('Citing authors: African or Africa-based')
src2 = 'outputs/output_for_table_2.txt'
for name, part in [('nonafr', parts[0]), ('afr', parts[1])]:
    for yr, val in re.findall(r'1956 - (\d{4}) : ([\d.]+) %', part):
        add(f'table2_{name}_{yr}', float(val), src2)
vals = {r['key']: r['value'] for r in rows}
add('T4', vals['table2_nonafr_2021'], src2, 'cell 9 first loop 2021')
add('T5', vals['table2_afr_2021'], src2, 'cell 9 second loop 2021')

# Cell 3 counts from executed notebook
nb = json.load(open(os.path.join(OUT, 'executed.ipynb')))
txt = ''
for c in nb['cells']:
    if c['cell_type'] == 'code' and 'Number of seed papers' in ''.join(c['source']):
        for o in c['outputs']:
            txt += ''.join(o.get('text', ''))
add('cell3_nb_papers', int(re.search(r'Number of seed papers: (\d+)', txt).group(1)), 'outputs/executed.ipynb')
add('cell3_nb_authors', int(re.search(r'Number of associated authors: (\d+)', txt).group(1)), 'outputs/executed.ipynb', 'T6 candidate 2')

with open(os.path.join(OUT, 'targets_extracted.csv'), 'w', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=['key', 'value', 'source_file', 'note']); w.writeheader(); w.writerows(rows)

# Boundary authority scores (unseeded nx.hits, same call as cell 8) on the cell 6 graphs
G = pickle.load(open(os.path.join(RUN, 'audit_G_citation_cell6.pkl'), 'rb'))['G_citation']
brows = []
for yr, lo, hi in [(2021, 40, 50), (2010, 18, 26)]:
    _, auth = nx.hits(G[yr])
    data = [(n, d.get('Author_Name'), d.get('Author_is_African', 0), d.get('Author_based_in_Africa', 0), auth[n]) for n, d in G[yr].nodes(data=True)]
    dfa = pd.DataFrame(data, columns=['AuthorID', 'Author_Name', 'Author_is_African', 'Author_based_in_Africa', 'Authority'])
    dfa.sort_values(by='Authority', ascending=False, inplace=True)
    dfa = dfa.reset_index(drop=True)
    for r in range(lo, hi + 1):
        x = dfa.iloc[r - 1]
        brows.append({'year': yr, 'rank': r, 'AuthorID': x.AuthorID, 'Author_is_African': x.Author_is_African,
                      'Author_based_in_Africa': x.Author_based_in_Africa, 'Authority': repr(float(x.Authority))})
pd.DataFrame(brows).to_csv(os.path.join(OUT, 'boundary_authority_scores.csv'), index=False)
print(open(os.path.join(OUT, 'targets_extracted.csv')).read())
print(pd.DataFrame(brows).to_string())
