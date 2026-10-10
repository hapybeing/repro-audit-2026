"""Build results.json for 01_5BIH0P, agent B, reading every number from files in outputs/.
usage: build_results.py PAPERDIR(REPO/papers/01_5BIH0P/B) START_HHMM END_HHMM (IST, from LOG.md)"""
import json, os, sys, datetime
B = sys.argv[1]; start, end = sys.argv[2], sys.argv[3]
O = lambda f: json.load(open(os.path.join(B, "outputs", f)))
ic = O("internal_checks.json"); rb = O("robustness.json"); xc = O("xvg_format_check.json"); ps = O("paper_scan.json")
gbp = os.path.join(B, "outputs", "gb_recompute_gb.json")
gb = json.load(open(gbp)) if os.path.exists(gbp) else None
T = ic["terms"]
def icrow(id_, key, paper_val):
    v = T[key]["mean"]
    return {"id": id_, "term": key, "prereg_author_value": paper_val, "author_dat_value_parsed": T[key]["author_dat_avg"],
            "recomputed_mean_from_perframe_csv": v, "match_to_2dp": round(v, 2) == paper_val,
            "recomputed_sd_ddof0": T[key]["sd_ddof0"], "recomputed_sd_ddof1": T[key]["sd_ddof1"], "author_dat_sd": T[key]["author_dat_sd"],
            "source_file": "outputs/internal_checks.json"}
# PREREG values for internal checks (copied from PREREG.md section 1, not paper targets)
internal = [icrow("I1", "GB_dTOTAL", -103.70), icrow("I2", "PB_dTOTAL", 14.42), icrow("I3_VDWAALS", "GB_dVDWAALS", -97.82),
            icrow("I3_EEL", "GB_dEEL", -668.97), icrow("I3_EGB", "GB_dEGB", 681.82), icrow("I3_ESURF", "GB_dESURF", -18.72)]
if gb:
    internal.append({"id": "I1_amber_rerun", "term": "GB dTOTAL recomputed with AmberTools 26 sander from deposited prmtop + mdcrd intermediates",
                     "n_frames": gb["delta_TOTAL"]["n_frames"], "recomputed_mean": gb["delta_TOTAL"]["mean"],
                     "deposited_mean_same_frames": gb["delta_TOTAL"]["deposited_mean_same_frames"],
                     "max_abs_perframe_diff_vs_deposited": gb["delta_TOTAL"]["max_abs_diff_vs_deposited_per_frame"],
                     "per_system": gb["systems"], "source_file": "outputs/gb_recompute_gb.json"})
ra, rbb, rc = rb["R_a"], rb["R_b"], rb["R_c"]
robust = [
 {"id": "R_a", "description": "Bootstrap of mean per-frame GB dTOTAL (20 frames), 10,000 resamples, default_rng(20261009); percentile 95% CI",
  "ran": True, "estimate": ra["bootstrap_mean"], "se_or_ci": f"95% percentile CI [{ra['ci_2.5']:.4f}, {ra['ci_97.5']:.4f}] kcal/mol; excludes 0: {ra['ci_excludes_0']}",
  "p_value": None, "same_direction_and_significance_as_paper": None, "source_file": "outputs/robustness.json",
  "note": "No paper value exists for 2XWT; compared only with the deposited GB mean (-103.70): same sign, CI excludes 0. Not a different MD seed (only seed 3 deposited)."},
 {"id": "R_b", "description": "Drop frames with |z|>3 (ddof=1) on per-frame GB dTOTAL; if none, drop single lowest and highest frame",
  "ran": True, "estimate": rbb["mean"], "se_or_ci": f"SEM {rbb['sem']:.4f} (ddof=1, n={rbb['n']})", "p_value": None,
  "same_direction_and_significance_as_paper": None, "source_file": "outputs/robustness.json",
  "note": f"max |z| = {rbb['max_abs_z']:.3f}, {rbb['n_dropped_absz_gt3']} frames with |z|>3, so fallback trim applied (dropped {rbb.get('dropped_low')} and {rbb.get('dropped_high')}). No paper value."},
 {"id": "R_c", "description": "Poisson-Boltzmann instead of Generalized Born: mean per-frame PB dTOTAL, same 20 frames",
  "ran": True, "estimate": rc["pb_mean"], "se_or_ci": f"SEM {rc['pb_sem_ddof1']:.4f} (ddof=1, n=20)", "p_value": None,
  "same_direction_and_significance_as_paper": None, "source_file": "outputs/robustness.json",
  "note": f"Sign differs from GB ({rc['gb_mean']:.4f}); same_sign_as_gb={rc['same_sign_as_gb']}. Descriptive only; no paper value. Optional R_c2 (igb=2) not run."}]
