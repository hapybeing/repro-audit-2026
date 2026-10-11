# Summarises outputs/Ra_boot.csv into outputs/Ra_summary.json (R_a, pre-registered).
import csv, json, math, sys
OUT = sys.argv[1]
rows = list(csv.DictReader(open(f"{OUT}/Ra_boot.csv")))
reps = sorted({int(r["rep"]) for r in rows})
ok = [float(r["est"]) for r in rows if r["est"] not in ("", "NA") and r["error"] == "0"]
nonconv = sum(1 for r in rows if r["converged"] in ("0", "0.0"))
fail = len(rows) - len(ok)
def q7(xs, p):
    xs = sorted(xs); h = (len(xs) - 1) * p; lo = math.floor(h)
    return xs[lo] + (h - lo) * (xs[min(lo + 1, len(xs) - 1)] - xs[lo])
mean = sum(ok) / len(ok); sd = math.sqrt(sum((x - mean) ** 2 for x in ok) / (len(ok) - 1))
share_le0 = sum(1 for x in ok if x <= 0) / len(ok)
t1 = None
for r in csv.DictReader(open(f"{OUT}/targets_extracted.csv")):
    if r["quantity"] == "T1_beta_model3": t1 = float(r["value"])
res = {"B_planned": 999, "rows": len(rows), "unique_reps": len(reps), "successful": len(ok), "failed": fail,
       "nonconverged_flagged": nonconv, "estimate_T1": t1, "boot_mean": mean, "boot_sd": sd,
       "pct_2.5": q7(ok, 0.025), "pct_97.5": q7(ok, 0.975), "share_le_0": share_le0,
       "p_boot": min(2 * share_le0, 1.0), "seed": 20261011}
json.dump(res, open(f"{OUT}/Ra_summary.json", "w"), indent=1); print(json.dumps(res, indent=1))
