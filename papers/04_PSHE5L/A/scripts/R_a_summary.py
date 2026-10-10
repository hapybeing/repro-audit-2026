"""Summarise outputs/R_a_boot.csv into outputs/R_a_summary.json (median, percentile 95% CI, share b1<0, failures)."""
import csv, json, os, statistics
OUT = os.path.join(os.path.dirname(__file__), "..", "outputs")
rows = list(csv.DictReader(open(os.path.join(OUT, "R_a_boot.csv"))))
reps = sorted(int(r["rep"]) for r in rows)
assert len(reps) == len(set(reps)), "duplicate replicates"
ok = [r for r in rows if r["converged"] == "TRUE" and r["b1_std"] not in ("", "NA")]
def pct(xs, q):  # type-7 quantile (R default)
    xs = sorted(xs); h = (len(xs) - 1) * q; lo = int(h); hi = min(lo + 1, len(xs) - 1)
    return xs[lo] + (h - lo) * (xs[hi] - xs[lo])
res = {"replicates_attempted": len(rows), "replicates_ok": len(ok), "replicates_failed_or_nonconverged": len(rows) - len(ok),
       "seed": 20261009}
for name in ("b1_std", "indirect_std"):
    xs = [float(r[name]) for r in ok]
    res[name] = {"median": statistics.median(xs), "ci95_lower": pct(xs, 0.025), "ci95_upper": pct(xs, 0.975),
                 "share_below_0": sum(x < 0 for x in xs) / len(xs), "ci_excludes_0": pct(xs, 0.025) > 0 or pct(xs, 0.975) < 0}
json.dump(res, open(os.path.join(OUT, "R_a_summary.json"), "w"), indent=1)
print(json.dumps(res, indent=1))
