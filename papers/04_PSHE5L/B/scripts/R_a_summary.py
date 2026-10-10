# Summarise R_a bootstrap replicates from outputs/R_a_boot.csv into outputs/R_a_summary.json.
import csv, json, statistics, os
D = os.path.join(os.path.dirname(__file__), "..", "outputs")
rows = list(csv.DictReader(open(os.path.join(D, "R_a_boot.csv"))))
reps = sorted({int(r["rep"]) for r in rows})
assert len(reps) == len(rows), "duplicate replicate rows"
ok = [r for r in rows if r["converged"].upper() == "TRUE" and r["b1_std"] not in ("", "NA")]
def pct(v, q):  # R type-7 quantile
    v = sorted(v); h = (len(v) - 1) * q; lo = int(h); hi = min(lo + 1, len(v) - 1)
    return v[lo] + (h - lo) * (v[hi] - v[lo])
out = {"replicates_total": len(rows), "replicates_ok": len(ok),
       "replicates_failed_or_nonconverged": len(rows) - len(ok),
       "failed_errors": sorted({r["error"] for r in rows if r not in ok})}
for k in ("b1_std", "indirect1_std"):
    v = [float(r[k]) for r in ok]
    out[k] = {"median": statistics.median(v), "ci2.5": pct(v, 0.025), "ci97.5": pct(v, 0.975),
              "share_below_0": sum(x < 0 for x in v) / len(v)}
json.dump(out, open(os.path.join(D, "R_a_summary.json"), "w"), indent=1)
print(json.dumps(out, indent=1))
