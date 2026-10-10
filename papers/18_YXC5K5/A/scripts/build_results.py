# Builds results.json from files in outputs/ (no hand-typed estimates). Paper values are copied from ../targets.json (PREREG).
import csv, json, re, os
os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/..")
def load_ext(p):
    d = {}
    for r in csv.DictReader(open(p)): d[(r["object"], r["key"])] = r["value"]
    return d
X = load_ext("outputs/targets_extracted.csv")
f = lambda o, k: float(X[(o, k)])
mm = {k.split("|")[0]: None for (o, k) in X if o == "metrics_matrix"}
rows = sorted(mm)
HL = {r: f("metrics_matrix", r + "|HammingLoss") for r in rows}
F1 = {r: f("metrics_matrix", r + "|F1") for r in rows}
T1 = HL["GPT 4o 8 Few Shot"]; T2 = f("undergrads8", "Hamming Loss"); T3 = HL["GPT 4o 4 Few Shot"]
T4 = F1["GPT 4o 8 Few Shot"]; T5 = f("metrics_matrix", "GPT 4o 8 Few Shot|Mean"); T6 = int(X[("n", "nrow_pi10mat")])
author8 = 100 * f("author", "pct1s_8lab_share")
n_ok = T6 == int(X[("n", "nrow_gpt4o10mat_fewx")]) == int(X[("n", "nrow_hum10matx")])
concl = {
 "T1": (T1 <= min(HL.values()) and T1 > T2, f"lowest of {len(HL)} LLM rows: {T1 <= min(HL.values())}; above T2: {T1 > T2}"),
 "T2": (all(T2 < v for v in HL.values()), f"undergraduate HL below all {len(HL)} LLM rows"),
 "T3": (T3 > T1, "T3 > T1"),
 "T4": (T4 >= max(F1.values()), f"highest F1 of {len(F1)} LLM rows"),
 "T5": (T5 > author8, f"T5 above author 8-label % 1s ({author8:.4f})"),
 "T6": (abs(T6 - 589) <= 5 and n_ok, f"N within 5 of 589; model and undergraduate matrices also {T6} rows: {n_ok}"),
}
repro = {"T1": T1, "T2": T2, "T3": T3, "T4": T4, "T5": T5, "T6": T6}
src = "outputs/targets_extracted.csv"
targets = []
for t in json.load(open("../targets.json")):
    pv, dec, rv = t["paper_value"], t["paper_rounding_decimals"], repro[t["id"]]
    ad = rv - pv; rd = ad / pv
    m = round(rv, dec) == pv if dec > 0 else int(round(rv)) == pv
    note = concl[t["id"]][1]
    if t["id"] == "T4": note += f"; secondary only: F1 with positive class '1' = {float(X[('secondary','F1_positive1_gpt4o10_few_mean')]):.4f}"
    targets.append(dict(id=t["id"], description=t["description"], paper_value=pv, paper_rounding_decimals=dec,
        reproduced_value=rv, source_file=src, abs_diff=ad, rel_diff=rd, match_to_rounding=m, within_5pct=abs(rd) <= 0.05,
        same_conclusion=concl[t["id"]][0], note=note))
