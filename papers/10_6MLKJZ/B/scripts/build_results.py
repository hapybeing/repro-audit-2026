"""Agent B: build results.json for 10_6MLKJZ from files in outputs/ (no hand-typed reproduced numbers)."""
import csv, json, os
B = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(B)))
O = lambda f: os.path.join(B, "outputs", f)
targets_pre = json.load(open(os.path.join(REPO, "papers/10_6MLKJZ/targets.json")))
ss = {r["id"]: r for r in csv.DictReader(open(O("sample_sizes.csv")))}
fc = json.load(open(O("figure_claims.json")))
rb = json.load(open(O("robustness.json")))
cc = json.load(open(O("code_checks.json")))
t3alt = dict(l.strip().split(",") for l in open(O("t3_alt_count.csv")))
notes = {
 "T1": "Same count over all of pooled_df2 (what the by = ~ sector calls group): %s. table(match_data$D) at 03 line 94 gives %s, i.e. profile rows (2 per respondent at task 1), not respondents; halved this equals 1285 / 333." % (ss["sec_all_private"]["n"], open(O("table_match_data_D.txt")).read().split()[-2:]),
 "T2": "Same count over all of pooled_df2: %s." % ss["sec_all_public"]["n"],
 "T3": "pooled_df2 holds %s civic respondents (Sample label '%s'). Decomposition by survey_data.csv sector (outputs/t3_civic_decomposition.csv): Private + Public + empty-string sector = %s, which equals the paper's 1849 (1285 + 333 + 231 'no sector'); the other civic respondents have sector '.b' or are absent from survey_data.csv. The deposited R code contains no step that removes them; they carry no sector, so they do not enter the sector-grouped Figures 1, 2, A2, A3." % (t3alt["civic_respondents_in_pooled_df2"], ss["sample_label_civic"]["definition"], t3alt["civic_private_public_or_empty_sector"]),
 "T4": "Sample label: %s." % ss["sample_label_hsvn"]["definition"],
 "T5": "Sample label: %s." % ss["sample_label_uhh"]["definition"],
 "T6": "Sample label: %s. Table 2 value 123 matched (the paper text says 127)." % ss["sample_label_rh"]["definition"],
}
targets = []
for t in targets_pre:
    rv = float(ss[t["id"]]["n"]); pv = t["paper_value"]
    ad = rv - pv; rd = ad / pv
    w5 = abs(rd) <= 0.05
    targets.append({"id": t["id"], "description": t["description"], "paper_value": pv, "paper_rounding_decimals": t["paper_rounding_decimals"],
        "reproduced_value": rv, "source_file": "outputs/sample_sizes.csv", "abs_diff": ad, "rel_diff": round(rd, 6),
        "match_to_rounding": round(rv, t["paper_rounding_decimals"]) == pv, "within_5pct": w5, "same_conclusion": w5,
        "note": notes[t["id"]] + " Figure-claim checks: FC1 count=%s (claim 0, holds=%s); FC2 holds=%s; FC3 strict=%s, lenient=%s (outputs/figure_claims.json)." % (
            fc["FC1"]["count_excluding_0"], fc["FC1"]["same_conclusion"], fc["FC2"]["same_conclusion"], fc["FC3"]["strict_same_conclusion"], fc["FC3"]["lenient_same_conclusion"])})
