"""Build results.json for 20_SINIYU agent A from files in outputs/ and the frozen targets.json. No number is typed here."""
import json, csv, re, os
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(HERE)
targets = json.load(open("../targets.json"))
ext = {r["id"]: r for r in csv.DictReader(open("outputs/targets_extracted.csv"))}
dep = json.load(open("outputs/deposit_module_search.json"))
obs = json.load(open("outputs/code_observation_checks.json"))
log = open("outputs/O_B_Ku.log").read()
err = next(l for l in log.splitlines() if "Error" in l)
exit_code = open("outputs/O_B_Ku_exit.txt").read().strip()
T = []
for t in targets:
    r = ext[t["id"]]
    rv = float(r["value"]) if r["value"] else None
    pv, dec = t["paper_value"], t["paper_rounding_decimals"]
    if rv is None:
        ad = rd = m = w = sc = None
    else:
        ad = abs(rv - pv); rd = (rv - pv) / pv
        m = round(rv, dec) == pv; w = abs(rd) <= 0.05; sc = None
    T.append({"id": t["id"], "description": t["description"], "paper_value": pv, "paper_rounding_decimals": dec,
              "reproduced_value": rv, "source_file": "outputs/targets_extracted.csv", "abs_diff": ad, "rel_diff": rd,
              "match_to_rounding": m, "within_5pct": w, "same_conclusion": sc,
              "note": "not produced: " + r["reason"] + " (detail in " + r["source"] + ")"})
rob_note = "not run: starts from the O-B data vector that O_B_Ku.py never builds (" + err.strip() + ", outputs/O_B_Ku.log)"
R = [{"id": i, "description": d, "ran": False, "estimate": None, "se_or_ci": "", "p_value": None,
      "same_direction_and_significance_as_paper": None, "source_file": "outputs/O_B_Ku.log", "note": rob_note}
     for i, d in [("R_a", "Bootstrap of the Ku O-B mean, 2000 resamples, rng default_rng(20261010)"),
                  ("R_b", "Drop |z|>3 O-B values (np.std ddof=0), mean, 95% t-interval, one-sample t-test vs 0"),
                  ("R_c", "Copy of O_B_Ku.py without lines 419-420 (6000 m height cap), mean, n, 95% t-interval, p")]]
res = {
 "paper_id": "20_SINIYU", "agent": "A", "run_date_ist": "2026-10-11",
 "ran": False,
 "could_not_run_reason": "codes/figure6/O_B_Ku.py (the only deposited script that computes a target, T1/T2) stops at line 17: "
     + err.strip() + " (" + exit_code + "). The f2py module interp_radar is not in the deposit (" + str(dep["n_files_scanned"])
     + " files scanned, outputs/deposit_module_search.json) nor in the locations the data statement names (../DATA_STATEMENT.md). "
     "No deposited code computes Table 1 (T3-T6). No replacement code written, per batch 4 brief and class decision 5.",
 "targets": T, "robustness": R,
 "bugs": [],
 "code_observations_unverified": [
   {"file": "codes/figure6/O_B_Ku.py", "line": 420,
    "description": "Line 419 sets radar_Z_out to NaN where >6000; line 420 then tests radar_Z_out>6000. to mask obs_mesh_meso, which is False for NaN, so line 420 masks nothing. Whether the 6000 m cut still acts depends on the undeposited interp_radar_ppi.",
    "evidence": "outputs/code_observation_checks.json obs1_obs_cells_masked_on_toy_array = " + str(obs["obs1_obs_cells_masked_on_toy_array"]) + "; effect on T1/T2 not measurable"},
   {"file": "codes/figure6/O_B_Ku.py", "line": 345,
    "description": "Line 344 sets B_value to 0 where ZH<0; line 345 overwrites B_value with raw ZH/Rvar, so the clip has no effect.",
    "evidence": "outputs/code_observation_checks.json: " + str(obs["obs2_swath_ZH_n_below_0"]) + " of " + str(obs["obs2_swath_ZH_n_finite"]) + " swath ZH values are below 0; lines 479-480 later drop interpolated values <18, so any effect is only through the interpolation, which cannot be run"}],
 "env_fixes": [
   "diffs/README.md: symlink FY3G_PMR.HDF -> FY3G_PMR.HDF4 (rar member, unrar-free -x), path-only",
   "diffs/README.md: symlink gep00/postvar.nc -> postvar.nc, path-only",
   "diffs/README.md: symlink gep00/swath_spaceborn.nc -> swath_spaceborn_mu3.nc, path-only",
   "environment.txt: Debian package time 1.9-0.2+b1 installed to provide /usr/bin/time -v (PREREG step 6); no authors' file edited"],
 "proposed_class": "C",
 "class_reason": "Materials incomplete: the only script that computes a pre-registered target (Figure 6a Ku O-B mean and count) imports interp_radar, which is not deposited or in any location the data statement names, and no deposited code computes Table 1; 0 of 6 targets produced (CHANGELOG #4, batch 4 class decision 5).",
 "confidence": "high",
 "confidence_reason": "Failure is a deterministic ModuleNotFoundError at the import line, independent of environment; absence backed by a scripted deposit scan and the pre-registered search log.",
 "time_minutes": 11,
 "uncertainties": [
   "The absence searches for interp_radar outside the deposit were done at pre-registration (../DATA_STATEMENT.md) and not repeated by agent A; an uncited copy (e.g. ZJU-AERO 0.4.1, zju_aero_env.tar.gz, Zenodo 10.5281/zenodo.19562313 data.zip) was not checked there and would not change the main class under CHANGELOG #4 in any case.",
   "Whether the deposited swath_spaceborn_mu3.nc is the exact file the authors read as gep00/swath_spaceborn.nc is inferred (figure7 names the _mu3 file); it could not be tested because the run stops first.",
   "Out of scope by design (PREREG): Figure 6b RH O-B, Figures 7 and 9 to 13 and the forecast-improvement claims (need CMA-MESO and 3D-Var, not public, and undeposited forecast/MET files).",
   "time_minutes is agent A's wall time from LOG.md (00:18 to 00:29 IST) plus writing; the runbook asks for it from LOG.md timestamps."]
}
json.dump(res, open("results.json", "w"), indent=1)
print(json.dumps({k: res[k] for k in ("ran", "proposed_class")}), [(t["id"], t["paper_value"], t["reproduced_value"]) for t in T])