desc = {
 "R_a": "Bootstrap resample of articles: set.seed(20261010), 1000 resamples of row indices applied to all matrices with the authors' row pairing; estimate = T1; CI = 95% percentile of D = T1 - undergraduate 8-label HL; p = min(1, 2*share D<=0).",
 "R_b": "Outlier exclusion: drop rows with |z| > 3 of k = rowSums(pi10mat) (author labels per article), same row positions dropped from all matrices; recompute; bootstrap as R_a for criterion (iii).",
 "R_c": "Alternative analysis choice: copy of the Rmd with one line `pi = pi %>% arrange(docid)` after line 108 (benchmark paired with model rows by docid); rerun whole copy; bootstrap as R_a on realigned matrices.",
}
rob = []
for c in ["R_a", "R_b", "R_c"]:
    s = next(csv.DictReader(open(f"outputs/{c}_summary.csv")))
    g = lambda k: float(s[k])
    note = (f"n_rows_used {int(g('n_rows_used'))}, dropped {int(g('n_dropped'))}; D = {g('D'):.4f}; bootstrap SE(D) = {g('D_boot_se'):.4f}; "
            f"T1 95% CI [{g('T1_ci_lo'):.4f}, {g('T1_ci_hi'):.4f}]; T3 - T1 = {g('T3minusT1'):.4f}; rank of GPT 4o Few Shot 8 among 18 LLM specs = {int(g('rank_T1_of_18'))}; "
            f"share of resamples where it is lowest = {g('share_resamples_T1_lowest'):.3f}; U8 = {g('U8'):.4f}. "
            f"p = 0 means no resample had D <= 0 (resolution 1/1000). Significance criterion (iii) is the audit's own reading; the paper reports no test.")
    if c == "R_c":
        Y = load_ext("outputs/R_c_targets_extracted.csv")
        note += (f" Diagnostics: identical(pi$docid, gpt4o 8 few docid) original {X[('diag','identical_pi_gpt4o10few_docid')]}, copy {Y[('diag','identical_pi_gpt4o10few_docid')]}; "
                 f"identical(pi$docid, human 10 docid) original {X[('diag','identical_pi_human10_docid')]}, copy {Y[('diag','identical_pi_human10_docid')]}. "
                 f"Copy values: T1 {float(Y[('metrics_matrix','GPT 4o 8 Few Shot|HammingLoss')]):.4f}, T2 {float(Y[('undergrads8','Hamming Loss')]):.4f}, "
                 f"T3 {float(Y[('metrics_matrix','GPT 4o 4 Few Shot|HammingLoss')]):.4f}, T4 {float(Y[('metrics_matrix','GPT 4o 8 Few Shot|F1')]):.4f}, "
                 f"T5 {float(Y[('metrics_matrix','GPT 4o 8 Few Shot|Mean')]):.2f}, T6 {Y[('n','nrow_pi10mat')]}, "
                 f"AUC GPT 4o 8 Few Shot {float(Y[('metrics_matrix','GPT 4o 8 Few Shot|AUC')]):.4f} (original {f('metrics_matrix','GPT 4o 8 Few Shot|AUC'):.4f}). Full table: outputs/R_c_targets_extracted.csv.")
    rob.append(dict(id=c, description=desc[c], ran=True, estimate=g("T1"),
        se_or_ci=f"95% percentile CI of D [{g('D_ci_lo'):.4f}, {g('D_ci_hi'):.4f}]", p_value=g("p_value"),
        same_direction_and_significance_as_paper=s["same_direction_and_significance"] == "TRUE",
        source_file=f"outputs/{c}_summary.csv", note=note))
