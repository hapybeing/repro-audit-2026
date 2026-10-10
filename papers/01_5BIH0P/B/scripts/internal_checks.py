"""Agent B internal checks I1-I3 for 01_5BIH0P.
Reads the deposited FINAL_RESULTS_MMPBSA.csv (per-frame values) and FINAL_RESULTS_MMPBSA.dat (author summary),
recomputes mean/SD/SEM of Delta terms, also re-derives Delta = Complex - Receptor - Ligand per frame,
and cross-checks against RESULTS_gmx_MMPBSA.h5. Writes outputs/ files."""
import csv, json, re, sys, os
import numpy as np
RAW = sys.argv[1]; OUT = sys.argv[2]
os.makedirs(OUT, exist_ok=True)

def read_blocks(path):
    blocks = {}; model = None; sec = None; header = None
    for row in csv.reader(open(path)):
        if not row or all(not c.strip() for c in row):
            sec = None; continue
        s = row[0].strip()
        if s in ("GENERALIZED BORN:", "POISSON BOLTZMANN:"):
            model = "GB" if s.startswith("GEN") else "PB"; continue
        if s.endswith("Energy Terms"):
            sec = s.split()[0]; header = None; continue
        if sec and header is None:
            header = row; blocks[(model, sec)] = {"cols": header, "rows": []}; continue
        if sec:
            blocks[(model, sec)]["rows"].append([float(x) for x in row])
    return blocks

def read_dat_delta(path):
    res = {}; model = None; in_delta = False
    for line in open(path, encoding="utf8"):
        if line.startswith("GENERALIZED BORN"): model = "GB"; in_delta = False
        if line.startswith("POISSON BOLTZMANN"): model = "PB"; in_delta = False
        if line.startswith("Delta (Complex - Receptor - Ligand)"): in_delta = True; continue
        m = re.match(r"^\u0394(\S+)\s+(-?[\d.]+)\s+(-?[\d.]+)\s+(-?[\d.]+)\s+(-?[\d.]+)\s+(-?[\d.]+)", line)
        if in_delta and m and model:
            res[(model, m.group(1))] = dict(zip(["avg", "sd_prop", "sd", "sem_prop", "sem"], map(float, m.groups()[1:])))
    return res

b = read_blocks(os.path.join(RAW, "FINAL_RESULTS_MMPBSA.csv"))
dat = read_dat_delta(os.path.join(RAW, "FINAL_RESULTS_MMPBSA.dat"))
out = {"source_csv": "raw/FINAL_RESULTS_MMPBSA.csv", "source_dat": "raw/FINAL_RESULTS_MMPBSA.dat", "terms": {}}
per_frame = {}
for model, terms in (("GB", ["TOTAL", "VDWAALS", "EEL", "EGB", "ESURF", "GGAS", "GSOLV"]),
                     ("PB", ["TOTAL", "VDWAALS", "EEL", "EPB", "ENPOLAR", "EDISPER", "GGAS", "GSOLV"])):
    D = b[(model, "Delta")]; C = b[(model, "Complex")]; Rr = b[(model, "Receptor")]; L = b[(model, "Ligand")]
    frames = [r[0] for r in D["rows"]]
    assert frames == [r[0] for r in C["rows"]] == [r[0] for r in Rr["rows"]] == [r[0] for r in L["rows"]]
    for t in terms:
        i = D["cols"].index(t)
        x = np.array([r[i] for r in D["rows"]])
        crl = np.array([c[C["cols"].index(t)] - r[Rr["cols"].index(t)] - l[L["cols"].index(t)]
                        for c, r, l in zip(C["rows"], Rr["rows"], L["rows"])])
        per_frame[(model, t)] = x
        n = len(x)
        d = dat.get((model, t), {})
        out["terms"][f"{model}_d{t}"] = {
            "n_frames": n, "frames": frames if t == "TOTAL" else None,
            "mean": float(x.mean()), "sd_ddof1": float(x.std(ddof=1)), "sd_ddof0": float(x.std(ddof=0)),
            "sem_ddof1": float(x.std(ddof=1) / np.sqrt(n)), "sem_ddof0": float(x.std(ddof=0) / np.sqrt(n)),
            "mean_from_complex_minus_receptor_minus_ligand": float(crl.mean()),
            "max_abs_perframe_delta_vs_CRL": float(np.max(np.abs(x - crl))),
            "author_dat_avg": d.get("avg"), "author_dat_sd": d.get("sd"), "author_dat_sem": d.get("sem"),
            "mean_rounded2_equals_author": (round(float(x.mean()), 2) == d.get("avg")) if d else None,
            "abs_diff_mean_vs_author": (abs(float(x.mean()) - d["avg"]) if d else None),
        }
