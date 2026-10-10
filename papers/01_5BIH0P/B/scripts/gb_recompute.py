"""Parse Agent B sander (AmberTools) GB re-run outputs on the deposited intermediates and compare to the deposited
per-frame FINAL_RESULTS_MMPBSA.csv. ESURF = surften*SASA + surfoff (gmx_MMPBSA convention, surften=0.0072, surfoff=0),
SASA from Agent B's own cpptraj LCPO 'surf' run (B_<sys>_surf.dat) and, for comparison, from the deposited surf.dat files.
usage: gb_recompute.py GBDIR RAWDIR OUTDIR TAG"""
import re, sys, os, json, csv
import numpy as np
GB, RAW, OUT, TAG = sys.argv[1:5]
TERMS = ["BOND", "ANGLE", "DIHED", "UB", "IMP", "CMAP", "VDWAALS", "EEL", "1-4 VDW", "1-4 EEL", "EGB"]
pat = re.compile(r"(1-4 VDW|1-4 EEL|[A-Z]+)\s*=\s*(-?[\d.]+(?:E[-+]?\d+)?)")
def parse_mdout(path):
    frames = []; cur = None
    for line in open(path):
        if "FINAL RESULTS" in line: cur = {}; frames.append(cur); continue
        if cur is not None:
            for k, v in pat.findall(line): cur.setdefault(k, float(v))
    return frames
def read_surf(path):
    return np.array([float(l.split()[1]) for l in open(path) if not l.startswith("#") and l.strip()])
dep = {}
rows = list(csv.reader(open(os.path.join(RAW, "FINAL_RESULTS_MMPBSA.csv"))))
sec = None
for r in rows:
    if not r: sec = None; continue
    if r[0].startswith("POISSON"): break
    if r[0].endswith("Energy Terms"): sec = r[0].split()[0]; hdr = None; continue
    if sec and r[0].startswith("Frame"): hdr = r; dep[sec] = []; continue
    if sec and hdr: dep[sec].append(dict(zip(hdr, map(float, r))))
res = {"tag": TAG, "systems": {}}
tot = {}
for s, key in (("complex", "Complex"), ("receptor", "Receptor"), ("ligand", "Ligand")):
    fr = parse_mdout(os.path.join(GB, f"B_{s}_{TAG}.mdout"))
    n = len(fr)
    surfB_p = os.path.join(GB, f"B_{s}_surf.dat")
    surfB = read_surf(surfB_p) if os.path.exists(surfB_p) else None
    surfA = read_surf(os.path.join(RAW, f"_GMXMMPBSA_{s}_gb_surf.dat.0"))
    esurf = 0.0072 * (surfB if surfB is not None else surfA)
    e = np.array([sum(f[t] for t in TERMS) for f in fr]) + esurf[:n]
    tot[s] = e
    d = np.array([x["TOTAL"] for x in dep[key]])
    egb = np.array([f["EGB"] for f in fr]); degb = np.array([x["EGB"] for x in dep[key]])
    res["systems"][s] = {"n_frames": n, "max_abs_diff_TOTAL_vs_deposited": float(np.max(np.abs(e - d[:n]))) if n else None,
                         "max_abs_diff_EGB_vs_deposited": float(np.max(np.abs(egb - degb[:n]))) if n else None,
                         "esurf_source": "B cpptraj surf" if surfB is not None else "deposited surf.dat",
                         "max_abs_diff_SASA_B_vs_deposited": float(np.max(np.abs(surfB - surfA))) if surfB is not None else None}
n = min(len(v) for v in tot.values())
delta = tot["complex"][:n] - tot["receptor"][:n] - tot["ligand"][:n]
depd = np.array([x["TOTAL"] for x in dep["Delta"]])[:n]
res["delta_TOTAL"] = {"n_frames": n, "mean": float(delta.mean()), "sd_ddof0": float(delta.std()), "sd_ddof1": float(delta.std(ddof=1)) if n > 1 else None,
                      "per_frame": [float(x) for x in delta], "deposited_per_frame": [float(x) for x in depd],
                      "max_abs_diff_vs_deposited_per_frame": float(np.max(np.abs(delta - depd))) if n else None,
                      "deposited_mean_same_frames": float(depd.mean()) if n else None}
json.dump(res, open(os.path.join(OUT, f"gb_recompute_{TAG}.json"), "w"), indent=1)
print(json.dumps({k: v for k, v in res.items()}, indent=1)[:2500])
