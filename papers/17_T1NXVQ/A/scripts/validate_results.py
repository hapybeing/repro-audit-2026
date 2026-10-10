#!/usr/bin/env python3
"""Agent A, 17_T1NXVQ: check results.json parses and every reproduced number appears in its source file in outputs/."""
import csv, json, os
A = "/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/17_T1NXVQ/A"
d = json.load(open(f"{A}/results.json")); out = []; ok_all = True
def found(val, files):
    for f in files:
        p = os.path.join(A, f.strip())
        if not os.path.exists(p) or not p.endswith(".csv"): continue
        for row in csv.reader(open(p)):
            for c in row:
                try:
                    if abs(float(c) - val) < 1e-12: return f.strip()
                except ValueError: pass
    return None
for t in d["targets"]:
    if t["reproduced_value"] is None: out.append(f"{t['id']}: null"); continue
    s = found(t["reproduced_value"], [t["source_file"]]); ok_all &= s is not None
    out.append(f"{t['id']}: {t['reproduced_value']} found in {s}")
for r in d["robustness"]:
    if r["estimate"] is None: out.append(f"{r['id']}: not run"); continue
    s = found(r["estimate"], r["source_file"].split(";")); ok_all &= s is not None
    out.append(f"{r['id']}: {r['estimate']} found in {s}")
for o in d.get("other_checks", []):
    v = o.get("max_abs_diff")
    if v is not None:
        s = found(v, [o["source_file"]]); ok_all &= s is not None; out.append(f"{o['id']}: {v} found in {s}")
txt = json.dumps(d, ensure_ascii=False)
out.append(f"em dash present: {chr(0x2014) in txt}")
out.append(f"ALL TRACED: {ok_all}")
open(f"{A}/outputs/validate_results.txt", "w").write("\n".join(out) + "\n"); print("\n".join(out))
