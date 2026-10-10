#!/usr/bin/env python3
"""Builds results.json for 06_VSV5DM agent B from files in outputs/. Paper values copied from targets.json (PREREG)."""
import csv, json, re, os, math, html
B = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
O = os.path.join(B, "outputs")
P = os.path.dirname(B)
tj = {t["id"]: t for t in json.load(open(os.path.join(P, "targets.json")))}
rows = {r["level"]: r for r in csv.DictReader(open(os.path.join(O, "targets_extracted.csv")))}
f = lambda x: float(x)
src = "outputs/targets_extracted.csv"
spec = {
 "T1": (f(rows["Democratic White Women"]["AME"]), f(rows["Democratic White Women"]["AME_p"])),
 "T2": (f(rows["Democratic Men of Color"]["AME"]), f(rows["Democratic Men of Color"]["AME_p"])),
 "T3": (f(rows["Democratic Women of Color"]["AME"]), f(rows["Democratic Women of Color"]["AME_p"])),
 "T4": (f(rows["Democratic White Women"]["AME_p"]), None),
 "T5": (f(rows["Democratic White Women"]["coef"]), f(rows["Democratic White Women"]["coef_p"])),
 "T6": (f(rows["Democratic White Women"]["nobs"]), None),
}
def concl(tid, v, p):
    if tid == "T1": return v > 0 and 0.05 <= p < 0.10
    if tid in ("T2", "T3"): return v > 0 and p < 0.05
    if tid == "T4": return 0.05 <= v < 0.10
    if tid == "T5": return v > 0 and 0.05 <= p < 0.10
    if tid == "T6": return int(round(v)) == 635
coefp = f(rows["Democratic White Women"]["coef_p"])
notes = {
 "T1": "AME p (delta method, summary(margins)) = %.6f; CI [%.4f, %.4f]; paper A8 CI (-0.3 20.72)." % (spec["T1"][1], f(rows["Democratic White Women"]["AME_lower"]), f(rows["Democratic White Women"]["AME_upper"])),
 "T2": "AME p = %.6f; CI [%.4f, %.4f]; paper A8 CI (4.88 29.68)." % (spec["T2"][1], f(rows["Democratic Men of Color"]["AME_lower"]), f(rows["Democratic Men of Color"]["AME_upper"])),
 "T3": "AME p = %.6f; CI [%.4f, %.4f]; paper A8 CI (2.69 27.42)." % (spec["T3"][1], f(rows["Democratic Women of Color"]["AME_lower"]), f(rows["Democratic Women of Color"]["AME_upper"])),
 "T4": ("Pre-registered quantity is the AME p from summary(margins(...)): reproduced %.6f, which rounds to %.3f, not 0.054. "
        "The quasi-Poisson coefficient p for Democratic White Women from summary(covid) (t test, dispersion %.4f), printed by the authors' own code in outputs/multivariate_full_run.log, is %.6f, which rounds to %.3f and equals the paper's 0.054. "
        "Observation only: the paper's 'p = .054' matches the coefficient p, not the AME p; the paper's conclusion band (0.05 <= p < 0.10) holds for both.")
        % (spec["T4"][0], spec["T4"][0], f(rows["Democratic White Women"]["dispersion"]), coefp, coefp),
 "T5": "coef SE %.5f (paper 0.09), t-test p %.6f (one star in A10, legend *p<0.1)." % (f(rows["Democratic White Women"]["coef_SE"]), coefp),
 "T6": "643 rows in by_leg2; 8 dropped for missing age_rescaled (5) or Last.Vote.Share (3), see outputs/group_counts_check.txt.",
}
targets = []
for tid in ["T1","T2","T3","T4","T5","T6"]:
    t = tj[tid]; pv = t["paper_value"]; d = t["paper_rounding_decimals"]; v, p = spec[tid]
    ad = v - pv; rd = ad / pv
    targets.append({"id": tid, "description": t["description"], "paper_value": pv, "paper_rounding_decimals": d,
        "reproduced_value": v, "source_file": src, "abs_diff": ad, "rel_diff": rd,
        "match_to_rounding": round(v + 0.0, d) == pv if d > 0 else int(round(v)) == int(pv),
        "within_5pct": abs(rd) <= 0.05, "same_conclusion": concl(tid, v, p), "note": notes[tid]})
# cross-check against authors' own html outputs
a8 = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", open(os.path.join(O, "marginaleffects_table_white_men_gop.doc")).read()))
a10 = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html.unescape(open(os.path.join(O, "CountModel_WhiteGOPmen_reference_racegenderparty.doc")).read())))
xc = {"A8_DWW": re.search(r"Democratic White Women ([\-\d\.]+ \( [\-\d\.]+ [\-\d\.]+ \))", a8).group(1),
      "A8_DMOC": re.search(r"Democratic Men of Color ([\-\d\.]+ \( [\-\d\.]+ [\-\d\.]+ \))", a8).group(1),
      "A8_DWOC": re.search(r"Democratic Women of Color ([\-\d\.]+ \( [\-\d\.]+ [\-\d\.]+ \))", a8).group(1)}
