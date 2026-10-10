"""Build results.json for 04_PSHE5L Agent A. All reproduced numbers are read from files in outputs/.
paper_value entries are read from REPO/papers/04_PSHE5L/targets.json (copied from the paper in PREREG.md)."""
import csv, json, os, re, datetime
HERE = os.path.dirname(os.path.abspath(__file__)); A = os.path.dirname(HERE); OUT = os.path.join(A, "outputs")
targets = json.load(open(os.path.join(A, "..", "targets.json")))
def rd(p): return list(csv.DictReader(open(os.path.join(OUT, p))))
def lookup(fname, lhs, op, rhs, col):
    for r in rd(fname):
        if r["lhs"] == lhs and r["op"] == op and (op == ":=" or r["rhs"] == rhs): return float(r[col])
    raise KeyError((fname, lhs, op, rhs))
keys = {"T1": ("violence", "~", "polgriev"), "T2": ("violence", "~", "econgriev"), "T3": ("polgriev", "~", "econgriev"),
        "T4": ("indirect1_econgriev", ":=", ""), "T5": ("total_effect_econgriev", ":=", "")}
paper_p = {"T1": 0.006, "T2": 0.005, "T3": 0.000, "T4": 0.028, "T5": 0.020}  # from PREREG.md section 1 (context)
fit = {r["measure"]: float(r["value"]) for r in rd("structural_fit.csv")}
dfit = {r["measure"]: float(r["value"]) for r in rd("diag_q15na_fit.csv")}
tout = []
for t in targets:
    k = keys[t["id"]]
    v = lookup("structural_stdsol.csv", *k, "est.std")
    p_std = lookup("structural_stdsol.csv", *k, "pvalue"); p_un = lookup("structural_pe.csv", *k, "pvalue")
    dv = lookup("diag_q15na_stdsol.csv", *k, "est.std")
    pv = t["paper_value"]; dec = t["paper_rounding_decimals"]
    ad = v - pv; rel = ad / abs(pv)
    same = (v * pv > 0) and ((p_un < 0.05) == (paper_p[t["id"]] < 0.05))
    tout.append({"id": t["id"], "description": t["description"], "paper_value": pv, "paper_rounding_decimals": dec,
                 "reproduced_value": v, "source_file": "outputs/structural_stdsol.csv", "abs_diff": ad, "rel_diff": rel,
                 "match_to_rounding": round(v, dec) == pv, "within_5pct": abs(rel) <= 0.05, "same_conclusion": same,
                 "note": (f"Primary run (as deposited, Q15 code 8 kept), est.std from standardizedSolution(structural). "
                          f"p (summary()/parameterEstimates, unstandardized z test) = {p_un:.4f}; p (standardizedSolution, delta method) = {p_std:.4f}; "
                          f"paper p = {paper_p[t['id']]:.3f}; the paper's p values match the unstandardized ones to 3 decimals. "
                          f"DIAGNOSTIC run (authors' line 188 re-enabled, Q15 code 8 = NA): est.std = {dv:.4f} (outputs/diag_q15na_stdsol.csv). "
                          f"lavaan nobs = {int(fit['nobs'])} (paper n = 1139).")})
# robustness
ra = json.load(open(os.path.join(OUT, "R_a_summary.json")))
def rbrow(fname):
    rows = rd(fname); b = [r for r in rows if r["quantity"] == "b1_violence_on_polgriev"][0]; i = [r for r in rows if r["quantity"] == "indirect1_econgriev"][0]
    return b, i
