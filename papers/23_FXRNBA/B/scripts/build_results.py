#!/usr/bin/env python3
"""Builds results.json for 23_FXRNBA agent B from files in outputs/ (no hand-typed reproduced numbers)."""
import csv, json, os, re, math
import statistics
def pct(xs, q):  # linear interpolation, same as R quantile type 7 / numpy default
    xs = sorted(xs); h = (len(xs) - 1) * q / 100.0; lo = math.floor(h); hi = math.ceil(h)
    return xs[lo] + (h - lo) * (xs[hi] - xs[lo])
B = "/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/23_FXRNBA/B"
REPO = "/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo"
O = os.path.join(B, "outputs")
def readkv(fn):
    with open(os.path.join(O, fn)) as f:
        return {r["quantity"]: (float(r["value"]) if r["value"] not in ("", "NA") else None) for r in csv.DictReader(f)}
tfile = "targets_extracted.csv" if os.path.exists(os.path.join(O, "targets_extracted.csv")) else "targets_extracted_part.csv"
t = readkv(tfile)
tpart = readkv("targets_extracted_part.csv")
paper = {d["id"]: d for d in json.load(open(os.path.join(REPO, "papers/23_FXRNBA/targets.json")))}
rep = {"T1": "T1_beta_model3", "T2": "T2_p_model3_grab_by_name", "T3": "T3_N_main", "T4": "T4_F_model3",
       "T5": "T5_fs_coef_model3_feols", "T6": "T6_cand1_pct_exp_unrounded"}
rob = readkv("robustness_Rb_Rc.csv") if os.path.exists(os.path.join(O, "robustness_Rb_Rc.csv")) else {}
def rnd(x, d):  # round half away from zero
    q = 10 ** d
    return math.floor(abs(x) * q + 0.5) / q * (1 if x >= 0 else -1)
targets = []
sc = {}
sc["T1"] = t["T1_beta_model3"] > 0 and t["T2_p_model3_grab_by_name"] < 0.05
sc["T2"] = t["T2_p_model3_grab_by_name"] < 0.05
sc["T3"] = t["T3_N_main"] == 7163
sc["T4"] = t["T4_F_model3"] > 10
sc["T5"] = t["T5_fs_coef_model3_feols"] > 0 and t["T5_fs_p_model3_normal"] < 0.05
sc["T6"] = t["T6_cand1_pct_exp_unrounded"] > 0 and sc["T1"]
notes = {
 "T2": "Candidate (2) summary(ivglm) Pr(>|z|) = %.10g (identical to candidate 1)." % t["T2_p_model3_summary_ivglm"] if t.get("T2_p_model3_summary_ivglm") is not None else "",
 "T5": "Prose value. Clustered SE %.6g, normal p %.3g. Candidate (3), glm first stage as in run_ivglm: %s. Candidate (2) (plots script b_fs) not run." % (
        t["T5_fs_se_model3_clustered"], t["T5_fs_p_model3_normal"], ("%.6g" % rob["T5_cand3_glm_fs_coef"]) if rob.get("T5_cand3_glm_fs_coef") is not None else "not computed"),
 "T6": "Scored with the first pre-registered formula 100*(exp(b3*fs3)-1). Other candidates: linear 100*b3*fs3 = %.6g; exp with rounded 7.0 = %.6g. No deposited script computes this value." % (t["T6_cand2_pct_linear"], t["T6_cand3_pct_exp_rounded7"]),
 "T4": "fixest %s." % "0.14.2 (current CRAN); pre-registered 0.13.2 fallback not needed since the value matched",
}
for tid in ["T1", "T2", "T3", "T4", "T5", "T6"]:
    pv = paper[tid]["paper_value"]; d = paper[tid]["paper_rounding_decimals"]; rv = t[rep[tid]]
    ad = abs(rv - pv); rd = (rv - pv) / pv
    targets.append({"id": tid, "description": paper[tid]["description"], "paper_value": pv, "paper_rounding_decimals": d,
                    "reproduced_value": rv, "source_file": "outputs/" + tfile, "abs_diff": ad, "rel_diff": rd,
                    "match_to_rounding": rnd(rv, d) == pv, "within_5pct": abs(rd) <= 0.05, "same_conclusion": sc[tid],
                    "note": notes.get(tid, "") + (" Full-run value equals the 1-668 subset run value." if tfile == "targets_extracted.csv" and tpart[rep[tid]] == rv else "")})
