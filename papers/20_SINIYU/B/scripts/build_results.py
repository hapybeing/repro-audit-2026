"""Agent B: build results.json for 20_SINIYU from files in outputs/ and the frozen targets.json."""
import json, csv, re, os, datetime
B = "/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/20_SINIYU/B"
P = os.path.dirname(B)
O = os.path.join(B, "outputs")
targets = json.load(open(os.path.join(P, "targets.json")))
ext = {r["quantity"]: r for r in csv.DictReader(open(os.path.join(O, "targets_extracted.csv")))}
log = open(os.path.join(O, "O_B_Ku.log")).read()
err = re.search(r"(ModuleNotFoundError: .*)", log)
err = err.group(1) if err else None
mod = json.load(open(os.path.join(O, "deposit_module_search.json")))
inp = json.load(open(os.path.join(O, "input_check.json")))
demo = json.load(open(os.path.join(O, "code_observation_demo.json")))

def num(q):
    v = ext.get(q, {}).get("value", "")
    return float(v) if v not in ("", None) else None

tl = []
for t in targets:
    rv, src, note = None, None, ""
    if t["id"] == "T1":
        rv, src = num("T1_mean_unrounded"), "outputs/targets_extracted.csv"
        note = f"Not produced. codes/figure6/O_B_Ku.py stops at line 17: {err} (outputs/O_B_Ku.log). Module not in deposit (outputs/deposit_module_search.json) or cited locations (DATA_STATEMENT.md)."
    elif t["id"] == "T2":
        v = num("T2_count"); rv = int(v) if v is not None else None; src = "outputs/targets_extracted.csv"
        note = f"Not produced; same failure as T1 ({err})."
    else:
        note = "No deposited code computes Table 1 (no volume-matching script; grep in outputs/deposit_module_search.json content_hits shows none). Not produced; no replacement code written (batch4 decision 5)."
    pv = t["paper_value"]; d = t["paper_rounding_decimals"]
    if rv is not None:
        ad = abs(rv - pv); rd = (rv - pv) / pv
        m2r = round(rv, d) == pv; w5 = abs(rd) <= 0.05
    else:
        ad = rd = m2r = w5 = None
    tl.append({"id": t["id"], "description": t["description"], "paper_value": pv, "paper_rounding_decimals": d,
               "reproduced_value": rv, "source_file": src, "abs_diff": ad, "rel_diff": rd,
               "match_to_rounding": m2r, "within_5pct": w5, "same_conclusion": None, "note": note})

rob_reason = f"Not run: needs the O-B `data` vector built by O_B_Ku.py, which stops at line 17 ({err})."
rob = [
 {"id": "R_a", "description": "Bootstrap of T1 mean: default_rng(20261010), 2000 resamples with replacement, percentile 95% CI, bootstrap SE, two-sided bootstrap p", "ran": False, "estimate": None, "se_or_ci": "", "p_value": None, "same_direction_and_significance_as_paper": None, "source_file": "outputs/O_B_Ku.log", "note": rob_reason},
 {"id": "R_b", "description": "Drop |z|>3 (np.std ddof=0) from data; mean, n dropped, 95% t-interval, one-sample t-test vs 0", "ran": False, "estimate": None, "se_or_ci": "", "p_value": None, "same_direction_and_significance_as_paper": None, "source_file": "outputs/O_B_Ku.log", "note": rob_reason},
 {"id": "R_c", "description": "Copy of O_B_Ku.py without lines 419-420 (6000 m height cap); mean, n, 95% t-interval, p vs 0", "ran": False, "estimate": None, "se_or_ci": "", "p_value": None, "same_direction_and_significance_as_paper": None, "source_file": "outputs/O_B_Ku.log", "note": rob_reason + " The modified copy would fail at the same import."},
]

