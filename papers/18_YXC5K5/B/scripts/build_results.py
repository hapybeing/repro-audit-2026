#!/usr/bin/env python3
"""Build results.json for 18_YXC5K5 agent B. Every reproduced number is read from files in outputs/; paper values from ../targets.json."""
import csv, json, os
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def kv(path):
    with open(os.path.join(HERE, path)) as f: return {r["name"]: r["value"] for r in csv.DictReader(f)}
def summ(path):
    with open(os.path.join(HERE, path)) as f: return next(csv.DictReader(f))
def pts(path):
    with open(os.path.join(HERE, path)) as f: return {r["spec"]: float(r["hamming_loss"]) for r in csv.DictReader(f)}
def checks():
    with open(os.path.join(HERE, "outputs/checks.csv")) as f: return {r["check"]: r["value"] for r in csv.DictReader(f)}
tg = json.load(open(os.path.join(HERE, "..", "targets.json")))
pv = {t["id"]: t for t in tg}
main = kv("outputs/targets_extracted.csv"); rc = kv("outputs/R_c_targets_extracted.csv"); ck = checks()
mm = lambda d, r, c: float(d[f"metrics_matrix|{r}|{c}"])
llm_rows = sorted({k.split("|")[1] for k in main if k.startswith("metrics_matrix|")})
assert len(llm_rows) == 18, llm_rows
hl = {r: mm(main, r, "HammingLoss") for r in llm_rows}; f1 = {r: mm(main, r, "F1") for r in llm_rows}
T = {"T1": mm(main, "GPT 4o 8 Few Shot", "HammingLoss"), "T2": float(main["undergrads8|Hamming Loss"]),
     "T3": mm(main, "GPT 4o 4 Few Shot", "HammingLoss"), "T4": mm(main, "GPT 4o 8 Few Shot", "F1"),
     "T5": mm(main, "GPT 4o 8 Few Shot", "Mean"), "T6": float(main["nrow_pi10mat"])}
nrows_equal = main["nrow_pi10mat"] == main["nrow_gpt4o10mat_fewx"] == main["nrow_hum10matx"]
concl = {"T1": hl["GPT 4o 8 Few Shot"] <= min(hl.values()) and T["T1"] > T["T2"],
         "T2": all(T["T2"] < v for v in hl.values()),
         "T3": T["T3"] > T["T1"],
         "T4": f1["GPT 4o 8 Few Shot"] >= max(f1.values()),
         "T5": T["T5"] > float(main["author_pct1s_8lab_line2067"]),
         "T6": abs(T["T6"] - 589) <= 5 and nrows_equal}
src = {"T1": "outputs/targets_extracted.csv (metrics_matrix|GPT 4o 8 Few Shot|HammingLoss)", "T2": "outputs/targets_extracted.csv (undergrads8|Hamming Loss)",
       "T3": "outputs/targets_extracted.csv (metrics_matrix|GPT 4o 4 Few Shot|HammingLoss)", "T4": "outputs/targets_extracted.csv (metrics_matrix|GPT 4o 8 Few Shot|F1)",
       "T5": "outputs/targets_extracted.csv (metrics_matrix|GPT 4o 8 Few Shot|Mean)", "T6": "outputs/targets_extracted.csv (nrow_pi10mat)"}
notes = {"T1": f"Lowest of 18 LLM rows: {hl['GPT 4o 8 Few Shot'] <= min(hl.values())}; above T2: {T['T1'] > T['T2']}.",
         "T2": "Undergraduate 8-label hamming loss below every one of the 18 LLM rows: %s." % concl["T2"],
         "T3": "T3 > T1: %s." % concl["T3"],
         "T4": "Pre-registered candidate (caret default positive class '0'). Highest F1 of the 18 LLM rows: %s. Secondary context only, positive class '1': %.4f (outputs/checks.csv)." % (concl["T4"], float(ck["secondary|F1_positive1_GPT4o8Few_mean_na_rm"])),
         "T5": "Author 8-label share of 1s by script (line 2067 expression): %.4f; T5 above it: %s." % (float(main["author_pct1s_8lab_line2067"]), concl["T5"]),
         "T6": "nrow(pi10mat)=%s, nrow(gpt4o10mat_fewx)=%s, nrow(hum10matx)=%s." % (main["nrow_pi10mat"], main["nrow_gpt4o10mat_fewx"], main["nrow_hum10matx"])}
