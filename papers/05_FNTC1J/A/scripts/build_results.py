#!/usr/bin/env python3
"""Build results.json for 05_FNTC1J agent A from files in outputs/ (no hand-typed numbers).

Numbers come from:
  outputs/targets_coefs.csv, outputs/targets_fit.csv     (extract_targets.R on the main run)
  outputs/Ra_bootstrap_summary.csv                        (robust_Ra_bootstrap.R)
  outputs/Rb_cooks.csv                                    (robust_Rb_cooks.R)
  outputs/Rc_coefs.csv                                    (extract_targets.R on the R_c run)
Paper values come from ../targets.json (copied from the paper in PREREG.md).
Text judgments (bugs, uncertainties, notes) come from outputs/review.json, written by the auditor.
Class is computed mechanically from the targets; class_reason text is from review.json.
"""
import csv, json, math, os, re

A = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
O = os.path.join(A, "outputs")


def rcsv(name):
    with open(os.path.join(O, name), newline="") as f:
        return list(csv.DictReader(f))


def fnum(x):
    if x is None or x in ("", "NA"):
        return None
    return float(x)


targets_paper = json.load(open(os.path.join(os.path.dirname(A), "targets.json")))
coefs = rcsv("targets_coefs.csv")
fit = rcsv("targets_fit.csv")
review = json.load(open(os.path.join(O, "review.json")))


def coef(rows, model, term):
    r = [x for x in rows if x["model"] == model and x["term"] == term]
    assert len(r) == 1, (model, term)
    return r[0]


spec = {
    "T1": ("CTB", "ConspMent_index", 0.001),
    "T2": ("misinfo", "ConspMent_index", 0.01),
    "T3": ("CTB", "EpistBel_Truth_index", 0.001),
    "T4": ("misinfo", "EpistBel_Truth_index", 0.01),
}
out_targets = []
for t in targets_paper:
    tid = t["id"]
    pv = t["paper_value"]
    dec = t["paper_rounding_decimals"]
    if tid in spec:
        model, term, alpha = spec[tid]
        r = coef(coefs, model, term)
        rv = fnum(r["odds_ratio"])
        padj = fnum(r["p_bonf"])
        same = (rv > 1) and (padj < alpha)
        note = (f"log-odds {fnum(r['log_odds']):.4f}, HC3 SE {fnum(r['se_hc3']):.4f}, raw p {fnum(r['p_raw']):.3g}, "
                f"Bonferroni p ({r['n_terms']} terms) {padj:.3g}; criterion OR > 1 and adj p < {alpha}")
        src = "outputs/targets_coefs.csv"
    else:  # T5
        r = [x for x in fit if x["model"] == "CTB"][0]
        rv = fnum(r["nobs"])
        same = abs(rv - pv) <= 5
        note = f"nobs(model_CTB); misinfo model nobs = {[x for x in fit if x['model']=='misinfo'][0]['nobs']}; criterion within 5 of {pv}"
        src = "outputs/targets_fit.csv"
    ad = abs(rv - pv)
    rd = (rv - pv) / pv
    out_targets.append({
        "id": tid, "description": t["description"], "paper_value": pv, "paper_rounding_decimals": dec,
        "reproduced_value": rv, "source_file": src, "abs_diff": ad, "rel_diff": rd,
        "match_to_rounding": round(rv, dec) == round(pv, dec) if dec > 0 else int(round(rv)) == int(pv),
        "within_5pct": abs(rd) <= 0.05, "same_conclusion": bool(same),
        "note": note + ("; " + review.get("target_notes", {}).get(tid, "") if review.get("target_notes", {}).get(tid) else ""),
    })