r = xc
bugs = [
 {"file": "xvg2csv.py (identical copy xvg2csv-1.py)", "line": 31,
  "description": "Legend test l.startswith('@ s') also matches GROMACS '@ subtitle' lines, so the subtitle is taken as a column label and cut by split()[3:] and [1:-1].",
  "evidence": f"2xwt-rs3-310k-200ns-rmsd.xvg contains '@ subtitle \"Protein after lsq fit to Protein\"' and no '@ s0 legend' line; script header written: '{r['2xwt-rs3-310k-200ns-rmsd']['first_line_written']}'; Dataverse ingest variable names {r['2xwt-rs3-310k-200ns-rmsd']['dataverse_ingest_varnames']}. Same in 400 ns RMSD file. Label only; values unaffected."},
 {"file": "xvg2csv.py (identical copy xvg2csv-1.py)", "line": 25,
  "description": "First column label is hard-coded 'Time (ps)' regardless of the x axis of the .xvg file.",
  "evidence": f"RMSD .xvg files were made with '-tu ns' and declare {r['2xwt-rs3-310k-200ns-rmsd']['xvg_axis_and_legend_lines'][0]!r}, but the deposited CSV/.tab column is named 'Time (ps)' (values 0.0, 0.01, ... are ns). Units label wrong in deposited 200 ns and 400 ns RMSD .tab files."},
 {"file": "xvg2csv.py (identical copy xvg2csv-1.py)", "line": 36,
  "description": "Header row is written only when the number of '@ s' lines equals columns-1; for a .xvg with no legend lines (gmx rmsf) no header is written.",
  "evidence": f"2xwt-rs3-400ns-310k-rmsf.csv first line is '{r['2xwt-rs3-400ns-310k-rmsf']['first_line_written']}' ({r['2xwt-rs3-400ns-310k-rmsf']['data_rows_in_xvg']} data rows); Dataverse ingest then used that row as variable names {r['2xwt-rs3-400ns-310k-rmsf']['dataverse_ingest_varnames']} and the ingested .tab has {r['2xwt-rs3-400ns-310k-rmsf']['dataverse_ingest_caseQnty']} cases, so residue 1 is missing from the ingested table (the original CSV still has it)."}]
t0 = datetime.datetime.strptime(start, "%H:%M"); t1 = datetime.datetime.strptime(end, "%H:%M")
gb_note = ("AmberTools GB rerun from deposited intermediates: " + (f"{gb['delta_TOTAL']['n_frames']} frames, max per-frame |diff| vs deposited dTOTAL {gb['delta_TOTAL']['max_abs_diff_vs_deposited_per_frame']:.4f} kcal/mol" if gb else "not completed"))
res = {
 "paper_id": "01_5BIH0P", "agent": "B", "run_date_ist": "2026-10-09", "ran": True,
 "could_not_run_reason": "No paper target exists for this dataset: the paper reports computed numbers only for 5DK3 (RMSD) and 6UMT (binding free energies); 2XWT appears only as a Table 1 metadata row (5 seeds, 200 ns, footnote b). The production trajectory is not deposited, so no RMSD/RMSF/Rg/SASA/H-bond series can be regenerated. Only internal-consistency checks and pre-registered robustness checks on the deposited MMPBSA per-frame data were run.",
 "targets": [],
 "internal_checks": internal,
 "robustness": robust,
 "bugs": bugs,
 "env_fixes": ["diffs/xvg2csv.py.diff: Python 2 print statements converted to print() calls so the script runs under Python 3.12 (no python2 interpreter available); no logic change."],
 "proposed_class": "C",
 "class_reason": "The deposit cannot reproduce any number reported in the paper: the paper reports no computed value for 2XWT, and the inputs needed to regenerate the 2XWT analyses (production .xtc trajectories) are not deposited. What can be run (the gmx_MMPBSA summary from its own per-frame data, " + ("and a sander GB rerun from the deposited intermediates" if gb else "") + ") is internally consistent, but that is not a reproduction of the paper.",
 "confidence": "medium",
 "confidence_reason": "Facts are checked by script, but C versus E (or 'not applicable') is a judgement because there is no paper target at all.",
 "time_minutes": int((t1 - t0).total_seconds() // 60),
 "uncertainties": [
  "Class choice: PROTOCOL classes assume a paper number exists; C is chosen because the materials do not support any reported number. E would also be defensible only if one treats the missing trajectory as 'could not run'; we did run what exists.",
  "PREREG asked for sample SD (ddof=1); the author SDs in FINAL_RESULTS_MMPBSA.dat match population SD (ddof=0): GB dTOTAL SD ddof0 %.4f vs ddof1 %.4f vs author %.2f. Means are unaffected." % (T["GB_dTOTAL"]["sd_ddof0"], T["GB_dTOTAL"]["sd_ddof1"], T["GB_dTOTAL"]["author_dat_sd"]),
  "Images embedded in Supporting file 1 (12 images) and the main figures were not OCR'd; their text and captions do not mention 2XWT, and the main-text figures concern other PDB entries.",
  "Table 1 lists 2XWT with 200 ns while the dataset title says 400 ns; 400 ns files are dated 2024-06-11 (after acceptance). The 400 ns RMSD series starts at about 4.48 nm at t=0 and contains a duplicated time point at 200 ns (40,002 rows), while the 200 ns series starts at 0.0005 nm; cause cannot be determined without the trajectories. Descriptive only, not a paper number.",
  gb_note,
  "Environment differs from the authors' (AmberTools 26 on aarch64 vs Amber 21 / gmx_MMPBSA 1.5.2 on x86_64)."]
}
json.dump(res, open(os.path.join(B, "results.json"), "w"), indent=1)
print(json.dumps({k: res[k] for k in ("proposed_class", "time_minutes")}), len(internal))