targets = []
for tid in ["T1", "T2", "T3", "T4", "T5", "T6"]:
    p = pv[tid]["paper_value"]; d = pv[tid]["paper_rounding_decimals"]; r = T[tid]
    targets.append({"id": tid, "description": pv[tid]["description"], "paper_value": p, "paper_rounding_decimals": d,
                    "reproduced_value": r, "source_file": src[tid], "abs_diff": abs(r - p), "rel_diff": (r - p) / p,
                    "match_to_rounding": round(r, d) == round(p, d), "within_5pct": abs((r - p) / p) <= 0.05,
                    "same_conclusion": concl[tid], "note": notes[tid]})
def rob(rid, path, desc, extra):
    s = summ(path); b = lambda k: s[k].strip() == "TRUE"; f = lambda k: float(s[k])
    return {"id": rid, "description": desc, "ran": True, "estimate": f("T1"),
            "se_or_ci": "T1 95%% percentile CI [%.4f, %.4f]; D = T1 - undergrad8 = %.4f, 95%% percentile CI [%.4f, %.4f], bootstrap SE of D %.4f; seed 20261010, 1000 resamples" % (f("T1_ci_lo"), f("T1_ci_hi"), f("D"), f("D_ci_lo"), f("D_ci_hi"), f("D_boot_se")),
            "p_value": f("p_value"), "same_direction_and_significance_as_paper": b("same_direction_and_significance"),
            "source_file": path,
            "note": ("n_rows %s, dropped %s; undergrad8 hamming %.4f; rank of GPT 4o Few Shot 8 among 18 LLM specs %s; T3 - T1 %.4f; share of resamples where it is lowest %.3f; criteria (i) %s (ii) %s (iii) %s. p-value = min(1, 2*share D<=0), the audit's own reading; the paper reports no test. "
                     % (s["n_rows"], s["n_dropped"], f("U8"), s["rank_T1_among_18"], f("T3_minus_T1"), f("share_resamples_T1_lowest"), s["crit_i"], s["crit_ii"], s["crit_iii"])) + extra}
rcx = ("Diagnostics: identical(pi$docid, gpt4o 8 few docid) original=%s, R_c copy=%s; identical(pi$docid, human10 docid) original=%s, R_c copy=%s. "
       "R_c full rerun values (outputs/R_c_targets_extracted.csv): T1 %.4f, T2 %.4f, T3 %.4f, T4 %.4f, T5 %.2f, T6 %d. "
       "Docid-paired FP/FN cells (outputs/checks.csv): GPT 4o Few Shot 8 FP %s FN %s of %s; undergrad 8 FP %s FN %s."
       % (main["identical_pi_docid_vs_gpt4o10few_docid"], rc["identical_pi_docid_vs_gpt4o10few_docid"], main["identical_pi_docid_vs_human10_docid"], rc["identical_pi_docid_vs_human10_docid"],
          mm(rc, "GPT 4o 8 Few Shot", "HammingLoss"), float(rc["undergrads8|Hamming Loss"]), mm(rc, "GPT 4o 4 Few Shot", "HammingLoss"), mm(rc, "GPT 4o 8 Few Shot", "F1"), mm(rc, "GPT 4o 8 Few Shot", "Mean"), int(float(rc["nrow_pi10mat"])),
          ck["Rc_by_docid|GPT4o8Few|FP(model1,bench0)"], ck["Rc_by_docid|GPT4o8Few|FN(model0,bench1)"], ck["Rc_by_docid|GPT4o8Few|cells"], ck["Rc_by_docid|Undergrad8|FP(model1,bench0)"], ck["Rc_by_docid|Undergrad8|FN(model0,bench1)"]))
