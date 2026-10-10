# Build results.json for 04_PSHE5L, Agent B. Every number is read from files in outputs/;
# paper values come from ../../targets.json (copied from PREREG.md).
import csv, json, os, re, math
HERE = os.path.dirname(os.path.abspath(__file__))
B = os.path.dirname(HERE); OUT = os.path.join(B, "outputs"); PAPER = os.path.dirname(B)

def rows(fn): return list(csv.DictReader(open(os.path.join(OUT, fn))))
def find(rs, lhs, op, rhs=None):
    m = [r for r in rs if r["lhs"] == lhs and r["op"] == op and (rhs is None or r["rhs"] == rhs)]
    assert len(m) == 1, (lhs, op, rhs, len(m)); return m[0]
def fitv(fn):
    return {r["measure"]: float(r["value"]) for r in rows(fn)}

targets_paper = json.load(open(os.path.join(PAPER, "targets.json")))
mapping = {"T1": ("violence", "~", "polgriev"), "T2": ("violence", "~", "econgriev"),
           "T3": ("polgriev", "~", "econgriev"), "T4": ("indirect1_econgriev", ":=", None),
           "T5": ("total_effect_econgriev", ":=", None)}
paper_p = {"T1": 0.006, "T2": 0.005, "T3": 0.000, "T4": 0.028, "T5": 0.020}  # copied from PREREG.md section 1
ss, pe = rows("primary_structural_stdsol.csv"), rows("primary_structural_pe.csv")
dss = rows("diag_q15na_structural_stdsol.csv")
pfit, dfit = fitv("primary_structural_fit.csv"), fitv("diag_q15na_structural_fit.csv")
cfit = fitv("primary_structural_ctrl_fit.csv")

targets = []
for t in targets_paper:
    lhs, op, rhs = mapping[t["id"]]
    s, p, d = find(ss, lhs, op, rhs), find(pe, lhs, op, rhs), find(dss, lhs, op, rhs)
    v = float(s["est.std"]); pv = t["paper_value"]; dec = t["paper_rounding_decimals"]
    p_unstd, p_std = float(p["pvalue"]), float(s["pvalue"])
    absd = v - pv; reld = absd / abs(pv)
    same = (math.copysign(1, v) == math.copysign(1, pv)) and (p_unstd < 0.05) == (paper_p[t["id"]] < 0.05)
    targets.append({
        "id": t["id"], "description": t["description"], "paper_value": pv, "paper_rounding_decimals": dec,
        "reproduced_value": v, "source_file": "outputs/primary_structural_stdsol.csv",
        "abs_diff": absd, "rel_diff": reld, "match_to_rounding": round(v, dec) == pv,
        "within_5pct": abs(reld) <= 0.05, "same_conclusion": same,
        "note": (f"est.std (std.all) from standardizedSolution(structural), primary as-deposited run, lavaan nobs "
                 f"{int(pfit['nobs'])} (paper n 1,139). p from summary()/parameterEstimates (unstandardized z test) = "
                 f"{p_unstd:.4f}; p from standardizedSolution (delta method) = {p_std:.4f}; paper p = {paper_p[t['id']]:.3f}. "
                 f"DIAGNOSTIC run (line 188 Q15==8 -> NA) est.std = {float(d['est.std']):.4f} "
                 f"(outputs/diag_q15na_structural_stdsol.csv).")})

