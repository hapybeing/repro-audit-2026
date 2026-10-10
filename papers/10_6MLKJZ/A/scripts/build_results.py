# Builds results.json from files in outputs/ and the frozen targets.json. Run from anywhere.
import json, csv, re, os
A = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
O = os.path.join(A, "outputs")
targets = json.load(open(os.path.join(A, "..", "targets.json")))
ss = {r["id"]: r for r in csv.DictReader(open(os.path.join(O, "sample_sizes.csv")))}
fc = json.load(open(os.path.join(O, "figure_claims.json")))
ra = json.load(open(os.path.join(O, "robustness_R_a.json")))
rb = json.load(open(os.path.join(O, "robustness_R_b.json")))
rc = json.load(open(os.path.join(O, "robustness_R_c.json")))
dg = json.load(open(os.path.join(O, "diag_T3_and_join.json")))
fcs = (f"FC1 count {fc['FC1']['count_CI_excludes_0']} of {fc['FC1']['n_levels']} levels (paper 0, same={fc['FC1']['same_conclusion']}); "
       f"Since levels excluding 0: {fc['FC1']['Since_levels']}; FC2 largest range: "
       f"{ {k: v['largest'] for k, v in fc['FC2']['by_sector'].items()} } (same={fc['FC2']['same_conclusion']}); "
       f"FC3 strict={fc['FC3']['same_conclusion_strict']}, lenient={fc['FC3']['same_conclusion_lenient']} (outputs/figure_claims.json)")
tctx = dg["T3_context"]
alt_total = int(ss["T1"]["value"]) + int(ss["T2"]["value"]) + int(tctx["civic_sectorNA_in_survey_v184_ger"].get("1", 0))
notes = {
 "T1": "Also equals distinct respondents in match_data with D=0; table(match_data$D) prints 2570 = rows at task 1 (2 profiles per respondent), not respondents.",
 "T2": "table(match_data$D) prints 666 rows = 2 x 333 respondents.",
 "T3": (f"Distinct civic respondents in pooled_df2 = {ss['T3']['value']} (also the N in the Sample label). Of these, {tctx['civic_sectorNA']} have sector NA: "
        f"{tctx['civic_sectorNA_not_in_survey_data']} are not in survey_data.csv at all, and of the {tctx['civic_sectorNA_in_survey_data']} that are, "
        f"v184_ger is '1' for {tctx['civic_sectorNA_in_survey_v184_ger'].get('1')} and '.b' for {tctx['civic_sectorNA_in_survey_v184_ger'].get('.b')}. "
        f"T1 + T2 + the '1' group = {alt_total}. The deposited R code has no step that reduces the civic sample to Table 2's total; "
        "the figures group only by sector, so Figures 1-2 use exactly the T1/T2 respondents (outputs/diag_T3_and_join.json)."),
 "T4": "Sample label hsvn shows N = 528 (510 Public Administration + 18 with student NA).",
 "T5": "Sample label uhh shows N = 744 (636 + 108 with student NA).",
 "T6": "Sample label rh shows N = 128 (123 + 5 with student NA). Paper text says 127; Table 2 says 123.",
}
T = []
for t in targets:
    rv = int(ss[t["id"]]["value"]); pv = t["paper_value"]
    ad = rv - pv; rd = ad / pv
    T.append({"id": t["id"], "description": t["description"], "paper_value": pv, "paper_rounding_decimals": t["paper_rounding_decimals"],
              "reproduced_value": rv, "source_file": "outputs/sample_sizes.csv", "abs_diff": ad, "rel_diff": round(rd, 6),
              "match_to_rounding": round(rv, t["paper_rounding_decimals"]) == pv, "within_5pct": abs(rd) <= 0.05,
              "same_conclusion": abs(rd) <= 0.05, "note": notes[t["id"]] + (" Figure-claim checks: " + fcs if t["id"] == "T1" else "")})
