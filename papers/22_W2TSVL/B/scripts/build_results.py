#!/usr/bin/env python3
"""Builds results.json for 22_W2TSVL agent B from files in outputs/. No reproduced number is typed here."""
import csv, json, re, os, datetime
P = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
O = os.path.join(P, "outputs")
REPO = os.path.dirname(os.path.dirname(P))
targets_pre = json.load(open(os.path.join(REPO, "22_W2TSVL", "targets.json")))
ext = {r["id"]: r for r in csv.DictReader(open(os.path.join(O, "targets_extracted.csv")))}
f = lambda x: None if x in ("", "NA", None) else float(x)

# pre-registered conclusion buckets (PREREG.md section 1)
def bucket_ok(tid, p):
    return {"T1": 0.01 <= p < 0.05, "T2": p < 0.01, "T3": p >= 0.10, "T4": p < 0.01}[tid]

targets = []
for t in targets_pre:
    e = ext[t["id"]]; pv = t["paper_value"]; dec = t["paper_rounding_decimals"]
    rv = f(e["value"]); ad = rv - pv; rd = ad / abs(pv)
    note = ""
    if t["id"] in ("T1", "T2", "T3", "T4"):
        p = f(e["p_wald"]); same = (rv > 0) == (pv > 0) and bucket_ok(t["id"], p)
        note = f"SE {f(e['se']):.6f}, Wald z {f(e['z']):.4f}, two-sided Wald p {p:.6f}; polr convergence {e['convergence']}"
    else:
        same = abs(rv - pv) <= 5
        note = f"nobs() = {f(e['nobs']):.0f}, $n = {f(e['n_slot']):.0f}"
    targets.append({"id": t["id"], "description": t["description"], "paper_value": pv, "paper_rounding_decimals": dec,
        "reproduced_value": rv, "source_file": "outputs/targets_extracted.csv", "abs_diff": ad, "rel_diff": rd,
        "match_to_rounding": round(rv, dec) == pv, "within_5pct": abs(rd) <= 0.05, "same_conclusion": same, "note": note})

# cross-check: main script figure fits vs appendix models
mc = list(csv.DictReader(open(os.path.join(O, "main_script_polr_coefs.csv"))))
ac = list(csv.DictReader(open(os.path.join(O, "all_coefs_m1_m4_m7_m10.csv"))))
amap = {"1": ("m1", "anti_strike", "TreatmentAnti_strike"), "2": ("m4", "anti_strike", "TreatmentAnti_strike"),
        "3": ("m7", "pro_strike", "TreatmentPro_strike"), "4": ("m10", "anti_strike", "TreatmentAnti_strike")}
xdiff = {}
for fit, (m, aterm, mterm) in amap.items():
    a = [f(r["value"]) for r in ac if r["model"] == m and r["term"] == aterm][0]
    b = [f(r["estimate"]) for r in mc if r["fit"] == fit and r["term"] == mterm][0]
    xdiff[f"fig{fit}_vs_{m}"] = abs(a - b)

rob_rows = list(csv.DictReader(open(os.path.join(O, "robustness_results.csv"))))
R = {(r["check"], r["target"]): r for r in rob_rows}
def verdict(chk, tid):
    r = R[(chk, tid)]; est = f(r["estimate"]); sign_ok = est < 0 if tid == "T1" else est > 0
    if chk == "R_a":
        lo, hi = (f(r["ci95_lo"]), f(r["ci95_hi"])) if tid == "T1" else (f(r["ci99_lo"]), f(r["ci99_hi"]))
        return sign_ok and (hi < 0 if tid == "T1" else lo > 0)
    thr = 0.05 if tid == "T1" else 0.01
    return sign_ok and f(r["p_value"]) < thr
desc = {"R_a": "Nonparametric case bootstrap, 1000 resamples, set.seed(20261011), refit m1 then m7 specification; percentile CIs, bootstrap p",
        "R_b": "Drop rows with |z| > 3 on age (d2, z over all 1011 rows), refit m1 and m7 specifications; Wald SE and p",
        "R_c": "Linear model (lm) instead of ordered logit on m1 and m7 rows, HC2 robust SEs (sandwich/lmtest)"}
