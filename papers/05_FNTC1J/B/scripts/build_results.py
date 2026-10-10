#!/usr/bin/env python3
"""Agent B: build results.json for 05_FNTC1J from files in outputs/ (no typed numbers for reproduced values)."""
import csv, json, os, re
from datetime import datetime
B = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(B)))
O = os.path.join(B, "outputs")
targets = json.load(open(os.path.join(REPO, "papers/05_FNTC1J/targets.json")))
rd = lambda f: list(csv.DictReader(open(os.path.join(O, f))))
main = rd("main_targets.csv"); fit = rd("main_fit.csv")
def term(rows, model, t): return [r for r in rows if r["model"] == model and r["term"] == t][0]
spec = {"T1": ("model_CTB", "ConspMent_index"), "T2": ("model_misinfo", "ConspMent_index"),
        "T3": ("model_CTB", "EpistBel_Truth_index"), "T4": ("model_misinfo", "EpistBel_Truth_index")}
T = []
for t in targets:
    pv = t["paper_value"]; dec = t["paper_rounding_decimals"]
    if t["id"] in spec:
        r = term(main, *spec[t["id"]]); val = float(r["odds_ratio"]); pb = float(r["p_bonf"])
        thr = 0.001 if t["id"] in ("T1", "T3") else 0.01
        concl = (val > 1) and (pb < thr)
        note = f"log-odds {float(r['log_odds']):.4f}, HC3 SE {float(r['se_hc3']):.4f}, raw p {float(r['p_raw']):.3g}, Bonferroni p {pb:.3g} (threshold {thr}); nobs {r['nobs']}"
        src = "outputs/main_targets.csv"
    else:
        val = float([f for f in fit if f["model"] == "model_CTB"][0]["nobs"]); concl = abs(val - pv) <= 5
        note = "nobs(model_CTB); nobs(model_misinfo) = " + [f for f in fit if f["model"] == "model_misinfo"][0]["nobs"]
        src = "outputs/main_fit.csv"
    ad = val - pv; rel = ad / pv
    T.append({"id": t["id"], "description": t["description"], "paper_value": pv, "paper_rounding_decimals": dec,
              "reproduced_value": val, "source_file": src, "abs_diff": ad, "rel_diff": rel,
              "match_to_rounding": round(val, dec) == round(pv, dec), "within_5pct": abs(rel) <= 0.05,
              "same_conclusion": bool(concl), "note": note})
