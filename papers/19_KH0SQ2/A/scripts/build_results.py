#!/usr/bin/env python3
"""Builds results.json for 19_KH0SQ2 agent A from files in outputs/. No number is typed here except paper values,
which are read from REPO/papers/19_KH0SQ2/targets.json (copied from PREREG.md)."""
import csv, json, os, re, datetime
A = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAPER = os.path.dirname(A)
O = os.path.join(A, "outputs")
def rcsv(f): return list(csv.DictReader(open(os.path.join(O, f))))
tg = json.load(open(os.path.join(PAPER, "targets.json")))
ex = rcsv("targets_extracted.csv")
def get(model, term): return [r for r in ex if r["model"] == model and r["term"] == term][0]
spec = {"T1": ("res4", "TreatmentQuota"), "T2": ("res1", "TreatmentQuota"), "T3": ("resg1", "resp_genderMale"),
        "T4": ("resg2", "resp_genderMale"), "T5": ("res1", None), "T6": ("res4", None)}
nsame = {"T5": ["res1", "res2", "res3", "resg1"], "T6": ["res4", "res5", "res6", "resg2"]}
targets = []
for t in tg:
    m, term = spec[t["id"]]; pv = t["paper_value"]; dec = t["paper_rounding_decimals"]
    if term:
        r = get(m, term); val = float(r["estimate"]); p = float(r["p"]); se = float(r["se"])
        if t["id"] == "T1": same = val < 0 and p < 0.05; note = f"SE {se:.4f}, summary.lm p {p:.4g}; ** bucket (0.01<=p<0.05): {0.01 <= p < 0.05}"
        elif t["id"] == "T2": same = p >= 0.10; note = f"SE {se:.4f}, summary.lm p {p:.4g}"
        else: same = val < 0 and p < 0.01; note = f"SE {se:.4f}, summary.lm p {p:.4g}"
    else:
        ns = sorted({int(get(mm, "(Intercept)")["nobs"]) for mm in nsame[t["id"]]})
        val = float(get(m, "(Intercept)")["nobs"]); same = (val == pv)
        note = f"nobs across models {nsame[t['id']]}: {ns}"
    ad = val - pv; rd = ad / abs(pv) if pv != 0 else None
    targets.append({"id": t["id"], "description": t["description"], "paper_value": pv, "paper_rounding_decimals": dec,
        "reproduced_value": val, "source_file": "outputs/targets_extracted.csv", "abs_diff": ad, "rel_diff": rd,
        "match_to_rounding": round(val, dec) == round(pv, dec), "within_5pct": (abs(rd) <= 0.05) if rd is not None else None,
        "same_conclusion": same, "note": note})
# cross-check from main text script
xc = os.path.join(O, "crosscheck_main_text.csv")
cross = rcsv("crosscheck_main_text.csv") if os.path.exists(xc) else []
rob = []
ra = {r["target"]: r for r in rcsv("R_a_bootstrap.csv")}
rb = {r["target"]: r for r in rcsv("R_b_weight_outliers.csv")}
rc = {r["target"]: r for r in rcsv("R_c_unweighted.csv")}
def same_p(tid, est, p):
    if tid == "T1": return est < 0 and p < 0.05
    if tid == "T2": return p >= 0.10
    return est < 0 and p < 0.01
def same_boot(tid, r):
    f = lambda k: float(r[k])
    if tid == "T1": return f("ci95_hi") < 0
    if tid == "T2": return f("ci90_lo") <= 0 <= f("ci90_hi")
    return f("ci99_hi") < 0
def sec_ra():
    return "; ".join(f"{t}: est {float(r['estimate']):.4f}, boot SE {float(r['boot_se']):.4f}, 90% [{float(r['ci90_lo']):.4f}, {float(r['ci90_hi']):.4f}], 95% [{float(r['ci95_lo']):.4f}, {float(r['ci95_hi']):.4f}], 99% [{float(r['ci99_lo']):.4f}, {float(r['ci99_hi']):.4f}], p_boot {float(r['p_boot']):.4g}, NA draws {r['n_na']}, same as paper: {same_boot(t, r)}" for t, r in sorted(ra.items()))
def sec_p(d, extra=""):
    return "; ".join(f"{t}: est {float(r['estimate']):.4f}, SE {float(r['se']):.4f}, p {float(r['p']):.4g}" + (f", dropped {r['n_dropped']}" if 'n_dropped' in r else "") + f", same as paper: {same_p(t, float(r['estimate']), float(r['p']))}" for t, r in sorted(d.items()))