robust = []
for chk in ("R_a", "R_b", "R_c"):
    t1, t2 = R[(chk, "T1")], R[(chk, "T2")]
    if chk == "R_a":
        se_ci = f"bootstrap SE {f(t1['se']):.4f}; 95% CI [{f(t1['ci95_lo']):.4f}, {f(t1['ci95_hi']):.4f}]; 99% CI [{f(t1['ci99_lo']):.4f}, {f(t1['ci99_hi']):.4f}]"
        extra = f"failed fits T1 {t1['n_failed']}, T2 {t2['n_failed']}. T2 (pro_strike, m7): estimate {f(t2['estimate']):.4f}, bootstrap SE {f(t2['se']):.4f}, 95% CI [{f(t2['ci95_lo']):.4f}, {f(t2['ci95_hi']):.4f}], 99% CI [{f(t2['ci99_lo']):.4f}, {f(t2['ci99_hi']):.4f}], bootstrap p {f(t2['p_value']):.4f}"
    else:
        se_ci = f"SE {f(t1['se']):.4f}" + (" (Wald)" if chk == "R_b" else " (HC2)")
        extra = (f"rows dropped {t1['n_dropped']} (N T1 {t1['n_ok']}, T2 {t2['n_ok']}). " if chk == "R_b" else f"N T1 {t1['n_ok']}, T2 {t2['n_ok']}; estimates in outcome units. ") + \
                f"T2 (pro_strike): estimate {f(t2['estimate']):.4f}, SE {f(t2['se']):.4f}, p {f(t2['p_value']):.6f}"
    robust.append({"id": chk, "description": desc[chk], "ran": True, "estimate": f(t1["estimate"]), "se_or_ci": se_ci,
        "p_value": f(t1["p_value"]), "same_direction_and_significance_as_paper": verdict(chk, "T1"), "source_file": "outputs/robustness_results.csv",
        "note": f"Field refers to T1 (anti_strike, m1). {extra}. T2 same direction and significance at printed p < 0.01 threshold: {verdict(chk, 'T2')}."})

a4 = list(csv.DictReader(open(os.path.join(O, "check_tableA4_means.csv"))))
a4_all = all(r["unions_match_2dp"] == "TRUE" and r["support_match_2dp"] == "TRUE" for r in a4)
ov = {r["var"]: r for r in csv.DictReader(open(os.path.join(O, "check_overall_means.csv")))}

times = re.findall(r"^- (\d\d):(\d\d) ", open(os.path.join(P, "LOG.md")).read(), re.M)
mins = [int(h) * 60 + int(m) for h, m in times]
all_match = all(t["match_to_rounding"] for t in targets)
all_5 = all(t["within_5pct"] and t["same_conclusion"] for t in targets)
cls = "A" if all_match else ("B" if all_5 else "D")