hlr = {r: mm(rc, r, "HammingLoss") for r in llm_rows}; f1r = {r: mm(rc, r, "F1") for r in llm_rows}
r1, r2, r3 = hlr["GPT 4o 8 Few Shot"], float(rc["undergrads8|Hamming Loss"]), hlr["GPT 4o 4 Few Shot"]
rc_concl = "T1 lowest of 18 and above T2: %s; T2 below all 18 LLMs: %s; T3 > T1: %s; T4 highest F1 of 18: %s; T5 above author share: %s" % (
    r1 <= min(hlr.values()) and r1 > r2, all(r2 < v for v in hlr.values()), r3 > r1, f1r["GPT 4o 8 Few Shot"] >= max(f1r.values()),
    mm(rc, "GPT 4o 8 Few Shot", "Mean") > float(rc["author_pct1s_8lab_line2067"]))
robustness = [
    rob("R_a", "outputs/R_a_summary.csv", "Bootstrap resample of articles (rows), seed 20261010, 1000 resamples, authors' row pairing kept", ""),
    rob("R_b", "outputs/R_b_summary.csv", "Drop rows with |z|>3 on k = rowSums(pi10mat) (author's labels per article), same rows dropped from every matrix, then R_a bootstrap on the reduced rows", "k distribution: outputs/R_b_k_distribution.csv."),
    rob("R_c", "outputs/R_c_summary.csv", "Pair benchmark and model rows by docid: copy of the Rmd with one line 'pi = pi %>% arrange(docid)' after line 108 (diffs/R_c_Benchmarking_DataAnalysis_docid_sort.diff), full rerun, then R_a bootstrap", rcx)]
bugs = [
    {"file": "Benchmarking_DataAnalysis.Rmd", "line": 108,
     "description": "Author benchmark is compared with model and undergraduate codings by row position, but the rows are in different docid orders. pi (pi_codings_2ndhalf.csv, read line 102, de-duplicated line 108) keeps the file's unsorted docid order, while all model files and human10_agree.csv are sorted by docid; calculate_hamming_loss (line 1552), the F1/recall/precision/AUC functions and get_means comparisons pair rows by index. So, in the run, each article's author codes are compared with a different article's model codes. The '% 1s' column is unaffected (it uses only the model matrix).",
     "evidence": "Run outputs: identical(pi$docid, gpt4o 8-label few-shot docid) = %s although the sets are equal (setequal %s); only %s of 589 rows share the same docid at the same position; first pi docids '%s' vs model '%s' (outputs/checks.csv, outputs/targets_extracted.csv). With docid pairing (R_c), GPT 4o Few Shot 8-label mismatches are FP %s / FN %s of 4712 cells, the counts printed in supplement Table A5 (369 / 150), while the as-deposited positional pairing gives FP %s / FN %s; hamming loss %.4f vs %.4f."
                 % (main["identical_pi_docid_vs_gpt4o10few_docid"], main["setequal_pi_docid_vs_gpt4o10few_docid"], ck["main|rows_with_same_docid_in_same_position"], ck["main|first10_pi_docid"], ck["main|first10_gpt4o10few_docid"],
                    ck["Rc_by_docid|GPT4o8Few|FP(model1,bench0)"], ck["Rc_by_docid|GPT4o8Few|FN(model0,bench1)"], ck["main_by_position|GPT4o8Few|FP(model1,bench0)"], ck["main_by_position|GPT4o8Few|FN(model0,bench1)"], mm(rc, "GPT 4o 8 Few Shot", "HammingLoss"), T["T1"])},
    {"file": "Benchmarking_DataAnalysis.Rmd", "line": 2050,
     "description": "undergrads8 (lines 2050-2056) and undergrads4 (lines 2058-2064) compute AUC, Recall and F1 from gpt10mat / gpt4mat (GPT 4 Turbo Zero Shot output) instead of the undergraduate matrices; only their Hamming Loss and % 1s use hum10matx / hum4mat. Table A1's undergraduate AUC/Recall/F1 therefore repeat the GPT 4 Turbo Zero Shot values. Does not affect T2 (Hamming Loss).",
     "evidence": "outputs/checks.csv: undergrads8 AUC/Recall/F1 equal GPT 4 Turbo 8 Zero Shot = %s/%s/%s; undergrads4 equal GPT 4 Turbo 4 Zero Shot = %s/%s/%s."
                 % tuple(ck[k] for k in ["undergrads8_AUC_equals_GPT4Turbo8Zero", "undergrads8_Recall_equals_GPT4Turbo8Zero", "undergrads8_F1_equals_GPT4Turbo8Zero", "undergrads4_AUC_equals_GPT4Turbo4Zero", "undergrads4_Recall_equals_GPT4Turbo4Zero", "undergrads4_F1_equals_GPT4Turbo4Zero"])}]
