#!/usr/bin/env python3
"""Agent B, 14_CJISMY: build results.json from files in outputs/ (numbers parsed, never typed)."""
import csv, json, os, re
from pathlib import Path

B = Path(__file__).resolve().parents[1]
REPO = B.parents[2]
OUT = B / "outputs"
targets = json.load(open(REPO / "papers/14_CJISMY/targets.json"))

rows = list(csv.DictReader(open(OUT / "targets_extracted.csv")))
def get(model, term):
    for r in rows:
        if r["model"] == model and r["term"] == term:
            return r
    return None

levels = rows[0]["factor_levels_in_order"].split("|")
fixest_version = rows[0]["fixest_version"]

spec = {
    "T1": ("model1_full_model_h1", "resource_and_agriculture", "pos", 0.001),
    "T2": ("model3_full_model_h1_max", "resource_and_agriculture", "pos", 0.01),
    "T3": ("model2_full_model_h1_n_resources", "none_one_or_both_nats_agri_charNone", "neg", 0.01),
    "T4": ("model2_full_model_h1_n_resources", "none_one_or_both_nats_agri_charSingle", "neg", 0.001),
}
def band(p):
    for cut, lab in [(0.001, "p<0.001 (***)"), (0.01, "p<0.01 (**)"), (0.05, "p<0.05 (*)"), (0.1, "p<0.1 (.)")]:
        if p < cut:
            return lab
    return "p>=0.1"

tlist = []
for t in targets:
    tid = t["id"]; pv = t["paper_value"]; dec = t["paper_rounding_decimals"]
    e = {"id": tid, "description": t["description"], "paper_value": pv, "paper_rounding_decimals": dec}
    if tid in spec:
        model, term, sign, thr = spec[tid]
        r = get(model, term)
        if tid in ("T3", "T4") and levels[0] != "Both":
            r = None
        if r is None:
            e.update(reproduced_value=None, source_file="outputs/targets_extracted.csv", abs_diff=None, rel_diff=None,
                     match_to_rounding=None, within_5pct=None, same_conclusion=None,
                     note=f"not produced as-is; factor levels {levels}")
        else:
            est = float(r["estimate"]); p = float(r["p_fixest"]); se = float(r["se_cluster"])
            ok_sign = est > 0 if sign == "pos" else est < 0
            e.update(reproduced_value=est, source_file="outputs/targets_extracted.csv",
                     abs_diff=est - pv, rel_diff=(est - pv) / abs(pv),
                     match_to_rounding=round(est, dec) == pv, within_5pct=abs((est - pv) / pv) <= 0.05,
                     same_conclusion=bool(ok_sign and p < thr),
                     note=(f"clustered SE {se:.4f} (rounds to {round(se, 2)}); fixest coeftable p {p:.3g}, band {band(p)}; "
                           f"normal p {float(r['p_normal']):.3g}; reference level '{levels[0]}'; fixest {fixest_version}"))
    else:  # T5
        r = get("model1_full_model_h1", "resource_and_agriculture")
        n = int(float(r["nobs"]))
        e.update(reproduced_value=n, source_file="outputs/targets_extracted.csv", abs_diff=n - pv, rel_diff=(n - pv) / pv,
                 match_to_rounding=n == pv, within_5pct=abs((n - pv) / pv) <= 0.05, same_conclusion=abs(n - pv) <= 5,
                 note=f"country FE groups {r['n_fe_groups']} (paper 62); Models 2-4 nobs "
                      + ", ".join(get(m, 'n_orgs')["nobs"] for m in ["model2_full_model_h1_n_resources", "model3_full_model_h1_max", "model4_full_model_h1_n_resources_max"]))
    tlist.append(e)

# robustness
rb = list(csv.DictReader(open(OUT / "robustness.csv")))
def rrow(check, target):
    return next(r for r in rb if r["check"] == check and r["target"] == target)
desc = {
    "R_a": "Country-cluster bootstrap, 1000 resamples of the 62 countries, seed 20261010, refit with boot_id FE and clusters; T1 coefficient (Model 1)",
    "R_b": "Drop cases with Cook's distance > 4/N from lm(F1 + factor(country)) on the estimation sample (non-finite kept), refit Model 1; T1 coefficient",
    "R_c": "Model 1 without country fixed effects (pooled OLS), SE clustered by country, same estimation sample; T1 coefficient",
}
robust = []
for c in ["R_a", "R_b", "R_c"]:
    r = rrow(c, "T1_model1"); s = rrow(c, "T2_model3")
    est = float(r["estimate"]); p = float(r["p"])
    if c == "R_a":
        lo, hi = float(r["ci_low"]), float(r["ci_high"])
        same = est > 0 and lo > 0
        se_ci = f"bootstrap SD {float(r['se']):.4f}; percentile 95% CI [{lo:.4f}, {hi:.4f}]; failed draws {r['n_failed']}"
        sec = (f"Model 3 secondary: estimate {float(s['estimate']):.4f}, bootstrap SD {float(s['se']):.4f}, "
               f"CI [{float(s['ci_low']):.4f}, {float(s['ci_high']):.4f}], p {float(s['p']):.3g}")
    else:
        same = est > 0 and p < 0.05
        se_ci = f"clustered SE {float(r['se']):.4f}; N {r['n']}" + (f"; dropped {r['n_dropped']}" if r["n_dropped"] not in ("", "NA") else "")
        sec = (f"Model 3 secondary: estimate {float(s['estimate']):.4f}, SE {float(s['se']):.4f}, p {float(s['p']):.3g}, N {s['n']}"
               + (f", dropped {s['n_dropped']}" if s["n_dropped"] not in ("", "NA") else ""))
    note = f"p<0.001 also holds: {p < 0.001}. {r['note']}. {sec}".replace("..", ".")
    robust.append({"id": c, "description": desc[c], "ran": True, "estimate": est, "se_or_ci": se_ci, "p_value": p,
                   "same_direction_and_significance_as_paper": bool(same), "source_file": "outputs/robustness.csv", "note": note})