m = re.search(r"Democratic White Women (\S+ \(\S+\) \**) ?(\S+ \(\S+\) \**)", a10); xc["A10_DWW_All_and_COVID"] = [m.group(1).strip(), m.group(2).strip()] if m else None
m = re.search(r"Num\. obs\. ((?:\d+ ){2})", a10); xc["A10_Num_obs_All_and_COVID"] = m.group(1).strip() if m else None
for t in targets: t["note"] += " Authors' html output cross-check: " + json.dumps(xc) if t["id"] == "T1" else ""
# robustness
def rd_csv(fn): return list(csv.DictReader(open(os.path.join(O, fn))))
dem3 = ["Democratic White Women","Democratic Men of Color","Democratic Women of Color"]
ra = {r["level"]: r for r in rd_csv("R_a_bootstrap_summary.csv")}
chk = rd_csv("R_a_direct_formula_check.csv")
rb = {r["level"]: r for r in rd_csv("R_b_outlier_exclusion.csv")}
rc = {r["level"]: r for r in rd_csv("R_c_negbin.csv")}
def pat(l, est, p, ci=None):
    if l == "Democratic White Women": return est > 0 and 0.05 <= p < 0.10
    return est > 0 and p < 0.05
def sec_a():
    s = []
    for l in ["Democratic Men of Color","Democratic White Women"]:
        r = ra[l]; e = f(r["original_AME"]); p = f(r["p_boot"])
        s.append("%s: AME %.4f, boot SE %.4f, 95%% pct CI [%.4f, %.4f], p_boot %.3f, matches paper pattern: %s" % (l, e, f(r["boot_SE"]), f(r["ci_lower"]), f(r["ci_upper"]), p, pat(l, e, p)))
    return "; ".join(s)
def sec(tab):
    s = []
    for l in ["Democratic Men of Color","Democratic White Women"]:
        r = tab[l]; e = f(r["AME"]); p = f(r["p"])
        s.append("%s: AME %.4f, SE %.4f, p %.4f, CI [%.4f, %.4f], matches paper pattern: %s" % (l, e, f(r["SE"]), p, f(r["lower"]), f(r["upper"]), pat(l, e, p)))
    return "; ".join(s)
woc = "Democratic Women of Color"
rob = []
r = ra[woc]
rob.append({"id": "R_a", "description": "Case bootstrap, set.seed(20261010), B=1000 resamples of the 635 model rows, quasi-Poisson refit, direct AME formula; primary estimate Democratic Women of Color AME", "ran": True,
  "estimate": f(r["original_AME"]), "se_or_ci": "boot SE %.4f; 95%% percentile CI [%.4f, %.4f]" % (f(r["boot_SE"]), f(r["ci_lower"]), f(r["ci_upper"])),
  "p_value": f(r["p_boot"]), "same_direction_and_significance_as_paper": (f(r["ci_lower"]) > 0 or f(r["ci_upper"]) < 0) and f(r["original_AME"]) > 0,
  "source_file": "outputs/R_a_bootstrap_summary.csv",
  "note": "Resamples dropped (level absent or NA coef): %s of 1000. Direct-formula check vs margins: max abs diff %.3g over 5 levels (outputs/R_a_direct_formula_check.csv). Secondary: %s. Draws in outputs/R_a_bootstrap_draws.csv." % (r["n_dropped"], max(f(c["abs_diff"]) for c in chk), sec_a())})
r = rb[woc]
rob.append({"id": "R_b", "description": "Drop rows with |z| > 3 on covid within the 635 model rows, refit identical quasi-Poisson, margins AME; primary Democratic Women of Color", "ran": True,
  "estimate": f(r["AME"]), "se_or_ci": "SE %.4f; 95%% CI [%.4f, %.4f]" % (f(r["SE"]), f(r["lower"]), f(r["upper"])), "p_value": f(r["p"]),
  "same_direction_and_significance_as_paper": f(r["AME"]) > 0 and f(r["p"]) < 0.05, "source_file": "outputs/R_b_outlier_exclusion.csv",
  "note": "Rows dropped: %s (covid > %.2f; values %s); groups: %s; n used %s. Secondary: %s." % (r["n_dropped"], f(r["z_cut_value"]), r["dropped_covid_values"], r["dropped_groups"], r["n_used"], sec(rb))})
r = rc[woc]
rob.append({"id": "R_c", "description": "Negative binomial (MASS::glm.nb) with identical formula on the 635 rows, margins AME; primary Democratic Women of Color", "ran": True,
  "estimate": f(r["AME"]), "se_or_ci": "SE %.4f; 95%% CI [%.4f, %.4f]" % (f(r["SE"]), f(r["lower"]), f(r["upper"])), "p_value": f(r["p"]),
  "same_direction_and_significance_as_paper": f(r["AME"]) > 0 and f(r["p"]) < 0.05, "source_file": "outputs/R_c_negbin.csv",
  "note": "theta %.4f (SE %.4f), converged %s, warnings: '%s'. Secondary: %s." % (f(r["theta"]), f(r["theta_SE"]), r["converged"], r["warnings"], sec(rc))})
