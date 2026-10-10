#!/usr/bin/env python3
"""Build results.json for 06_VSV5DM agent A from files in outputs/ and the frozen targets.json. No hand-typed estimates."""
import csv, json, math, os, re, datetime
HERE = os.path.dirname(os.path.abspath(__file__)); A = os.path.dirname(HERE); P = os.path.dirname(A)
OUT = os.path.join(A, "outputs")
targets = {t["id"]: t for t in json.load(open(os.path.join(P, "targets.json")))}
rows = list(csv.DictReader(open(os.path.join(OUT, "targets_extracted.csv"))))
def get(q, term):
    for r in rows:
        if r["quantity"] == q and r["term"] == term: return r
    raise KeyError((q, term))
def f(x): return None if x in ("", "NA", None) else float(x)
def rnd(x, d):  # round half away from zero, as in the paper's tables
    return math.floor(abs(x) * 10**d + 0.5) / 10**d * (1 if x >= 0 else -1)

spec = {
 "T1": ("AME", "rpgDemocratic White Women", "estimate"),
 "T2": ("AME", "rpgDemocratic Men of Color", "estimate"),
 "T3": ("AME", "rpgDemocratic Women of Color", "estimate"),
 "T4": ("AME", "rpgDemocratic White Women", "p"),
 "T5": ("coef", "rpgDemocratic White Women", "estimate"),
 "T6": ("nobs", "covid", "estimate"),
}
def conclusion(tid):
    if tid == "T1":
        r = get("AME", "rpgDemocratic White Women"); return f(r["estimate"]) > 0 and 0.05 <= f(r["p"]) < 0.10
    if tid in ("T2", "T3"):
        r = get(*spec[tid][:2]); return f(r["estimate"]) > 0 and f(r["p"]) < 0.05
    if tid == "T4":
        p = f(get("AME", "rpgDemocratic White Women")["p"]); return 0.05 <= p < 0.10
    if tid == "T5":
        r = get("coef", "rpgDemocratic White Women"); return f(r["estimate"]) > 0 and 0.05 <= f(r["p"]) < 0.10
    if tid == "T6":
        return f(get("nobs", "covid")["estimate"]) == targets["T6"]["paper_value"]
tout = []
for tid in ["T1", "T2", "T3", "T4", "T5", "T6"]:
    t = targets[tid]; q, term, col = spec[tid]
    r = get(q, term); v = f(r[col]); pv = t["paper_value"]; d = t["paper_rounding_decimals"]
    ad = v - pv; rd = ad / pv
    note = f"p = {f(r['p']):.4f}" if r["p"] not in ("", "NA") else ""
    if tid == "T4":
        cp = f(get("coef", "rpgDemocratic White Women")["p"])
        note = (f"Delta-method AME p from summary(margins()) as pre-registered = {v:.6f} (rounds to {rnd(v,3)}). "
                f"The quasi-Poisson coefficient p for the same group from summary(covid) = {cp:.6f} (rounds to {rnd(cp,3)}), which equals the paper's .054 to rounding. "
                "The pre-registered quantity does not match; the coefficient p does. Which of the two the text reports is not stated in the paper.")
    if tid in ("T1", "T2", "T3"):
        note += f"; delta-method 95% CI [{f(r['lower']):.4f}, {f(r['upper']):.4f}] (Table A8 prints the CI rounded to 2 dp)"
    if tid == "T5":
        note += f"; SE {f(r['se']):.4f} (A10: 0.09); one star (p < 0.1) as in A10"
    tout.append({"id": tid, "description": t["description"], "paper_value": pv, "paper_rounding_decimals": d,
                 "reproduced_value": v, "source_file": "outputs/targets_extracted.csv",
                 "abs_diff": ad, "rel_diff": rd, "match_to_rounding": rnd(v, d) == pv,
                 "within_5pct": abs(rd) <= 0.05, "same_conclusion": conclusion(tid), "note": note.strip("; ")})

