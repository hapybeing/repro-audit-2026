"""PREREG step 6: read the unrounded O-B vector (outputs/ob_data.npy) or o_b_pvp.csv written by O_B_Ku.py and write
outputs/targets_extracted.csv (T1 mean, T2 count, SD, median). If neither exists (script did not reach line 494),
write the row with empty values and the reason. T3-T6 have no deposited code and are written as not produced."""
import os, csv, numpy as np
RUN = "/workspace/audit_runs/20_SINIYU/A/run/figure6"
OUT = "outputs/targets_extracted.csv"
rows = []
src = None
for cand in ["outputs/ob_data.npy", os.path.join(RUN, "o_b_pvp.csv")]:
    if os.path.exists(cand): src = cand; break
if src:
    data = np.load(src) if src.endswith(".npy") else np.loadtxt(src, delimiter=",")
    rows.append({"id": "T1", "value": repr(float(np.mean(data))), "source": src, "reason": ""})
    rows.append({"id": "T2", "value": str(len(data)), "source": src, "reason": ""})
else:
    log = open("outputs/O_B_Ku.log").read()
    err = [l for l in log.splitlines() if "Error" in l]
    reason = "O_B_Ku.py did not produce o_b_pvp.csv: " + (err[0] if err else "unknown")
    rows += [{"id": t, "value": "", "source": "outputs/O_B_Ku.log", "reason": reason} for t in ("T1", "T2")]
for t in ("T3", "T4", "T5", "T6"):
    rows.append({"id": t, "value": "", "source": "outputs/deposit_module_search.json",
                 "reason": "no deposited code computes Table 1"})
with open(OUT, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["id", "value", "source", "reason"]); w.writeheader(); w.writerows(rows)
print(open(OUT).read())
