"""Builds results.json from files in outputs/ (agent B, paper 24_U9CKK6). No hand-typed reproduced numbers."""
import csv, json, os, datetime, math
B = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); O = os.path.join(B, "outputs")
tj = {t["id"]: t for t in json.load(open(os.path.join(B, "..", "targets.json")))}
rows = {r["id"]: r for r in csv.DictReader(open(os.path.join(O, "targets_extracted.csv")))}
pdf = json.load(open(os.path.join(O, "pdf_cell_check.json")))
def f(x):
    try: v = float(x); return None if math.isnan(v) else v
    except Exception: return None
def bucket(p):
    return None if p is None else ("***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else "n.s.")
want = {"T1": "***", "T2": "***", "T3": "***", "T5": "**", "T6": "*"}
targets = []
for tid in ["T1", "T2", "T3", "T4", "T5", "T6"]:
    t, r = tj[tid], rows[tid]; pv = t["paper_value"]; dec = t["paper_rounding_decimals"]
    est = f(r["estimate"]); p = f(r["p_naive"]); se = f(r["se"])
    ad = None if est is None else est - pv; rd = None if est is None else (est - pv) / pv
    mtr = None if est is None else round(est, dec) == pv
    if tid == "T4":
        sc = None if est is None else abs(est - 266854) <= 5; note = f"nobs; groups MEP {r['n_mep']}, party {r['n_party']}"
    else:
        sc = None if est is None else (est > 0 and bucket(p) == want[tid])
        note = (f"SE {se:.5f} (rounds to {round(se, 2):.2f}); naive normal p {p:.3g} (texreg default, pre-registered) = star bucket {bucket(p)}, paper {want[tid]}; "
                f"model {r['model']}, nobs {r['nobs']}; lme4 convergence messages: {r['conv_messages']}")
    targets.append({"id": tid, "description": t["description"], "paper_value": pv, "paper_rounding_decimals": dec,
        "reproduced_value": est, "source_file": "outputs/targets_extracted.csv", "abs_diff": ad, "rel_diff": rd,
        "match_to_rounding": mtr, "within_5pct": None if rd is None else abs(rd) <= 0.05, "same_conclusion": sc, "note": note})
def rcsv(name):
    p = os.path.join(O, name); return list(csv.DictReader(open(p))) if os.path.exists(p) else None
rob = []
rc = rcsv("R_c_factor_year.csv")
if rc:
    x = rc[0]; e, p = f(x["estimate"]), f(x["p_naive"])
    rob.append({"id": "R_c", "description": "Refit cycle_AE_fit2 with as.factor(year) instead of linear year; T1 coefficient", "ran": True,
        "estimate": e, "se_or_ci": f"SE {f(x['se']):.5f}", "p_value": p, "same_direction_and_significance_as_paper": e > 0 and p < 0.001,
        "source_file": "outputs/R_c_factor_year.csv", "note": f"nobs {x['nobs']}; convergence: {x['conv']}"})
rb = rcsv("R_b_outliers_T1.csv"); rbs = rcsv("R_b_outliers_T5_T6.csv")
if rb:
    x = rb[0]; e, p = f(x["estimate"]), f(x["p_naive"]); sec = []
    for y in (rbs or []):
        ye, yp = f(y["estimate"]), f(y["p_naive"]); lo, hi = (0.001, 0.01) if y["target"] == "T5" else (0.01, 0.05)
        sec.append({"target": y["target"], "estimate": ye, "se": f(y["se"]), "p_naive": yp, "rows_dropped": int(y["rows_dropped"]), "nobs": int(y["nobs"]),
                    "same_direction_and_paper_star_bucket": ye > 0 and lo <= yp < hi, "p_below_0.05": yp < 0.05})
    rob.append({"id": "R_b", "description": "Drop rows with |z| > 3 on embed_dict_scale within the cycle_AE_fit2 estimation sample; refit; T1 coefficient", "ran": True,
        "estimate": e, "se_or_ci": f"SE {f(x['se']):.5f}", "p_value": p, "same_direction_and_significance_as_paper": e > 0 and p < 0.001,
        "source_file": "outputs/R_b_outliers_T1.csv", "note": f"rows dropped {x['rows_dropped']}, nobs {x['nobs']}; convergence: {x['conv']}. Secondary (outputs/R_b_outliers_T5_T6.csv): " + json.dumps(sec)})
ra = rcsv("R_a_summary.csv"); rap = rcsv("R_a_partial.csv")
if ra:
    x = ra[0]; K, Kd = int(float(x["K_rule"])), int(float(x["K_done"])); e = f(x["original_estimate"]); pn = f(x["p_normal"])
    lo, hi = f(x["q025"]), f(x["q975"]); full = Kd + int(float(x["failed"])) >= K
    conv_warn = sum(1 for r in rap if r["conv"] not in ("none", "")) if rap else None
    rob.append({"id": "R_a", "description": "Party-cluster bootstrap of T1 (204 parties resampled with replacement, seed 20261011, draws pre-generated), refit cycle_AE_fit2", "ran": full,
        "estimate": e, "se_or_ci": f"bootstrap SE {f(x['boot_se']):.5f}; 95% percentile interval [{lo:.5f}, {hi:.5f}]", "p_value": pn,
        "same_direction_and_significance_as_paper": (e > 0 and lo > 0 and pn < 0.001),
        "source_file": "outputs/R_a_summary.csv",
        "note": f"K rule = {K} (first refit {open(os.path.join(O,'R_a_K.txt')).read().split()[-1][:5]} s); successful refits {Kd}; failed refits {x['failed']}; refits with lme4 convergence messages {conv_warn}. "
                f"Percentile interval excludes 0: {lo > 0}; normal p from estimate/bootstrap SE < 0.001: {pn < 0.001}. "
                + ("" if full else f"Stopped at the wall-time deadline before reaching K; reported on {Kd} draws (deviation from the K rule, see LOG.md). ")
                + "Per-draw results: outputs/R_a_partial.csv; draws: outputs/R_a_draws.rds."})
allA = all(t["match_to_rounding"] for t in targets); allB = all(t["same_conclusion"] for t in targets)
log = open(os.path.join(B, "LOG.md")).read()
start = datetime.datetime(2026, 10, 11, 5, 43); now = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)
res = {"paper_id": "24_U9CKK6", "agent": "B", "run_date_ist": "2026-10-11", "ran": True, "could_not_run_reason": "",
 "targets": targets, "robustness": rob, "bugs": [],
 "code_observations": [
   {"file": "Scripts/6_analysis1.R", "lines": [356, 365, 374, 384, 410], "kind": "verified by run",
    "description": "Table 1 models enter `year` as a numeric linear term (year is double in EP_debates_07062023.Rdata), while the texreg call (custom.gof.rows) and the printed Table 1 say 'Year Fixed Effects: Yes'. The deposited linear-year code reproduces the printed Table 1 Model 2 AIC 738747.50 and log likelihood -369309.75 exactly (outputs/modelinfo_cycle_AE_fit2.txt, outputs/AE_cycle_240124.tex), so the printed numbers come from the linear-year specification and the 'Year Fixed Effects' row label does not describe it. R_c (factor year) gives T1 0.017, same sign and p < 0.001."},
   {"file": "Scripts/6_analysis1.R", "lines": [132, 246], "kind": "unverified observation (not run; outside the pre-registered line ranges)",
    "description": "Models at lines 132 and 246 use `right` and `left`, which no deposited script creates (text search of 6_analysis1.R); a top-to-bottom run would stop at line 132. These models feed appendix results, not the targets."},
   {"file": "Scripts/9_analysis4.R", "lines": [30, 32, 36, 43, 47], "kind": "unverified observation (code reading; no effect on any target)",
    "description": "Script 9 adds year_mon (line 30) and EU_sal (left_join, line 32) before radical (line 36), so the centering index 117:118 (lines 43, 47), copied from script 6 where column 118 is radical, selects year_mon instead of radical. Neither year_mon nor radical enters the Table 2 models, and radical_scale is re-standardised by scale() anyway, so T5 and T6 are unaffected."}],
 "env_fixes": [
   "diffs/run_table1.diff: ran 6_analysis1.R lines 1-53 and 346-416 verbatim (class decision 2); added saveRDS after each model and timestamps; working directory set to the run folder with Data/ and Tables/ created",
   "diffs/run_table1_F1F2.diff: pre-registered memory fallback F1 (blank text and ori_text after load) and F2 (save, rm, gc; rebuild the combined texreg table from saved models), plus a resume guard; used only for cycle_AE_fit_group (Model 4, not a target) after the plain run passed the 3000 MB RSS trigger (3369 MB, MemAvailable 437 MB) while fitting it",
   "diffs/run_table2.diff: ran 9_analysis4.R lines 1-123 verbatim; added saveRDS after each model and timestamps (plain run, peak RSS 2542 MB, no fallback needed)",
   "packages: Debian binaries (lme4 1.1-37, tidyverse, ggeffects, skimr, zoo, sjmisc) and CRAN source installs into the per-run library (texreg, sjPlot, sjstats, fixest and dependencies); no versions pinned by the authors (environment.txt)"],
 "proposed_class": "A" if allA else ("B" if allB else "see note"),
 "class_reason": ("All six targets reproduced to the printed rounding with the pre-registered naive p in the paper's star bucket; Table 1 Model 2 AIC and log likelihood also match exactly." if allA else "Not all targets matched to rounding; see targets."),
 "confidence": "high",
 "confidence_reason": "Target models came from the authors' deposited code and data run unchanged (target models without any memory fallback); estimates, N, groups, AIC and logLik match the PDF; final confidence depends on agreement with agent A.",
 "time_minutes": round((now - start).total_seconds() / 60),
 "uncertainties": [
   "Package versions are current Debian/CRAN (lme4 1.1-37); the authors pinned none. Exact AIC/logLik agreement suggests no material drift.",
   "T1 to T3, T5, T6 are printed to 2 decimals, so within_5pct against the printed value is not informative (PREREG note); match_to_rounding is the meaningful test.",
   "cycle_AE, cycle_AE_fit2 and cycle_AE_fit3 come from the plain run; cycle_AE_fit_group came from the F1/F2 run (the plain run was stopped by the memory watchdog during that fit). The combined Table 1 .tex in outputs/ was written by the F1/F2 script from the four saved models.",
   "Robustness refits (R_a, R_b, R_c) use model.frame() of the saved original model as the estimation sample, as PREREG defines it, with as.factor(country) restored to a plain country column; the refit formula is the authors' formula.",
   "R_b secondary checks: T5 keeps its sign and the ** bucket after outlier exclusion; T6 keeps its sign but p rises above 0.05 (see R_b note). This is reported only and does not change the class.",
   "R_a: the party-cluster bootstrap SE of T1 (about 0.0082) is larger than the lmer model SE (0.0048); the percentile interval excludes 0 but the normal p (about 0.026) is not < 0.001, so R_a does not meet the pre-registered 'same significance' condition. The bootstrap was stopped once by the wall-time deadline at 166 draws and resumed from the saved pre-generated draws to the full K = 178 (LOG.md). Robustness does not change the class.",
   "Target cells were checked against the publisher PDF text obtained by web_fetch (outputs/pdf_cell_check.json); the copy came via a fallback fetcher, not a direct PDF download."]}
json.dump(res, open(os.path.join(B, "results.json"), "w"), indent=1)
print(json.dumps({k: res[k] for k in ["proposed_class", "time_minutes"]}), [(t["id"], t["reproduced_value"], t["match_to_rounding"], t["same_conclusion"]) for t in targets])