rb_b, rb_i = rbrow("R_b_outliers.csv"); rc_b, rc_i = rbrow("R_c_unweighted.csv")
def sig(x): return float(x) < 0.05
rob = [
 {"id": "R_a", "description": "Nonparametric case bootstrap, 1000 replicates, set.seed(20261009) once; rows resampled with their WTS weights; same cfa() call; est.std of b1 and indirect1_econgriev; percentile 95% CI", "ran": True,
  "estimate": ra["b1_std"]["median"], "se_or_ci": f"b1 percentile 95% CI [{ra['b1_std']['ci95_lower']:.4f}, {ra['b1_std']['ci95_upper']:.4f}]",
  "p_value": None, "same_direction_and_significance_as_paper": (ra["b1_std"]["median"] < 0) and ra["b1_std"]["ci_excludes_0"],
  "source_file": "outputs/R_a_summary.json (from outputs/R_a_boot.csv)",
  "note": (f"estimate = bootstrap median of b1 est.std. Replicates attempted {ra['replicates_attempted']}, usable {ra['replicates_ok']}, failed or non-converged {ra['replicates_failed_or_nonconverged']} (excluded). "
           f"Share of replicates with b1 < 0: {ra['b1_std']['share_below_0']:.3f}. Indirect effect (T4): median {ra['indirect_std']['median']:.4f}, 95% CI [{ra['indirect_std']['ci95_lower']:.4f}, {ra['indirect_std']['ci95_upper']:.4f}], CI excludes 0: {ra['indirect_std']['ci_excludes_0']}. "
           "Resample indices for all 1000 replicates were drawn in order right after the single set.seed call and stored, to make the run resumable.")},
 {"id": "R_b", "description": "Drop rows with |z| > 3 on unweighted z of viol_mean = rowMeans(Q25B, Q25C, Q25D); refit same model", "ran": True,
  "estimate": float(rb_b["est_std"]), "se_or_ci": f"SE(std) {float(rb_b['se_std']):.4f}; 95% CI [{float(rb_b['ci_lower_std']):.4f}, {float(rb_b['ci_upper_std']):.4f}]",
  "p_value": float(rb_b["p_unstd"]), "same_direction_and_significance_as_paper": float(rb_b["est_std"]) < 0 and sig(rb_b["p_unstd"]),
  "source_file": "outputs/R_b_outliers.csv",
  "note": (f"Rows dropped: {int(float(rb_b['rows_dropped']))} (max |z| {float(rb_b['max_abs_z']):.3f}); nobs {int(float(rb_b['nobs']))}. p_value = unstandardized z test (as in paper); p of est.std = {float(rb_b['p_std']):.4f}. "
           f"Indirect (T4) est.std {float(rb_i['est_std']):.4f}, p unstd {float(rb_i['p_unstd']):.4f}, p std {float(rb_i['p_std']):.4f}.")},
 {"id": "R_c", "description": "Unweighted: identical cfa() call without sampling.weights, all 1203 rows", "ran": True,
  "estimate": float(rc_b["est_std"]), "se_or_ci": f"SE(std) {float(rc_b['se_std']):.4f}; 95% CI [{float(rc_b['ci_lower_std']):.4f}, {float(rc_b['ci_upper_std']):.4f}]",
  "p_value": float(rc_b["p_unstd"]), "same_direction_and_significance_as_paper": float(rc_b["est_std"]) < 0 and sig(rc_b["p_unstd"]),
  "source_file": "outputs/R_c_unweighted.csv",
  "note": (f"nobs {int(float(rc_b['nobs']))}. p_value = unstandardized z test; p of est.std = {float(rc_b['p_std']):.4f}. b1 keeps sign and p < .05 but is smaller in size. "
           f"Indirect (T4) est.std {float(rc_i['est_std']):.4f}, p unstd {float(rc_i['p_unstd']):.4f}, p std {float(rc_i['p_std']):.4f}: not significant at .05 unweighted.")},
]
cmp = {r["item"]: r for r in json.load(open(os.path.join(OUT, "primary_vs_diagnostic.json")))}
bugs = [
 {"file": "Rural Populism - Socius - Public Code.R", "line": 188,
  "description": ("Q15 (conservatism) code 8 is left in the data and used as a numeric value above 7 in every model, because the recode to NA is commented out. "
                  "The script's own comment on that line gives the scale as 'Liberal 1 - 7 Conservative'. What code 8 means could not be determined: no public codebook or questionnaire for this 2021 survey was found "
                  "(the OSF parent project only documents the 2020 wave, where Q15 is a different question). The authors' commented recodes elsewhere set analogous extra codes to NA (QF 6 'No answer', line 43-44; XQ14 4 and 5, lines 134-135, active)."),
  "evidence": (f"outputs/data_facts.txt: Q15 takes values 1-8, with 64 rows = 8; 1203 - 64 = 1139 = paper's n. Published coefficients T1-T5 match only the run with code 8 kept; "
               f"the published structural fit (chi2 516.954, robust CFI .911, TLI .892) matches only the run with code 8 set to NA "
               f"(primary chi2.scaled {cmp['structural_fit:chisq.scaled']['primary']:.3f}, diagnostic {cmp['structural_fit:chisq.scaled']['diagnostic_q15_8_as_NA']:.3f}; outputs/primary_vs_diagnostic.csv).")},
]
time_minutes = None
log = open(os.path.join(A, "LOG.md")).read()
m = re.search(r"TIME_MINUTES:\s*(\d+)", log)
if m: time_minutes = int(m.group(1))
res = {"paper_id": "04_PSHE5L", "agent": "A", "run_date_ist": "2026-10-09", "ran": True, "could_not_run_reason": "",
 "targets": tout, "robustness": rob, "bugs": bugs,
 "env_fixes": ["diffs/01_data_path.diff: script reads a non-public 117-column file (line 9); path changed to the public OSF extract Rural_Populism_Dataset.csv",
               "diffs/02_raw_q24_absent.diff: RAW_Q24A-I columns absent from the public extract, mutate(across(all_of())) errored; lines 17, 19, 20, 22 commented out (variables never used later)",
               "diffs/03_gt_library.diff: gt not installable (V8 needs system libv8, unavailable on Debian 13 arm64); library(gt) commented out (no gt function is called)"],
 "proposed_class": "A",
 "class_reason": ("All five headline standardized coefficients reproduce exactly to the paper's 3 decimals (and the paper's p values match the unstandardized z tests) from the deposited code with three environment fixes. "
                  "Caveat on PROTOCOL section 7: the Dataverse deposit contains code only; the data come from the authors' OSF component (osf.io/mtd4z), which the paper does not cite, in a reduced 30-column extract under a different file name, so judged on the Dataverse deposit alone the materials are incomplete (class C); "
                  "I propose A because the authors' own public materials reproduce the targets exactly, but flag this for the batch decision. The paper's structural-model fit statistics and n = 1,139 correspond to a different data state (Q15 code 8 as missing) than its coefficients."),
 "confidence": "medium",
 "confidence_reason": "Targets matched by script with the pinned lavaan 0.6-19, but the data are an unlinked OSF extract and the paper's fit statistics and n come from a different data state than its coefficients; B not yet compared.",
 "time_minutes": time_minutes,
 "uncertainties": [
   "Data provenance: the CSV is linked to this paper only by the OSF component title, the byte-identical code file and matching variables; the paper does not cite it.",
   "Meaning of Q15 code 8 (64 rows) could not be determined from any public codebook.",
   f"n: lavaan reports nobs = {int(fit['nobs'])} in both the primary and diagnostic runs (FIML keeps rows with missing Q15); the paper reports 1,139 = rows with Q15 != 8. How the authors obtained 1,139 is not determined.",
   f"Structural fit: primary run chi2.scaled {fit['chisq.scaled']:.3f}, robust CFI {fit['cfi.robust']:.3f}, robust TLI {fit['tli.robust']:.3f} vs paper 516.954/.911/.892; the diagnostic run gives {dfit['chisq.scaled']:.3f}/{dfit['cfi.robust']:.3f}/{dfit['tli.robust']:.3f}. SRMR and robust RMSEA agree in both. The paper's fit and coefficients thus come from two different data states.",
   f"Controls model (context): primary run gives chi2.scaled {cmp['controls_model_fit:chisq.scaled']['primary']:.3f}, df 201, n {int(cmp['controls_model_fit:nobs']['primary'])}, equal to the paper's 779.793 / 201 / 998; the diagnostic run does not ({cmp['controls_model_fit:chisq.scaled']['diagnostic_q15_8_as_NA']:.3f}).",
   "Table 1 reliability values (not targets) printed by the script (alpha, CR, AVE in outputs/full_script_output.txt) do not equal the paper's Table 1 values recorded in PREREG.md (e.g. paper alpha .856 and .891 for the last two factors); not investigated further because Table 1 is not a target.",
   "Authors pinned no package versions; lavaan 0.6-19 / semTools 0.5-6 were chosen by the PREREG as contemporaneous with the 2024-11 deposit. Whether the authors used them is unknown.",
   "Robustness R_a: the 1000 resample index vectors were drawn up front after set.seed(20261009) (same sequence as drawing inside the loop, given only sample() uses the RNG); a strict in-loop implementation would give the same draws unless lavaan consumes RNG, which was not checked.",
   "Controls-model dummies code non-substantive answers as 0 (QF 6 'No answer' as not college, QB 12 as not over 65, QC 3/4 as not male); the script's comment at lines 118-119 states this choice. Affects the controls model only, not the targets; recorded as an observation, not a bug."]
}
json.dump(res, open(os.path.join(A, "results.json"), "w"), indent=1)
print("written; class", res["proposed_class"], [ (t["id"], round(t["reproduced_value"],4), t["match_to_rounding"]) for t in tout])
