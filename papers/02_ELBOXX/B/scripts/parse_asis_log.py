"""Parse the two htest blocks from the as-is Path A logr log (outputs/pathA_asis/replication.log)."""
import re, csv, sys
B = sys.argv[1]
txt = open(f"{B}/outputs/pathA_asis/replication.log").read()
blocks = re.findall(r"data:\s+(\S+) and \S+\nt = ([\d.]+), df = (\d+), p-value [<=] ([\d.e+-]+)\n.*?\n95 percent confidence interval:\n\s*([\d.]+) ([\d.]+)\nsample estimates:\n\s*cor\s*\n\s*([\d.]+)", txt, re.S)
rows = []
for (var, t, df, p, lo, hi, r), test in zip(blocks, ["M1", "M2"]):
    rows.append(dict(route="A_asis_date2026", test=test, r=r, ci_lo=lo, ci_hi=hi, t=t, df=df, p=p, n=int(df) + 2))
with open(f"{B}/outputs/pathA_asis/targets_asis.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print(rows)
