"""Agent B: build results.json for 13_DX5T9G from files in outputs/ (no hand-typed reproduced numbers)."""
import csv, json, os, re
from datetime import datetime
B = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
O = os.path.join(B, "outputs")
REPO = os.path.dirname(os.path.dirname(os.path.dirname(B)))
targets = json.load(open(os.path.join(REPO, "papers", "13_DX5T9G", "targets.json")))
ext = {r["id"]: r for r in csv.DictReader(open(os.path.join(O, "targets_extracted.csv")))}
mle = {r["id"]: r for r in csv.DictReader(open(os.path.join(O, "main_refit_mle.csv")))}
out_t = []
for t in targets:
    r = ext[t["id"]]; pv = t["paper_value"]; d = t["paper_rounding_decimals"]
    rep = float(r["Mean"]) if t["id"] in ("T1","T2","T3","T4") else int(float(r["N"]))
    ad = abs(rep - pv); rd = (rep - pv) / abs(pv)
    if t["id"] in ("T1","T2","T3","T4"):
        p = float(r["pvalue"]); same = (rep < 0) and (p < 0.01)
        m = mle[t["id"]]
        note = (f"Mean of 5000 parametric draws (pre-registered candidate 1). SD {float(r['SD']):.4f}, code p-value {p:.3g}. "
                f"Candidate 2 MLE coef {float(m['MLE']):.4f} (analytic SE {float(m['SE_analytic']):.4f}, Wald p {float(m['p_wald']):.3g}). "
                "Produced by the PREREG labelled fallback (m = 1, simulations skipped) after the full 03 was OOM-killed.")
    else:
        same = abs(rep - pv) <= 5; note = "N = nrow(tmp) of the main model rows."
    out_t.append({"id": t["id"], "description": t["description"], "paper_value": pv, "paper_rounding_decimals": d,
                  "reproduced_value": rep, "source_file": "outputs/targets_extracted.csv",
                  "abs_diff": round(ad, 6), "rel_diff": round(rd, 6),
                  "match_to_rounding": round(rep, d) == pv, "within_5pct": abs(rd) <= 0.05,
                  "same_conclusion": bool(same), "note": note})
def rows(f): return {r["id"]: r for r in csv.DictReader(open(os.path.join(O, f)))}
ra = rows("R_a_bootstrap_summary.csv"); rb = rows("R_b_extreme_weights.csv"); rc = rows("R_c_unweighted.csv")
rbi = {r["country"]: r for r in csv.DictReader(open(os.path.join(O, "R_b_exclusion_info.csv")))}
def sec(d, key, fmt):
    return "; ".join(f"{i}: {fmt(d[i])}" for i in ("T1","T3","T4"))
