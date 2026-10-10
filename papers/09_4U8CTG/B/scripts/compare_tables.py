#!/usr/bin/env python3
"""Compare regenerated .tex tables (run/) with deposited copies (deposit/); copies regenerated tables to outputs/tables_regenerated and writes outputs/table_compare.json + diffs."""
import os, json, shutil, subprocess, sys
S = '/workspace/audit_runs/09_4U8CTG/B'
B = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out = os.path.join(B, 'outputs', 'tables_regenerated'); os.makedirs(out, exist_ok=True)
res = {}
for sub in ('tables_supplementary_materials',):
    dep = os.path.join(S, 'deposit', sub); run = os.path.join(S, 'run', sub)
    for f in sorted(os.listdir(dep)):
        a = os.path.join(dep, f); b = os.path.join(run, f)
        # run/ started as a copy of deposit/, so a table counts as regenerated only if its mtime is newer than the copy
        regenerated = os.path.getmtime(b) > os.path.getmtime(os.path.join(S, 'run', 'README.md')) + 1
        norm = lambda p: [l.rstrip() for l in open(p, encoding='utf-8', errors='replace').read().replace('\r\n', '\n').split('\n')]
        same = norm(a) == norm(b)
        if regenerated: shutil.copy(b, os.path.join(out, f))
        d = subprocess.run(['diff', '-u', '--strip-trailing-cr', a, b], capture_output=True, text=True).stdout
        if regenerated and not same:
            open(os.path.join(out, f + '.diff'), 'w').write(d)
        res[f] = {'regenerated': regenerated, 'identical_to_deposit_ignoring_line_endings': same if regenerated else None,
                  'n_diff_lines': sum(1 for l in d.split('\n') if l[:1] in '+-' and l[:3] not in ('+++', '---')) if regenerated else None}
json.dump(res, open(os.path.join(B, 'outputs', 'table_compare.json'), 'w'), indent=1)
for k, v in res.items(): print(k, v)