ra, rbb, rc = rb["R_a"], rb["R_b"], rb["R_c"]
robust = [
 {"id": "R_a", "description": "Respondent-level cluster bootstrap within sector, seed 20261009, B=1000; E1 = Figure 1 MM of Composition '2 Adults, 3 Childr.', Private Sector; percentile 95% CI", "ran": True,
  "estimate": ra["estimate"], "se_or_ci": "boot SE %.6f; 95%% percentile CI [%.6f, %.6f]" % (ra["boot_se"], ra["ci_lower"], ra["ci_upper"]), "p_value": ra["p_value"],
  "same_direction_and_significance_as_paper": ra["same"], "source_file": "outputs/robustness.json",
  "note": "p = 0 means no bootstrap draw was at or below 0.5 (p < 1/1000). Secondary FC1 count with percentile CIs: %s (paper 0). Levels outside FC1 whose CI excludes 0: %s. Respondents resampled: %s." % (ra["fc1_count"], ra["other_levels_excl0"], ra["n_resp"])},
 {"id": "R_b", "description": "Drop respondents below the 1st or above the 99th percentile of Qualtrics 'Duration (in seconds)' within each of the four samples; rerun Figure 1 and 2 cj() calls", "ran": True,
  "estimate": rbb["estimate"], "se_or_ci": "SE %.6f; 95%% CI [%.6f, %.6f]" % (rbb["se"], rbb["ci_lower"], rbb["ci_upper"]), "p_value": rbb["p_value"],
  "same_direction_and_significance_as_paper": rbb["same"], "source_file": "outputs/robustness.json",
  "note": "Respondents dropped: %s (total %s). FC1 count on reduced data: %s (paper 0)." % ({k: v["dropped"] for k, v in rbb["dropped_per_sample"].items()}, rbb["total_dropped"], rbb["fc1_count"])},
 {"id": "R_c", "description": "AMCE instead of MM (cregg amce, by sector, baseline '1 Adult'); primary AMCE of '2 Adults, 3 Childr.' for Private Sector; secondary cj_anova omnibus test of sector differences", "ran": True,
  "estimate": rc["estimate"], "se_or_ci": "SE %.6f; 95%% CI [%.6f, %.6f]" % (rc["se"], rc["ci_lower"], rc["ci_upper"]), "p_value": rc["p_value"],
  "same_direction_and_significance_as_paper": rc["same"], "source_file": "outputs/robustness.json",
  "note": "Secondary omnibus cj_anova by sector: F = %.6f, p = %.6f; pre-registered rule (p >= .05 = no difference, as the paper) gives same_as_paper = %s. cregg's cj_anova is an unclustered nested-model F test, and pooled_df2 carries the duplicated rows described under bugs, so this p-value treats rows as independent." % (rc["anova_F"], rc["anova_p"], rc["anova_same_as_paper"])},
]
bugs = [{"file": "Prioritzing_Social_Needs/analysis/03_data_prep_and_merge.R", "line": 133,
  "description": "left_join(pooled_df2, ebalw) duplicates rows: ebalw comes from match_data filtered to task == 1 (line 92), which has 2 rows (profiles) per respondent, so every matched civic respondent's 16 rows become 32. pooled_df2 is overwritten by this join and is the input of every cj() call in 04_analysis.R (Figures 1-4, A3, A4), and match_cj (Figure A2) inherits the duplication.",
  "evidence": "dplyr warns 'Detected an unexpected many-to-many relationship' (outputs/run_authors_warnings.txt). outputs/code_checks.json: %s rows vs %s distinct (respondent, task, profile); %s respondents have 32 rows. Rerunning Figure 1/2 cj() on de-duplicated rows changes MMs by at most %s and SEs by at most %.2f%% relative; FC1 count stays %s (outputs/code_check_dedup_fig1_mm.csv, code_check_dedup_fig2_mmdiff.csv). Respondents with an NA balance covariate (na.omit, line 122) keep 16 rows, so they get half the weight of others." % (
    cc["rows_total"], cc["distinct_resp_task_profile"], cc["respondents_with_32_rows"], cc["fig1_max_abs_estimate_change_dedup"], 100 * cc["fig1_max_rel_se_change_dedup"], cc["fc1_count_dedup"])}]