a = ra["T2"]
rob = [
 {"id": "R_a", "description": "Nonparametric case bootstrap within country, weights w held fixed, set.seed(20261010) once, 1000 resamples UK then US, weighted multinom refit; estimate = original-sample MLE; p = min(2*mean(b>=0),1); significant if 99% percentile CI excludes 0",
  "ran": True, "estimate": float(a["estimate_MLE"]),
  "se_or_ci": f"boot SE {float(a['boot_SE']):.4f}; 95% [{float(a['ci95_lo']):.3f}, {float(a['ci95_hi']):.3f}]; 99% [{float(a['ci99_lo']):.3f}, {float(a['ci99_hi']):.3f}]",
  "p_value": float(a["p_boot"]),
  "same_direction_and_significance_as_paper": float(a["estimate_MLE"]) < 0 and float(a["ci99_hi"]) < 0,
  "source_file": "outputs/R_a_bootstrap_summary.csv",
  "note": f"Primary = T2. Non-converged fits: UK {a['n_nonconverged']}, US {ra['T3']['n_nonconverged']}. Secondary: " +
          sec(ra, None, lambda r: f"MLE {float(r['estimate_MLE']):.3f}, 99% [{float(r['ci99_lo']):.3f}, {float(r['ci99_hi']):.3f}], p {float(r['p_boot']):.3g}")},
 {"id": "R_b", "description": "Drop rows with |z(w)| > 3 within country (fallback: top 1% of w if none); refit authors' main model with set.seed(1230), mvrnorm 5000, Mean/SD/pvalue (df = combined post-exclusion N)",
  "ran": True, "estimate": float(rb["T2"]["Mean"]), "se_or_ci": f"SD {float(rb['T2']['SD']):.4f}",
  "p_value": float(rb["T2"]["pvalue"]),
  "same_direction_and_significance_as_paper": float(rb["T2"]["Mean"]) < 0 and float(rb["T2"]["pvalue"]) < 0.01,
  "source_file": "outputs/R_b_extreme_weights.csv",
  "note": f"UK rule: {rbi['UK']['rule']}, dropped {rbi['UK']['rows_dropped']}; US rule: {rbi['US']['rule']}, dropped {rbi['US']['rows_dropped']}. |z|>3 on log cases: UK {rbi['UK']['info_n_absz3_logcases']}, US {rbi['US']['info_n_absz3_logcases']}; on Age: UK {rbi['UK']['info_n_absz3_age']}, US {rbi['US']['info_n_absz3_age']} (outputs/R_b_exclusion_info.csv). Secondary: " +
          sec(rb, None, lambda r: f"Mean {float(r['Mean']):.3f}, p {float(r['pvalue']):.3g}")},
 {"id": "R_c", "description": "Unweighted estimation of the main model (no weights), set.seed(1230), mvrnorm 5000, authors' Mean/SD/pvalue",
  "ran": True, "estimate": float(rc["T2"]["Mean"]), "se_or_ci": f"SD {float(rc['T2']['SD']):.4f}; MLE {float(rc['T2']['MLE']):.4f}",
  "p_value": float(rc["T2"]["pvalue"]),
  "same_direction_and_significance_as_paper": float(rc["T2"]["Mean"]) < 0 and float(rc["T2"]["pvalue"]) < 0.01,
  "source_file": "outputs/R_c_unweighted.csv",
  "note": "Secondary: " + sec(rc, None, lambda r: f"Mean {float(r['Mean']):.3f}, p {float(r['pvalue']):.3g}")},
]
sc = json.load(open(os.path.join(O, "secondary_check.json")))
cc = open(os.path.join(O, "code_checks.txt")).read()
c3 = re.findall(r"Check 3 (\w+) T_who None->WHO: mean change using combined data \(as coded, n=\d+\) ([\d.-]+); using own-country rows \(n=\d+\) ([\d.-]+)", cc)
bugs = [
 {"file": "code/06_Estimate Open.R", "line": 199,
  "description": "Footnote 20 verisimilitude probit models (mod_UK line 197-199, mod_US line 201-203) pass weights as `...$w1`, but the prepared data has no column w1 (01_Prepare data.R creates only `w`). `$w1` returns NULL, so these two bayesglm models run unweighted, unlike every other model in the deposit. Not a target.",
  "evidence": "outputs/code_checks.txt Check 2: columns of output/Prepped_survey_data.csv are X, T_health_cap, T_cases, Y, Authoritarianism, T_who, Gender_male, Age, LR, Edu_university, Country, w; is.null(subset(...)$w1) is TRUE. Lines 199 and 203."},
 {"file": "code/06_Estimate Open.R", "line": 72,
  "description": "Inside the country loop (i = 1 US, i = 2 UK) the counterfactual data for the change-in-probability simulations is `tmp_0 <- tmp_1 <- data`, the combined UK+US data, instead of the country subset `tmp` used to fit the model. Each country's effects in Figure A4 (Open_explore.pdf) are averaged over both samples' covariates. Numerically small. Not a target.",
  "evidence": "Line 72 vs lines 53-54 (tmp = country subset). outputs/code_checks.txt Check 3 (own re-run with an arbitrary seed, not the authors' draws): WHO None->WHO mean change, combined vs own-country rows: " + "; ".join(f"{c} {x} vs {y}" for c, x, y in c3)},
]
log = open(os.path.join(B, "LOG.md")).read()
ts = re.findall(r"^- (\d{4}-\d{2}-\d{2} \d{2}:\d{2})", log, re.M)
tmin = int((datetime.strptime(ts[-1], "%Y-%m-%d %H:%M") - datetime.strptime(ts[0], "%Y-%m-%d %H:%M")).total_seconds() // 60)
allA = all(t["match_to_rounding"] for t in out_t)
res = {"paper_id": "13_DX5T9G", "agent": "B", "run_date_ist": ts[0][:10], "ran": True, "could_not_run_reason": "",
 "targets": out_t, "robustness": rob, "bugs": bugs,
 "env_fixes": ["diffs/00_Run_it_all_cores.diff: registerDoMC cores 7 -> 1 for memory (PREREG allowed fix)",
               "diffs/03_Estimate_main_models_FALLBACK.diff: PREREG labelled fallback (m = 1 only, simulations skipped) after the unchanged full 03 was OOM-killed at 3.3 GB RSS",
               "diffs/00_FALLBACK_runner.diff: runner for 00 preliminaries + 01 + fallback 03 + 05",
               "package: logr 1.3.3 (authors' version) instead of 1.4.0, whose warning hook crashed read.dta13 in 01",
               "package: ebal 0.1-8 (authors' pin) via remotes::install_version",
               "package: reinstalled r-cran-readstata13 0.11.0-1 and r-cran-tmvtnorm 1.6-1+b1 (Debian) after they disappeared from the shared site library; copied directly used Debian binaries into the private run library"],
 "proposed_class": "A" if allA else "B",
 "class_reason": ("All six targets match the printed values to rounding (T1-T4 to 2 decimals as the pre-registered draw Mean, T5/T6 exactly), with negative WHO coefficients and code p < .01. "
                  "Targets came from the PREREG labelled fallback for 03 because the full 03 exceeded available memory; 01 ran unchanged.") if allA else "See targets.",
 "confidence": "high" if allA else "medium",
 "confidence_reason": "Script-matched to rounding with the authors' pinned ebal and logr; the only deviation is the pre-registered fallback, which by construction uses the same random draws as the full 03 (refit in robustness.R gives identical Mean).",
 "time_minutes": tmin,
 "uncertainties": [
   "The full 03_Estimate main models.R did not complete here (OOM at 3.3 GB RSS with about 3.1 GB available on the shared machine); targets come from the PREREG fallback. Outputs of 03's simulations, 04, 06, 07, 08 (Figures 3-6, A2-A4, Table A9, Estimates_numbers.csv) were not produced, so figure-based claims (e.g. WHO change in probability 0.13 UK, 0.11 US) were not checked.",
   "Memory gate: the brief says wait if free memory < 3 GB; the 'free' column stayed below 3 GB because about 3.9 GB was shared/tmpfs plus page cache from other processes, so MemAvailable >= 3 GB was used as the gate.",
   f"Secondary (not targets): {sc['n_who_cells_match']} of {sc['n_who_cells']} WHO cells in Tables 2-3 match the paper; 'leave open' proportions match: {sc['leave_open_match']} (outputs/secondary_check.json, Choices_prop from the unchanged 02 run).",
   f"Our regenerated Table 2 prints stars on UK All-neighbors Gender ({sc['star_observations']['UK_all_neighbors_gender_cell']}) and Ideology ({sc['star_observations']['UK_all_neighbors_ideology_cell']}), which the published table shows without stars (PREREG inconsistency 6). Values match; only the stars differ, which suggests a typesetting difference in the published table. Not a target. US Ideology (do not know), Threatened neighbors also gives {sc['star_observations']['US_threatened_ideology_dk_cell']} as printed (SD prints as 0.00).",
   "Unverified observation, 01_Prepare data.R lines 138-142: BES LR stays a factor after mapvalues and becomes character when rbind-ed with the numeric CCES LR, so the ebalance formula's LR >= 0.0 & LR <= 0.3 and LR >= 0.7 are string comparisons for UK target rows. In this C.UTF-8 locale they agree with the numeric comparison on all 2139 BES rows (outputs/code_checks.txt Check 1); under a locale whose collation ignores the minus sign (for example en_US) '-99' could sort above '0.7'. Not testable here (only C/POSIX locales installed). Weights here reproduce the targets exactly, so no effect on this run.",
   "Unverified observation, 01_Prepare data.R line 162: the 10,000 target-population rows are drawn with sample() without the CCES/BES survey weights, so the population weights carried in t_data$w are not used in entropy balancing (they are used only in 02's population descriptives). Could be intended; not a confirmed bug.",
   "pvalue in 03 uses df = nrow(data) of the combined UK+US data rather than the country N; with N about 1600 this has no practical effect on stars.",
   "The tool issued the first fallback launch twice; the duplicate failed immediately on a transient missing plyr. All reported numbers come from the single successful fallback run and the sequential robustness runs.",
 ]}
json.dump(res, open(os.path.join(B, "results.json"), "w"), indent=1)
for t in out_t: print(t["id"], t["paper_value"], t["reproduced_value"], t["match_to_rounding"], t["same_conclusion"])
for r in rob: print(r["id"], r["estimate"], r["p_value"], r["same_direction_and_significance_as_paper"])
print(res["proposed_class"], res["time_minutes"])
