#!/usr/bin/env python3
"""Build results.json for 13_DX5T9G agent A from files in outputs/. No hand-typed reproduced numbers."""
import csv, json, os, re
P = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
O = os.path.join(P, "outputs")
REPO = os.path.dirname(os.path.dirname(P))
targets = json.load(open(os.path.join(os.path.dirname(P), "targets.json")))
rd = lambda f: list(csv.DictReader(open(os.path.join(O, f))))
ext = {r["id"]: r for r in rd("targets_extracted.csv")}
f = lambda x: None if x in ("", "NA", None) else float(x)

# cross-check printed table strings
def tex_cell(fn, rowname):
    for line in open(os.path.join(O, fn)):
        if line.startswith(rowname + " &"):
            return line.split("&")[1].strip().rstrip("\\").strip()
    return None
tex = {"T1": ("Table_2_table_main_UK_1.tex", "WHO (recommendation)"),
       "T2": ("Table_2_table_main_UK_1.tex", "WHO (recommendation, ratification)"),
       "T3": ("Table_3_table_main_US_1.tex", "WHO (recommendation)"),
       "T4": ("Table_3_table_main_US_1.tex", "WHO (recommendation, ratification)")}
def tex_n(fn):
    m = re.search(r"based on (\d+) observations", open(os.path.join(O, fn)).read())
    return int(m.group(1)) if m else None

out_t = []
for t in targets:
    e = ext[t["id"]]; pv = t["paper_value"]; dec = t["paper_rounding_decimals"]
    if t["id"] in ("T5", "T6"):
        rv = f(e["N"]); note = "N = nrow(tmp) column of store_estimates Coefficients (fallback run); table caption prints %s" % tex_n("Table_2_table_main_UK_1.tex" if t["id"] == "T5" else "Table_3_table_main_US_1.tex")
        same = abs(rv - pv) <= 5
    else:
        rv = f(e["Mean"]); p = f(e["pvalue"])
        same = (rv < 0) and (p < 0.01)
        note = ("Mean of 5000 mvrnorm draws (pre-registered candidate 1), fallback run. SD %.4f, code pvalue %.3g. "
                "Candidate 2 MLE (labelled refit of identical multinom call) %.4f, analytic SE %.4f, Wald p %.3g. Printed cell in reproduced .tex: %s"
                % (f(e["SD"]), p, f(e["MLE_refit"]), f(e["SE_analytic_refit"]), f(e["p_wald_refit"]), tex_cell(*tex[t["id"]])))
    ad = abs(rv - pv); rel = ad / abs(pv)
    out_t.append({"id": t["id"], "description": t["description"], "paper_value": pv, "paper_rounding_decimals": dec,
                  "reproduced_value": rv, "source_file": "outputs/targets_extracted.csv", "abs_diff": ad, "rel_diff": rel,
                  "match_to_rounding": round(rv, dec) == pv, "within_5pct": rel <= 0.05, "same_conclusion": bool(same), "note": note})

def sec(rows, tid):
    return [r for r in rows if r["target"] == tid][0]
ra = rd("R_a_bootstrap.csv"); rb = rd("R_b_extreme_weights.csv"); rbi = rd("R_b_exclusion_info.csv"); rc = rd("R_c_unweighted.csv")
def others_a():
    return "; ".join("%s MLE %.3f, boot SE %.3f, 99%% PI [%.3f, %.3f], p_boot %s" % (r["target"], f(r["estimate_mle"]), f(r["boot_se"]), f(r["q005"]), f(r["q995"]), r["p_boot"]) for r in ra if r["target"] != "T2")
def others(rows):
    return "; ".join("%s Mean %.3f, SD %.3f, p %.3g" % (r["target"], f(r["Mean"]), f(r["SD"]), f(r["pvalue"])) for r in rows if r["target"] != "T2")