res = {"paper_id": "10_6MLKJZ", "agent": "B", "run_date_ist": "2026-10-10", "ran": True, "could_not_run_reason": "",
 "targets": targets, "robustness": robust, "bugs": bugs,
 "env_fixes": ["diffs/00_raw_data_lowercase_symlinks.diff: code reads data_uhh.csv / data_hsvn.csv, deposit has data_UHH.csv / data_HSVN.csv (case-sensitive Linux); lower-case symlinks added in the run copy",
               "diffs/01_package_cjoint_2.1.0.diff: cjoint 2.1.3 (current CRAN) fails in read.qualtrics and uses different ID column names; cjoint 2.1.0 (CRAN version at the authors' last revision, July 2023) installed from the CRAN archive with shinyBS 0.61.1",
               "cregg 0.4.0 from the CRAN archive (archived 2024-09-05), as PREREG section 2"],
 "uncertainties": []}
fails = [t["id"] for t in targets if not t["within_5pct"]]
fcs_hold = fc["FC1"]["same_conclusion"] and fc["FC2"]["same_conclusion"] and fc["FC3"]["strict_same_conclusion"]
exact = [t["id"] for t in targets if t["match_to_rounding"]]
res["proposed_class"] = "C"
res["class_reason"] = ("T3 (general population total) is reproduced as %d against the paper's 1849 (rel diff %.3f): the extra civic respondents have no sector or no survey_data record and the deposited code has no step that removes them, so the code does not produce Table 2's total (undocumented step). %s are exact and FC1-FC3 hold (%s), so the headline figures' samples and conclusions reproduce; alternative class on T1, T2, T4-T6 and FC1-FC3 alone: A." % (
    targets[2]["reproduced_value"], targets[2]["rel_diff"], ", ".join(exact), "all strict" if fcs_hold else "not all"))
res["confidence"] = "medium"
res["confidence_reason"] = "Numbers matched by script with byte-identical deposit files, but the class depends on a judgment call (whether a T3 miss that does not enter the figures is C), a package pin was needed (cjoint 2.1.0), and A vs B comparison is not yet done."
res["time_minutes"] = 26
res["uncertainties"] = [
 "Class: T3 fails the pre-registered 5%% rule, but the extra %s respondents have no usable sector and cannot enter Figures 1, 2, A2, A3; whether this is C (undocumented sample step) or a non-headline miss is a judgment call for the comparison. %s" % (int(targets[2]["reproduced_value"] - targets[2]["paper_value"]), notes["T3"]),
 "PREREG risk section expected the general-population counts might match the appendix (1336 / 352 / 1937); they match Table 2 instead (1285 / 333). The 88 civic respondents absent from survey_data.csv equal footnote 5's 88 non-German respondents in number; that they are the same people is not verifiable from the deposit.",
 "In survey_data.csv, for civic respondents v184_ger is 'Ja' for exactly the 333 Public Sector respondents and 'Nein' for exactly the 1285 Private Sector ones (outputs/t3_sector_by_v184_ger.csv). 03 line 98 names v184_ger == 'Ja' 'nongerman'. If v184_ger were nationality this cross-tab would be unexpected; the variable is not documented in the deposit and nongerman is not used in any balance or estimate, so this is an unverified observation with no effect on results.",
 "FC1 holds (0 of the FC1 levels), but 2 Duration-of-unemployment levels ('1 Year', '3 Years') have mm_diff CIs excluding 0 (outputs/figure_claims.json), as visible in the published Figure 2; the text makes no claim about duration.",
 "R_c secondary: cj_anova by sector gives p < .05 (see robustness note); that test ignores respondent clustering and runs on the duplicated rows, so it is likely anti-conservative. Robustness does not change the class.",
 "Package drift: cobalt 5.0.0 pulled ggplot2 4.0.3 into the run library; regenerated PNGs (outputs/figures_regenerated/) match the deposited figure_02.png by eye apart from font rendering; no pixel comparison was pre-registered. No ggplot 'Removed rows' warnings were raised (the Figure 2/4 axis limits did not clip any CI).",
 "time_minutes is from LOG.md timestamps (12:47 to about 13:13 UTC)."]
json.dump(res, open(os.path.join(B, "results.json"), "w"), indent=1)
for t in targets: print(t["id"], t["paper_value"], t["reproduced_value"], t["match_to_rounding"], t["within_5pct"])
print(res["proposed_class"], res["class_reason"])