def readcsv(n): return list(csv.DictReader(open(os.path.join(OUT, n))))
def pick(rs, g): return [r for r in rs if r["group"] == g][0]
rob = []
# R_a
ra = readcsv("R_a_bootstrap.csv"); chk = readcsv("R_a_direct_formula_check.csv")
chk_ok = all(r["within_1e6"] == "TRUE" for r in chk)
w = pick(ra, "Democratic Women of Color"); lo, hi = f(w["lower"]), f(w["upper"])
def sec_ra(g, sig_rule):
    r = pick(ra, g); l, h, p = f(r["lower"]), f(r["upper"]), f(r["p"])
    return f"{g}: AME {f(r['AME']):.3f}, percentile CI [{l:.3f}, {h:.3f}], boot p {p:.3f}, matches paper pattern: {sig_rule(f(r['AME']), p, l, h)}"
rob.append({"id": "R_a", "description": "Case bootstrap, set.seed(20261010), B = 1000 resamples of the 635 model rows, refit quasi-Poisson, direct AME; percentile 95% CI", "ran": True,
    "estimate": f(w["AME"]), "se_or_ci": f"percentile 95% CI [{lo:.4f}, {hi:.4f}]; bootstrap SE {f(w['boot_se']):.4f}",
    "p_value": f(w["p"]), "same_direction_and_significance_as_paper": f(w["AME"]) > 0 and lo > 0,
    "source_file": "outputs/R_a_bootstrap.csv",
    "note": (f"Primary: Democratic Women of Color. Resamples used {w['B_used']} of {w['B_requested']}, dropped {w['dropped']}. Direct AME formula equals margins AME within 1e-6 for all five levels: {chk_ok} (outputs/R_a_direct_formula_check.csv). Secondary: "
             + sec_ra("Democratic Men of Color", lambda a, p, l, h: a > 0 and l > 0) + "; "
             + sec_ra("Democratic White Women", lambda a, p, l, h: a > 0 and 0.05 <= p < 0.10))})
# R_b and R_c
for rid, fn, desc in [("R_b", "R_b_outlier_exclusion.csv", "Drop rows with |z| > 3 on covid within the 635 model rows, refit quasi-Poisson, margins AMEs"),
                      ("R_c", "R_c_negbin.csv", "MASS::glm.nb with the identical formula on the 635 rows, margins AMEs")]:
    rs = readcsv(fn); w = pick(rs, "Democratic Women of Color")
    sec = []
    for g, rule in [("Democratic Men of Color", lambda a, p: a > 0 and p < 0.05), ("Democratic White Women", lambda a, p: a > 0 and 0.05 <= p < 0.10)]:
        r = pick(rs, g)
        sec.append(f"{g}: AME {f(r['AME']):.3f}, SE {f(r['SE']):.3f}, p {f(r['p']):.4f}, matches paper pattern: {rule(f(r['AME']), f(r['p']))}")
    extra = (f"n used {w['n_used']}, dropped {w['n_dropped']} ({w['dropped_groups']})" if rid == "R_b"
             else f"theta {f(w['theta']):.4f}, converged {w['converged']}, warnings: '{w['warnings']}'")
    rob.append({"id": rid, "description": desc, "ran": True, "estimate": f(w["AME"]),
        "se_or_ci": f"delta-method SE {f(w['SE']):.4f}; 95% CI [{f(w['lower']):.4f}, {f(w['upper']):.4f}]",
        "p_value": f(w["p"]), "same_direction_and_significance_as_paper": f(w["AME"]) > 0 and f(w["p"]) < 0.05,
        "source_file": "outputs/" + fn, "note": f"Primary: Democratic Women of Color. {extra}. Secondary: " + "; ".join(sec)})