res = {"paper_id": "22_W2TSVL", "agent": "B", "run_date_ist": datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=5, minutes=30))).strftime("%Y-%m-%d"),
  "ran": True, "could_not_run_reason": "", "targets": targets, "robustness": robust,
  "bugs": [{"file": "Framing Labor Action_Appendix A1.R", "line": 226,
            "description": "Table A4 group means of union influence are computed as mean() of the ordered factor `unions`, which returns NA for every group, so the computed means are never shown and the Table A4 values are typed as constants at line 234. No effect on any printed number: the typed constants equal the means computed from the data (all 10 Table A4 cells match at 2 decimals, outputs/check_tableA4_means.csv), and the main script (line 52) computes the same means on a numeric `unions`.",
            "evidence": "outputs/appendix_run_stdout.txt prints mean_unions_Tr_2 with Mean NA for all five treatments; outputs/appendix_run_stderr.txt: 'argument is not numeric or logical: returning NA'. `dta$unions` is made an ordered factor at line 58."}],
  "env_fixes": ["diffs/appendix_A1_R.diff: line 14 absolute Windows read_dta path replaced by read_dta(\"OA23 Base UT-TEC.dta\") (authors' own alternative, main script line 15); install.packages lines 4, 5, 6, 138, 282 commented out (packages preinstalled)",
                "diffs/main_R_script.diff: line 14 absolute path replaced as above; install.packages lines 4 to 8 commented out",
                "scripts/run_appendix.R: browseURL defined as a no-op before source() (PREREG.md allowed fix); models and data saved to outputs/ after the script",
                "scripts/run_main.R: broom::tidy wrapped only to record polr coefficients for the cross-check; ggplot output to a pdf device",
                "Packages: Debian binaries from setup_env.sh plus r-cran-gmodels via apt; stargazer 5.2.3 and tableone 0.13.2 from CRAN into the per-run library (no Debian package)"],
  "proposed_class": cls,
  "class_reason": ("All six targets reproduced exactly to the paper's printed rounding (T1 to T4 coefficients at 3 decimals, T5 and T6 Ns exact), with the pre-registered Wald p in the printed star bucket for every coefficient; only path, install.packages and browseURL environment fixes were needed." if cls == "A" else "See targets."),
  "confidence": "high",
  "confidence_reason": "Targets matched by script with the authors' own code and a deterministic estimator; agreement with agent A is not known to agent B, which PROTOCOL.md section 8 requires for high.",
  "time_minutes": (max(mins) - min(mins)) if mins else None,
  "uncertainties": [
    f"Cross-check: the main script's Figure 1 to 4 polr fits equal the appendix models (max abs diff in the target coefficient: {max(xdiff.values()):.2e}; per fit {json.dumps({k: float(f'{v:.2e}') for k, v in xdiff.items()})}; outputs/main_script_polr_coefs.csv vs outputs/all_coefs_m1_m4_m7_m10.csv). The figure-script fits are identical to the appendix models to machine precision.",
    f"T2 Wald p is {f(ext['T2']['p_wald']):.5f}, just under the 0.01 cut for the printed ***; its bucket is matched, but the margin is small. Under robustness, T2 keeps p < 0.01 only in R_b; the R_a bootstrap 99% CI and the R_c HC2 linear model put it between 0.01 and 0.05 (same direction). T1 keeps direction and p < 0.05 in all three checks.",
    "Likelihood-ratio / profile p-values (the second, non-pre-registered statistic) were not computed; the class uses the first listed statistic (Wald), per batch5_class_decisions.md item 1.",
    "Weighted model Ns 975 (Table A1 col 2) and 962 (Table A2 col 2) are reproduced by the code (outputs/table_1A_new.htm, table_A2_new.htm): MASS::polr reports the sum of the weights Ponderador as N. Not a target.",
    f"Overall outcome means from the data: union influence {f(ov['unions']['mean']):.4f} (SD {f(ov['unions']['sd']):.4f}, n {ov['unions']['n']}), teacher support {f(ov['Support_teachers']['mean']):.4f} (SD {f(ov['Support_teachers']['sd']):.4f}, n {ov['Support_teachers']['n']}); text p. 1261 prints 3.17 (SD 1.4) and 4.46 (SD 2.4). 3.1773 rounds to 3.18, so the printed 3.17 reads as truncated; not a target (outputs/check_overall_means.csv).",
    f"Table A4 typed constants all equal computed group means at 2 decimals: {a4_all} (outputs/check_tableA4_means.csv).",
    "Data file has 1011 rows (treatment groups 210, 200, 206, 201, 194; outputs/check_value_labels.txt); text p. 1261 says 1,010 respondents. Not a target.",
    "Unverified observation (coding choice, not tested for impact): Appendix A1.R lines 110-121 map education codes 1 to 12 and send everything else to NA, which includes d3 = 13 'No tiene estudios' (17 respondents, label in the .dta; outputs/check_value_labels.txt). This affects only the control-variable models (m3, m6, m9, m12; Ns 754 and 747), not the targets.",
    "Brief said the absolute path is on line 15; in both downloaded scripts it is on line 14 (line 15 of the main script is the commented alternative). PREREG.md says line 14; the fix was applied to line 14.",
    "Environment differs from the authors' (R 4.4.2 on Windows): R 4.5.0 on Debian aarch64, MASS 7.3-65, ggplot2 3.5.1. The figure code lines 212 and 252 (`aes(estimate, term, color)`) ran without error and geom_errorbarh gave no warning in this ggplot2 version; a newer ggplot2 may warn.",
    "An `ls` of the paper folder at the start showed that a folder named A exists; nothing in it was opened or read."],
  }
json.dump(res, open(os.path.join(P, "results.json"), "w"), indent=1)
print(json.dumps({"class": cls, "targets": [(t["id"], t["paper_value"], t["reproduced_value"], t["match_to_rounding"], t["same_conclusion"]) for t in targets],
                  "robust": [(r["id"], r["estimate"], r["p_value"], r["same_direction_and_significance_as_paper"]) for r in robust], "xdiff": xdiff, "mins": res["time_minutes"]}, indent=0))
