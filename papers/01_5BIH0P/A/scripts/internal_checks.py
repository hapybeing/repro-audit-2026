"""Pre-registered internal checks I1-I3 and robustness R_a, R_b, R_c for 01_5BIH0P (PREREG.md sections 2-3),
plus supplementary consistency checks (not pre-registered, labelled 'supp').
Input: deposited FINAL_RESULTS_MMPBSA.csv / .dat, *_gb.mdout.0, *_gb_surf.dat.0 (raw/files).
Output: REPO/papers/01_5BIH0P/A/outputs/*.csv|json. All numbers written by this script."""
import csv, json, re, os
import numpy as np

RAW = "/workspace/audit_runs/01_5BIH0P/A/raw/files"
OUT = "/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/01_5BIH0P/A/outputs"
os.makedirs(OUT, exist_ok=True)

# ---- parse FINAL_RESULTS_MMPBSA.csv into {model: {table: [rows]}}
lines = open(os.path.join(RAW, "FINAL_RESULTS_MMPBSA.csv")).read().splitlines()
data, model, table, header = {}, None, None, None
for ln in lines:
    s = ln.strip()
    if s in ("GENERALIZED BORN:", "POISSON BOLTZMANN:"):
        model = "GB" if s.startswith("GEN") else "PB"; data[model] = {}; continue
    if s.endswith("Energy Terms"):
        table = s.split()[0]; data[model][table] = []; header = None; continue
    if not s: continue
    row = next(csv.reader([s]))
    if row[0].startswith("Frame"):
        header = row; continue
    if header and model and table:
        data[model][table].append({h: float(v) for h, v in zip(header, row)})

def col(model, table, name):
    return np.array([r[name] for r in data[model][table]])

frames = col("GB", "Delta", "Frame #").astype(int)
assert len(frames) == 20, len(frames)