r1 = ra["T1"]
rob.append({"id": "R_a", "description": "Case bootstrap, 2000 resamples per model, set.seed(20261010) once, order res4, res1, resg1, resg2; percentile CIs; primary T1 (res4 Quota)",
  "ran": True, "estimate": float(r1["estimate"]), "se_or_ci": f"boot SE {float(r1['boot_se']):.4f}; 95% percentile CI [{float(r1['ci95_lo']):.4f}, {float(r1['ci95_hi']):.4f}]",
  "p_value": float(r1["p_boot"]), "same_direction_and_significance_as_paper": same_boot("T1", r1), "source_file": "outputs/R_a_bootstrap.csv",
  "note": "All targets: " + sec_ra()})
r1 = rb["T1"]
rob.append({"id": "R_b", "description": "Drop |z|>3 on survey Weight within each country's estimation sample (Support |z|>3 drops 0, see support_absz_gt3_dropped), refit weighted; primary T1",
  "ran": True, "estimate": float(r1["estimate"]), "se_or_ci": f"SE {float(r1['se']):.4f}; n dropped {r1['n_dropped']} of {r1['n_before']}",
  "p_value": float(r1["p"]), "same_direction_and_significance_as_paper": same_p("T1", float(r1["estimate"]), float(r1["p"])), "source_file": "outputs/R_b_weight_outliers.csv",
  "note": "All targets: " + sec_p(rb) + "; cases dropped by |z|>3 on Support: " + ", ".join(f"{t} {r['support_absz_gt3_dropped']}" for t, r in sorted(rb.items()))})
r1 = rc["T1"]
rob.append({"id": "R_c", "description": "Unweighted OLS on the same estimation samples; primary T1",
  "ran": True, "estimate": float(r1["estimate"]), "se_or_ci": f"SE {float(r1['se']):.4f}",
  "p_value": float(r1["p"]), "same_direction_and_significance_as_paper": same_p("T1", float(r1["estimate"]), float(r1["p"])), "source_file": "outputs/R_c_unweighted.csv",
  "note": "All targets: " + sec_p(rc)})
cfg = json.load(open(os.path.join(A, "scripts", "results_text.json")))
log = open(os.path.join(A, "LOG.md")).read()
ts = re.findall(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}) IST", log)
fmt = "%Y-%m-%d %H:%M"; tmin = int((datetime.datetime.strptime(ts[-1], fmt) - datetime.datetime.strptime(ts[0], fmt)).total_seconds() // 60)
unc = list(cfg["uncertainties"])
if cross:
    unc.append("Cross-check from main_text_figs_JEPP_FINAL.R (outputs/crosscheck_main_text.csv): " + "; ".join(f"{r['object']} {r['term']} {float(r['estimate']):.6f}" for r in cross))
desc = rcsv("descriptive_country_counts.csv")
unc.append("Descriptive country counts in all_merged.RData (outputs/descriptive_country_counts.csv): " + ", ".join(f"{r['country']} {r['Freq']}" for r in desc) + "; the paper text gives UK N = 1,708, France N = 969, combined 2677 (not targets).")
sec = [get("res2", "resp_genderMale"), get("res5", "resp_genderMale"), get("res1", "(Intercept)"), get("res4", "(Intercept)"), get("res6", "TreatmentQuota:resp_genderMale:Masculine")]
unc.append("Secondary context (PREREG, not targets; outputs/targets_extracted.csv): " + "; ".join(f"{r['model']} {r['term']} {float(r['estimate']):.4f} (SE {float(r['se']):.4f}, p {float(r['p']):.4g})" for r in sec))
allA = all(t["match_to_rounding"] for t in targets)
res = {"paper_id": "19_KH0SQ2", "agent": "A", "run_date_ist": ts[0][:10], "ran": True, "could_not_run_reason": "",
  "targets": targets, "robustness": rob, "bugs": cfg["bugs"], "env_fixes": cfg["env_fixes"],
  "proposed_class": "A" if allA else cfg["fallback_class"], "class_reason": cfg["class_reason"] if allA else "see LOG.md",
  "alternative_class": cfg.get("alternative_class"), "confidence": cfg["confidence"], "confidence_reason": cfg["confidence_reason"],
  "time_minutes": tmin, "uncertainties": unc}
json.dump(res, open(os.path.join(A, "results.json"), "w"), indent=1)
print(json.dumps({"class": res["proposed_class"], "targets": [(t["id"], t["paper_value"], t["reproduced_value"], t["match_to_rounding"], t["same_conclusion"]) for t in targets],
  "rob": [(r["id"], r["estimate"], r["p_value"], r["same_direction_and_significance_as_paper"]) for r in rob], "time": tmin}, indent=1))
