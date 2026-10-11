"""Builds results.json for 22_W2TSVL agent A from files in outputs/. No numbers typed here except paper values read from targets.json."""
import csv, json, os, re, datetime
A = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(A, "outputs")
targets = json.load(open(os.path.join(A, "..", "targets.json")))
ext = {r["id"]: r for r in csv.DictReader(open(os.path.join(OUT, "targets_extracted.csv")))}
rob = json.load(open(os.path.join(OUT, "robustness.json")))
sup = json.load(open(os.path.join(OUT, "supplement_target_check.json")))
xc = list(csv.DictReader(open(os.path.join(OUT, "crosscheck_main_vs_appendix.csv"))))
obs = json.load(open(os.path.join(OUT, "code_observations_check.json")))

# pre-registered conclusion buckets (PREREG section 1)
bucket = {"T1": (lambda b, p: b < 0 and 0.01 <= p < 0.05), "T2": (lambda b, p: b > 0 and p < 0.01),
          "T3": (lambda b, p: b > 0 and p >= 0.10), "T4": (lambda b, p: b < 0 and p < 0.01)}
tlist = []
for t in targets:
    r = ext[t["id"]]; v = float(r["value"]); pv = t["paper_value"]; d = t["paper_rounding_decimals"]
    ad = abs(v - pv); rd = ad / abs(pv)
    if t["id"] in bucket:
        p = float(r["p_wald"]); same = bucket[t["id"]](v, p)
        note = (f"SE {float(r['se']):.4f}, Wald z {float(r['z']):.4f}, two-sided Wald p {p:.4g} (pre-registered); "
                f"secondary LR p {float(r['p_lr_secondary']):.4g}. Main-script polr fit gives the same coefficient (crosscheck_main_vs_appendix.csv).")
    else:
        same = abs(v - pv) <= 5
        note = f"nobs() = {int(v)}; m$n = {int(float(r['n_slot']))}."
    note += f" Cell re-checked in publisher supplement PDF: {sup[t['id']]['read']} (agrees with targets.json: {sup[t['id']]['agrees']})."
    tlist.append({"id": t["id"], "description": t["description"], "paper_value": pv, "paper_rounding_decimals": d,
                  "reproduced_value": v, "source_file": "outputs/targets_extracted.csv",
                  "abs_diff": ad, "rel_diff": rd, "match_to_rounding": round(v, d) == round(pv, d),
                  "within_5pct": rd <= 0.05, "same_conclusion": same, "note": note})

ra, rb, rc = rob["R_a"], rob["R_b"], rob["R_c"]
robl = [
 {"id": "R_a", "description": "Case bootstrap, set.seed(20261011), 1000 resamples, refit m1 (then m7); percentile CIs, two-sided bootstrap p",
  "ran": True, "estimate": ra["T1"]["estimate"],
  "se_or_ci": f"boot SE {ra['T1']['boot_se']:.4f}; 95% CI [{ra['T1']['ci95'][0]:.4f}, {ra['T1']['ci95'][1]:.4f}]; 99% CI [{ra['T1']['ci99'][0]:.4f}, {ra['T1']['ci99'][1]:.4f}]",
  "p_value": ra["T1"]["p_boot"], "same_direction_and_significance_as_paper": ra["T1"]["same"],
  "source_file": "outputs/robustness.json",
  "note": (f"T1: {ra['T1']['n_failed']} failed fits of {ra['T1']['n_resamples']}. Secondary T2 (m7 pro_strike): estimate {ra['T2']['estimate']:.4f}, boot SE {ra['T2']['boot_se']:.4f}, "
           f"95% CI [{ra['T2']['ci95'][0]:.4f}, {ra['T2']['ci95'][1]:.4f}], 99% CI [{ra['T2']['ci99'][0]:.4f}, {ra['T2']['ci99'][1]:.4f}], boot p {ra['T2']['p_boot']}, "
           f"{ra['T2']['n_failed']} failed; pre-registered T2 criterion (99% CI excludes 0) met: {ra['T2']['same']}. Draws: outputs/bootstrap_*_draws.csv.")},
 {"id": "R_b", "description": "Drop rows with |z(age d2)| > 3 over all 1011 rows, refit m1 and m7, Wald SE and p",
  "ran": True, "estimate": rb["T1"]["estimate"], "se_or_ci": f"Wald SE {rb['T1']['se']:.4f}", "p_value": rb["T1"]["p"],
  "same_direction_and_significance_as_paper": rb["T1"]["same"], "source_file": "outputs/robustness.json",
  "note": (f"{rb['rows_dropped_total']} rows dropped (max |z| {rb['max_abs_z']:.3f}); T1 N {rb['T1']['nobs']}. Secondary T2: estimate {rb['T2']['estimate']:.4f}, SE {rb['T2']['se']:.4f}, "
           f"p {rb['T2']['p']:.4g}, N {rb['T2']['nobs']}; T2 criterion (p < 0.01, positive) met: {rb['T2']['same']}.")},
 {"id": "R_c", "description": "OLS of outcome on treatment dummies (m1 and m7 rows), HC2 robust SEs",
  "ran": True, "estimate": rc["T1"]["estimate"], "se_or_ci": f"HC2 SE {rc['T1']['se_hc2']:.4f}", "p_value": rc["T1"]["p"],
  "same_direction_and_significance_as_paper": rc["T1"]["same"], "source_file": "outputs/robustness.json",
  "note": (f"Outcome units (1 to 5 scale), N {rc['T1']['nobs']}. Secondary T2 (1 to 7 scale): estimate {rc['T2']['estimate']:.4f}, HC2 SE {rc['T2']['se_hc2']:.4f}, "
           f"p {rc['T2']['p']:.4g}, N {rc['T2']['nobs']}; T2 criterion (p < 0.01, positive) met: {rc['T2']['same']}.")},
]