allA = all(t["match_to_rounding"] for t in targets)
allB = all(t["within_5pct"] and t["same_conclusion"] for t in targets)
failing = [t["id"] for t in targets if not t["match_to_rounding"]]
res = {"paper_id": "06_VSV5DM", "agent": "B", "run_date_ist": "2026-10-10", "ran": True, "could_not_run_reason": "",
 "targets": targets, "robustness": rob,
 "bugs": [{"file": "Multivariate Analysis.Rmd", "line": 1095,
   "description": "Hard-coded sample-size labels in the detailed race and ethnicity chunk do not match the deposited data (labels only; the means in that table and all model estimates are unaffected). Line 1094 hard-codes freq c(335,102,42,52,48,46,19,4,2,1,1,1) and line 1095 labels 'Black Men (n=42)', 'Black Women (n=52)', 'Latino Men (n=48)', 'Latina Woman (n=46)', 'Asian Women (n=4)', 'Middle Eastern Men (n=1)'.",
   "evidence": "table(by_leg$race_gender) in outputs/group_counts_check.txt gives Black Man 44, Black Woman 50, Latino Man 47, Latina Woman 47, Asian American Woman 5, Middle Eastern Man 2 (White Woman 101, matching the label but not freq 102). race_gender is a factor whose level order equals the label order, so group_by rows align with labels; the labels appear in the authors' output outputs/meansbyraceandgenderandethnicity.doc. Not used by any target."}],
 "env_fixes": ["diffs/README.md: created the three output folders the code writes to (no authors' file edited)",
               "diffs/README.md: rtweet installed as Debian binary r-cran-rtweet 2.0.0, so library(rtweet) ran unchanged (no comment-out needed)"],
 "proposed_class": None, "class_reason": "", "confidence": "medium", "confidence_reason": "", "time_minutes": None,
 "uncertainties": []}
if allA: res["proposed_class"] = "A"
elif allB: res["proposed_class"] = "B"
else: res["proposed_class"] = "C"
res["class_reason"] = ("Strict reading: targets not matching to rounding: %s. T1, T2, T3, T5, T6 match the paper to rounding (and the authors' own A8/A10 html outputs reproduce the published cells), but T4 as pre-registered (AME p from summary(margins)) is %.4f vs the paper's 0.054 (rel diff %.1f%%, outside 5%%, same conclusion band), so neither A nor B applies and D does not apply (conclusion unchanged); the source of the text's p = .054 is unclear from the code, as it equals the coefficient p (%.4f), hence C. Alternative: A if T4 is read as the coefficient p." % (", ".join(failing) or "none", spec["T4"][0], 100 * targets[3]["rel_diff"], coefp))
res["confidence_reason"] = "All numbers matched by script and the full authors' pipeline ran without error, but the class turns on a judgement about which p-value the text's .054 reports; package versions are not pinned by the authors."
# time from LOG.md timestamps
log = open(os.path.join(B, "LOG.md")).read()
ts = re.findall(r"^- (\d\d):(\d\d)", log, re.M)
if ts:
    mins = [int(h) * 60 + int(m) for h, m in ts]; res["time_minutes"] = max(mins) - min(mins)
res["uncertainties"] = [
 "T4: the pre-registered AME p (0.0569) differs from the paper's .054 by more than 5% relative; the coefficient t-test p (0.0542) printed by the authors' code equals .054. Which quantity the text reports cannot be confirmed from the deposit; this drives the C vs A proposal.",
 "Package versions: none pinned by the authors; run used R 4.5.0, margins 0.3.28, prediction 0.3.18 (Debian), texreg 1.40 (see environment.txt). Exact agreement of A8 and A10 cells suggests drift is not material.",
 "R_a bootstrap and R_c negative binomial change the significance pattern for some groups (see robustness notes); robustness does not change the class.",
 "Time-Series Analysis.Rmd (glmer models, Table 1, A16 to A20) was not run; PREREG says it is not needed for any target.",
 "Sage supplementary ZIP was not checked by agent B (not needed; Dataverse deposit holds every file the code reads).",
 "R_a 'same_direction_and_significance_as_paper' for the primary estimate uses the PREREG rule: percentile 95% CI excludes 0."]
json.dump(res, open(os.path.join(B, "results.json"), "w"), indent=1)
print(json.dumps({k: res[k] for k in ["proposed_class","class_reason","time_minutes"]}, indent=1))
for t in targets: print(t["id"], t["paper_value"], t["reproduced_value"], t["match_to_rounding"], t["within_5pct"], t["same_conclusion"])
for r in rob: print(r["id"], r["estimate"], r["p_value"], r["same_direction_and_significance_as_paper"])
print(xc)
