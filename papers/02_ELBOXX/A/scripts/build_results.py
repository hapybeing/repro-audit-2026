#!/usr/bin/env python3
"""Build results.json for 02_ELBOXX Agent A from files in outputs/ (no hand-typed numbers).
paper_value / rounding come from ../targets.json (copied from PREREG.md)."""
import csv, json, re, os
A = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
O = os.path.join(A, "outputs")
targets = json.load(open(os.path.join(os.path.dirname(A), "targets.json")))
def rows(f): return list(csv.DictReader(open(os.path.join(O, f))))
def facts(f): return {r["fact"]: r["value"] for r in rows(f)}
rec = "targets_pathA_faketime20250506.csv"
pa = {r["test"]: r for r in rows(rec)}
pb = {r["test"]: r for r in rows("targets_pathB.csv")}
pc = {r["test"]: r for r in rows("targets_pathA_clock2026.csv")}
src = {"T1": ("M2_test2_pubdef1", "r"), "T2": ("M2_test2_pubdef1", "ci_low"), "T3": ("M2_test2_pubdef1", "ci_high"),
       "T4": ("M1_test1_all", "r"), "T5": ("M1_test1_all", "ci_low")}
out_t = []
for t in targets:
    test, col = src[t["id"]]
    v = float(pa[test][col]); pv = t["paper_value"]; k = t["paper_rounding_decimals"]
    p = float(pa[test]["p"]); est = float(pa[test]["r"])
    vb = float(pb[test][col]); vc = float(pc[test][col])
    note = (f"Path A run of record (authors' code unchanged, clock set to 2025-05-06 with faketime), N={pa[test]['n']}, "
            f"df={pa[test]['df']}, p={p:.3g}. Path B (shipped RData) = {vb:.10g} "
            f"(match_to_rounding {round(vb, k) == pv}). Path A with real clock 2026-10-09 = {vc:.10g}, N={pc[test]['n']} "
            f"(rel diff {(vc - pv) / pv:+.4f}).")
    if t["id"] in ("T2", "T3"):
        note += (" Journal CI digits could not be read directly (Wiley HTML drops the bracket; PDF blocked). "
                 "Author preprint (peterbils.com 2024-06) reads [0.1317, 0.1935], agreeing with PREREG.")
    if t["id"] == "T5":
        note += (" Journal CI digits could not be read directly from any open copy; the 2024-06 author preprint has an older "
                 "M1 result (0.05132, [0.0363, 0.0662]), so it cannot confirm T5. Value as in PREREG.")
    out_t.append({"id": t["id"], "description": t["description"], "paper_value": pv, "paper_rounding_decimals": k,
        "reproduced_value": v, "source_file": "outputs/" + rec, "abs_diff": abs(v - pv), "rel_diff": (v - pv) / pv,
        "match_to_rounding": round(v, k) == pv, "within_5pct": abs((v - pv) / pv) <= 0.05,
        "same_conclusion": (est > 0 and p < 0.05), "note": note})
rob = {r["check"]: r for r in rows("robustness_pathA_faketime20250506.csv")}
def f(x): return None if x in ("", "NA") else float(x)
desc = {"R_a": "Nonparametric bootstrap of M2 Pearson r, 1000 row resamples of pubdef (pub_def == 1), seed 20261009, percentile 95% CI",
        "R_b": "Drop rows of pubdef with |z| > 3 on disputes or secret_alliances (sample mean/sd), rerun cor.test",
        "R_c": "OLS disputes ~ secret_alliances on pubdef, slope tested with year-clustered SE (vcovCL, HC1)"}
out_r = []
for k in ("R_a", "R_b", "R_c"):
    r = rob[k]; est = f(r["estimate"]); lo, hi = f(r["ci_low"]), f(r["ci_high"]); p = f(r["p"])
    if k == "R_a":
        se = f"bootstrap SE {f(r['se']):.6g}; percentile 95% CI [{lo:.6g}, {hi:.6g}]"; same = est > 0 and lo > 0
    elif k == "R_b":
        se = f"95% CI [{lo:.6g}, {hi:.6g}]; n={r['n']}; dropped {r['n_dropped']}"; same = est > 0 and p < 0.05
    else:
        se = f"clustered SE {f(r['se']):.6g}; 95% CI [{lo:.6g}, {hi:.6g}]"; same = est > 0 and p < 0.05
    out_r.append({"id": k, "description": desc[k], "ran": True, "estimate": est, "se_or_ci": se, "p_value": p,
                  "same_direction_and_significance_as_paper": same, "source_file": "outputs/robustness_pathA_faketime20250506.csv",
                  "note": r["note"]})
S1, S2 = rob["S1"], rob["S2"]
mid = facts("mid_direction_check.csv"); cr = facts("code_review_facts.csv")
cmpd = rows("compare_d_rebuilt_vs_shipped.csv")
fa_ident = all(r["identical_values"] == "TRUE" for r in cmpd if r["comparison"].startswith("pathA_faketime"))
bugs = [{"file": "analysis_data_creation.R", "line": 81,
  "description": "disputes counts dyadic MIDs initiated BY the country, not 'initiated against' it as the code comment (line 84) and the paper text state. Lines 81-82 keep rows with stateb == country and dyad_rolea == 3 (state A is the dyadic target), so the country (state B) is the dyadic initiator.",
  "evidence": (f"dyadic_mid_4.02.csv is directed (share of rows with a mirror row = {mid['share_rows_with_mirror_row']}); "
               f"codebook DYAD_ROLEA: 1 = initiator, 3 = target; among the {mid['code_selection_rows']} rows the code keeps, dyad_roleb values = {mid['code_selection_dyad_roleb_values']}. "
               f"Example rows: {mid['example_first_dispute']}. Information only: recounting with the country as target gives M2 r = {float(mid['info_M2_with_country_as_target_r']):.4f} "
               f"(CI {mid['info_M2_with_country_as_target_ci']}, p = {float(mid['info_M2_with_country_as_target_p']):.2g}) and M1 r = {float(mid['info_M1_with_country_as_target_r']):.4f}; "
               "same sign and significance as the paper. Details: outputs/code_review.md, outputs/mid_direction_check.csv.")}]
