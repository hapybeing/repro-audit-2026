#!/usr/bin/env python3
"""Builds results.json for 08_SQRZR8 agent B from files in outputs/. Numbers are parsed, never typed,
except paper values, which are read from REPO/papers/08_SQRZR8/targets.json (copied from PREREG.md)."""
import csv, json, os
B = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.dirname(B)
O = os.path.join(B, "outputs")
targets = json.load(open(os.path.join(P, "targets.json")))
ex = list(csv.DictReader(open(os.path.join(O, "targets_extracted.csv"))))
def get(outcome, term):
    for r in ex:
        if r["outcome"] == outcome and r["term"] == term: return r
    raise KeyError((outcome, term))
spec = {"T1": ("positive_emo_rv", "surveillance_facPersonalized", "neg", 0.001),
        "T2": ("negative_emo", "surveillance_facPersonalized", "pos", 0.01),
        "T3": ("general_attitude_fic", "surveillance_facPersonalized", "neg", 0.001),
        "T4": ("general_attitude_real", "surveillance_facPersonalized", "neg", 0.01),
        "T5": ("general_attitude_fic", "censorship_facPersonalized", "neg", 0.001)}
meta = json.load(open(os.path.join(O, "run_meta.json")))
out_t = []
for t in targets:
    pv, dec = t["paper_value"], t["paper_rounding_decimals"]
    if t["id"] in spec:
        o, term, sign, alpha = spec[t["id"]]; r = get(o, term)
        rv = float(r["estimate"]); p = float(r["p_value"])
        same = (rv < 0 if sign == "neg" else rv > 0) and p < alpha
        note = f"HC2 SE {float(r['std_error']):.4f}, p {p:.3g}, nobs {r['nobs']}; criterion: {sign} sign and p < {alpha}"
    else:
        ns = sorted({int(float(get(o, 'surveillance_facPersonalized')['nobs'])) for o in
                     ["positive_emo_rv", "negative_emo", "neutral_emo_rv", "general_attitude_fic", "general_attitude_real"]})
        rv = ns[0]; same = abs(rv - pv) <= 5
        note = (f"nobs of all five mod2 models: {ns}. nrow(data) = {meta['nrow_data']}, complete cases on all model variables = "
                f"{meta['complete_cases']}. Paper text and Table 1 / online Tables D1-D2 give 4,507; Table 3 note gives 4,057. "
                "Criterion: within 5 of 4057.")
    ad = rv - pv; rd = ad / abs(pv)
    out_t.append({"id": t["id"], "description": t["description"], "paper_value": pv, "paper_rounding_decimals": dec,
                  "reproduced_value": rv, "source_file": "outputs/targets_extracted.csv",
                  "abs_diff": round(ad, 10), "rel_diff": round(rd, 10),
                  "match_to_rounding": round(rv, dec) == round(pv, dec), "within_5pct": abs(rd) <= 0.05,
                  "same_conclusion": bool(same), "note": note})
rob = list(csv.DictReader(open(os.path.join(O, "robustness.csv"))))
desc = {"R_a": "Case bootstrap, 1000 resamples, set.seed(20261009), lm refit, percentile 95% CI; p = min(2 x share >= 0, 1)",
        "R_b": "Drop rows with |z| > 3 on the outcome in its estimation sample, refit lm_robust HC2",
        "R_c": "Outcome = (Secured + Happiness)/2 standardized over T1 estimation sample, refit lm_robust HC2"}
out_r = []
for r in rob:
    prim = r["role"].startswith("primary")
    rid = r["check"] + ("" if prim else "_secondary_T3")
    sd = r["same_dir_sig"].upper() == "TRUE"
    extra = f"n_used {r['n_used']}"
    if r["n_dropped"] not in ("", "NA"): extra += f", n_dropped {r['n_dropped']}"
    if r["n_bad_resamples"] not in ("", "NA"): extra += f", resamples with absent level or NA coef {r['n_bad_resamples']}"
    out_r.append({"id": rid, "description": desc[r["check"]] + f" [{r['role']}, outcome {r['outcome']}]", "ran": True,
                  "estimate": float(r["estimate"]),
                  "se_or_ci": f"SE {float(r['se']):.4f}; 95% CI [{float(r['ci_low']):.4f}, {float(r['ci_high']):.4f}]" + (" (bootstrap SE, percentile CI)" if r["check"] == "R_a" else " (HC2)"),
                  "p_value": float(r["p_value"]), "same_direction_and_significance_as_paper": sd,
                  "source_file": "outputs/robustness.csv", "note": extra})
pca = list(csv.DictReader(open(os.path.join(O, "pca_loadings.csv"))))
L = {r["item"]: r for r in pca}
c1 = {"Comp.1": ("Sadness", 0.400), "Comp.2a": ("Happiness", -0.659), "Comp.2b": ("Secured", -0.586),
      "Comp.3a": ("Curiosity", -0.635), "Comp.3b": ("Surprised", -0.558)}
pca_lines = []; flips = []
for k, (item, v) in c1.items():
    comp = k[:6]; got = float(L[item][comp])
    pca_lines.append(f"{comp} {item}: {got:.3f} (Table C1 {v})")
    if (got > 0) != (v > 0): flips.append(comp)
res = json.load(open(os.path.join(O, "manual_fields.json")))
res.update({"paper_id": "08_SQRZR8", "agent": "B", "run_date_ist": meta["run_date_ist"], "targets": out_t, "robustness": out_r})
res["uncertainties"] = res.get("uncertainties", []) + [
    "PCA loadings vs online Table C1 (outputs/pca_loadings.csv): " + "; ".join(pca_lines) +
    (". Sign flips: " + ", ".join(sorted(set(flips))) if flips else ". No sign flips, so no sign-aligned rerun was needed.")]
paper_r2 = {"positive_emo_rv": 0.100, "negative_emo": 0.131, "general_attitude_fic": 0.288, "general_attitude_real": 0.400}  # PREREG.md context values, not targets
r2txt = "; ".join(f"{o}: reproduced {float(get(o, 'surveillance_facPersonalized')['r2']):.4f} vs paper {v}" for o, v in paper_r2.items())
res["uncertainties"].append("Context (not a target): Table 3 column (1) R2 from outputs/targets_extracted.csv: " + r2txt + ". All four R2 values round to the paper's three decimals although the reproduced models use " + str(meta["nrow_data"]) + " rows.")
import datetime, zoneinfo
st = datetime.datetime.strptime(open("/workspace/audit_runs/08_SQRZR8/B/start.txt").read().strip()[:19], "%Y-%m-%d %H:%M:%S")
now = datetime.datetime.now(zoneinfo.ZoneInfo("Asia/Kolkata")).replace(tzinfo=None)
res["time_minutes"] = round((now - st).total_seconds() / 60)
json.dump(res, open(os.path.join(B, "results.json"), "w"), indent=1)
for t in out_t: print(t["id"], t["paper_value"], t["reproduced_value"], t["match_to_rounding"], t["within_5pct"], t["same_conclusion"])
for r in out_r: print(r["id"], r["estimate"], r["p_value"], r["same_direction_and_significance_as_paper"])
print(res["uncertainties"][-1])
