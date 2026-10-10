#!/usr/bin/env python3
"""Build results.json for 14_CJISMY agent A from files in outputs/ (numbers are never typed here)."""
import csv, json, os, re
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
O = os.path.join(D, "outputs")
T = json.load(open(os.path.join(D, "..", "targets.json")))
rows = list(csv.DictReader(open(os.path.join(O, "targets_extracted.csv"))))
def get(model, term): return next(r for r in rows if r["model"] == model and r["term"] == term)
spec = {"T1": ("full_model_h1", "resource_and_agriculture", ">", 0.001),
        "T2": ("full_model_h1_max", "resource_and_agriculture", ">", 0.01),
        "T3": ("full_model_h1_n_resources", "none_one_or_both_nats_agri_charNone", "<", 0.01),
        "T4": ("full_model_h1_n_resources", "none_one_or_both_nats_agri_charSingle", "<", 0.001)}
def band(p): return "p<0.001" if p < 0.001 else "p<0.01" if p < 0.01 else "p<0.05" if p < 0.05 else "p<0.1" if p < 0.1 else "p>=0.1"
levels = rows[0]["factor_levels"].split("|"); fxv = rows[0]["fixest_version"]
targets = []
for t in T:
    pv, dec = t["paper_value"], t["paper_rounding_decimals"]
    if t["id"] in spec:
        m, term, sign, thr = spec[t["id"]]
        r = get(m, term); est = float(r["estimate"]); p = float(r["p"])
        ok_sign = est > 0 if sign == ">" else est < 0
        same = ok_sign and p < thr
        note = f"SE {float(r['se']):.4f}; fixest coeftable p {p:.3g} ({band(p)}); normal p {float(r['p_normal']):.3g}; reference level {levels[0]}; fixest {fxv}"
        src = "outputs/targets_extracted.csv"
    else:
        r = get("full_model_h1", "resource_and_agriculture"); est = float(r["nobs"])
        same = abs(est - pv) <= 5
        note = f"nobs(full_model_h1); country FE groups {r['n_fe_groups']}; fixest {fxv}"
        src = "outputs/targets_extracted.csv"
    ad = est - pv; rd = ad / abs(pv)
    targets.append({"id": t["id"], "description": t["description"], "paper_value": pv, "paper_rounding_decimals": dec,
                    "reproduced_value": est, "source_file": src, "abs_diff": ad, "rel_diff": rd,
                    "match_to_rounding": round(est, dec) == pv if t["id"] != "T5" else est == pv,
                    "within_5pct": abs(rd) <= 0.05, "same_conclusion": bool(same), "note": note})
rb = list(csv.DictReader(open(os.path.join(O, "robustness.csv"))))
desc = {"R_a": "Country-cluster bootstrap, 1000 resamples of 62 countries, set.seed(20261010), refit feols(F1 | boot_id, cluster=~boot_id); estimate = original-sample coefficient; percentile 95% CI; p = 2 x min tail share",
        "R_b": "Exclude cases with Cook's distance > 4/N from lm(F1 + factor(countries_gwid)) (non-finite kept), refit feols(F1 | countries_gwid, cluster=~countries_gwid)",
        "R_c": "No country fixed effects: feols(F1, cluster=~countries_gwid) on the estimation sample"}
rob = []
for cid in ["R_a", "R_b", "R_c"]:
    prim = next(r for r in rb if r["check"] == cid and r["outcome"] == "disagreement")
    sec = next(r for r in rb if r["check"] == cid and r["outcome"] == "share_disagreement")
    est, se, p = float(prim["estimate"]), float(prim["se"]), float(prim["p"])
    if cid == "R_a":
        lo, hi = float(prim["ci_lo"]), float(prim["ci_hi"]); sesc = f"bootstrap SD {se:.4f}; 95% percentile CI [{lo:.4f}, {hi:.4f}]"
        same = est > 0 and lo > 0
        extra = f"successful draws {prim['n_boot_ok']}, failed {prim['n_boot_failed']}"
        sec_s = f"Model 3 secondary: est {float(sec['estimate']):.4f}, CI [{float(sec['ci_lo']):.4f}, {float(sec['ci_hi']):.4f}], p {float(sec['p']):.3g}"
    else:
        sesc = f"country-clustered SE {se:.4f}"; same = est > 0 and p < 0.05
        extra = f"N used {prim['n_used']}" + (f", dropped {prim['n_dropped']}; {prim['note']}" if cid == "R_b" else "")
        sec_s = f"Model 3 secondary: est {float(sec['estimate']):.4f}, SE {float(sec['se']):.4f}, p {float(sec['p']):.3g}, N {sec['n_used']}"
    rob.append({"id": cid, "description": desc[cid], "ran": True, "estimate": est, "se_or_ci": sesc, "p_value": p,
                "same_direction_and_significance_as_paper": bool(same), "source_file": "outputs/robustness.csv",
                "note": f"{extra}; p<0.001: {p < 0.001}; {sec_s}"})