rob = []
# R_a
ra = [x for x in rcsv("Ra_bootstrap_summary.csv") if x["model"] == "CTB" and x["term"] == "ConspMent_index"][0]
lo, hi = fnum(ra["or_pct_ci_low"]), fnum(ra["or_pct_ci_high"])
rob.append({
    "id": "R_a", "description": "Case bootstrap, 1000 resamples, set.seed(20261009), percentile 95% CI of OR for ConspMent_index in model_CTB",
    "ran": True, "estimate": fnum(ra["or_original"]),
    "se_or_ci": f"percentile 95% CI {lo:.4f} to {hi:.4f}; bootstrap SE of log-odds {fnum(ra['boot_se_logodds']):.4f}; non-converged resamples {ra['n_not_converged']} of {ra['B']}",
    "p_value": fnum(ra["p_boot"]),
    "same_direction_and_significance_as_paper": bool(fnum(ra["or_original"]) > 1 and lo > 1),
    "source_file": "outputs/Ra_bootstrap_summary.csv", "note": review.get("robust_notes", {}).get("R_a", ""),
})
# R_b
rb = [x for x in rcsv("Rb_cooks.csv") if x["model"] == "CTB" and x["term"] == "ConspMent_index"][0]
rob.append({
    "id": "R_b", "description": "Drop cases with Cook's distance > 4/N from model_CTB, refit, HC3 SE, Bonferroni over 19 terms",
    "ran": True, "estimate": fnum(rb["odds_ratio"]),
    "se_or_ci": f"HC3 SE of log-odds {fnum(rb['se_hc3']):.4f}; Wald 95% CI of OR {fnum(rb['or_ci_low']):.4f} to {fnum(rb['or_ci_high']):.4f}; dropped {rb['n_dropped']} of {rb['N_original']} (threshold {fnum(rb['threshold']):.6f}); Bonferroni p {fnum(rb['p_bonf']):.3g}",
    "p_value": fnum(rb["p_raw"]),
    "same_direction_and_significance_as_paper": bool(fnum(rb["odds_ratio"]) > 1 and fnum(rb["p_bonf"]) < 0.001),
    "source_file": "outputs/Rb_cooks.csv", "note": review.get("robust_notes", {}).get("R_b", ""),
})
# R_c
rc = coef(rcsv("Rc_coefs.csv"), "CTB", "ConspMent_index")
rob.append({
    "id": "R_c", "description": "SDO_index rebuilt from SDO1_r, SDO2, SDO3_r, SDO4 (line 1035), whole script rerun with set.seed(2000); OR for ConspMent_index in model_CTB",
    "ran": True, "estimate": fnum(rc["odds_ratio"]),
    "se_or_ci": f"HC3 SE of log-odds {fnum(rc['se_hc3']):.4f}; HC3 95% CI of OR {fnum(rc['or_ci_low']):.4f} to {fnum(rc['or_ci_high']):.4f}; Bonferroni p {fnum(rc['p_bonf']):.3g}; nobs {rc['nobs']}",
    "p_value": fnum(rc["p_raw"]),
    "same_direction_and_significance_as_paper": bool(fnum(rc["odds_ratio"]) > 1 and fnum(rc["p_bonf"]) < 0.001),
    "source_file": "outputs/Rc_coefs.csv", "note": review.get("robust_notes", {}).get("R_c", ""),
})

# class, mechanically
if all(t["match_to_rounding"] for t in out_targets):
    cls = "A"
elif all(t["within_5pct"] and t["same_conclusion"] for t in out_targets):
    cls = "B"
else:
    cls = review.get("class_if_not_AB", "D")

# time from LOG.md timestamps (lines starting '- HH:MM')
times = [tuple(map(int, m.groups())) for m in re.finditer(r"^- (\d\d):(\d\d) ", open(os.path.join(A, "LOG.md")).read(), re.M)]
mins = [h * 60 + m for h, m in times]
tmin = max(mins) - min(mins) if mins else None

res = {
    "paper_id": "05_FNTC1J", "agent": "A", "run_date_ist": review["run_date_ist"],
    "ran": True, "could_not_run_reason": "",
    "targets": out_targets, "robustness": rob, "bugs": review["bugs"], "env_fixes": review["env_fixes"],
    "proposed_class": cls, "class_reason": review["class_reason"][cls],
    "confidence": review["confidence"], "confidence_reason": review["confidence_reason"],
    "time_minutes": tmin, "uncertainties": review["uncertainties"],
}
json.dump(res, open(os.path.join(A, "results.json"), "w"), indent=1, ensure_ascii=False)
print(json.dumps({"class": cls, "targets": [(t["id"], t["paper_value"], t["reproduced_value"], t["match_to_rounding"]) for t in out_targets],
                  "robust": [(r["id"], r["estimate"], r["p_value"], r["same_direction_and_significance_as_paper"]) for r in rob]}, indent=1))