R = [
 {"id": "R_a", "description": "Respondent-level cluster bootstrap (B=1000, seed 20261009) of E1 = Figure 1 MM of Composition '2 Adults, 3 Childr.', Private Sector",
  "ran": True, "estimate": ra["E1_cregg"], "se_or_ci": f"bootstrap SE {ra['boot_se']:.6f}; percentile 95% CI [{ra['boot_ci_lower']:.6f}, {ra['boot_ci_upper']:.6f}]",
  "p_value": ra["p_value"], "same_direction_and_significance_as_paper": ra["same_dir_sig"], "source_file": "outputs/robustness_R_a.json",
  "note": f"p = 0 means no bootstrap draw <= 0.5 (resolution 1/1000). Secondary FC1 count (bootstrap percentile CIs) = {ra['FC1_count']} (paper 0). Since levels excluding 0: {ra['Since_Education_levels_excl0']}. Rows as in pooled_df2 (including the duplicated rows, see bugs); unweighted check equals cregg: {ra['E1_unweighted_check']:.9f}."},
 {"id": "R_b", "description": "Drop respondents below 1st / above 99th percentile of Qualtrics 'Duration (in seconds)' within each of the 4 samples, rerun Figure 1 and 2 cj() calls",
  "ran": True, "estimate": rb["E1"], "se_or_ci": f"SE {rb['se']:.6f}; 95% CI [{rb['lower']:.6f}, {rb['upper']:.6f}]", "p_value": rb["p_value"],
  "same_direction_and_significance_as_paper": rb["same_dir_sig"], "source_file": "outputs/robustness_R_b.json",
  "note": f"Dropped {rb['total_dropped']} respondents ({ {k: v['dropped'] for k, v in rb['per_sample'].items()} }); sector groups now {rb['n_resp_private']} private / {rb['n_resp_public']} public. FC1 count = {rb['FC1_count']} (paper 0). z vs 0.5 = {rb['z_vs_0.5']:.3f}."},
 {"id": "R_c", "description": "AMCE instead of MM: Composition '2 Adults, 3 Childr.' vs '1 Adult', Private Sector; secondary cj_anova omnibus test of sector differences",
  "ran": True, "estimate": rc["AMCE"], "se_or_ci": f"clustered SE {rc['se']:.6f}; 95% CI [{rc['lower']:.6f}, {rc['upper']:.6f}]", "p_value": rc["p_value"],
  "same_direction_and_significance_as_paper": rc["same_dir_sig"], "source_file": "outputs/robustness_R_c.json",
  "note": (f"Secondary (pre-registered as written): cj_anova F = {rc['anova_F']:.4f}, df = {rc['anova_df']}, p = {rc['anova_p']:.6f}; same conclusion as paper (p >= .05): {rc['anova_same_conclusion']}. "
           f"This test is unclustered and runs on pooled_df2 rows including the duplicated rows from the many-to-many join (resid. df 51662, outputs/robustness_R_c_anova.txt). "
           f"Supplementary, not pre-registered: on de-duplicated rows F = {dg['supp_R_c_anova_dedup']['dedup_unclustered_F']:.4f}, p = {dg['supp_R_c_anova_dedup']['dedup_unclustered_p']:.4f} "
           "(outputs/supp_R_c_anova_dedup.txt; passing id= to cj_anova gave the same F, so cregg 0.4.0 cj_anova does not cluster).")},
]
jd = dg["join_duplication"]
bugs = [{"file": "Prioritzing_Social_Needs/analysis/03_data_prep_and_merge.R", "line": 133,
  "description": "left_join(pooled_df2, ebalw) is many-to-many: ebalw comes from match_data filtered to task == 1, which has two rows (two profiles) per respondent, so every pooled_df2 row of a respondent in X is matched twice and duplicated. pooled_df2 is then used for Figures 1-4 and A3-A4.",
  "evidence": (f"dplyr warning 'Detected an unexpected many-to-many relationship' (outputs/run_authors_log.txt); table(match_data$D) = 2570/666 rows for 1285/333 respondents; pooled_df2 has {jd['rows_pooled_df2']} rows for {jd['respondents']} respondents "
               f"({jd['rows_per_resp']}), {jd['rows_after_dedup']} after removing exact duplicates. {jd['sector_resp_with_16_rows']} sector respondents (NA on a balance variable) keep 16 rows, the other {jd['sector_resp_with_32_rows']} get 32, so they are weighted half as much. "
               f"Effect on the figures is small: max |change| of a Figure 1 MM {jd['fig1_max_abs_diff_estimate']:.5f}, of a Figure 2 difference {jd['fig2_max_abs_diff_estimate']:.5f}; same Figure 2 levels exclude 0 after de-duplication ({jd['fig2_dedup_levels_CI_excl0']}) (outputs/diag_T3_and_join.json, outputs/code_check_join_dedup_fig1.csv). Statement `pooled_df2 <- left_join(pooled_df2, ebalw)` starts at line 133; ebalw is built at line 131 from X (lines 103-112).")}]