maxdiff = max(float(r["abs_diff"]) for r in xc)
all_exact = all(t["match_to_rounding"] for t in tlist)
all_5 = all(t["within_5pct"] and t["same_conclusion"] for t in tlist)
cls = "A" if all_exact else ("B" if all_5 else "C")

log = open(os.path.join(A, "LOG.md")).read()
stamps = re.findall(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}) IST", log)
fmt = "%Y-%m-%d %H:%M"
mins = round((datetime.datetime.strptime(stamps[-1], fmt) - datetime.datetime.strptime(stamps[0], fmt)).total_seconds() / 60)

res = {
 "paper_id": "22_W2TSVL", "agent": "A", "run_date_ist": stamps[0][:10], "ran": True, "could_not_run_reason": "",
 "targets": tlist, "robustness": robl,
 "bugs": [],
 "code_observations": [
  {"file": "Framing Labor Action_Appendix A1.R", "line": 110, "type": "verified observation, no target affected",
   "description": "Education recode maps d3 codes 1-12 only; code 13 ('No tiene estudios', no schooling) becomes NA instead of 'basica', together with code 14 (NS/NC).",
   "evidence": f"outputs/code_observations_check.json: d3 == 13 for {obs['d3_eq_13_n']} rows, all NA in education_levels ({obs['education_NA_among_d3_13']}); education_levels NA total {obs['education_levels_NA_n']}. Affects only the control-variable models (m3, m6, m9, m12) and the balance tables, not T1 to T6. Could be a deliberate choice; not judged."},
  {"file": "Framing Labor Action_Appendix A1.R", "line": 224, "type": "verified observation, no target affected",
   "description": "Table A4 group means of `unions` are computed on an ordered factor, so mean() returns NA with a warning; the table values are typed as constants at line 234.",
   "evidence": "outputs/appendix_stdout.txt warning 'argument is not numeric or logical: returning NA'; outputs/code_observations_check.json shows the numeric group means round to the typed constants (and the support means at line 264 also match to 2 decimals)."},
  {"file": "Framing Labor Action_R script.R", "line": 212, "type": "unverified observation",
   "description": "aes(estimate, term, color) passes an undefined `color` positionally; with ggplot2 3.5.1 the script ran to the end without error and drew 4 pages (outputs/main_script_figures.pdf). Not inspected further; figures only."}
 ],
 "code_review_scope": "Read both deposited R scripts in full (Appendix A1.R 319 lines, R script.R 266 lines). No bug found that affects the targets.",
 "env_fixes": ["diffs/appendix_A1_R.diff: absolute Windows data path at line 14 replaced by the relative file name; install.packages() lines 4-6, 138, 282 commented out",
               "diffs/main_R_script.diff: absolute Windows data path at line 14 replaced by the relative file name; install.packages() lines 4-8 commented out",
               "scripts/run_appendix.R: browseURL defined as a no-op before source() (no edit to the authors' file)",
               "stargazer 5.2.3, tableone 0.13.2, gmodels 2.19.1 installed from CRAN source into the per-run library (no Debian binaries for stargazer/tableone)"],
 "cross_checks": {"main_script_vs_appendix_max_abs_coef_diff": maxdiff, "source_file": "outputs/crosscheck_main_vs_appendix.csv",
                  "supplement_cells_agree_with_targets_json": sup["all_agree"], "supplement_source_file": "outputs/supplement_target_check.json"},
 "proposed_class": cls,
 "class_reason": ("All six targets reproduced exactly to the printed rounding by the authors' own Appendix A1 script with path/install/browseURL fixes only, with the same sign and pre-registered Wald-p star bucket; the main script's figure models give identical coefficients."
                  if cls == "A" else "See targets."),
 "confidence": "high",
 "confidence_reason": "Exact match by script, deterministic code with no randomness, and only path-type fixes; pending agent B.",
 "time_minutes": mins,
 "uncertainties": [
  "Run on R 4.5.0 aarch64 Debian with MASS 7.3.65 versus the authors' R 4.4.2 on Windows; coefficients agree to all printed digits, so this did not matter here.",
  "R_a secondary T2: the pre-registered 99% percentile CI for the pro-strike effect on strike support includes 0 by a small margin (see robustness note), although the 95% CI excludes 0; T1 criterion is met.",
  "R_c secondary T2: OLS with HC2 gives p about 0.02 for the pro-strike effect, above the paper's printed 0.01 threshold for the ordered logit; sign agrees. T1 criterion met.",
  "Batch brief mentions 'path line 15' for paper 22; the read_dta call with the absolute path is on line 14 of both scripts (line 15 of the main script is the authors' commented relative-path alternative). Line 14 was edited, which is what PREREG.md describes.",
  "Weighted-model Ns (975, 962 in Tables A1/A2 col 2) were reproduced in the stargazer output (outputs/table_1A_new.htm, table_A2_new.htm) but why they differ from the unweighted Ns was not investigated; not a target."
 ]
}
json.dump(res, open(os.path.join(A, "results.json"), "w"), indent=1)
print(json.dumps({k: res[k] for k in ["proposed_class", "time_minutes"]}), [(t["id"], t["paper_value"], t["reproduced_value"], t["match_to_rounding"], t["same_conclusion"]) for t in tlist])