a = sec(ra, "T2"); b = sec(rb, "T2"); c = sec(rc, "T2")
rob = [
 {"id": "R_a", "description": "Nonparametric case bootstrap within country, 1000 resamples, set.seed(20261010), weights w held fixed; primary quantity T2", "ran": True,
  "estimate": f(a["estimate_mle"]), "se_or_ci": "boot SE %.4f; 95%% PI [%.4f, %.4f]; 99%% PI [%.4f, %.4f]; %s converged fits used, %s non-converged" % (f(a["boot_se"]), f(a["q025"]), f(a["q975"]), f(a["q005"]), f(a["q995"]), a["n_boot_used"], a["n_nonconverged"]),
  "p_value": f(a["p_boot"]), "same_direction_and_significance_as_paper": f(a["estimate_mle"]) < 0 and f(a["q995"]) < 0,
  "source_file": "outputs/R_a_bootstrap.csv", "note": "p_boot = min(2*mean(b>=0),1); 0 means no resample of 1000 had b>=0 (p < 0.002 at this resolution). Bootstrap fits use Hess=FALSE (coefficients identical; Hessian not needed). Others: " + others_a()},
 {"id": "R_b", "description": "Drop rows with |z(w)|>3 within country, else top 1% of w; refit authors' main model; primary quantity T2", "ran": True,
  "estimate": f(b["Mean"]), "se_or_ci": "SD of draws %.4f; MLE %.4f; N %s" % (f(b["SD"]), f(b["MLE"]), b["N"]), "p_value": f(b["pvalue"]),
  "same_direction_and_significance_as_paper": f(b["Mean"]) < 0 and f(b["pvalue"]) < 0.01, "source_file": "outputs/R_b_extreme_weights.csv",
  "note": "Exclusion: " + "; ".join("%s rule %s, dropped %s (|z| log cases >3: %s, |z| age >3: %s)" % (r["country"], r["rule"], r["n_dropped"], r["n_absz_logcases_gt3"], r["n_absz_age_gt3"]) for r in rbi) + " (outputs/R_b_exclusion_info.csv). Others: " + others(rb)},
 {"id": "R_c", "description": "Unweighted estimation of the main model, set.seed(1230), mvrnorm 5000; primary quantity T2", "ran": True,
  "estimate": f(c["Mean"]), "se_or_ci": "SD of draws %.4f; MLE %.4f" % (f(c["SD"]), f(c["MLE"])), "p_value": f(c["pvalue"]),
  "same_direction_and_significance_as_paper": f(c["Mean"]) < 0 and f(c["pvalue"]) < 0.01, "source_file": "outputs/R_c_unweighted.csv", "note": "Others: " + others(rc)},
]
w1 = rd("check_06_w1.csv"); sc = rd("secondary_check.csv")
bugs = [{"file": "code/06_Estimate Open.R", "line": 199,
         "description": "Footnote 20 probit models mod_UK (lines 197-199) and mod_US (lines 201-203) pass weights as w=subset(data, ...)$w1, but the prepared data has no column w1 (01_Prepare data.R creates only w). $w1 is NULL, so both models are fitted unweighted, while the other models in 06 use weights=w.",
         "evidence": "outputs/check_06_w1.csv: w1_column_exists=%s; as-deposited fit equals unweighted fit: UK %s, US %s; equals w-weighted fit: UK %s, US %s; WHO coefficient as deposited %.3f (UK), %.3f (US) vs w-weighted %.3f, %.3f. Affects a footnote only, not any target. 06 itself was not run end to end; the check refits the two calls on the agent's prepared data." % (
            w1[0]["w1_column_exists"], w1[0]["as_deposited_equals_unweighted"], w1[1]["as_deposited_equals_unweighted"], w1[0]["as_deposited_equals_weighted_w"], w1[1]["as_deposited_equals_weighted_w"],
            f(w1[0]["coef_WHO_as_deposited"]), f(w1[1]["coef_WHO_as_deposited"]), f(w1[0]["coef_WHO_weighted_w"]), f(w1[1]["coef_WHO_weighted_w"]))}]
