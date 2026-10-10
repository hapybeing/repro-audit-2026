#!/usr/bin/env python3
"""Build results.json for 15_1BBC4E agent B from files in outputs/. Paper values are copied from targets.json (PREREG)."""
import csv, json, math, re, os
B = "/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/15_1BBC4E/B"
P = os.path.dirname(B)
o = lambda f: os.path.join(B, "outputs", f)
tg = {t["id"]: t for t in json.load(open(os.path.join(P, "targets.json")))}
ex = {r["id"]: r for r in csv.DictReader(open(o("targets_extracted.csv")))}
val = lambda k: float(ex[k]["value"])
rob = json.load(open(o("robustness.json")))
N = val("T4_candidate2")
max21, maxpair = val("max21"), ex["max21"]["note"]
concl = {
 "T1": lambda v: 0 < v < 0.73 and (maxpair.endswith(("AoW-ARD", "ARD-AoW")) or max21 < 0.73),
 "T2": lambda v: 0 < v < 0.73, "T3": lambda v: 0 < v < 0.73,
 "T4": lambda v: abs(v - 6067) / 6067 <= 0.05,
 "T5": lambda v: v < 0.05 * N,
 "T6": lambda v: abs(v - 3093) / 3093 <= 0.05,
}
targets = []
for k in ["T1", "T2", "T3", "T4", "T5", "T6"]:
    pv, d = tg[k]["paper_value"], tg[k]["paper_rounding_decimals"]
    rv = val(k); ad = rv - pv; rd = ad / pv
    note = ex[k]["note"]
    if k == "T4": note += f"; candidate 2 (sum of ead2 tally, Agreement across all.R) = {int(N)}"
    if k == "T1": note += f"; largest of 21 pairs: {maxpair} = {max21}"
    targets.append({"id": k, "description": tg[k]["description"], "paper_value": pv, "paper_rounding_decimals": d,
        "reproduced_value": rv, "source_file": "outputs/" + ex[k]["source"], "abs_diff": ad, "rel_diff": rd,
        "match_to_rounding": round(rv, d) == pv, "within_5pct": abs(rd) <= 0.05,
        "same_conclusion": bool(concl[k](rv)), "note": note})
def sig(est, lo, hi): return bool(est > 0 and lo > 0 and est < 0.73)
ra, rb, rc = rob["R_a"], rob["R_b"], rob["R_c"]
robustness = [
 {"id": "R_a", "description": "Country-cluster bootstrap (Final_Code), 1000 resamples, set.seed(20261010), pairwise-complete Pearson; T1 percentile 95% CI", "ran": True,
  "estimate": ra["estimate"], "se_or_ci": f"95% percentile CI [{ra['ci_low']:.4f}, {ra['ci_high']:.4f}]; bootstrap SE {ra['boot_se']:.4f}; share of resamples with T1 >= 0.73: {ra['share_ge_073']}; undefined resamples: {ra['n_undefined']}",
  "p_value": ra["p_value"], "same_direction_and_significance_as_paper": sig(ra["estimate"], ra["ci_low"], ra["ci_high"]), "source_file": "outputs/robustness.json",
  "note": f"Secondary 95% CIs: T2 {ra['secondary_ci']['T2']}, T3 {ra['secondary_ci']['T3']}, max of 21 {ra['secondary_ci']['max21']}. {ra['n_countries']} countries resampled; 123 rows with missing Final_Code have only RoW values and enter no correlation. p is the pre-registered min(2 x share of T1 <= 0, 1)."},
 {"id": "R_b", "description": "Leave-one-country-out influence on T1; drop top 1% of eligible countries (ceiling, at least 1); recompute 7x7 matrix; cor.test for T1", "ran": True,
  "estimate": rb["estimate"], "se_or_ci": f"cor.test 95% CI [{rb['ci_low']:.4f}, {rb['ci_high']:.4f}]", "p_value": rb["p_value"],
  "same_direction_and_significance_as_paper": sig(rb["estimate"], rb["ci_low"], rb["ci_high"]), "source_file": "outputs/robustness.json",
  "note": f"{rb['n_dropped']} of {rb['n_eligible_countries']} countries dropped: Final_Code {', '.join(rb['dropped'])} (outputs/R_b_dropped_country_names.txt), {rb['dropped_country_years']} rows; T1 pairs {rb['n_pairs']}. Secondary: T2 {rb['secondary']['T2']:.4f}, T3 {rb['secondary']['T3']:.4f}, largest pair {rb['secondary']['max_pair']} {rb['secondary']['max21']:.4f}, median {rb['secondary']['median21']:.4f}. p-value 0 means below double precision."},
 {"id": "R_c", "description": "Listwise common sample (all seven PDA dummies non-missing) instead of pairwise complete observations; cor.test for T1", "ran": True,
  "estimate": rc["estimate"], "se_or_ci": f"cor.test 95% CI [{rc['ci_low']:.4f}, {rc['ci_high']:.4f}]", "p_value": rc["p_value"],
  "same_direction_and_significance_as_paper": sig(rc["estimate"], rc["ci_low"], rc["ci_high"]), "source_file": "outputs/robustness.json",
  "note": f"N {rc['N']}. Secondary: T2 {rc['secondary']['T2']:.4f}, T3 {rc['secondary']['T3']:.4f}, largest pair {rc['secondary']['max_pair']} {rc['secondary']['max21']:.4f} (ARD-AoW is no longer the largest pair, but the largest stays below 0.73), median {rc['secondary']['median21']:.4f}. p-value 0 means below double precision."},
]
loc = list(csv.DictReader(open(o("factor_label_locale_check.csv"))))
loc_txt = "; ".join(f"{r['locale']} line {r['line']}: {r['all_correct']}" for r in loc if r["line"] != "NA")
tab3 = list(csv.DictReader(open(o("table3_full_comparison.csv"))))
n3 = sum(r["match_3dp"] == "TRUE" for r in tab3)
log = open(os.path.join(B, "LOG.md")).read()
def hm(tag):
    m = re.search(tag + r": \S+ (\d\d):(\d\d) IST", log); return int(m.group(1)) * 60 + int(m.group(2))
