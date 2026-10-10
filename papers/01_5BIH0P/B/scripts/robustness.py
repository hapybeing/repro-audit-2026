"""Agent B robustness checks R_a, R_b, R_c for 01_5BIH0P, exactly as in PREREG section 3.
Input: outputs/per_frame_delta.csv (written by internal_checks.py from the deposited FINAL_RESULTS_MMPBSA.csv)."""
import csv, json, sys, os
import numpy as np
OUT = sys.argv[1]
rows = list(csv.DictReader(open(os.path.join(OUT, "per_frame_delta.csv"))))
gb = np.array([float(r["GB_dTOTAL"]) for r in rows]); pb = np.array([float(r["PB_dTOTAL"]) for r in rows])
n = len(gb); res = {"n_frames": n, "seed": 20261009}
# R_a: bootstrap of mean, 10,000 resamples, default_rng(20261009)
rng = np.random.default_rng(seed=20261009)
idx = rng.integers(0, n, size=(10000, n))
bm = gb[idx].mean(axis=1)
lo, hi = np.percentile(bm, [2.5, 97.5])
res["R_a"] = {"bootstrap_mean": float(bm.mean()), "ci_2.5": float(lo), "ci_97.5": float(hi),
              "ci_excludes_0": bool(hi < 0 or lo > 0), "share_boot_means_below_0": float((bm < 0).mean()),
              "n_resamples": 10000, "method": "rng.integers(0,n,size=(10000,n)); percentile interval"}
# R_b: |z|>3 with ddof=1; fallback drop single lowest and highest
z = (gb - gb.mean()) / gb.std(ddof=1)
keep = np.abs(z) <= 3
rb = {"max_abs_z": float(np.max(np.abs(z))), "n_dropped_absz_gt3": int((~keep).sum())}
if (~keep).sum() > 0:
    x = gb[keep]; rb.update(rule="drop |z|>3", mean=float(x.mean()), sem=float(x.std(ddof=1) / np.sqrt(len(x))), n=int(len(x)))
else:
    x = np.sort(gb)[1:-1]
    rb.update(rule="no |z|>3; fallback 5% trim each side (drop single lowest and highest of 20)",
              mean=float(x.mean()), sem=float(x.std(ddof=1) / np.sqrt(len(x))), n=int(len(x)),
              dropped_low=float(np.sort(gb)[0]), dropped_high=float(np.sort(gb)[-1]))
res["R_b"] = rb
# R_c: PB instead of GB
res["R_c"] = {"pb_mean": float(pb.mean()), "pb_sd_ddof1": float(pb.std(ddof=1)), "pb_sem_ddof1": float(pb.std(ddof=1) / np.sqrt(n)),
              "gb_mean": float(gb.mean()), "same_sign_as_gb": bool(np.sign(pb.mean()) == np.sign(gb.mean())),
              "pb_t_vs_0": float(pb.mean() / (pb.std(ddof=1) / np.sqrt(n)))}
json.dump(res, open(os.path.join(OUT, "robustness.json"), "w"), indent=1)
print(json.dumps(res, indent=1))