allA = all(t["match_to_rounding"] for t in out_t)
res = {"paper_id": "13_DX5T9G", "agent": "A", "run_date_ist": "2026-10-10", "ran": True,
 "could_not_run_reason": "Full 00_Run it all.R was OOM-killed in 03 (simulation arrays; 3.04 GB RSS at kill, about 2-3 GB available on the shared machine). Targets come from the pre-registered fallback (authors' 03 estimation lines unchanged, simulations skipped); 04, 06, 07, 08 not run.",
 "targets": out_t, "robustness": rob, "bugs": bugs,
 "env_fixes": ["diffs/00_Run_it_all.R.diff: registerDoMC cores 7 to 1 (memory; allowed by PREREG)",
               "diffs/03_Estimate_main_models_FALLBACK.diff: labelled deviation, pre-registered fallback after OOM kill; simulation blocks removed, estimation lines unchanged",
               "diffs/00_fallback_runner.diff: runner for 00 preliminaries + 01 + fallback 03 + 05",
               "packages: ebal 0.1-8 and logr 1.3.3 (authors' versions) via remotes::install_version; r-cran-readstata13 0.11.0 and r-cran-tmvtnorm 1.6 via apt; other packages Debian versions (environment.txt)"],
 "proposed_class": "A" if allA else "B",
 "class_reason": ("All six targets match the printed Table 2 and Table 3 values to two decimals (N exactly), with negative WHO coefficients and code p-values below .01, using the authors' estimation code unchanged via the pre-registered fallback. As-is outcome (labelled deviation): the full deposited pipeline could not finish on this 7 GB shared machine (OOM in 03), which on its own would be E; per PREREG the class is proposed from the fallback." if allA else "Not all targets match to rounding; see targets."),
 "confidence": "medium",
 "confidence_reason": "Exact match by script, but the full pipeline could not finish (memory) so the pre-registered fallback was used, and R/package versions differ from the authors'; B not yet compared.",
 "time_minutes": None,
 "uncertainties": [
   "Targets come from the fallback run, not from the full 03 script. The fallback keeps the authors' estimation and draw lines unchanged; equality with a full run is argued from the code (set.seed(1230) immediately before multinom and mvrnorm), not observed.",
   "Secondary context (not targets): %d of 20 WHO cells of the reproduced Tables 2 and 3 equal the PREREG secondary values to two decimals, %d carry ** (outputs/secondary_check.csv)." % (sum(1 for r in sc if r["check"] == "WHO cell" and r["match_2dp"] == "True"), sum(1 for r in sc if r["check"] == "WHO cell" and r["has_two_stars"] == "True")),
   "PREREG inconsistency 6: the reproduced UK table prints Gender (male) All neighbors as -0.47* and Ideology (left-right) All neighbors as 1.76**, and Health capacity Threatened neighbors as 0.60 with a dagger; PREREG records the printed paper as -0.47 and 1.76 without stars and 0.60 with *. Stars only; not a target; the agent did not re-read the paper PDF (outputs/secondary_check.csv).",
   "PREREG inconsistency 7 reproduced: US Ideology (don't know), Threatened neighbors prints -7.81** (0.00) in outputs/Table_3_table_main_US_1.tex (near-empty cell; not a target).",
   "R_a: UK bootstrap SEs (about 0.42 to 0.44) are much larger than the authors' parametric SDs (about 0.27 to 0.28); US bootstrap SEs about 0.27 to 0.28 vs 0.23 to 0.24. Weights were held fixed; conclusion unchanged (99% intervals exclude 0).",
   "Unverified observation (01_Prepare data.R lines 121, 127, 136, 162): the CCES commonweight and BES wt_demog are stored as w but not used; target rows are sampled uniformly (sample(1:nrow(t_tmp), 10000, replace=TRUE)), so the entropy-balancing targets are unweighted CCES/BES moments. Whether this is intended could not be determined.",
   "Unverified observation (01 lines 153-154): runif() for the dummy M is called before set.seed(1230); M is only the left-hand side for model.matrix and does not affect the weights.",
   "Unverified observation (01 lines 121-126): 419 CCES rows with missing ideo5 stay in t_data; model.matrix drops them when sampled, so the effective target sample is slightly below 10000 in the US. Not tested for impact.",
   "Code review scope: read fully 00, 01, 03, 05 and X_Auxiliary; 02 lines 1-60; 06 lines 1-60 and 180-220 (plus grep for weights); 04, 07, 08 not read. Bugs list has one item (06 w1); no bug found in the target path.",
   "Version drift: R 4.5.0 vs 4.2.2, nnet 7.3-20 vs 7.3-18, MASS 7.3-65 vs 7.3-58.1, readstata13 0.11.0 vs 0.10.0, aarch64 Linux reference BLAS vs x86_64 macOS build; ebal and logr at the authors' versions."]}
# time from LOG.md timestamps
log = open(os.path.join(P, "LOG.md")).read()
ts = re.findall(r"^- (\d\d):(\d\d) ", log, re.M)
if ts:
    mins = [int(h) * 60 + int(m) for h, m in ts]
    res["time_minutes"] = max(mins) - min(mins)
json.dump(res, open(os.path.join(P, "results.json"), "w"), indent=1)
print(json.dumps({k: res[k] for k in ("proposed_class", "time_minutes")}), [(t["id"], t["paper_value"], t["reproduced_value"], t["match_to_rounding"]) for t in out_t])
