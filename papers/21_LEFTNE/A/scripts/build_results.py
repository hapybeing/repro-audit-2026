"""Builds results.json for 21_LEFTNE agent A from files in outputs/. Paper values are copied from targets.json (frozen PREREG)."""
import json, csv, math, datetime, re, pathlib
A = pathlib.Path("/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/21_LEFTNE/A")
O = A / "outputs"
targets = json.load(open(A.parent / "targets.json"))
ext = {r["id"]: r for r in csv.DictReader(open(O / "targets_extracted_lavaan073.csv"))}
ext619 = {r["id"]: r for r in csv.DictReader(open(O / "targets_extracted_lavaan0619_system.csv"))}
logx = json.load(open(O / "log_crosscheck.json"))
si = json.load(open(O / "si_A5_check.json"))
diag = json.load(open(O / "diagnostics.json"))
def f(x): return None if x in ("", "NA", None) else float(x)
def rnd(x, d):  # round half away from zero at d decimals
    q = 10 ** d; return math.floor(abs(x) * q + 0.5) / q * (1 if x >= 0 else -1)
crit = {"T1": ("p", 0.05), "T2": ("p", 0.05), "T3": ("p", 0.001), "T4": ("p", 0.001), "T5": ("p", 0.01)}
out_t = []
for t in targets:
    tid = t["id"]; r = ext[tid]; pv = t["paper_value"]; d = t["paper_rounding_decimals"]
    rep = f(r["estimate"]); p = f(r["p_value"])
    absd = rep - pv; reld = absd / pv if pv != 0 else None
    match = rnd(rep, d) == round(pv, d)
    if tid in crit:
        same = rep > 0 and p < crit[tid][1]
    else:
        same = abs(rep - pv) <= 5
    note = []
    if tid in ("T1", "T2", "T3", "T4", "T5"):
        note.append("SE %.6g, p %.6g, nobs %d (outputs/targets_extracted_lavaan073.csv)" % (f(r["se"]), p, int(float(r["nobs"]))))
        lx = logx[tid]; note.append("authors' printed log: est %s, p/se %s (%s)" % (lx["printed_est"], lx.get("printed_p", lx.get("printed_se")), lx["source"]))
    if tid in ("T1", "T2"):
        note.append("p rounds to 0.00 at 2 decimals: %s" % (rnd(p, 2) == 0.0))
        note.append("lavaan 0.6.19 (system) cross-check est %.6g (outputs/targets_extracted_lavaan0619_system.csv)" % f(ext619[tid]["estimate"]))
        a8 = logx["A8_Study %s Trump" % ("1" if tid == "T1" else "2")]
        note.append("candidate 2 (SI Table A8 mediate ACME, paper %s): deposited mediate() code gives %.4g (p %s), outputs/tableA8_mediate.csv; the paper's A8 value equals the lavaan estimate at printed precision" % (a8["paper_acme"], a8["acme"], a8["p_printed"]))
    if tid in ("T3", "T4"):
        cell = si["T3_cell_None_Trump"] if tid == "T3" else si["T4_cell_Party_TrumpParty"]
        note.append("SI Table A5 cell re-checked against the .doc itself: '%s' (outputs/si_A5_check.json)" % cell)
    if tid == "T6":
        note.append("nobs(mod2) = %d; the authors' export_summs log prints N %d (outputs/log_crosscheck.json). CES2020.RDS has %d compliers, none with missing outcome or treatment (outputs/diagnostics.json). N-only mismatch with all estimate targets matching: CHANGELOG_METHOD #6(a)." % (int(rep), logx["T6"]["printed_N"], diag["compliers_rows"]))
    out_t.append({"id": tid, "description": t["description"], "paper_value": pv, "paper_rounding_decimals": d,
                  "reproduced_value": rep, "source_file": "outputs/targets_extracted_lavaan073.csv",
                  "abs_diff": absd, "rel_diff": reld, "match_to_rounding": match, "within_5pct": abs(reld) <= 0.05,
                  "same_conclusion": same, "note": "; ".join(note)})