# Robustness
ra = json.load(open(os.path.join(OUT, "R_a_summary.json")))
b1 = ra["b1_std"]; ind = ra["indirect1_std"]
ra_sig = (b1["ci97.5"] < 0)
rb = {r["param"]: r for r in rows("R_b_outliers.csv")}; rc = {r["param"]: r for r in rows("R_c_unweighted.csv")}
def rrow(rid, desc, r, fn, extra):
    b, i = r["b1"], r["indirect1_econgriev"]
    est, pst = float(b["est_std"]), float(b["p_std"])
    return {"id": rid, "description": desc, "ran": True, "estimate": est,
            "se_or_ci": f"SE {float(b['se_std']):.4f}; 95% CI [{float(b['ci_lower_std']):.4f}, {float(b['ci_upper_std']):.4f}] (standardizedSolution)",
            "p_value": pst, "same_direction_and_significance_as_paper": (est < 0 and pst < 0.05),
            "source_file": fn,
            "note": (f"estimate = est.std of violence ~ polgriev (T1). p_value from standardizedSolution; unstandardized p = "
                     f"{float(b['p_unstd']):.4f}. indirect1_econgriev (T4) est.std = {float(i['est_std']):.4f}, p_std = "
                     f"{float(i['p_std']):.4f}, p_unstd = {float(i['p_unstd']):.4f}, 95% CI [{float(i['ci_lower_std']):.4f}, "
                     f"{float(i['ci_upper_std']):.4f}]; T4 same direction and p<.05: {float(i['est_std']) < 0 and float(i['p_std']) < 0.05}. "
                     f"nobs {int(float(b['nobs']))}. " + extra)}
robust = [
    {"id": "R_a", "description": "Case bootstrap, 1000 replicates, set.seed(20261009) once; resample rows with replacement keeping WTS, refit identical cfa(..., sampling.weights='WTS', missing='ML', estimator='MLR'); est.std of b1 and indirect1_econgriev; median and percentile 95% CI.",
     "ran": True, "estimate": b1["median"],
     "se_or_ci": f"bootstrap median; percentile 95% CI [{b1['ci2.5']:.4f}, {b1['ci97.5']:.4f}]",
     "p_value": None, "same_direction_and_significance_as_paper": ra_sig, "source_file": "outputs/R_a_summary.json",
     "note": (f"Replicates run {ra['replicates_total']}, usable {ra['replicates_ok']}, failed/non-converged excluded "
              f"{ra['replicates_failed_or_nonconverged']}. Share of b1 < 0: {b1['share_below_0']:.3f}. indirect1_econgriev: median "
              f"{ind['median']:.4f}, 95% CI [{ind['ci2.5']:.4f}, {ind['ci97.5']:.4f}], share < 0 {ind['share_below_0']:.3f}; T4 CI excludes 0: "
              f"{ind['ci97.5'] < 0}. Raw replicates: outputs/R_a_boot.csv.")},
    rrow("R_b", "Drop rows with |z| > 3 on unweighted z of rowMeans(Q25B, Q25C, Q25D); refit identical model.", rb,
         "outputs/R_b_outliers.csv", f"Rows dropped: {int(float(rb['b1']['rows_dropped']))}."),
    rrow("R_c", "Unweighted: identical call without sampling.weights = 'WTS' (all 1203 rows incl. 11 with WTS 0).", rc,
         "outputs/R_c_unweighted.csv", ""),
]

# time from LOG.md timestamps (HH:MM at line starts, same IST day)
ts = [int(h) * 60 + int(m) for h, m in re.findall(r"^- (\d\d):(\d\d)", open(os.path.join(B, "LOG.md")).read(), re.M)]
time_minutes = max(ts) - min(ts)