all_match = all(t["match_to_rounding"] for t in out_t)
res = {"paper_id": "02_ELBOXX", "agent": "A", "run_date_ist": "2026-10-09", "ran": True, "could_not_run_reason": "",
  "targets": out_t, "robustness": out_r, "bugs": bugs,
  "env_fixes": ["diffs/README.md: no author file changed. Original CSVs downloaded with ?format=original; working directory set to the file folder.",
                "diffs/README.md: process clock set to 2025-05-06 with faketime, because peacesciencer::create_stateyears(mry = TRUE) ends the frame at Sys.Date() year minus 1; with the real 2026 clock N becomes 17706 and T4/T5 move (T1-T3 unchanged).",
                "diffs/README.md: logr 1.3.8, common 1.1.3, peacesciencer 1.1.0 pinned via remotes::install_version; R 4.5.0 vs authors' 4.3.3; minor tidyverse component drift."],
  "proposed_class": "A" if all_match else "B",
  "class_reason": ("All five targets match the paper to its rounding with the authors' unchanged code in a clean library with pinned versions "
                   f"and the clock set to the authors' run date (rebuilt data identical to shipped data: {fa_ident}); the shipped RData gives the same numbers."),
  "confidence": "medium",
  "confidence_reason": "Exact match by script, but it needed an environment judgement (faketime) and the journal's CI digits (T2, T3, T5) could not be read from the journal itself; A/B agreement not yet known.",
  "time_minutes": None,
  "uncertainties": [
    "Without the clock fix (real date 2026-10-09) T4 and T5 do not match: see target notes; class would be B (T4 rel diff about +2.7%, T5 about +3.9%). I judged the clock setting an environment fix because no code changes and the authors' LOG.pdf shows the run date 2025-05-06.",
    "Journal CI digits: Wiley HTML (web_fetch) drops the CI brackets; pdfdirect and /pdf/ failed; curl got HTTP 403. T2/T3 agree with the author preprint (peterbils.com 2024-06) and with an exa.ai index excerpt of the journal text. T5 ([.03963]) could not be confirmed from any open copy I read; the preprint has an older M1 result (0.05132).",
    f"R_b (outlier exclusion) changes the significance conclusion of M2: r = {f(rob['R_b']['estimate']):.4f}, p = {f(rob['R_b']['p']):.2f} after dropping {rob['R_b']['n_dropped']} rows. R_a and R_c keep a positive significant estimate.",
    f"S1 (pub_def >= 1, n={S1['n']}): r = {f(S1['estimate']):.4f}, CI [{f(S1['ci_low']):.4f}, {f(S1['ci_high']):.4f}], p = {f(S1['p']):.2g}. S2 (year <= 2014, n={S2['n']}): r = {f(S2['estimate']):.4f}, p = {f(S2['p']):.2g}.",
    f"pub_def == 1 filter (replication.R line 24) keeps {cr['rows_pub_def_eq1']} country-years with exactly one public defensive alliance; the paper's sample wording ('member of a public defensive alliance') would give {cr['rows_pub_def_ge1']} rows (pub_def max {cr['max_pub_def']}). Whether '== 1' is intended cannot be determined; recorded as a discrepancy, not a bug.",
    f"M1 text says 'defensive secret alliances' and a yearly MID sum; code uses all secret alliances (secret, not secret_def) at country-year level. Information only: with yearly secret_def r = {float(cr['cor_M1_using_secret_def_sum']):.4f}; a system-year version ({cr['n_system_years']} years) gives r = {float(cr['cor_M1_system_year_level']):.4f}. Reported number matches the code; intent undeterminable; not counted as a bug.",
    f"secret_alliances counts alliance memberships (an alliance with k members counts k times), not distinct alliances ({cr['years_where_secret_alliances_ne_distinct_count']} years differ). Information only: distinct count gives M2 r = {float(cr['cor_M2_using_distinct_secret_count']):.4f}.",
    "Paper says MIDs 5.0; code uses dyadic MID 4.02 (ends 2014), so 2015-2024 country-years have disputes = 0 by construction. Documented in the code; not a bug.",
    "README names AJPS_rep.RData and codebook.pdf; the Dataverse has AJPS_analysis_data.RData and no project codebook. Did not block reproduction.",
    "peacesciencer 1.1.0 pulled stevemisc 1.9.0 (current CRAN); the authors' stevemisc version is not recorded. No effect seen (rebuilt data identical to shipped).",
    "The sandbox was recycled mid-run (R removed and reinstalled by another agent's setup_env.sh); the first as-is run (runA) happened before the recycle, the wrapper runs after. Both real-clock runs gave the same numbers."]}
log = open(os.path.join(A, "LOG.md")).read()
times = re.findall(r"^- (\d\d):(\d\d) ", log, re.M)
if times:
    m = [int(h) * 60 + int(mm) for h, mm in times]; res["time_minutes"] = max(m) - min(m)
json.dump(res, open(os.path.join(A, "results.json"), "w"), indent=1)
print(json.dumps({"class": res["proposed_class"], "targets": [(t["id"], t["paper_value"], t["reproduced_value"], t["match_to_rounding"]) for t in out_t],
                  "rob": [(r["id"], r["estimate"], r["p_value"], r["same_direction_and_significance_as_paper"]) for r in out_r], "time": res["time_minutes"]}, indent=0))