# per-frame table out
with open(os.path.join(OUT, "per_frame_delta.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["frame", "GB_dTOTAL", "GB_dVDWAALS", "GB_dEEL", "GB_dEGB", "GB_dESURF", "PB_dTOTAL"])
    for i, f in enumerate(frames):
        w.writerow([f] + [col("GB", "Delta", k)[i] for k in ("TOTAL", "VDWAALS", "EEL", "EGB", "ESURF")] + [col("PB", "Delta", "TOTAL")[i]])

def summ(x):
    x = np.asarray(x, float)
    sd = float(np.std(x, ddof=1))
    return {"n": int(x.size), "mean": float(x.mean()), "sd_ddof1": sd, "sem": sd / np.sqrt(x.size),
            "sd_ddof0": float(np.std(x, ddof=0)), "sem_ddof0": float(np.std(x, ddof=0) / np.sqrt(x.size))}

checks = {
    "I1_GB_dTOTAL": summ(col("GB", "Delta", "TOTAL")),
    "I2_PB_dTOTAL": summ(col("PB", "Delta", "TOTAL")),
    "I3_GB_dVDWAALS": summ(col("GB", "Delta", "VDWAALS")),
    "I3_GB_dEEL": summ(col("GB", "Delta", "EEL")),
    "I3_GB_dEGB": summ(col("GB", "Delta", "EGB")),
    "I3_GB_dESURF": summ(col("GB", "Delta", "ESURF")),
}

# ---- deposited summary values from FINAL_RESULTS_MMPBSA.dat (Delta blocks), for comparison
dat = open(os.path.join(RAW, "FINAL_RESULTS_MMPBSA.dat"), encoding="utf-8").read()
dep = {}
for mname, block in re.findall(r"(GENERALIZED BORN|POISSON BOLTZMANN):(.*?)(?=\n(?:GENERALIZED BORN|POISSON BOLTZMANN):|\Z)", dat, re.S):
    m = "GB" if mname.startswith("GEN") else "PB"
    delta = block.split("Delta (Complex - Receptor - Ligand):")[1]
    for ln in delta.splitlines():
        p = ln.split()
        if len(p) == 6 and p[0].startswith("Δ"):
            dep[f"{m}_d{p[0][1:]}"] = {"average": float(p[1]), "sd_prop": float(p[2]), "sd": float(p[3]),
                                       "sem_prop": float(p[4]), "sem": float(p[5])}
json.dump(dep, open(os.path.join(OUT, "deposited_delta_summary_from_dat.json"), "w"), indent=1)
json.dump(checks, open(os.path.join(OUT, "internal_checks.json"), "w"), indent=1)

# ---- R_a bootstrap
x = col("GB", "Delta", "TOTAL")
rng = np.random.default_rng(seed=20261009)
boots = np.array([rng.choice(x, size=x.size, replace=True).mean() for _ in range(10000)])
lo, hi = np.percentile(boots, [2.5, 97.5])
R_a = {"n_resamples": 10000, "seed": 20261009, "bootstrap_mean": float(boots.mean()),
       "ci_2.5": float(lo), "ci_97.5": float(hi), "ci_excludes_0": bool(hi < 0 or lo > 0), "point_estimate": float(x.mean())}

# ---- R_b outliers
z = (x - x.mean()) / np.std(x, ddof=1)
keep = np.abs(z) <= 3
R_b = {"rule": "|z|>3 (ddof=1); fallback 5% trimming (drop 1 lowest, 1 highest of 20)", "max_abs_z": float(np.abs(z).max()),
       "n_dropped_z3": int((~keep).sum()), "frames_dropped_z3": [int(f) for f in frames[~keep]]}
if (~keep).sum() > 0:
    s = summ(x[keep]); R_b.update({"applied": "z3", "mean": s["mean"], "sem": s["sem"], "n": s["n"]})
else:
    xs = np.sort(x)[1:-1]; s = summ(xs)
    R_b.update({"applied": "trim_1_each_side", "mean": s["mean"], "sem": s["sem"], "n": s["n"],
                "dropped_low": float(np.sort(x)[0]), "dropped_high": float(np.sort(x)[-1])})
# one-sample t-test p for the robustness mean vs 0 (descriptive)
try:
    from scipy import stats
except ImportError:
    stats = None
def tp(v):
    if stats is None: return None
    return float(stats.ttest_1samp(v, 0.0).pvalue)
R_a["p_t_full"] = tp(x)
R_b["p_t"] = tp(x[keep]) if R_b["applied"] == "z3" else tp(np.sort(x)[1:-1])

# ---- R_c PB instead of GB
pb = col("PB", "Delta", "TOTAL")
s = summ(pb)
R_c = {"model": "Poisson-Boltzmann (deposited per-frame PB Delta TOTAL)", "mean": s["mean"], "sem": s["sem"], "sd": s["sd_ddof1"],
       "n": s["n"], "p_t": tp(pb), "same_sign_as_GB": bool(np.sign(pb.mean()) == np.sign(x.mean())), "GB_mean": float(x.mean())}
json.dump({"R_a": R_a, "R_b": R_b, "R_c": R_c}, open(os.path.join(OUT, "robustness.json"), "w"), indent=1)

# ---- supplementary (not pre-registered): Delta = Complex - Receptor - Ligand per frame; mdout and surf.dat vs CSV
supp = {}
for m in ("GB", "PB"):
    d = col(m, "Delta", "TOTAL"); c = col(m, "Complex", "TOTAL") - col(m, "Receptor", "TOTAL") - col(m, "Ligand", "TOTAL")
    supp[f"{m}_delta_identity_max_abs_diff"] = float(np.abs(d - c).max())
surften = 0.0072
for part, tab in (("complex", "Complex"), ("receptor", "Receptor"), ("ligand", "Ligand")):
    md = open(os.path.join(RAW, f"_GMXMMPBSA_{part}_gb.mdout.0")).read()
    # only the first energy block after each 'NSTEP' header (later blocks in the same frame are decomposition checks)
    blocks = [b.split("CHECK DECOMP")[0] for b in md.split("   NSTEP ")[1:]]
    terms = {k: [float(re.search(rf"(?<!1-4 ){k}\s*=\s*(-?\d+\.\d+)", b).group(1)) for b in blocks] for k in ("VDWAALS", "EEL", "EGB", "BOND")}
    n = len(terms["VDWAALS"])
    diffs = {k: float(np.abs(np.array(terms[k]) - col("GB", tab, k)).max()) if len(terms[k]) == 20 else None for k in terms}
    sa = np.loadtxt(os.path.join(RAW, f"_GMXMMPBSA_{part}_gb_surf.dat.0"), comments="#")[:, 1]
    esurf_diff = float(np.abs(np.round(sa * surften, 2) - col("GB", tab, "ESURF")).max())
    supp[f"mdout_{part}"] = {"n_frames_in_mdout": n, "max_abs_diff_vs_csv": diffs, "esurf_from_surf_dat_max_abs_diff": esurf_diff}
json.dump(supp, open(os.path.join(OUT, "supplementary_consistency.json"), "w"), indent=1)
print(json.dumps({"checks": checks, "dep": dep, "R": {"R_a": R_a, "R_b": R_b, "R_c": R_c}, "supp": supp}, indent=1))
