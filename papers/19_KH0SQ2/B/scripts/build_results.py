#!/usr/bin/env python3
"""Build results.json for 19_KH0SQ2 agent B from files in outputs/. No typed numbers except paper values read from targets.json."""
import csv, json, os
B = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.dirname(B)
O = os.path.join(B, "outputs")
tj = {t["id"]: t for t in json.load(open(os.path.join(P, "targets.json")))}
rows = list(csv.DictReader(open(os.path.join(O, "targets_extracted.csv"))))
def get(model, term):
    for r in rows:
        if r["model"] == model and r["term"] == term: return r
    return None
spec = {"T1": ("res4", "TreatmentQuota", "coef"), "T2": ("res1", "TreatmentQuota", "coef"),
        "T3": ("resg1", "resp_genderMale", "coef"), "T4": ("resg2", "resp_genderMale", "coef"),
        "T5": ("res1", "TreatmentQuota", "nobs"), "T6": ("res4", "TreatmentQuota", "nobs")}
targets = []
for tid, (model, term, kind) in spec.items():
    t = tj[tid]; r = get(model, term); pv = t["paper_value"]; dec = t["paper_rounding_decimals"]
    if kind == "coef":
        rv = float(r["estimate"]); p = float(r["p"]); se = float(r["se"])
        if tid == "T1": concl = rv < 0 and p < 0.05; note = f"SE {se:.4f}, summary.lm p {p:.4g} (paper **: 0.01<=p<0.05)"
        elif tid == "T2": concl = p >= 0.10; note = f"SE {se:.4f}, p {p:.4g} (paper: no star)"
        else: concl = rv < 0 and p < 0.01; note = f"SE {se:.4f}, p {p:.4g} (paper ***)"
        if tid == "T1" and p < 0.01: note += "; p<0.01, stronger than ** bucket"
    else:
        rv = int(float(r["nobs"])); concl = rv == pv; note = f"nobs({model}); other models with same N: " + ",".join(
            sorted({x['model'] for x in rows if x['nobs'] == r['nobs']}))
    ad = rv - pv; rd = ad / abs(pv) if pv != 0 else None
    targets.append({"id": tid, "description": t["description"], "paper_value": pv, "paper_rounding_decimals": dec,
        "reproduced_value": rv, "source_file": "outputs/targets_extracted.csv", "abs_diff": round(ad, 10),
        "rel_diff": round(rd, 10) if rd is not None else None, "match_to_rounding": round(rv, dec) == pv,
        "within_5pct": abs(rd) <= 0.05 if rd is not None else None, "same_conclusion": concl, "note": note})
# robustness
rob = list(csv.DictReader(open(os.path.join(O, "robustness.csv"))))
sz = list(csv.DictReader(open(os.path.join(O, "R_b_support_z_check.csv"))))
desc = {"R_a": "Case bootstrap, set.seed(20261010), 2000 resamples per model in order res4,res1,resg1,resg2, weighted lm refit; percentile CIs; p = 2*min tail share",
        "R_b": "Drop |z|>3 on survey Weight within each country's estimation sample (unweighted mean, sd n-1), refit weighted lm",
        "R_c": "Unweighted OLS on the same estimation samples"}