# time from LOG.md timestamps (IST hh:mm at line start "- HH:MM")
times = re.findall(r"^- (\d{2}):(\d{2})", open(B / "LOG.md").read(), re.M)
mins = [int(h) * 60 + int(m) for h, m in times]
tmin = max(mins) - min(mins) if mins else None

all_exact = all(t["match_to_rounding"] for t in tlist)
all_5 = all(t["within_5pct"] and t["same_conclusion"] for t in tlist)
cls = "A" if all_exact else ("B" if all_5 else "C")

res = {
    "paper_id": "14_CJISMY", "agent": "B", "run_date_ist": "2026-10-10", "ran": True, "could_not_run_reason": "",
    "targets": tlist, "robustness": robust,
    "bugs": [],
    "code_review_summary": ("none found. Read all of crosssection_linear.R (228 lines) and funs_and_constants.R (58 lines); "
                            "other deposited scripts were not reviewed line by line."),
    "env_fixes": [
        "diffs/crosssection_linear.R.diff: library(specr) commented out for the main run (specr not yet installed then; no specr function is called in the script; after specr 1.0.0 was installed the unmodified script gave identical results, see outputs/specr_check.txt); both marginaleffects plot blocks wrapped in try() (PREREG step 4). No model or data line changed.",
        "Data placed as data/epro_data_h1.csv, data/epro_data_h2.csv, data/epro_geo_data_h3.csv via ?format=original (deposit is flat, code reads data/). Path-only, no file edit.",
        f"Packages: fixest {fixest_version} (authors' pin) and texreg 1.38.6 (authors' pin) built from the CRAN archive into a fresh library; dplyr 1.0.9 and vctrs 0.5.1 (authors' pins) built but could not be loaded with the rest of the installed stack (see LOG.md), so system dplyr 1.1.4 / vctrs 0.6.5 were used.",
    ],
    "proposed_class": cls,
    "class_reason": ("All five Table 1 targets reproduce to the printed rounding with the authors' pinned fixest 0.11.1, with significance bands matching the printed stars; "
                     "the factor reference level is 'Both' as in the paper." if cls == "A" else "See targets."),
    "confidence": "high",
    "confidence_reason": "Deterministic OLS; data checksums match PREREG; pinned fixest and texreg used; numbers parsed by script from coeftable output.",
    "time_minutes": tmin,
    "uncertainties": [],
}
unc = res["uncertainties"]
unc.append("dplyr 1.0.9 / vctrs 0.5.1 pins were not usable together with the system tidyverse stack (vctrs 0.5.1: 'namespace vctrs 0.5.1 is already loaded, but >= 0.6.0 is required'; dplyr 1.0.9: broom.mixed needs dplyr >= 1.0.10). The factor level order (Both, None, Single) came from dplyr 1.1.4 / vctrs 0.6.5; whether the authors' dplyr 1.0.9 gives the same order was not run, but the paper's printed baseline 'Both' matches.")
fl = list(csv.DictReader(open(OUT / "factor_levels.csv")))
unc.append("Model 2 category counts in mean_h1 (all 139 groups, before the one missing-covariate drop): " + ", ".join(f"{r['level']} {r['n_groups']}" for r in fl) + " (outputs/factor_levels.csv).")
rc = rrow("R_c", "T1_model1")
unc.append(f"R_c (no country fixed effects) gives a smaller T1 coefficient {float(rc['estimate']):.4f} with p {float(rc['p']):.3g}: the H1 association in the pooled model is not significant at 0.05 (robustness only, does not change the class).")
fig = OUT / "figure2_prose_check.csv"
if fig.exists():
    fr = list(csv.DictReader(open(fig)))
    unc.append("Context check, not pre-registered as a check (PREREG section 1 notes that p. 824 prose says a min-to-max change predicts a 0.2 point increase, Figure 2 left panel, while Table 1 Model 1 prints 0.51). The Figure 2 left-panel model in the code dichotomises the predictor (Both vs None/Single): " + "; ".join(f"{r['quantity']} = {r['value']}" for r in fr) + " (outputs/figure2_prose_check.csv). So the 0.2 in the prose is close in size to the Both vs None/Single gap of the dichotomised Figure 2 model, not to the Model 1 coefficient. Described, not judged.")
if (OUT / "specr_check.txt").exists():
    unc.append("specr: " + open(OUT / "specr_check.txt").read().strip())
json.dump(res, open(B / "results.json", "w"), indent=1)
print(json.dumps({k: res[k] for k in ["proposed_class", "time_minutes"]}))
for t in tlist:
    print(t["id"], t["paper_value"], t["reproduced_value"], t["match_to_rounding"], t["same_conclusion"])