allmatch = all(t["match_to_rounding"] for t in targets)
res = {"paper_id": "18_YXC5K5", "agent": "B", "run_date_ist": "2026-10-11", "ran": True, "could_not_run_reason": "",
       "targets": targets, "robustness": robustness, "bugs": bugs,
       "env_fixes": ["none to the authors' code: no file of the deposit was edited. Environment only: packages installed (Debian r-cran-* binaries plus irr and stargazer from CRAN into the per-run library), working directory set to the data folder, Rmd converted with knitr::purl(documentation=1). diffs/R_c_Benchmarking_DataAnalysis_docid_sort.diff is the pre-registered R_c robustness change, not an environment fix."],
       "proposed_class": "A" if allmatch else "B",
       "class_reason": ("All six targets match Supplement Table A1 / the printed N to the paper's rounding with Benchmarking_DataAnalysis.Rmd run exactly as deposited (batch 4 decision 4). " if allmatch else "Not all targets match to rounding. ")
                       + "Separately, the docid-paired rerun (R_c) gives much lower hamming losses (T1 %.3f, T2 %.3f) with the same ranking and direction; it does not change the class." % (mm(rc, "GPT 4o 8 Few Shot", "HammingLoss"), float(rc["undergrads8|Hamming Loss"])),
       "confidence": "medium",
       "confidence_reason": "Exact script match, but target paper values come from a viewer reading of the supplement and the as-deposited pairing of rows by position was confirmed by run; A/B agreement not known to B.",
       "time_minutes": None,
       "uncertainties": [
           "Paper values T3 to T5 come from a browser agent's Google Docs viewer reading of the supplement (PREREG); B did not re-open the supplement.",
           "The row-position pairing (bug 1) means the as-deposited Table A1 hamming loss, F1, recall, AUC and ICC compare different articles in 588 of 589 rows; the reproduced numbers match the printed table, which is consistent with (not proof of) the table having been produced with the same positional pairing. The docid-paired numbers reproduce the cell counts printed in Tables A5 (exactly) and A6 (undergrad FP %s vs printed 254; FN %s vs 180). Under docid pairing (R_c rerun) the pre-registered conclusion criteria evaluate to: %s." % (ck["Rc_by_docid|Undergrad8|FP(model1,bench0)"], ck["Rc_by_docid|Undergrad8|FN(model0,bench1)"], rc_concl),
           "Undergraduate '%% 1s' returned by the script is a proportion (%s), Table A1 prints 9.68; 100x the script value is %.2f, which does not equal 9.68 to 2 decimals. Not a target." % (ck["secondary|undergrads8_pct1s_as_returned_by_script"], 100 * float(ck["secondary|undergrads8_pct1s_as_returned_by_script"])),
           "Package versions differ from the author's (R 4.5.0 on aarch64 Linux vs R 4.3.3 on Windows; no pins exist). T4 depends on caret's default positive class; caret %s gave the printed value." % main["caret_version"],
           "The main run was killed twice by the shared machine's memory pressure (SIGKILL, rc 137) while rendering a plot; the third identical attempt finished (peak RSS about 399 MB). No code was changed between attempts.",
           "Label naming of Theme5/Theme6 (PREREG inconsistency 3) only affects per-label plots, not the pooled targets; not checked further."]}
lg = os.path.join(HERE, "LOG.md")
if os.path.exists(lg):
    import re
    ts = re.findall(r"(\d{2}:\d{2}) UTC", open(lg).read())
    if ts:
        h = lambda x: int(x[:2]) * 60 + int(x[3:])
        res["time_minutes"] = h(ts[-1]) - h(ts[0])
json.dump(res, open(os.path.join(HERE, "results.json"), "w"), indent=1)
print(json.dumps({t["id"]: [t["paper_value"], round(t["reproduced_value"], 6), t["match_to_rounding"], t["same_conclusion"]] for t in targets}))
print(res["proposed_class"], [ (r["id"], r["estimate"], r["same_direction_and_significance_as_paper"]) for r in robustness])