# code-review evidence read from outputs
cc = {r["session"] + "|" + r["model"]: r for r in csv.DictReader(open("outputs/row_pairing_confusion_counts.csv"))}
gm, gr = cc["main|GPT 4o Few Shot 8"], cc["Rc|GPT 4o Few Shot 8"]; um, ur = cc["main|Undergraduate Coders 8"], cc["Rc|Undergraduate Coders 8"]
ug = list(csv.DictReader(open("outputs/undergrad_row_check.csv")))
bugs = [
 dict(file="Benchmarking_DataAnalysis.Rmd", line=108,
  description="Author benchmark `pi` (read at line 102 from pi_codings_2ndhalf.csv, de-duplicated at line 108) is never sorted or joined by docid, but every metric (calculate_hamming_loss line 1552, F1/recall/precision via actual_list_10/actual_list_4 lines 124-128, calculate_auc line 1358, calculate_icc_scores line 1168, undergrads8/4 lines 2050-2064) compares it with the model and undergraduate matrices by row position. The model and human files are in ascending docid order; pi is not. So each article's model codes are compared with a different article's author codes.",
  evidence=(f"Run outputs: identical(pi$docid, gpt4o 8 few docid) = {X[('diag','identical_pi_gpt4o10few_docid')]}, docid sets equal = {X[('diag','setequal_pi_gpt4o10few_docid')]}, share of rows with the same docid at the same position = {float(X[('diag','share_rows_same_docid_pi_vs_gpt4o10few')]):.4f} (outputs/targets_extracted.csv); all 18 model and 2 human data frames share one docid order (outputs/model_files_docid_order.csv). "
   f"Pooled counts for GPT 4o Few Shot 8 labels, position pairing: FP {gm['FP']}, FN {gm['FN']}; docid pairing: FP {gr['FP']}, FN {gr['FN']} (outputs/row_pairing_confusion_counts.csv). The supplement's Table A5, built in Benchmarking_Supplementary.Rmd with left_join(pi10, by = 'docid'), prints FP 369 and FN 150 (as quoted in PREREG.md). Undergraduates: position FP {um['FP']}, FN {um['FN']}; docid FP {ur['FP']}, FN {ur['FN']} vs printed Table A6 FP 254, FN 180. "
   f"Author-benchmark AUC is about 0.50 for every model under position pairing and about 0.75 to 0.82 under docid pairing (outputs/analysis_log_main.txt vs outputs/analysis_log_Rc.txt stargazer tables). Table A1 values match the position-paired run."))
 ,dict(file="Benchmarking_DataAnalysis.Rmd", line=2051,
  description="undergrads8 (lines 2050-2056) and undergrads4 (lines 2058-2064), labelled 'undergraduate metrics for manual addition to table', compute AUC, Recall and F1 from gpt10mat / gpt4mat (GPT 4 Turbo Zero Shot output) instead of hum10mat / hum4mat; only Hamming Loss and % 1s use the undergraduate matrices. Affects the Table A1 undergraduate AUC/Recall/F1 cells, not T2.",
  evidence="outputs/undergrad_row_check.csv: undergrads AUC/Recall/F1 identical to metrics_matrix GPT 4 Turbo Zero Shot rows: " + "; ".join(f"{r['labels']}-label {r['stat']} identical={r['identical']}" for r in ug) + ". PREREG.md notes Table A1 prints the same values (0.48, 0.78, 0.84; 0.50, 0.71, 0.77) for both rows.")
]
log = open("LOG.md").read()
times = re.findall(r"^## (?:2026-10-11 )?(\d\d):(\d\d)", log, re.M)
t0 = int(times[0][0]) * 60 + int(times[0][1]); t1 = int(times[-1][0]) * 60 + int(times[-1][1])
all_match = all(t["match_to_rounding"] for t in targets)
res = dict(paper_id="18_YXC5K5", agent="A", run_date_ist="2026-10-11", ran=True, could_not_run_reason="",
  targets=targets, robustness=rob, bugs=bugs,
  env_fixes=["none: Benchmarking_DataAnalysis.Rmd ran unmodified (working directory set by cd in scripts/run_rmd.sh; packages installed: Debian r-cran-* binaries plus irr and stargazer from CRAN into the per-run library). diffs/R_c_Benchmarking_DataAnalysis_docid_sort.diff is the pre-registered R_c analysis copy, not an environment fix."],
  proposed_class="A" if all_match else "B",
  class_reason=("All six targets reproduced to the paper's rounding by running Benchmarking_DataAnalysis.Rmd exactly as deposited (batch4 class decision 4); all six conclusion criteria hold. "
     "The docid-paired rerun (R_c) changes the absolute values (T1 0.110, T2 0.093) but keeps the ranking, direction and bootstrap significance; per PROTOCOL section 7 it does not change the class."),
  confidence="high",
  confidence_reason="Deterministic script, unmodified, all targets matched by script with every input file checksum identical to the pre-registration download; agreement with agent B not yet known.",
  time_minutes=t1 - t0,
  uncertainties=[
   "Paper values come from a browser agent's reading of the supplement in the Google Docs viewer (PREREG section 4); I did not re-open the supplement. The exact match of all six cells supports that reading.",
   f"Not a target: Table A1 prints 9.68 for Undergraduate Coders 8 '% 1s'; the script's undergrads8 '% 1s' is {100*f('undergrads8','% 1s'):.2f} (outputs/targets_extracted.csv). I did not establish why.",
   "Row-pairing observation (bugs[0]) is confirmed by runs as a property of the deposited code and data; whether the printed Table A1 was meant to use docid pairing cannot be determined from the deposit. The paper's ranking and direction claims hold under both pairings (R_c), but the printed magnitudes (0.18, 0.15, 'by 0.03 points', AUC about 0.5) are those of the position pairing.",
   "Under docid pairing, undergraduate FP is 256 vs 254 printed in Table A6; Table A6 comes from Benchmarking_Supplementary.Rmd (not run), which may use a different undergraduate file (AI_goldstandard_ten_v2.csv). Unverified.",
   "Package versions differ from the author's (R 4.3.3, unpinned); here R 4.5.0 and Debian/CRAN current versions. Outputs are deterministic and matched, so drift did not matter for targets.",
   "R_a/R_b/R_c p-values are 0 at 1000-resample resolution and are the audit's own significance reading; the paper reports no tests."])
json.dump(res, open("results.json", "w"), indent=1)
print(json.dumps({t["id"]: (t["paper_value"], round(t["reproduced_value"], 6), t["match_to_rounding"], t["same_conclusion"]) for t in targets}))
print(res["proposed_class"], res["time_minutes"])