# per-frame table
with open(os.path.join(OUT, "per_frame_delta.csv"), "w", newline="") as f:
    w = csv.writer(f); keys = list(per_frame)
    w.writerow(["frame"] + [f"{m}_d{t}" for m, t in keys])
    for k, fr in enumerate(b[("GB", "Delta")]["rows"]):
        w.writerow([int(fr[0])] + [per_frame[key][k] for key in keys])
# h5 cross-check (independent copy of per-frame data stored by gmx_MMPBSA)
try:
    import h5py
    h = h5py.File(os.path.join(RAW, "RESULTS_gmx_MMPBSA.h5"), "r")
    paths = []
    h.visit(lambda p: paths.append(p))
    out["h5_paths_sample"] = paths[:80]
    hx = {}
    for model, key in (("GB", "gb"), ("PB", "pb")):
        for comp in ("complex", "receptor", "ligand"):
            g = f"normal/{key}/{comp}"
            if g in h:
                hx[(model, comp)] = {k: np.array(h[g][k]) for k in h[g].keys() if isinstance(h[g][k], h5py.Dataset)}
    chk = {}
    for model in ("GB", "PB"):
        if all((model, c) in hx for c in ("complex", "receptor", "ligand")):
            tot = {}
            for c in ("complex", "receptor", "ligand"):
                d = hx[(model, c)]
                keys = [k for k in d if k not in ("TOTAL", "GGAS", "GSOLV")]
                tot[c] = {k: d[k] for k in d}
            # Delta TOTAL from h5 if TOTAL present, else sum of components
            def total(d):
                if "TOTAL" in d: return d["TOTAL"]
                return sum(v for k, v in d.items() if k not in ("GGAS", "GSOLV"))
            dt = total(tot["complex"]) - total(tot["receptor"]) - total(tot["ligand"])
            chk[f"{model}_dTOTAL_h5_mean"] = float(np.mean(dt))
            chk[f"{model}_dTOTAL_h5_n"] = int(len(dt))
            chk[f"{model}_dTOTAL_h5_sd_ddof0"] = float(np.std(dt))
            chk[f"{model}_dTOTAL_h5_sd_ddof1"] = float(np.std(dt, ddof=1))
            chk[f"{model}_h5_component_keys"] = sorted(tot["complex"].keys())
            chk[f"{model}_max_abs_diff_h5_vs_csv_perframe"] = float(np.max(np.abs(np.round(dt, 2) - per_frame[(model, "TOTAL")])))
    out["h5_check"] = chk
except Exception as e:
    out["h5_check_error"] = repr(e)
json.dump(out, open(os.path.join(OUT, "internal_checks.json"), "w"), indent=1)
for k, v in out["terms"].items():
    print(k, round(v["mean"], 4), round(v["sd_ddof1"], 4), round(v["sd_ddof0"], 4), "author", v["author_dat_avg"], v["author_dat_sd"], v["mean_rounded2_equals_author"], "CRLdiff", v["max_abs_perframe_delta_vs_CRL"])
print(json.dumps(out.get("h5_check", out.get("h5_check_error")), indent=0)[:3000])
