# Compares the coefficient table printed in the deposited Regression.ipynb saved outputs (run 2024-09-28) with this run's
# outputs/regression_estimates.csv, at the 4 printed decimals (coef) and 3 (t). Also records saved N per model.
import json, sys, csv, re
nbp, O = sys.argv[1], sys.argv[2]
nb = json.load(open(nbp))
cellmap = {4:'results_1',5:'results_2',6:'results_3',7:'results_4',8:'results_S1',9:'results_S2',10:'results_S3',11:'results_S4'}
ours = {}
for r in csv.DictReader(open(O + '/outputs/regression_estimates.csv')):
    ours[(r['model'], r['variable'])] = r
rows = []
for ci, m in cellmap.items():
    txt = ''.join(''.join(o['data']['text/plain']) for o in nb['cells'][ci]['outputs'] if 'data' in o and 'text/plain' in o['data'])
    nsaved = re.search(r'No\. Observations:\s+(\d+)', txt).group(1)
    for line in txt.splitlines():
        p = line.split()
        if len(p) == 7 and (m, p[0]) in ours:
            o = ours[(m, p[0])]
            rows.append(dict(model=m, variable=p[0], saved_coef=p[1], saved_t=p[3], run_coef=f"{float(o['params']):.4f}",
                             run_t=f"{float(o['tvalues']):.3f}", saved_nobs=nsaved, run_nobs=int(float(o['nobs']))))
for r in rows:
    r['coef_match'] = (float(r['saved_coef']) == float(r['run_coef'])); r['t_match'] = (float(r['saved_t']) == float(r['run_t']))
    r['nobs_match'] = int(r['saved_nobs']) == r['run_nobs']
with open(O + '/outputs/saved_notebook_vs_run.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
n = len(rows); print('rows', n, 'coef_match', sum(r['coef_match'] for r in rows), 't_match', sum(r['t_match'] for r in rows),
      'nobs_match', sum(r['nobs_match'] for r in rows))
for r in rows:
    if not (r['coef_match'] and r['t_match']): print(r)