allA = all(t["match_to_rounding"] for t in tout)
allB = all(t["within_5pct"] and t["same_conclusion"] for t in tout)
if allA: cls, reason = "A", "All six targets match the paper to its reported rounding."
elif allB: cls, reason = "B", "All targets within 5% with the same conclusion."
else:
    bad = [t["id"] for t in tout if not t["match_to_rounding"]]
    cls = "C"
    reason = ("T1, T2, T3, T5, T6 match the paper exactly to rounding and the authors' own Table A8/A10 outputs reproduce the printed cells, but T4 (" + ", ".join(bad) +
              ") as pre-registered (delta-method AME p) is 0.057 vs the paper's .054 (5.4% relative, outside 5%), so neither A nor B holds by rule; the conclusion is unchanged (still 0.05 <= p < 0.10), so not D. "
              "The paper's .054 equals the quasi-Poisson coefficient p (0.0542) that the same code prints in summary(covid); which number the text reports is unclear, hence C. Alternative class if T4 is read as the coefficient p: A.")
LOG = open(os.path.join(A, "LOG.md")).read()
ts = re.findall(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}) IST", LOG)
fmt = "%Y-%m-%d %H:%M"
mins = int((datetime.datetime.strptime(ts[-1], fmt) - datetime.datetime.strptime(ts[0], fmt)).total_seconds() // 60) if len(ts) > 1 else None
res = {"paper_id": "06_VSV5DM", "agent": "A", "run_date_ist": "2026-10-10", "ran": True, "could_not_run_reason": "",
 "targets": tout, "robustness": rob, "bugs": [],
 "env_fixes": ["diffs/00_output_dirs.diff: created the three output folders the code writes into (not in deposit; README says runner creates them)",
               "diffs/README.md: margins 0.3.28, texreg 1.40, betareg 3.2.6, eeptools 1.3.0 installed from CRAN into a clean per-run library; rtweet 2.0.0 available as a Debian binary so library(rtweet) was not commented out; no file of the authors edited"],
 "proposed_class": cls, "class_reason": reason,
 "confidence": "medium",
 "confidence_reason": "Every number is parsed from script output and the authors' A8/A10 html files match the paper, but the class turns on a judgement about which p-value the text's .054 refers to; B has not been compared.",
 "time_minutes": mins,
 "uncertainties": [
  "T4: the paper's 'p = .054' equals the coefficient p in summary(covid) (0.0542), not the delta-method AME p in summary(margins) (0.0569) that PREREG maps T4 to. The class depends on this mapping (C as pre-registered; A if the coefficient p is meant).",
  "No R or package versions are given by the authors; run used R 4.5 on aarch64 with margins 0.3.28 / prediction 0.3.18. All other targets match to rounding, so version drift is not visible here.",
  "Code review covered Multivariate Analysis.Rmd lines 1-140 and 470-720 line by line, the coefficient-name mapping of the htmlreg call (checked against names(coef(covid)), outputs/extract_targets.log) and the hard-coded group sizes at purled lines 48/147 (match the data, outputs/group_size_check.txt). Remaining lines were run (full run, 0 errors, outputs/multivariate_full_run.log) but not read line by line. Time-Series Analysis.Rmd was not run (not needed for any target).",
  "Unverified observation (from PREREG, not checked by a run): the article says expected counts hold covariates at means; margins() computes average marginal effects over observed rows. The reported numbers equal the margins output, so this is a wording point only.",
  "Unverified observation: Tables A14/A15 titled 'Fractional Logit' are produced by betareg on proportions + 0.00001; not a target, not checked.",
  "Unverified observation: purled line 1051 hard-codes White Women freq 102 in the detailed-race table while other chunks use 101; not checked against data.",
  "643 rows in by_leg2 become 635 in the model because 5 rows lack age_rescaled and 3 lack Last.Vote.Share (outputs/group_size_check.txt); the paper does not state this.",
  "Robustness: the Democratic Women of Color and Democratic White Women results are sensitive (R_a and R_b move DWOC to p about 0.06; R_b makes DWW p 0.035; R_c negative binomial gives no group significant). Robustness does not change the class."]}
json.dump(res, open(os.path.join(A, "results.json"), "w"), indent=1)
print(json.dumps({k: res[k] for k in ["proposed_class", "time_minutes"]}))
for t in tout: print(t["id"], t["paper_value"], t["reproduced_value"], t["match_to_rounding"], t["within_5pct"], t["same_conclusion"])
for r in rob: print(r["id"], r["estimate"], r["p_value"], r["same_direction_and_significance_as_paper"])
