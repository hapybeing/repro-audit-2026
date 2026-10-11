# Builds results.json from files in outputs/. No numbers typed except paper values read from targets.json.
import csv, json, re, os, datetime
A = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.dirname(A); OUT = os.path.join(A, "outputs")
tj = {t["id"]: t for t in json.load(open(os.path.join(P, "targets.json")))}
ex = {r["quantity"]: float(r["value"]) for r in csv.DictReader(open(os.path.join(OUT, "targets_extracted.csv")))}
fixv = next(csv.DictReader(open(os.path.join(OUT, "targets_extracted.csv"))))["fixest_version"]
src = "outputs/targets_extracted.csv"
qmap = {"T1": "T1_beta_model3", "T2": "T2_p_model3_grab_by_name", "T3": "T3_N_main", "T4": "T4_F_model3",
        "T5": "T5_fs_coef_model3", "T6": "T6_cand1_exp"}
b, p = ex["T1_beta_model3"], ex["T2_p_model3_grab_by_name"]
concl = {"T1": b > 0 and p < 0.05, "T2": p < 0.05, "T3": int(round(ex["T3_N_main"])) == 7163,
         "T4": ex["T4_F_model3"] > 10, "T5": ex["T5_fs_coef_model3"] > 0 and ex["T5_fs_p_clustered"] < 0.05,
         "T6": ex["T6_cand1_exp"] > 0 and (b > 0 and p < 0.05)}
notes = {
 "T1": f"SE {ex['T1_se_model3']:.6f}. Models 1, 2, 4 coefficients {ex['M1_beta']:.4f}, {ex['M2_beta']:.4f}, {ex['M4_beta']:.4f} (secondary, not targets).",
 "T2": f"Candidate 2 (summary(iv3) Pr(>|z|)) = {ex['T2_p_model3_summary_ivglm']:.6f}, identical to candidate 1.",
 "T3": f"Co-pollutant sample N (Model 4, secondary) = {int(ex['N_copoll'])}.",
 "T4": f"fixest {fixv}; fixest 0.13.2 fallback not needed. Partial R2 Model 3 = {ex['partialR2_model3']:.4f}; first-stage F Models 1, 2, 4 = {ex['M1_F']:.2f}, {ex['M2_F']:.2f}, {ex['M4_F']:.2f}.",
 "T5": f"Candidate 1 coef(d3$fs)['z_smoke']; date-clustered SE {ex['T5_fs_se_clustered']:.4f}, p {ex['T5_fs_p_clustered']:.3g}, nobs {int(ex['T5_fs_nobs'])}. Prose-only value (class decision 5).",
 "T6": f"First pre-registered formula 100*(exp(T1*T5)-1) with unrounded objects. Candidate 2 (100*T1*T5) = {ex['T6_cand2_linear']:.4f}; candidate 3 (100*(exp(T1*7.0)-1)) = {ex['T6_cand3_exp_rounded7']:.4f}. Not computed in any deposited script.",
}
targets = []
for tid in ["T1", "T2", "T3", "T4", "T5", "T6"]:
    t = tj[tid]; pv = t["paper_value"]; d = t["paper_rounding_decimals"]; rv = ex[qmap[tid]]
    ad = abs(rv - pv); rd = (rv - pv) / pv
    targets.append({"id": tid, "description": t["description"], "paper_value": pv, "paper_rounding_decimals": d,
                    "reproduced_value": rv, "source_file": src, "abs_diff": ad, "rel_diff": rd,
                    "match_to_rounding": round(rv, d) == round(pv, d), "within_5pct": abs(rd) <= 0.05,
                    "same_conclusion": concl[tid], "note": notes[tid]})