# time from LOG.md timestamps
ts = re.findall(r"^- (\d{4}-\d{2}-\d{2} \d{2}:\d{2})", open(os.path.join(B, "LOG.md")).read(), re.M)
tt = [datetime.datetime.strptime(x, "%Y-%m-%d %H:%M") for x in ts]
minutes = int((max(tt) - min(tt)).total_seconds() // 60) if tt else None

res = {
 "paper_id": "20_SINIYU", "agent": "B", "run_date_ist": "2026-10-11",
 "ran": False,
 "could_not_run_reason": f"The only deposited script that computes a paper number (codes/figure6/O_B_Ku.py, T1/T2) fails at line 17: {err}. The f2py module interp_radar is not in the deposit (64 files/members searched, outputs/deposit_module_search.json) nor in the locations the data statement names (DATA_STATEMENT.md). No deposited code computes Table 1 (T3-T6). All other inputs O_B_Ku.py reads are present (outputs/input_check.json).",
 "targets": tl,
 "robustness": rob,
 "bugs": [],
 "code_observations_unverified": [
  {"file": "codes/figure6/O_B_Ku.py", "line": 420, "description": "Line 419 sets radar_Z_out to NaN where > 6000 m; line 420 then tests radar_Z_out>6000. to mask obs_mesh_meso, which is False for NaN, so line 420 masks no cells. Whether the 6000 m cut still acts depends on how the missing interp_radar_ppi treats NaN heights.", "evidence": f"outputs/code_observation_demo.json lines_419_420: cells_masked_by_420 = {demo['lines_419_420']['cells_masked_by_420']} on a toy array with two heights above 6000 m. Effect on T1/T2 not demonstrable without the module.", "status": "unverified observation"},
  {"file": "codes/figure6/O_B_Ku.py", "line": 345, "description": "Line 344 clips negative simulated ZH to 0 (xr.where(ZH<0, 0, ZH)); line 345 overwrites B_value with B_ds['ZH']/Rvar, so the clip has no effect. Same pattern in 1DVAR.py lines 311-312. Later B_KuRH<18 is set to NaN (line 480), so any effect would be only through the interpolation.", "evidence": f"outputs/code_observation_demo.json lines_343_345: negative_values_kept = {demo['lines_343_345']['negative_values_kept']}. Effect on outputs not demonstrable.", "status": "unverified observation"},
  {"file": "codes/figure6/O_B_Ku.py", "line": 20, "description": "plt.style.use(['science','no-latex']) raises OSError with SciencePlots 2.2.2 unless `import scienceplots` runs first (environment issue, cosmetic; not reached because line 17 fails first).", "evidence": "outputs/input_check.json 'scienceplots style': " + inp.get("scienceplots style", ""), "status": "environment observation, not a bug"},
 ],
 "env_fixes": ["diffs/paths_symlinks.txt: path-only symlinks FY3G_PMR.HDF -> extracted FY3G_PMR.HDF4, gep00/postvar.nc -> postvar.nc, gep00/swath_spaceborn.nc -> swath_spaceborn_mu3.nc (PREREG steps 1-3; batch4 decision 1). No authors' file was edited."],
 "proposed_class": "C",
 "class_reason": "Materials incomplete: O_B_Ku.py, the only deposited script computing a target (T1, T2), imports interp_radar, which is not in the deposit or any location the data statement names, and no deposited code computes Table 1 (T3-T6); per CHANGELOG #4 and batch4 decision 5 these count as not produced.",
 "confidence": "high",
 "confidence_reason": "The failure is deterministic (import error at line 17) and the absence is backed by a scripted search of every deposit file and archive member; no judgement about numbers was needed.",
 "time_minutes": minutes,
 "out_of_scope": "Claims needing CMA-MESO and its 3D-Var system (Figures 6b, 7, 9 to 13; forecast improvement, CSI/FBIAS) are out of scope per PREREG; not attempted.",
 "uncertainties": [
  "The search for interp_radar covered the deposit, the cited data locations (via DATA_STATEMENT.md, not repeated by B) and PyPI (404, uncited). Absence can only be shown within what was searched; ZJU-AERO 0.4.1 and uncited archives were not checked by B.",
  "Because the script never ran past line 17, no later blocker (memory for the 650 MB HDF arrays with ~1.6 GB free at run time, other runtime errors) could be tested.",
  "The two code observations (lines 419-420, 343-345) are shown only on toy arrays; their effect on T1/T2 is unknown.",
  "PREREG-flagged text/code differences (retrieval threshold >10 vs 'at least 10', pressure-level spacing, Table 1 'greater than 0.82' vs lowest value 0.82) were not testable.",
 ],
}
json.dump(res, open(os.path.join(B, "results.json"), "w"), indent=1)
print(json.dumps({k: res[k] for k in ["proposed_class", "time_minutes", "ran"]}), [(t["id"], t["paper_value"], t["reproduced_value"]) for t in tl])