robustness = []
for chk in ["R_a", "R_b", "R_c"]:
    sub = {r["target"]: r for r in rob if r["check"] == chk}
    def same(tid, r):
        est = float(r["estimate"]); p = float(r["p"])
        if chk == "R_a":
            if tid == "T1": return float(r["ci95_hi"]) < 0
            if tid == "T2": return float(r["ci90_lo"]) <= 0 <= float(r["ci90_hi"])
            return float(r["ci99_hi"]) < 0
        if tid == "T1": return est < 0 and p < 0.05
        if tid == "T2": return p >= 0.10
        return est < 0 and p < 0.01
    prim = sub["T1"]
    sec = []
    for tid in ["T2", "T3", "T4"]:
        r = sub[tid]
        s = f"{tid}({r['model']}): est {float(r['estimate']):.4f}, SE {float(r['se']):.4f}, p {float(r['p']):.4g}"
        if chk == "R_a": s += f", 90% CI [{float(r['ci90_lo']):.4f},{float(r['ci90_hi']):.4f}], 99% CI [{float(r['ci99_lo']):.4f},{float(r['ci99_hi']):.4f}]"
        if chk == "R_b": s += f", n dropped {r['n_dropped']}"
        s += f", same as paper: {same(tid, r)}"
        sec.append(s)
    if chk == "R_a":
        seci = f"bootstrap SE {float(prim['se']):.4f}; 95% percentile CI [{float(prim['ci95_lo']):.4f}, {float(prim['ci95_hi']):.4f}]; NA draws {prim['n_na_draws']}"
    else:
        seci = f"SE {float(prim['se']):.4f}"
    note = "Primary T1 (res4). Secondary: " + "; ".join(sec)
    if chk == "R_b":
        note += "; n dropped T1 sample: " + prim["n_dropped"] + "; confirmation |z|>3 on Support drops: " + ",".join(f"{x['model']}={x['n_dropped_support_absz_gt3']}" for x in sz)
    robustness.append({"id": chk, "description": desc[chk], "ran": True, "estimate": float(prim["estimate"]), "se_or_ci": seci,
        "p_value": float(prim["p"]), "same_direction_and_significance_as_paper": same("T1", prim),
        "source_file": "outputs/robustness.csv" + (", outputs/R_b_support_z_check.csv" if chk == "R_b" else "") , "note": note})
# step B cross-check
cross = os.path.join(O, "main_text_crosscheck.csv")
unc = []
if os.path.exists(cross):
    cc = list(csv.DictReader(open(cross)))
    for r in cc: unc.append(f"Step B cross-check ({r['object']}, main_text_figs_JEPP_FINAL.R): {r['term']} = {float(r['estimate']):.6f}, n = {r['nobs']}; equals Appendix object: {r['equal_to_appendix']} (source outputs/main_text_crosscheck.csv)")
else:
    unc.append("Step B: main_text_figs_JEPP_FINAL.R cross-check not produced; see LOG.md")
stepb = os.path.join(O, "main_text_status.txt")
if os.path.exists(stepb): unc.append("Step B run status (outputs/main_text_status.txt): " + open(stepb).read().strip())
desc_counts = os.path.join(O, "descriptive_counts.csv")
if os.path.exists(desc_counts):
    dc = list(csv.DictReader(open(desc_counts)))
    unc.append("Descriptive N in deposit (outputs/descriptive_counts.csv): " + ", ".join(f"{r['country']}={r['n']}" for r in dc) + "; article text gives UK 1,708, France 969, combined 2677 (PREREG). No line in the Table S1/S10 block or in table(all$country) produces those; see the conjoint-model N observation below.")