allA = all(t["match_to_rounding"] for t in targets)
res = {"paper_id": "15_1BBC4E", "agent": "B", "run_date_ist": "2026-10-10", "ran": True, "could_not_run_reason": "",
 "targets": targets, "robustness": robustness, "bugs": [],
 "code_observations_unverified": [{"file": "Scripts/Comparing Indices/Comparison.R", "lines": [105, 176, 183],
   "description": "Exploratory, not pre-registered, figures only (Figures 1 and 4). Factor levels are relabelled by position after as.factor(), so the label-to-variable mapping depends on the collation locale. Not a target and not a bug in this run.",
   "evidence": f"outputs/factor_label_locale_check.csv: {loc_txt}. Author comment at line 104 notes the level order sometimes switched."}],
 "env_fixes": ["No diff: corrr 0.4.5 and pacman 0.5.1 installed from CRAN source into the per-run library (no Debian binary). No author file changed (diffs/README.md)."],
 "proposed_class": "A" if allA else "B",
 "class_reason": f"All six targets reproduce exactly at the paper's printed precision from the unmodified deposited scripts and data (and {n3} of 21 Table 3 cells match to 3 decimals)." if allA else "Not all targets match to rounding.",
 "confidence": "high", "confidence_reason": "Deterministic correlations and counts on the deposited file, scripts run unmodified, every deposited file matches the PREREG sha256; agreement with agent A not yet checked by compare_ab.py.",
 "time_minutes": hm("End") - hm("Start"),
 "secondary": {"table3_cells_match_3dp": n3, "table3_cells": len(tab3), "median21": val("median21"), "mean21": val("mean21"), "source_file": "outputs/table3_full_comparison.csv; outputs/targets_extracted.csv"},
 "uncertainties": [
   "The Dataverse API on 2026-10-10 reports versionNumber 1, versionMinorNumber 1 (PREREG.md says version 1.0). All 49 files are byte-identical to the PREREG sha256 list, so this does not affect the run.",
   "T1 matches Table 3 (0.636); the prose says '.63' (PREREG inconsistency note). Median 0.398 reproduces the computed median of the printed table; the prose '.39' looks truncated (not a target).",
   "Robustness p-values of 0 from cor.test are below double precision, not exactly zero. The R_a p-value is the pre-registered bootstrap proportion (no resample had T1 <= 0).",
   "In R_c the largest pair is LIED-AoW, not ARD-AoW; still below 0.73.",
   "Appendix and data-preparation scripts were not run (PREREG: merged data used as deposited)."]}
json.dump(res, open(os.path.join(B, "results.json"), "w"), indent=1)
print(json.dumps({t["id"]: [t["paper_value"], t["reproduced_value"], t["match_to_rounding"]] for t in targets}), res["proposed_class"], res["time_minutes"])