# R_a
robust = []
ra_f = os.path.join(O, "Ra_boot.csv")
if os.path.exists(ra_f):
    rows = list(csv.DictReader(open(ra_f)))
    est = [float(r["est"]) for r in rows if r["est"] not in ("", "NA") and r["converged"] == "1"]
    nfail = len(rows) - len(est)
    lo, hi = pct(est, 2.5), pct(est, 97.5); sd = statistics.stdev(est)
    p = min(2 * sum(1 for e in est if e <= 0) / len(est), 1.0)
    orig = t["T1_beta_model3"]
    Bused = len(rows)
    ra_meta = json.load(open(os.path.join(O, "Ra_meta.json"))) if os.path.exists(os.path.join(O, "Ra_meta.json")) else {}
    summ = {"B_completed": Bused, "n_valid": int(len(est)), "n_failed_or_nonconverged": int(nfail), "boot_sd": sd,
            "pct_2.5": float(lo), "pct_97.5": float(hi), "boot_p": p, "boot_mean": statistics.mean(est), **ra_meta}
    json.dump(summ, open(os.path.join(O, "Ra_summary.json"), "w"), indent=1)
    robust.append({"id": "R_a", "description": "Date-cluster bootstrap of the full Model 3 2SRI estimator (seed 20261011, resample calendar dates, point estimate only)",
                   "ran": True, "estimate": orig, "se_or_ci": "bootstrap SE %.6g; 95%% percentile CI [%.6g, %.6g]" % (sd, lo, hi), "p_value": p,
                   "same_direction_and_significance_as_paper": bool(orig > 0 and lo > 0),
                   "source_file": "outputs/Ra_boot.csv; outputs/Ra_summary.json",
                   "note": "B used = %d (%s); %d valid replicates, %d failed or non-converged (not replaced). Estimate is the original T1 from outputs/%s." % (Bused, ra_meta.get("B_reason", ""), len(est), nfail, tfile)})
else:
    robust.append({"id": "R_a", "description": "Date-cluster bootstrap", "ran": False, "estimate": None, "se_or_ci": "", "p_value": None,
                   "same_direction_and_significance_as_paper": None, "source_file": "", "note": "not completed"})
if rob:
    robust.append({"id": "R_b", "description": "Drop station-days with pooled |z| > 3 on assault, refit Model 3 with authors' run_ivglm (date-clustered)",
                   "ran": True, "estimate": rob["Rb_beta"], "se_or_ci": "SE %.6g" % rob["Rb_se"], "p_value": rob["Rb_p"],
                   "same_direction_and_significance_as_paper": bool(rob["Rb_beta"] > 0 and rob["Rb_p"] < 0.05), "source_file": "outputs/robustness_Rb_Rc.csv",
                   "note": "N %d, dropped %d (%s); first-stage F %.4g; assault cutoffs [%.4g, %.4g]." % (rob["Rb_N"], rob["Rb_dropped"],
                        ", ".join("%s %d" % (k.replace("Rb_dropped_", ""), v) for k, v in rob.items() if k.startswith("Rb_dropped_")), rob["Rb_F"], rob["Rb_z_cutoff_assault_low"], rob["Rb_z_cutoff_assault_high"])})
    robust.append({"id": "R_c", "description": "Linear 2SLS: feols(log(1+assault) ~ W | station+year+month+dow | pm25_mean ~ z_smoke, cluster=~date)",
                   "ran": True, "estimate": rob["Rc_beta"], "se_or_ci": "clustered SE %.6g" % rob["Rc_se"], "p_value": rob["Rc_p"],
                   "same_direction_and_significance_as_paper": bool(rob["Rc_beta"] > 0 and rob["Rc_p"] < 0.05), "source_file": "outputs/robustness_Rb_Rc.csv",
                   "note": "N %d; first-stage ivwald F %.4g." % (rob["Rc_N"], rob["Rc_F_ivwald"])})