fig = {r["item"]: float(r["value"]) for r in csv.DictReader(open(os.path.join(O, "figure2_check.csv")))}
k = [x for x in fig if x.startswith("full_model_h1_graph:resource")][0]
rob.append({"id": "X_fig2", "description": "Exploratory, not pre-registered: model behind Figure 2 left panel (full_model_h1_graph, predictor recoded Both vs None/Single), checked against the p. 824 prose '0.2 point increase'",
            "ran": True, "estimate": fig[k], "se_or_ci": f"country-clustered SE {fig['full_model_h1_graph:se']:.4f}", "p_value": fig["full_model_h1_graph:p"],
            "same_direction_and_significance_as_paper": None, "source_file": "outputs/figure2_check.csv",
            "note": f"term {k.split(':')[1]}; estimation sample values of resource_and_agriculture: 0 n={int(fig['est_sample_n_resource_and_agriculture_eq_0'])}, 0.5 n={int(fig['est_sample_n_eq_0.5'])}, 1 n={int(fig['est_sample_n_eq_1'])}. Not part of the class."})
tm = [l for l in open(os.path.join(D, "LOG.md")) if re.match(r"- 2026-10-10 \d\d:\d\d", l)]
hm = lambda l: int(l[13:15]) * 60 + int(l[16:18])
res = {"paper_id": "14_CJISMY", "agent": "A", "run_date_ist": "2026-10-10", "ran": True, "could_not_run_reason": "",
       "targets": targets, "robustness": rob,
       "bugs": [],
       "code_review_scope": "Read all of crosssection_linear.R (lines 1-221), funs_and_constants.R and 01_make_directories.R. No bug found that affects Table 1.",
       "unverified_observations": [
           {"file": "crosssection_linear.R", "line": 26, "description": "Categorical H1 variable aggregated with Mode(); with two years per group, ties are broken by first occurrence (year 2000 value). Design choice consistent with the paper's 'nominal by mode' rule; not a bug.", "evidence": "funs_and_constants.R lines 51-58 (which.max returns the first maximum)"},
           {"file": "crosssection_linear.R", "line": 180, "description": "full_model_h3_prop_no_outliers is specified identically to full_model_h3 (no outlier filter despite the name). It is not printed in any screenreg/texreg call, so no table is affected.", "evidence": "lines 162-163 vs 180-181"},
           {"file": "crosssection_linear.R", "line": 92, "description": "Figure 2 left panel model recodes resource_and_agriculture to 'Both' only when the 2000-2019 mean equals 1; groups with mean 0.5 go to 'None/Single'. Plot-only; Table 1 uses the mean.", "evidence": "outputs/figure2_check.csv"}],
       "env_fixes": ["diffs/crosssection_linear.R.diff: library(specr) commented out (not installed, unused in script); library(broom.mixed) commented out (fails to load with pinned dplyr 1.0.9, unused in script)",
                     "package versions: fixest 0.11.1, dreamerr 1.2.3, texreg 1.38.6, dplyr 1.0.9 installed per the authors' readme pins; vctrs 0.5.1 installed but removed from the path because it broke loading of broom.mixed and patchwork, system vctrs 0.6.5 used (outputs/install_logs/)",
                     "data: original CSVs downloaded with ?format=original into data/ (no code change)"],
       "proposed_class": "A" if all(t["match_to_rounding"] for t in targets) else ("B" if all(t["within_5pct"] and t["same_conclusion"] for t in targets) else "C"),
       "class_reason": "", "confidence": "high", "confidence_reason": "",
       "time_minutes": hm(tm[-1]) - hm(tm[0]) if tm else None,
       "uncertainties": []}
res["class_reason"] = ("All five Table 1 targets reproduce to the printed rounding with the authors' pinned fixest 0.11.1; the full regenerated h1 table matches Table 1 coefficients, SEs, stars, N 138, 62 countries and R2. "
                       f"Reference level of the categorical variable as built by the code is '{levels[0]}', as the paper states.")
res["confidence_reason"] = "Deterministic OLS, authors' pinned estimation package, script ran end to end with two unused library() lines removed; pending agreement with agent B."
res["uncertainties"] = [
    "vctrs 0.5.1 (readme pin) could not be used at run time; dplyr 1.0.9 with vctrs 0.6.5 is a combination the authors did not have. Estimates are deterministic OLS and match, so this is unlikely to matter.",
    "Current CRAN fixest was not run as a comparison (PREREG makes it optional, only if 0.11.1 fails to build). With 0.11.1, N is 138 with 62 country groups, so no singleton drop occurred.",
    "R_c (no country FE) gives a smaller, non-significant coefficient (see robustness); this is a pre-registered alternative specification and does not change the class.",
    "Paper p. 824 prose '0.2 point increase' (Figure 2 left) is close in size to the Figure 2 model's Both vs None/Single gap (outputs/figure2_check.csv) and to the Model 3 coefficient 0.19; which one the prose refers to cannot be settled from the code. Exploratory, not pre-registered.",
    "Not run: panel scripts and the rest of the deposit (outside PREREG scope). Session RData (21.8 MB) kept in scratch only, sha256 in outputs/session.RData.sha256."]
json.dump(res, open(os.path.join(D, "results.json"), "w"), indent=1)
print(json.dumps({"class": res["proposed_class"], "targets": [(t["id"], t["paper_value"], t["reproduced_value"], t["match_to_rounding"], t["same_conclusion"]) for t in targets],
                  "rob": [(r["id"], r["estimate"], r["p_value"], r["same_direction_and_significance_as_paper"]) for r in rob], "time": res["time_minutes"]}, indent=0))
