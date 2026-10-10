# Builds results.json from files in outputs/. No reproduced number is typed here.
import csv, json, os, math
A = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
O = os.path.join(A, "outputs")
REPO = os.path.dirname(os.path.dirname(os.path.dirname(A)))
targets = json.load(open(os.path.join(REPO, "papers/08_SQRZR8/targets.json")))
rows = list(csv.DictReader(open(os.path.join(O, "targets_extracted.csv"))))
get = lambda o, t: next(r for r in rows if r["outcome"] == o and r["term"] == t)
spec = {"T1": ("positive_emo_rv","surveillance_facPersonalized", -1, 0.001),
        "T2": ("negative_emo","surveillance_facPersonalized", 1, 0.01),
        "T3": ("general_attitude_fic","surveillance_facPersonalized", -1, 0.001),
        "T4": ("general_attitude_real","surveillance_facPersonalized", -1, 0.01),
        "T5": ("general_attitude_fic","censorship_facPersonalized", -1, 0.001)}
out_t = []
for t in targets:
    pv, dec = t["paper_value"], t["paper_rounding_decimals"]
    if t["id"] in spec:
        o, term, sign, alpha = spec[t["id"]]; r = get(o, term)
        rv = float(r["estimate"]); p = float(r["p_value"])
        same = (math.copysign(1, rv) == sign) and p < alpha
        note = f"lm_robust {r['se_type']} SE {float(r['se']):.6f}, p {p:.3g}, nobs {r['nobs']}; criterion sign {'+' if sign>0 else '-'} and p < {alpha}"
    else:
        ns = sorted({int(float(r["nobs"])) for r in rows if r["term"] == "surveillance_facPersonalized"})
        rv = ns[0] if len(ns) == 1 else None
        same = (abs(rv - pv) <= 5) if rv is not None else None
        note = f"nobs of all five column (1) models: {ns}; criterion |N - 4057| <= 5"
    ad = abs(rv - pv) if rv is not None else None
    rd = (rv - pv) / abs(pv) if rv is not None else None
    out_t.append({"id": t["id"], "description": t["description"], "paper_value": pv, "paper_rounding_decimals": dec,
        "reproduced_value": rv, "source_file": "outputs/targets_extracted.csv",
        "abs_diff": ad, "rel_diff": rd,
        "match_to_rounding": (round(rv, dec) == pv) if rv is not None else None,
        "within_5pct": (abs(rd) <= 0.05) if rd is not None else None,
        "same_conclusion": same, "note": note})
rob = list(csv.DictReader(open(os.path.join(O, "robustness.csv"))))
desc = {"R_a": "Case bootstrap, 1000 resamples, set.seed(20261009), lm() refit, percentile 95% CI, p = min(2 x share >= 0, 1)",
        "R_b": "Drop |z| > 3 on the outcome within the estimation sample, refit lm_robust HC2",
        "R_c": "Outcome = standardized (Secured + Happiness)/2, same lm_robust formula"}
out_r = []
for r in rob:
    est = float(r["estimate"]); p = float(r["p_value"]); lo, hi = float(r["ci_low"]), float(r["ci_high"])
    if r["check"] == "R_a": same = est < 0 and hi < 0
    else: same = est < 0 and p < 0.001
    note = f"{r['role']}; outcome {r['outcome']}; n {r['n']}"
    if r["check"] == "R_a": note += f"; invalid draws {r['dropped_or_bad']}; valid draws {r['n_valid_draws']}"
    if r["check"] == "R_b": note += f"; rows dropped {r['dropped_or_bad']}"
    out_r.append({"id": r["check"] + ("" if r["role"].startswith("primary") else "_secondary_T3"),
        "description": desc[r["check"]], "ran": True, "estimate": est,
        "se_or_ci": f"SE {float(r['se']):.6f}; 95% CI [{lo:.6f}, {hi:.6f}]" + (" (percentile)" if r["check"]=="R_a" else " (HC2)"),
        "p_value": p, "same_direction_and_significance_as_paper": same, "source_file": "outputs/robustness.csv", "note": note})
pca = list(csv.DictReader(open(os.path.join(O, "pca_loadings.csv"))))
L = {r["item"]: r for r in pca}
c1 = {"Sadness": ("Comp.1", 0.400), "Happiness": ("Comp.2", -0.659), "Secured": ("Comp.2", -0.586),
      "Curiosity": ("Comp.3", -0.635), "Surprised": ("Comp.3", -0.558)}
pca_ok = all(math.copysign(1, float(L[i][c])) == math.copysign(1, v) for i, (c, v) in enumerate([]) ) if False else \
         all(math.copysign(1, float(L[i][c])) == math.copysign(1, v) for i, (c, v) in c1.items())
pca_txt = "; ".join(f"{i} {c} {float(L[i][c]):.3f} (Table C1 {v})" for i, (c, v) in c1.items())
fig3 = json.load(open(os.path.join(O, "code_check_fig3_labels.json")))
allA = all(t["match_to_rounding"] for t in out_t)
allB = all(t["within_5pct"] and t["same_conclusion"] for t in out_t)
coef_A = all(t["match_to_rounding"] for t in out_t if t["id"] != "T6")
res = {"paper_id": "08_SQRZR8", "agent": "A", "run_date_ist": "2026-10-10", "ran": True, "could_not_run_reason": "",
 "targets": out_t, "robustness": out_r, "bugs": [],
 "env_fixes": json.load(open(os.path.join(O, "env_fixes.json"))),
 "proposed_class": None, "class_reason": None, "confidence": None, "confidence_reason": None,
 "time_minutes": json.load(open(os.path.join(O, "timing.json")))["minutes"],
 "uncertainties": [], "context": {"pca_signs_match_table_C1": pca_ok, "pca_loadings": pca_txt, "pca_source_file": "outputs/pca_loadings.csv",
   "fig3_label_mapping_consistent": fig3["all_consistent"], "fig3_source_file": "outputs/code_check_fig3_labels.json",
   "all_targets_match_to_rounding": allA, "all_targets_within_5pct_same_conclusion": allB, "T1_to_T5_match_to_rounding": coef_A}}
extra = json.load(open(os.path.join(O, "class_and_notes.json")))
res.update({k: extra[k] for k in ["proposed_class","class_reason","confidence","confidence_reason","uncertainties"]})
res["bugs"] = extra.get("bugs", [])
res["code_observations"] = extra.get("code_observations", [])
json.dump(res, open(os.path.join(A, "results.json"), "w"), indent=1)
print(json.dumps({"targets": [(t["id"], t["paper_value"], t["reproduced_value"], t["match_to_rounding"], t["within_5pct"], t["same_conclusion"]) for t in out_t],
  "rob": [(r["id"], r["estimate"], r["p_value"], r["same_direction_and_significance_as_paper"]) for r in out_r], "pca_ok": pca_ok, "ctx": res["context"]}, indent=1))