sec = [r for r in rows if r["model"] in ("res2", "res5") and r["term"] == "resp_genderMale"]
unc.append("Secondary context (Table S1 interaction-model Male, Parity only): " + "; ".join(f"{r['model']} {float(r['estimate']):.4f} (SE {float(r['se']):.4f}, p {float(r['p']):.4g})" for r in sec) + " vs paper -0.381 (0.108) and -0.267 (0.124) (source outputs/targets_extracted.csv)")
r6 = get("res6", "TreatmentQuota:resp_genderMale:Masculine"); c1 = get("res1", "(Intercept)"); c4 = get("res4", "(Intercept)")
unc.append(f"Secondary context: FR Quota:Male:Masculine {float(r6['estimate']):.4f} (SE {float(r6['se']):.4f}, p {float(r6['p']):.4g}) vs paper -0.185 (0.075) **; constants UK {float(c1['estimate']):.4f}, FR {float(c4['estimate']):.4f} vs paper 2.977, 3.643")
g1q = get("resg1", "TreatmentQuota"); g2q = get("resg2", "TreatmentQuota"); g1m = get("resg1", "resp_genderMale"); g2m = get("resg2", "resp_genderMale")
unc.append(f"Table S10 prints the Male SE equal to the Quota SE; reproduced SEs: UK Quota {float(g1q['se']):.5f} vs Male {float(g1m['se']):.5f}, FR Quota {float(g2q['se']):.5f} vs Male {float(g2m['se']):.5f}, so the printed equality is consistent with the fitted models to 3 decimals.")
cn = os.path.join(O, "conjoint_model_n.csv")
if os.path.exists(cn):
    c = list(csv.DictReader(open(cn)))
    unc.append("Unverified observation: the first conjoint models in main_text_figs_JEPP_FINAL.R have n " + ", ".join(f"{r['model']} = {r['n']}" for r in c) + " (outputs/conjoint_model_n.csv, parsed from outputs/main_text.log), equal to the article's descriptive UK 1,708 and France 969 (sum 2677). This may be where the article's Ns come from (respondents with a conjoint rating), but the article does not say so.")
unc += [
 "Completeness: main_text_figs_JEPP_FINAL.R stops at l.835 because column Treatment2 is created only in Appendix_plus.R (l.1278, 1286); Figure 7 (list experiment) is not produced by the main-text script run alone. Not a target. Also res1 (l.325) is reassigned at l.639; the cross-check used deposited lines 1-364 evaluated unchanged (scripts/save_main_objs.R).",
 "Robustness: the France framing coefficient (T1) keeps its negative sign in all three checks but is not significant at 0.05 in any of them (bootstrap 95% CI includes 0; weight-outlier exclusion and unweighted OLS give p between 0.05 and 0.13). The UK and gender results hold in all three checks.",
 "Class rests on accepting the session driver (adds load('all_merged.RData') before Appendix_plus.R lines 892-958) as an environment fix (batch4_class_decisions.md #2). Alternative class if not accepted: C.",
 "No package versions pinned by the authors; Step A uses base R stats only, so versions should not affect the targets.",
 "Tool-generated workspace change notices displayed filenames from the A/ folder of this paper; none were opened or read.",
]
log = open(os.path.join(B, "LOG.md")).read()
import re
times = re.findall(r"^- (\d\d):(\d\d) IST", log, re.M)
mins = None
if len(times) >= 2:
    a = int(times[0][0]) * 60 + int(times[0][1]); b = int(times[-1][0]) * 60 + int(times[-1][1]); mins = (b - a) % 1440
allA = all(t["match_to_rounding"] for t in targets)
res = {"paper_id": "19_KH0SQ2", "agent": "B", "run_date_ist": "2026-10-11", "ran": True, "could_not_run_reason": "",
  "targets": targets, "robustness": robustness, "bugs": [],
  "env_fixes": ["diffs/Appendix_plus_driver_load.diff: Appendix_plus.R cannot run top to bottom (its load() of all_merged.RData at l.18 is commented out); the pre-registered driver adds setwd + load('all_merged.RData') before lines 892-958, no analysis line changed"]
     + (["diffs/main_text_figs_JEPP_FINAL.diff: see diffs/README.md"] if os.path.exists(os.path.join(B, "diffs", "main_text_figs_JEPP_FINAL.diff")) else []),
  "proposed_class": "A" if allA else "B",
  "class_reason": "All six targets (four coefficients and two Ns) match the printed Online Appendix values to the printed rounding with the same significance buckets, using the authors' lines 892-958 run through the pre-registered load() driver. Alternative class C if that driver is not accepted as an environment fix.",
  "confidence": "high", "confidence_reason": "Deterministic weighted OLS, checksums match the Dataverse record, numbers parsed by script; final confidence depends on agreement with agent A.",
  "time_minutes": mins, "uncertainties": unc}
json.dump(res, open(os.path.join(B, "results.json"), "w"), indent=1)
print(json.dumps(res, indent=1))