# time from LOG.md
log = open(os.path.join(B, "LOG.md")).read()
ts = re.findall(r"2026-10-11 (\d\d):(\d\d)", log)
mins = [int(h) * 60 + int(m) for h, m in ts]
tmin = (max(mins) - min(mins)) if mins else None
allmatch = all(x["match_to_rounding"] for x in targets)
unc = [
 "Supplementary Information was not readable for the pre-registration (captcha); SI tables were not compared.",
 "T5 and T6 are prose values; T6 is computed by our extraction script with the first pre-registered formula, not by any deposited script.",
 "Upstream construction of the merged station-day CSVs from raw sources is not deposited, so the data-building step was not audited.",
 "T5 candidate (2) (plots script first stage on its own main sample) was not run; wildfire_plots.R is not needed for any target.",
 "Package versions are current CRAN (fixest 0.14.2, ivtools 2.3.0) because the authors pinned none; all targets matched so no fallback was tried.",
]
if rob.get("EXPL_N_model3_vars_only") is not None:
    unc.append("Exploratory, not pre-registered (outputs/robustness_Rb_Rc.csv): listwise deletion over Model 3 variables only gives N %d (%d more rows than N_main), beta %.6g, p %.4g. This describes the sample-definition difference noted as PREREG inconsistency 1." % (
        rob["EXPL_N_model3_vars_only"], rob["EXPL_rows_dropped_by_extra_naomit_cols"], rob["EXPL_beta"], rob["EXPL_p"]))
fullran = os.path.exists(os.path.join(O, "table1_objects.rds"))
if not fullran:
    unc.append("The full authors' script did not complete; targets come from the unchanged lines 1-668 subset run.")
res = {"paper_id": "23_FXRNBA", "agent": "B", "run_date_ist": "2026-10-11", "ran": True, "could_not_run_reason": "",
       "targets": targets, "robustness": robust,
       "bugs": [],
       "env_fixes": ["No file edited (diffs/README.md). Files placed in the folder layout the code expects ('Data Analysis/', 'Beats/', 'Crime Data/'), working directory set to that folder, CSVs downloaded with ?format=original, R run with LC_ALL=C.UTF-8, packages installed from current CRAN into a per-run library."],
       "proposed_class": "A" if allmatch else "B",
       "class_reason": ("All six pre-registered targets (Model 3 2SRI coefficient, p, N, first-stage F, first-stage coefficient and the derived 3.6%) reproduce to the paper's printed rounding from the authors' unchanged code and deposited data." if allmatch else "Not all targets match to rounding; see targets."),
       "confidence": "high" if allmatch else "medium",
       "confidence_reason": "Numbers matched by script with the authors' code unchanged; final confidence also depends on agreement with agent A, which B has not seen.",
       "time_minutes": tmin, "uncertainties": unc,
       "code_review": "None found. Read wildfire_data_analysis.R lines 1-680 in full (preprocessing, samples, helpers, Table 1) and skimmed section headers of the rest; wildfire_plots.R not reviewed beyond PREREG notes. Unverified observations are in LOG.md.",
       "full_script_completed": fullran}
json.dump(res, open(os.path.join(B, "results.json"), "w"), indent=1)
print(json.dumps({k: res[k] for k in ["proposed_class", "time_minutes", "full_script_completed"]}))
for x in targets: print(x["id"], x["paper_value"], x["reproduced_value"], x["match_to_rounding"])
for r in robust: print(r["id"], r["estimate"], r["p_value"], r["same_direction_and_significance_as_paper"])