# time from LOG timestamps
ts = re.findall(r"^- (\d\d):(\d\d) ", open(os.path.join(A, "LOG.md")).read(), re.M)
mins = [int(h) * 60 + int(m) for h, m in ts]
res = {"paper_id": "10_6MLKJZ", "agent": "A", "run_date_ist": "2026-10-10", "ran": True, "could_not_run_reason": "",
 "targets": T, "robustness": R, "bugs": bugs,
 "env_fixes": ["diffs/00_raw_data_lowercase_symlinks.diff: code reads data_uhh.csv / data_hsvn.csv, deposit has data_UHH.csv / data_HSVN.csv (case-sensitive Linux); symlinks in the run copy, no code change",
   "diffs/README.md item 2: cjoint 2.1.0 (CRAN archive, current when scripts were last revised in July 2023) instead of 2.1.3; 2.1.3 fails in read.qualtrics ('replacement has 0 rows')",
   "diffs/README.md item 3: cregg 0.4.0 from CRAN archive tarball (archived 2024-09-05)",
   "diffs/README.md item 4: 04_analysis.R run after sourcing 01-03 by a wrapper, since its source() lines are commented out (no code change)"],
 "proposed_class": None, "class_reason": "", "confidence": "medium", "confidence_reason": "", "time_minutes": max(mins) - min(mins) if mins else None,
 "uncertainties": []}
allexact = all(t["match_to_rounding"] for t in T); all5 = all(t["within_5pct"] for t in T)
fcok = fc["FC1"]["same_conclusion"] and fc["FC2"]["same_conclusion"] and fc["FC3"]["same_conclusion_strict"]
if allexact and fcok: cls = "A"
elif all5 and fcok: cls = "B"
else: cls = "C"
res["proposed_class"] = cls
failed = [t["id"] for t in T if not t["within_5pct"]]
res["class_reason"] = (f"T1, T2, T4, T5, T6 reproduce exactly and FC1-FC3 hold, but T3 (Table 2 general-population total) does not: {failed} gives "
  f"{ss['T3']['value']} vs 1849. The step that reduces the 2482 civic respondents the code keeps to 1849 is not in the deposited code (undocumented step), "
  "so the reported total cannot be produced from it; under PROTOCOL 7 / batch 2 decision 3 that is C, not D, since the figures' sector groups (1285 / 333) and all figure claims reproduce.") if cls == "C" else "All targets and figure claims as pre-registered."
res["confidence_reason"] = "Single agent run (B not compared); class hinges on how T3's undocumented sample step is read; package versions differ from the authors' unrecorded ones."
res["uncertainties"] = [
 "Figure-claim checks (pre-registered, not in targets.json): " + fcs,
 f"Alternative reading (judgment, not pre-registered): if T3 is read as the respondents survey_data.csv codes (sector Private/Public plus v184_ger == '1'), the count is {alt_total}, equal to 1849, and every target would be exact (class A). I did not adopt it because targets.json defines T3 on pooled_df2 and it rests on my reading of a Stata-coded variable without a codebook.",
 f"The {tctx['civic_sectorNA_not_in_survey_data']} civic respondents absent from survey_data.csv equal the 88 non-German respondents footnote 5 excludes; and 1849 + 88 = 1937, the appendix total. This is a numeric coincidence check, not verified with a nationality variable.",
 "Unverified observation: in 03_data_prep_and_merge.R line 98 (`match_data$nongerman <- as.numeric(match_data$v184_ger == \"Ja\")`), v184_ger is used as a nationality flag, but among civic respondents with a sector it is 'Ja' for exactly the 333 public and 'Nein' for exactly the 1285 private respondents (outputs/diag_T3_and_join.json), so it may be a sector variable. nongerman is not used in any estimate, so this has no effect on outputs.",
 "R_c secondary omnibus test fails the paper's conclusion as pre-registered (p = %.4f), but that test is unclustered and inflated by the duplicated rows; on de-duplicated rows p = %.4f (supplementary, not pre-registered)." % (rc["anova_p"], dg["supp_R_c_anova_dedup"]["dedup_unclustered_p"]),
 "Figure 2 levels of Duration '1 Year' and '3 Years' have 95% CIs excluding 0 (also in R_a and R_b). The paper makes no claim about Duration, so FC1 is unaffected; noted as in PREREG.",
 "No CI end fell outside the Figure 2 / 4 axis limits (no ggplot 'Removed rows' warnings in outputs/run_authors_log.txt). Regenerated Figures 1 and 2 look the same as the deposited PNGs by eye (outputs/figures_regenerated/); no pixel comparison.",
 "Authors' package versions are not recorded. cjoint 2.1.0 was chosen by release date; cregg 0.4.0, ggplot2 4.0.3, rvest 1.0.4 used (environment.txt).",
 "The data cleaning the paper describes (speeders, inconsistent patterns, German nationality only) is not in the deposited R code; the raw files are not pre-restricted (2482 civic respondents survive the R filters).",
 "Agent B has not been compared; per PROTOCOL 8 confidence cannot be high before that."]
json.dump(res, open(os.path.join(A, "results.json"), "w"), indent=1, ensure_ascii=False)
print(json.dumps({k: res[k] for k in ["proposed_class", "time_minutes"]}), [(t["id"], t["paper_value"], t["reproduced_value"], t["match_to_rounding"]) for t in T])
