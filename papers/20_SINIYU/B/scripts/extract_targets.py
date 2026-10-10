"""Agent B: extract T1/T2 from outputs/o_b_pvp.csv and outputs/ob_data.npy if the authors'
script produced them. Writes outputs/targets_extracted.csv. Values are null when the files do not exist."""
import os, csv, numpy as np
O = "/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/20_SINIYU/B/outputs"
rows = []
npy, csvf = os.path.join(O, "ob_data.npy"), os.path.join(O, "o_b_pvp.csv")
if os.path.exists(npy):
    d = np.load(npy)
    rows += [("T1_mean_unrounded", repr(float(np.mean(d))), "ob_data.npy"), ("T2_count", str(len(d)), "ob_data.npy"),
             ("sd_ddof0", repr(float(np.std(d))), "ob_data.npy"), ("median", repr(float(np.median(d))), "ob_data.npy")]
else:
    rows += [("T1_mean_unrounded", "", "ob_data.npy not produced"), ("T2_count", "", "ob_data.npy not produced")]
if os.path.exists(csvf):
    c = np.loadtxt(csvf, delimiter=",")
    rows += [("T1_mean_of_rounded_csv", repr(float(np.mean(c))), "o_b_pvp.csv"), ("csv_rows", str(len(c)), "o_b_pvp.csv")]
else:
    rows += [("T1_mean_of_rounded_csv", "", "o_b_pvp.csv not produced"), ("csv_rows", "", "o_b_pvp.csv not produced")]
with open(os.path.join(O, "targets_extracted.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(["quantity", "value", "source"]); w.writerows(rows)
print(open(os.path.join(O, "targets_extracted.csv")).read())