rbc = {r["check"]: r for r in csv.DictReader(open(os.path.join(OUT, "robustness_Rb_Rc.csv")))}
ra = json.load(open(os.path.join(OUT, "Ra_summary.json")))
f = lambda x: float(x)
rob = [
 {"id": "R_a", "description": "Date-cluster bootstrap (seed 20261011, B=999) of the Model 3 2SRI point estimate on seattle_main (N 7163); percentile 95% interval",
  "ran": True, "estimate": ra["estimate_T1"], "se_or_ci": f"bootstrap SD {ra['boot_sd']:.6f}; 95% percentile CI [{ra['pct_2.5']:.6f}, {ra['pct_97.5']:.6f}]",
  "p_value": ra["p_boot"], "same_direction_and_significance_as_paper": ra["estimate_T1"] > 0 and ra["pct_2.5"] > 0,
  "source_file": "outputs/Ra_summary.json (replicates outputs/Ra_boot.csv, indices outputs/Ra_boot_indices.rds)",
  "note": f"{ra['successful']} successful replicates of {ra['B_planned']}, {ra['failed']} failed, {ra['nonconverged_flagged']} flagged non-converged; bootstrap mean {ra['boot_mean']:.6f}. B=999 kept (20 replicates took 5.5 s)."},
 {"id": "R_b", "description": "Drop station-days with |z|>3 on assault (pooled z over 7163 rows), refit Model 3 with authors' run_ivglm/grab_by_name/fs_diag",
  "ran": True, "estimate": f(rbc["R_b"]["estimate"]), "se_or_ci": f"SE {f(rbc['R_b']['se']):.6f}; 95% CI [{f(rbc['R_b']['ci_low']):.6f}, {f(rbc['R_b']['ci_high']):.6f}]",
  "p_value": f(rbc["R_b"]["p"]), "same_direction_and_significance_as_paper": f(rbc["R_b"]["estimate"]) > 0 and f(rbc["R_b"]["p"]) < 0.05,
  "source_file": "outputs/robustness_Rb_Rc.csv",
  "note": f"N {int(f(rbc['R_b']['n']))}, dropped {int(f(rbc['R_b']['n_dropped']))} ({rbc['R_b']['dropped_by_station']}); all dropped rows have assault >= {int(f(rbc['R_b']['min_dropped_assault']))}; first-stage F {f(rbc['R_b']['first_stage_F']):.2f}."},
 {"id": "R_c", "description": "Linear 2SLS: feols(log(1+assault) ~ W | station+year+month+dow | pm25_mean ~ z_smoke, cluster=~date)",
  "ran": True, "estimate": f(rbc["R_c"]["estimate"]), "se_or_ci": f"SE {f(rbc['R_c']['se']):.6f}; 95% CI [{f(rbc['R_c']['ci_low']):.6f}, {f(rbc['R_c']['ci_high']):.6f}]",
  "p_value": f(rbc["R_c"]["p"]), "same_direction_and_significance_as_paper": f(rbc["R_c"]["estimate"]) > 0 and f(rbc["R_c"]["p"]) < 0.05,
  "source_file": "outputs/robustness_Rb_Rc.csv",
  "note": f"N {int(f(rbc['R_c']['n']))}; first-stage Wald F (ivwald, clustered) {f(rbc['R_c']['first_stage_F']):.2f}; fixest {fixv}."},
]
expl = json.load(open(os.path.join(OUT, "exploratory_na_rows.json")))
allA = all(t["match_to_rounding"] for t in targets)
allB = all(t["within_5pct"] and t["same_conclusion"] for t in targets)
cls = "A" if allA else ("B" if allB else "C")
log = open(os.path.join(A, "LOG.md")).read()
times = re.findall(r"^- (\d{2}):(\d{2}) ", log, re.M)
tm = [int(h) * 60 + int(m) for h, m in times]
res = {
 "paper_id": "23_FXRNBA", "agent": "A",
 "run_date_ist": datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=5, minutes=30))).strftime("%Y-%m-%d"),
 "ran": True, "could_not_run_reason": "",
 "targets": targets, "robustness": rob,
 "bugs": [],
 "code_review": "none found. Read wildfire_data_analysis.R lines 1-668 in full (preprocessing, sample construction, helpers, Table 1) and section 7 (lines 842-900); the rest of the script (sections 6B, 8-17) and wildfire_plots.R were not reviewed line by line. All 17 sections ran without error.",
 "env_fixes": [
   "none to code: no file was edited, so diffs/ holds only README.md. The deposit's Dataverse folder labels match the paths in the code, so files were placed in 'Data Analysis/', 'Beats/', 'Crime Data/' under the working directory.",
   "Dataverse ?format=original CSVs used (PREREG, class decision 3); sha256 of all 14 files match PREREG.md.",
   "LC_ALL=C.UTF-8 for the run (PREREG allowed locale fix).",
   f"fixest {fixv}, ivtools, weathermetrics, ahaz, dreamerr, stringmagic installed from CRAN source into a per-run library (no Debian r-cran binaries exist for them); everything else from Debian system R packages.",
 ],
 "proposed_class": cls,
 "class_reason": ("All six targets reproduced to the paper's rounding by the unchanged deposited script (T6 with the first pre-registered formula), with no code edits." if cls == "A" else "See targets."),
 "confidence": "high" if cls == "A" else "medium",
 "confidence_reason": "Unchanged code, checksummed deposit files, deterministic estimator; subset and full runs gave identical numbers (pending agreement with agent B per PROTOCOL section 8).",
 "time_minutes": (max(tm) - min(tm)) if tm else None,
 "uncertainties": [
   "T5 and T6 are prose values; T6 is not computed in any deposited script, so its formula is our first pre-registered candidate (candidate 2 rounds to 3.5 and candidate 3 to 3.6, see T6 note).",
   "Supplementary Information (tables B1 to B14) was not compared: it could not be opened during pre-registration (captcha); the script's SI tables are saved in outputs/author_tables/ unchecked.",
   "wildfire_plots.R was not run (not needed for any target, PREREG step 4 optional); figure-based numbers such as the 2.2% per IQR were not checked.",
   f"EXPLORATORY (not pre-registered): PREREG inconsistency 1 has no effect on this deposit: rows with complete Model 3 variables = {expl['rows_complete_model3_vars']}, of which {expl['rows_dropped_only_by_extra_columns']} are dropped only by the extra na.omit columns (outputs/exploratory_na_rows.json, plain CSV count).",
   "The sandbox restarted once mid-run (full run killed, then rerun from scratch); system R was reinstalled by setup_env.sh, so the system package set may differ slightly from the subset run. Both runs gave identical target numbers.",
   "The upstream build of the merged station-day CSVs from raw sources is not deposited (data-statement finding, class decision 7); the audit starts from the deposited merged CSVs.",
 ],
}
json.dump(res, open(os.path.join(A, "results.json"), "w"), indent=1)
print(json.dumps({k: res[k] for k in ["proposed_class", "time_minutes"]}), [(t["id"], t["paper_value"], round(t["reproduced_value"], 6), t["match_to_rounding"]) for t in targets])