# Robustness
def rd(fn): return list(csv.DictReader(open(O / fn)))
rob = []
for st, prim in (("study1", True), ("study2", False)):
    s = rd("Ra_summary_%s.csv" % st)[0]; est = f(s["estimate"]); lo, hi = f(s["boot_ci_low"]), f(s["boot_ci_high"])
    rob.append({"id": "R_a" if prim else "R_a_secondary", "description": "Case bootstrap (K=%s, seed 20261011) of the %s SEM indirect effect indirTRUMPanger (%s)" % (s["K"], "Study 1" if prim else "Study 2", "T1" if prim else "T2"),
                "ran": True, "estimate": est, "se_or_ci": "percentile 95%% CI [%.6g, %.6g]; bootstrap SD %.6g" % (lo, hi, f(s["boot_sd"])),
                "p_value": f(s["p_value"]), "same_direction_and_significance_as_paper": est > 0 and lo > 0,
                "source_file": "outputs/Ra_summary_%s.csv" % st, "note": "rows %s = lavaan nobs %s; %s of %s fits ok, %s failed; p = min(2 x share of draws <= 0, 1); draws in outputs/Ra_draws_%s.csv" % (s["n_rows"], s["lavaan_nobs"], s["n_ok"], s["K"], s["n_failed"], st)})
for r in rd("Rb_summary.csv"):
    prim = r["part"] == "T3"; est, p = f(r["estimate"]), f(r["p_value"])
    rob.append({"id": "R_b" if prim else "R_b_secondary", "description": "Drop |z| > 3 on the outcome (%s) and refit %s" % ("anger" if prim else "Engage", "lm(anger ~ TREATMENT), Trump coefficient (T3)" if prim else "the Study 1 SEM, indirTRUMPanger (T1)"),
                "ran": True, "estimate": est, "se_or_ci": "SE %.6g" % f(r["se"]), "p_value": p,
                "same_direction_and_significance_as_paper": est > 0 and p < (0.001 if prim else 0.05), "source_file": "outputs/Rb_summary.csv",
                "note": "%s of %s rows dropped (max |z| %.4g); refit nobs %s" % (r["n_dropped"], r["n_before"], f(r["max_abs_z"]), r["nobs"]) + ("" if prim else "; no row exceeded |z| 3, so the estimate equals the original")})
for r in rd("Rc_summary.csv"):
    prim = r["study"] == "study1"; est, p = f(r["estimate"]), f(r["p_value"])
    rob.append({"id": "R_c" if prim else "R_c_secondary", "description": "SEM on the Alexa, Trump and Clinton arms only, MARCH and METOO terms removed, indirTRUMPanger (%s)" % ("Study 1, T1" if prim else "Study 2, T2"),
                "ran": True, "estimate": est, "se_or_ci": "SE %.6g" % f(r["se"]), "p_value": p,
                "same_direction_and_significance_as_paper": est > 0 and p < 0.05, "source_file": "outputs/Rc_summary.csv",
                "note": "nobs %s. Equals the deposited mediate() ACME point estimate for the same study (outputs/tableA8_mediate.csv)" % r["nobs"]})
crc = json.load(open(O / "code_review_check.json"))
bugs = [{"file": "02- Replication_Appendix.R", "line": 87,
         "description": "In the Table A3 block (demographics for Study 2, NORC), partisanship is tabulated from `df` (the Study 1 Qualtrics data) instead of `df_TESS`; lines 74-93 use df_TESS for every other row of Table A3.",
         "evidence": "Line 87: `df %%>%% tabyl(PARTISANSHIP, sort = TRUE)`. Output is Study 1's distribution (Democrat %s, Independent %s, Republican %s; same as Table A1 line 56). NORC.RDS has its own PARTISANSHIP column (Democrat %s, Independent %s, Republican %s). SI Table A3 prints Republican 34.98%%, Democrat 36.68%%, Independent 26.10%%, identical to SI Table A1. Source: outputs/code_review_check.json, outputs/appendix_log.txt lines 410-415 and 477-482. Not a target; does not affect any estimate." % (
             crc["line87_output_df_PARTISANSHIP"][0]["percent"], crc["line87_output_df_PARTISANSHIP"][1]["percent"], crc["line87_output_df_PARTISANSHIP"][3]["percent"],
             crc["norc_PARTISANSHIP_tabyl"][0]["percent"], crc["norc_PARTISANSHIP_tabyl"][1]["percent"], crc["norc_PARTISANSHIP_tabyl"][2]["percent"])}]
all_match = all(t["match_to_rounding"] for t in out_t)
est_match = all(t["match_to_rounding"] for t in out_t if t["id"] != "T6")
cls = "A" if all_match else ("C" if est_match else ("B" if all(t["within_5pct"] and t["same_conclusion"] for t in out_t) else "C"))
log = (A / "LOG.md").read_text() if (A / "LOG.md").exists() else ""
ts = re.findall(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}) IST", log)
mins = None
if ts:
    t0 = datetime.datetime.strptime(ts[0], "%Y-%m-%d %H:%M"); t1 = datetime.datetime.strptime(ts[-1], "%Y-%m-%d %H:%M"); mins = int((t1 - t0).total_seconds() / 60)
