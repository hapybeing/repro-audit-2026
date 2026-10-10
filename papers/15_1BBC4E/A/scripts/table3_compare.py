# Compare all 21 Table 3 cells (secondary context printed in PREREG.md section 1) with the reproduced corr.ea matrix.
import csv, re
P = "/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/15_1BBC4E/"
txt = open(P + "PREREG.md").read()
line = [l for l in txt.splitlines() if l.startswith("Secondary context only")][0]
names = ["LIED", "RoW", "Polity", "FH", "ARD", "AoW", "CPR"]
paper = {}
for n in names:
    vals = [float(x) for x in re.search(n + r" row ([0-9. ]+)", line).group(1).split()]
    others = [m for m in names if m != n]
    for o, v in zip(others, vals): paper[(n, o)] = v
rep = {}
for r in csv.DictReader(open(P + "A/outputs/corr_ea_fullprec.csv")):
    for o in names:
        if r[o] != "NA": rep[(r["term"], o)] = float(r[o])
rows = []
for i, a in enumerate(names):
    for b in names[i + 1:]:
        rows.append(dict(row=a, col=b, paper=paper[(a, b)], reproduced=rep[(a, b)], match_3dp=round(rep[(a, b)], 3) == paper[(a, b)]))
with open(P + "A/outputs/table3_full_comparison.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print(sum(r["match_3dp"] for r in rows), "of", len(rows), "cells match to 3 dp")