# Robustness
ra = {r["quantity"]: r for r in rd("Ra_bootstrap_summary.csv")}
rb = rd("Rb_cooks_summary.csv")
rc = rd("Rc_targets.csv")
a1 = ra["T1_ConspMent_CTB"]
sec_a = "; ".join(f"{k}: OR {float(v['estimate_OR']):.3f} [{float(v['ci_low_OR']):.3f}, {float(v['ci_high_OR']):.3f}]" for k, v in ra.items() if k != "T1_ConspMent_CTB")
b1 = term(rb, "model_CTB", "ConspMent_index")
sec_b = "; ".join(f"{r['model']} {r['term']}: OR {float(r['OR']):.3f}, Bonf p {float(r['p_bonf']):.3g}, dropped {r['n_dropped']}" for r in rb if not (r['model']=="model_CTB" and r['term']=="ConspMent_index"))
c1 = term(rc, "model_CTB", "ConspMent_index")
sec_c = "; ".join(f"{r['model']} {r['term']}: OR {float(r['odds_ratio']):.3f}, Bonf p {float(r['p_bonf']):.3g}" for r in rc if not (r['model']=="model_CTB" and r['term']=="ConspMent_index"))
R = [
 {"id": "R_a", "description": "Case bootstrap, 1000 resamples, set.seed(20261009), refit identical glm; OR for ConspMent_index in model_CTB; percentile 95% CI; p = min(2*share(log-odds<=0),1)",
  "ran": True, "estimate": float(a1["estimate_OR"]),
  "se_or_ci": f"percentile 95% CI OR [{float(a1['ci_low_OR']):.4f}, {float(a1['ci_high_OR']):.4f}]; bootstrap SE log-odds {float(a1['boot_se_logodds']):.4f}; non-converged {a1['n_not_converged']} of {a1['boot_n']}",
  "p_value": float(a1["p_boot"]), "same_direction_and_significance_as_paper": a1["same_direction_and_significance"] == "TRUE",
  "source_file": "outputs/Ra_bootstrap_summary.csv", "note": "Secondary: " + sec_a},
 {"id": "R_b", "description": "Drop cases with Cook's distance > 4/N from final model_CTB, refit, HC3; OR for ConspMent_index",
  "ran": True, "estimate": float(b1["OR"]),
  "se_or_ci": f"HC3 SE log-odds {float(b1['se_hc3']):.4f}; 95% CI OR [{float(b1['ci_low_OR']):.4f}, {float(b1['ci_high_OR']):.4f}]; dropped {b1['n_dropped']} of {b1['N_original']}",
  "p_value": float(b1["p_bonf"]), "same_direction_and_significance_as_paper": b1["same_direction_and_significance"] == "TRUE",
  "source_file": "outputs/Rb_cooks_summary.csv", "note": f"p_value is Bonferroni-adjusted (raw p {float(b1['p_raw']):.3g}). Secondary: " + sec_b},
 {"id": "R_c", "description": "SDO_index from the 4 items SDO1_r, SDO2, SDO3_r, SDO4 (line 1035 only), whole script rerun from set.seed(2000); OR for ConspMent_index in model_CTB",
  "ran": True, "estimate": float(c1["odds_ratio"]),
  "se_or_ci": f"HC3 SE log-odds {float(c1['se_hc3']):.4f}",
  "p_value": float(c1["p_bonf"]), "same_direction_and_significance_as_paper": (float(c1["odds_ratio"]) > 1 and float(c1["p_bonf"]) < 0.001),
  "source_file": "outputs/Rc_targets.csv", "note": f"p_value is Bonferroni-adjusted (raw p {float(c1['p_raw']):.3g}); nobs {c1['nobs']}. Secondary: " + sec_c},
]
extra = json.load(open(os.path.join(B, "scripts", "judgements.json")))  # text judgements only, no reproduced numbers
sdo = rd("diag_sdo_facts.csv")[0]; selcols = [r["selected_columns"] for r in rd("diag_sdo_selected_columns.csv")]
r14 = rd("review_row1400.csv")[0]; imp = rd("review_row1400_impact.csv")
errf = "errors_main.csv" if os.path.exists(os.path.join(O, "errors_main.csv")) else "errors_main_upto3677.csv"
errs = rd(errf)
bugs = [
 {"file": "MisinfoCT_HSK.r", "line": 1035,
  "description": "SDO_index = rowMeans(select(., starts_with('SDO'))) averages six columns (the four raw items plus the reversed copies SDO1_r and SDO3_r), so each reversed item cancels its original; the index is not the intended 4-item scale (SDO1_r, SDO2, SDO3_r, SDO4, as in the script's reliability check at line 982). SDO is a control in the T1-T4 models; R_c measures the effect.",
  "evidence": f"Columns selected just before line 1029: {', '.join(selcols)} (outputs/diag_sdo_selected_columns.csv). SDO1+SDO1_r==12 for all rows: {sdo['sdo1_plus_sdo1r_all_equal_12']}; SDO3+SDO3_r==12: {sdo['sdo3_plus_sdo3r_all_equal_12']}. On the {sdo['n_complete_sdo']} of {sdo['n_rows']} rows with all SDO items, index == 4 + (SDO2+SDO4)/6 (max abs diff {float(sdo['max_abs_diff_orig_vs_4_plus_SDO2_SDO4_over_6_complete']):.1e}); correlation with the 4-item mean {float(sdo['cor_orig_vs_4item_complete']):.3f} (outputs/diag_sdo_facts.csv)."},
 {"file": "MisinfoCT_HSK.r", "line": 1770,
  "description": "Hard-coded removal of the case with raw row name '1400' as an 'influential outlier' does not match the script's own screens in the deposited data (top-3 Cook's distance via plot(model, which = 4, id.n = 3), |std. residual| > 3). Effect on T1-T4 is below the reported rounding; it is why T5 is 2962 rather than 2963.",
  "evidence": f"outputs/review_row1400.csv: cases with |std resid|>3: {r14['n_abs_std_resid_gt3']} (max {float(r14['max_abs_std_resid']):.2f}); top-3 Cook's D row names {r14['top3_cooksd_rownames']}; row '1400' Cook's D rank {r14['rowname_1400_cooksd_rank']} of {r14['n_rows_before_removal']}, std resid {float(r14['rowname_1400_std_resid']):.3f}. Keeping it: CT OR ConspMent {float(imp[0]['OR_ConspMent']):.4f}, Truth {float(imp[0]['OR_Truth']):.4f}, N {imp[0]['nobs']} (outputs/review_row1400_impact.csv)."},
]
for r in errs:
    bugs.append({"file": "MisinfoCT_HSK.r", "line": int(r["first_line"]),
                 "description": "Runtime error when the script is run top to bottom (after all target computations; does not touch T1-T5).",
                 "evidence": f"lines {r['first_line']}-{r['last_line']}: {r['message'].strip()} (outputs/{errf}; 3142-3148: bare '-----' line 3142 is parsed as unary minus joined to the assignment at 3146; 3149 follows from it; 3153: $COVID_CTB partially matches the factor COVID_CTB_dummy)"})
extra["bugs"] = bugs
res = {"paper_id": "05_FNTC1J", "agent": "B", "run_date_ist": "2026-10-09", "ran": True, "could_not_run_reason": "",
       "targets": T, "robustness": R, "bugs": extra["bugs"], "env_fixes": extra["env_fixes"],
       "proposed_class": extra["proposed_class"], "class_reason": extra["class_reason"],
       "confidence": extra["confidence"], "confidence_reason": extra["confidence_reason"],
       "time_minutes": extra["time_minutes"], "uncertainties": extra["uncertainties"]}
# consistency guard: class A requires all targets match to rounding
if res["proposed_class"] == "A": assert all(t["match_to_rounding"] for t in T), "class A but not all targets match"
json.dump(res, open(os.path.join(B, "results.json"), "w"), indent=1, ensure_ascii=False)
print(json.dumps(T, indent=1)); print(json.dumps(R, indent=1))