res = {"paper_id": "21_LEFTNE", "agent": "A", "run_date_ist": datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=5, minutes=30))).strftime("%Y-%m-%d"),
 "ran": True, "could_not_run_reason": "", "targets": out_t, "robustness": rob, "bugs": bugs,
 "env_fixes": ["diffs/Replication_Text_plot_try.diff: 6 figure-printing statements wrapped in try(print({...})); hrbrthemes::theme_ipsum_rc font (Roboto Condensed) unavailable to the pdf device stopped the script at line 71 ('invalid font type'). PREREG-listed plot-only fix; no estimation line changed",
               "diffs/Replication_Appendix_plot_try.diff: same fix for 5 figure-printing statements in the Appendix script",
               "packages: lavaan 0.7.3 (current CRAN, first in the PREREG order; not in the authors' Packages vector) and aod, Rmisc, interplot, margins, janitor, jtools, huxtable, dotwhisker, hrbrthemes, effectsize, mediation, qualtRics (plus dependencies, including newer ggplot2, scales, insight, parameters) from CRAN source into the per-run library; Debian r-cran-* binaries for the rest; apt libarchive-dev (for CRAN archive, a qualtRics dependency)",
               "working directory set to the unzipped Data.zip folder (scripts read the RDS files by bare name); no path edits"],
 "proposed_class": cls,
 "class_reason": "T1 to T5 (all estimate targets) reproduce to the paper's rounding with the pre-registered lavaan and lm objects; T6, the Table 3 N, is 698 in the run and in the authors' own printed output against 697 in the paper, an N-only mismatch that CHANGELOG_METHOD #6(a) and batch 5 decision 9 class as C. Under a literal PROTOCOL section 7 reading it would be B (all within 5%, same conclusions).",
 "confidence": "medium",
 "confidence_reason": "All numbers matched by script and the lavaan factor input caused no issue, but the class rests on the N-only rule and on Agent B's independent run; package versions are current CRAN, not the authors' (none pinned).",
 "time_minutes": mins,
 "uncertainties": [
  "T6: the deposited CES2020.RDS has 698 compliers with complete data, so the code cannot give 697; why the paper prints 697 could not be determined (all Table 3 estimates, SEs, stars, intercept and R2 match).",
  "SI Table A8 (candidate 2 for T1/T2): the four printed values (0.002 p .475; 0.017 p .004; -0.000 p .982; 0.080 p .000) equal the lavaan 5-arm SEM indirect effects and p-values at printed precision, not the output of the deposited mediate() code (0.0031 p .438; 0.0252 p .006; -0.0001 p .940; 0.108 p <.001, seed 20241130, mediation 4.5.1). The mediate point estimates equal the 3-arm SEM of R_c. So Table A8 appears to come from the lavaan model rather than the A8 code block (observation from runs, not a judgement). Bootstrap p-values also depend on mediation version and RNG.",
  "PREREG inconsistency 1 resolved by run: the Clinton p-values in Table 1 (0.48, 0.98) also equal the lavaan p-values (0.475, 0.982), so both Table 1 and Table A8 are consistent with the lavaan SEM.",
  "PREREG inconsistency 4: the 3-arm Study 1 data have 586 rows (matches text n = 586); Table A5 N 584 reflects 2 rows with missing anger.",
  "PREREG inconsistency 3 confirmed: the Study 1 and Study 2 SEMs use all five arms (nobs 977 and 1030); restricting to three arms (R_c) gives larger indirect effects (0.025, 0.108), same direction and significance.",
  "Plot-only fix: figures that use theme_ipsum_rc did not render (try() caught 'invalid font type'); no figure claim is a target, and figures were not compared with the paper.",
  "lavaan 0.7.3 summary() abbreviates the defined-parameter labels (e.g. indirTRUMPangr); values were read via parameterEstimates() by label and cross-checked against the printed log. lavaan 0.6.19 (system Debian) gives identical T1/T2.",
  "Results with no deposited code (PREREG inconsistencies 5 to 7: combined indirect effects, Democratic-women subgroup values, Cohen's d, SI Table C1 and Figures C1 to C3) were not checked; they are not targets.",
  "SI Table A5 cells were checked from catdoc text of the .doc binary (table cells in reading order), not from a rendered page; the cell order matched the row and column labels."]}
json.dump(res, open(A / "results.json", "w"), indent=1)
print(json.dumps({k: res[k] for k in ("proposed_class", "time_minutes")}), [(t["id"], t["paper_value"], round(t["reproduced_value"], 6), t["match_to_rounding"], t["within_5pct"], t["same_conclusion"]) for t in out_t])
for r in rob: print(r["id"], r["estimate"], r["se_or_ci"], r["p_value"], r["same_direction_and_significance_as_paper"])