all_match = all(t["match_to_rounding"] for t in targets)
res = {
 "paper_id": "04_PSHE5L", "agent": "B", "run_date_ist": "2026-10-09", "ran": True, "could_not_run_reason": "",
 "targets": targets, "robustness": robust,
 "bugs": [],
 "env_fixes": ["diffs/01_data_path.diff: line 9 data path changed to the public OSF extract Rural_Populism_Dataset.csv (the named file is not in the Dataverse deposit)",
               "diffs/02_comment_out_RAW_Q24_mutate.diff: lines 19-20 error because RAW_Q24A-I are absent from the public extract; created variables unused"],
 "proposed_class": "A" if all_match else "B",
 "class_reason": ("All five standardized targets from the as-deposited code (two PREREG-allowed environment fixes) match the paper to 3 decimals, and the paper's p values match the unstandardized z-test p values. "
                  "The data had to come from the authors' OSF component, not the Dataverse deposit (code only); see uncertainties for why class C was considered."),
 "confidence": "medium",
 "confidence_reason": (f"Targets match exactly, but data came from OSF not the deposit, lavaan n is {int(pfit['nobs'])} not 1,139, and the paper's main-model fit statistics "
                       f"(chi2 516.954) match only the Q15-code-8-as-NA diagnostic run (chi2 {dfit['chisq.scaled']:.3f}), not the primary run (chi2 {pfit['chisq.scaled']:.3f})."),
 "time_minutes": time_minutes,
 "uncertainties": [
  "Data source: the Dataverse deposit contains only the R script; the CSV was downloaded from the authors' OSF component https://osf.io/mtd4z/ (not cited in the paper). It is a 30-column extract with a different file name from the 117-column file the script reads. If the audit requires the Dataverse deposit alone to be sufficient, the deposit is incomplete (no data, no README), which would point to class C under PROTOCOL section 7; I propose A because the targets reproduce exactly from the authors' own public data and code, but the batch report should note this judgement.",
  f"Primary (as deposited, Q15 code 8 kept): main-model fit scaled chi2 {pfit['chisq.scaled']:.3f}, df {pfit['df.scaled']:.0f}, robust CFI {pfit['cfi.robust']:.3f}, robust TLI {pfit['tli.robust']:.3f}, SRMR {pfit['srmr']:.3f}, robust RMSEA {pfit['rmsea.robust']:.3f}, nobs {int(pfit['nobs'])}. Paper: 516.954, 141, .911, .892, .058, .062, n 1,139.",
  f"Diagnostic (line 188 active, Q15 == 8 -> NA): fit scaled chi2 {dfit['chisq.scaled']:.3f}, df {dfit['df.scaled']:.0f}, CFI {dfit['cfi.robust']:.3f}, TLI {dfit['tli.robust']:.3f}, SRMR {dfit['srmr']:.3f}, RMSEA {dfit['rmsea.robust']:.3f}, nobs {int(dfit['nobs'])} (FIML keeps the 64 rows). These equal the paper's fit numbers, but the diagnostic's coefficients do not equal the paper's tables (see target notes). So the paper's coefficients and its main-model fit statistics correspond to two different Q15 codings; I cannot determine why.",
  f"Paper n = 1,139 equals 1203 - 64 (rows with Q15 = 8) but lavaan reports nobs {int(pfit['nobs'])} in both runs. Controls model: nobs {int(cfit['nobs'])}, scaled chi2 {cfit['chisq.scaled']:.3f}, df {cfit['df.scaled']:.0f} in the primary run (paper: 998, 779.793, 201).",
  "Q15 code 8: no public codebook for the 2021 survey labels it. The same team's OSF GND experiment code (https://osf.io/download/6aghr/, lines 73-77, on data with identical Q15 frequencies) maps Q15 == 8 to 'Missing', and the script's own comment says 'Liberal 1 - 7 Conservative'. Whether code 8 should be missing in this paper's model is undeterminable from the public materials; not listed as a bug.",
  "Paper p values match the unstandardized z-test p values from summary() (e.g. T2 .0054 vs paper .005), not the standardizedSolution delta-method p values (T2 .0020). Standardized values assumed std.all (lavaan default est.std).",
  "Table 1 reliability values (not a target) were not reproduced by the script's rel()/reliability() output; see outputs/code_review.md item 4.",
  "Environment: R 4.5.0 (system) used instead of the PREREG's R 4.4.3 path, which does not exist on this machine (brief instructed system Rscript). lavaan 0.6-19 and semTools 0.5-6 pinned versions were installed and used from the fresh library.",
  "R_b and R_c significance judged with standardizedSolution p values; unstandardized p values are in the notes and lead to the same conclusions.",
  "Process note: a ps listing displayed file names of Agent A's running scripts for this paper; no Agent A file was opened or read.",
 ]}
json.dump(res, open(os.path.join(B, "results.json"), "w"), indent=1)
print(json.dumps({"class": res["proposed_class"], "targets": [(t["id"], t["paper_value"], round(t["reproduced_value"], 4), t["match_to_rounding"]) for t in targets],
                  "robust": [(r["id"], r["estimate"], r["p_value"], r["same_direction_and_significance_as_paper"]) for r in robust], "time": time_minutes}, indent=1))
