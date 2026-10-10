"""Frames are compared by order (AmberTools numbers them 0..19, gmx_MMPBSA 10..1910).
Parse AmberTools MMPBSA.py GB recompute outputs (igb=5 and igb=2) and compare igb=5 per frame with the deposited GB values.
Writes outputs/amber_gb_recompute.json and copies run outputs into outputs/amber/."""
import csv, json, os, shutil, numpy as np
A = "/workspace/audit_runs/01_5BIH0P/A"
O = "/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/01_5BIH0P/A/outputs"
os.makedirs(f"{O}/amber", exist_ok=True)
def parse(path):
    data, table, header = {}, None, None
    for ln in open(path).read().splitlines():
        s = ln.strip()
        if s.startswith("POISSON BOLTZMANN"): break   # GB block only
        if s.endswith("Energy Terms"): table = s.split()[0].capitalize(); data[table] = []; header = None; continue
        if not s or table is None or s.endswith(":"): continue
        row = next(csv.reader([s]))
        if row[0].startswith("Frame"):
            # AmberTools 26 names Delta columns 'DELTA TOTAL', 'DELTA G gas'; gmx_MMPBSA uses 'TOTAL', 'GGAS'
            header = [h.replace("DELTA ", "").replace("G gas", "GGAS").replace("G solv", "GSOLV") for h in row]; continue
        if header:
            try: data[table].append({h: float(v) for h, v in zip(header, row) if h})
            except ValueError: pass
    return data
dep = parse(f"{A}/raw/files/FINAL_RESULTS_MMPBSA.csv")   # GB block of the deposited file
out = {}
for igb in (5, 2):
    d = f"{A}/gb_igb{igb}"; csvp = f"{d}/FINAL_RESULTS_igb{igb}.csv"; rec = {"ran": os.path.exists(csvp)}
    for f in (f"FINAL_RESULTS_igb{igb}.dat", f"FINAL_RESULTS_igb{igb}.csv", "mmpbsa_stdout.txt", "mdin_extdiel.diff", "gb.in", "_MMPBSA_gb.mdin"):
        if os.path.exists(f"{d}/{f}"): shutil.copy(f"{d}/{f}", f"{O}/amber/igb{igb}_{f}")
    if rec["ran"]:
        r = parse(csvp); delta = r["Delta"]
        tot = np.array([x["TOTAL"] for x in delta]); sd1 = float(np.std(tot, ddof=1))
        rec.update({"n_frames": len(delta), "delta_total_mean": float(tot.mean()), "delta_total_sd_ddof1": sd1,
                    "delta_total_sem_ddof1": sd1 / np.sqrt(len(tot)), "sem_text": f"SEM {sd1/np.sqrt(len(tot)):.2f} (ddof=1, n={len(tot)})",
                    "delta_means": {k: float(np.mean([x[k] for x in delta])) for k in delta[0] if k != "Frame #"}})
        if igb == 5:
            cmpd = {}
            for tab in ("Complex", "Receptor", "Ligand", "Delta"):
                for k in ("VDWAALS", "EEL", "EGB", "ESURF", "TOTAL"):
                    a = np.array([x[k] for x in r[tab]]); b = np.array([x[k] for x in dep[tab]])
                    cmpd[f"{tab}_{k}_max_abs_diff_vs_deposited"] = float(np.abs(a - b).max())
            rec["per_frame_comparison_with_deposited_GB"] = cmpd
        else:
            rec["note"] = f"igb=2 Delta TOTAL mean vs igb=5 recompute: same sign = {np.sign(tot.mean()) == np.sign(out['igb5'].get('delta_total_mean', np.nan))}"
    out[f"igb{igb}"] = rec
json.dump(out, open(f"{O}/amber_gb_recompute.json", "w"), indent=1)
print(json.dumps(out, indent=1))
