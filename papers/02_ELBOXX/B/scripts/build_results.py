"""Build results.json for 02_ELBOXX, Agent B, from files in outputs/. No reproduced number is typed here."""
import csv, json, math, os, sys
B = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO_PAPER = os.path.dirname(B)
targets_def = json.load(open(os.path.join(REPO_PAPER, "targets.json")))  # paper values copied from PREREG.md

def rd(p): return list(csv.DictReader(open(os.path.join(B, p))))
ext = {(r["route"], r["test"]): r for r in rd("outputs/targets_extracted.csv")}
asis = {(r["route"], r["test"]): r for r in rd("outputs/pathA_asis/targets_asis.csv")}
rob = {r["id"]: r for r in rd("outputs/robustness_results.csv")}
facts = {r["key"]: r["value"] for r in rd("outputs/code_review_facts.csv")}
diag = {r["label"]: r for r in rd("outputs/code_review_diagnostic_correlations.csv")}

MAP = {"T1": ("M2", "r"), "T2": ("M2", "ci_lo"), "T3": ("M2", "ci_hi"), "T4": ("M1", "r"), "T5": ("M1", "ci_lo")}
REC = "A_fixed_date2025"
targets = []
for t in targets_def:
    test, field = MAP[t["id"]]
    row = ext[(REC, test)]
    v = float(row[field]); pv = t["paper_value"]; dec = t["paper_rounding_decimals"]
    ad = v - pv; rel = ad / pv
    sig = float(row["p"]) < 0.05 and float(row["r"]) > 0 and float(row["ci_lo"]) > 0
    a = asis[("A_asis_date2026", test)][field]; b = ext[("B_shortcut", test)][field]
    targets.append(dict(id=t["id"], description=t["description"], paper_value=pv, paper_rounding_decimals=dec,
        reproduced_value=v, source_file="outputs/targets_extracted.csv (route A_fixed_date2025; log in outputs/pathA_fixed/replication.log)",
        abs_diff=ad, rel_diff=rel, match_to_rounding=round(v, dec) == round(pv, dec),
        within_5pct=abs(rel) <= 0.05, same_conclusion=sig,
        note=(f"Path A of record = authors' code unchanged, clock set to 2025-05-06 (env fix). "
              f"As-is run with 2026 clock: {a} (outputs/pathA_asis/targets_asis.csv, n={asis[('A_asis_date2026', test)]['n']}). "
              f"Path B shortcut (shipped RData): {b} (n={ext[('B_shortcut', test)]['n']}). "
              f"Route A n={row['n']}, t={float(row['t']):.6g}, df={row['df']}, p={float(row['p']):.4g}.")))

def bool_or_none(x): return x
robust = []
desc = {"R_a": "Nonparametric bootstrap of Pearson r on pubdef (pub_def == 1), 1000 reps, seed 20261009, percentile 95% CI",
        "R_b": "Drop rows with |z| > 3 on disputes or secret_alliances within pubdef, rerun cor.test",
        "R_c": "OLS disputes ~ secret_alliances on pubdef with year-clustered HC1 SE (sandwich::vcovCL)"}
for k in ["R_a", "R_b", "R_c"]:
    r = rob[k]; est = float(r["estimate"]); lo = float(r["ci_lo"]); hi = float(r["ci_hi"])
    p = None if r["p_value"] in ("", "NA") else float(r["p_value"])
    same = est > 0 and lo > 0 and (p is None or p < 0.05)
    se = "" if r["se"] in ("", "NA") else f"SE {float(r['se']):.6g}; "
    robust.append(dict(id=k, description=desc[k], ran=True, estimate=est,
        se_or_ci=f"{se}95% CI [{lo:.6g}, {hi:.6g}]", p_value=p,
        same_direction_and_significance_as_paper=same, source_file="outputs/robustness_results.csv",
        note=f"n={r['n']}" + ("" if r["n_dropped"] in ("", "NA") else f", dropped={r['n_dropped']}") + f"; {r['note']}"))

s1, s2 = rob["S1"], rob["S2"]
dt = diag["M2 disputes = focal is dyadic target, rows per dyad-year as coded"]
dt1 = diag["M2 disputes = focal is dyadic target, first dyad-year only"]
bugs = [dict(file="analysis_data_creation.R", line=82,
    description=("`disputes` is meant to count MIDs initiated against the country (comment line 75: 'number of disputes initiated against'; "
                 "paper: 'MIDs initiated against that country'), but lines 81-82 keep rows where the focal country is stateb and dyad_rolea == 3, "
                 "i.e. state A (the partner) is the target, so the focal country is the dyadic initiator. The variable counts disputes the country initiated."),
    evidence=(f"Dyadic MID 4.02 is directed (every dyad in both orders: {facts['dataset_is_directed_every_dyad_both_orders']}); codebook: DYAD_ROLEA 1=Initiator, 3=Target of dyadic MID. "
              f"Of the {facts['rows_counted_total']} rows counted, {facts['counted_rows_whose_mirror_row_has_focal_as_initiator(dyad_rolea==1)']} have a mirror row coding the focal state as dyadic initiator (dyad_rolea==1) and {facts['counted_rows_whose_mirror_row_has_focal_as_target(dyad_rolea==3, unmirrored coding)']} as target. "
              f"Country-years where disputes differs from the focal-as-initiator count: {facts['n_countryyears_disputes_ne_focal_initiator_count']} of 17511 (cor {float(facts['cor_disputes_with_focal_initiator_count']):.4f}); from the focal-as-target count: {facts['n_countryyears_disputes_ne_focal_target_count']} (cor {float(facts['cor_disputes_with_focal_target_count']):.4f}). Example MID 2 (USA rolea=1 primary initiator vs UK, 1902-1903, outputs/code_review_example_mid2.csv): "
              f"disputes USA 1902 = {facts['disputes_USA_1902']}, UK 1902 = {facts['disputes_UK_1902']}. Diagnostic (not pre-registered) M2 with focal-as-target counting: "
              f"r = {float(dt['r']):.4f} [{float(dt['ci_lo']):.4f}, {float(dt['ci_hi']):.4f}], n={dt['n']}; first dyad-year only: r = {float(dt1['r']):.4f} [{float(dt1['ci_lo']):.4f}, {float(dt1['ci_hi']):.4f}] "
              f"(outputs/code_review_diagnostic_correlations.csv).")),
    dict(file="analysis_data_creation.R", line=81,
    description=("Disputes are matched on strtyr (MID start year) but the dyadic file has one row per dyad-year, so a dispute lasting k calendar years "
                 "is counted k times in its start year."),
    evidence=(f"Of the {facts['rows_counted_total']} rows with dyad_rolea == 3, {facts['rows_counted_with_durindx_gt1']} have durindx > 1 (second or later dyad-year) and are still counted in strtyr. "
              f"Example MID 2 (1902-1903): 2 rows counted for USA in 1902. Diagnostic M2 as coded but first dyad-year only: r = "
              f"{float(diag['M2 as coded but first dyad-year only']['r']):.4f} (outputs/code_review_diagnostic_correlations.csv)."))]

res = dict(paper_id="02_ELBOXX", agent="B", run_date_ist="2026-10-09", ran=True, could_not_run_reason="",
    targets=targets, robustness=robust, bugs=bugs,
    env_fixes=["diffs/run_pathA_faketime_date.diff: peacesciencer 1.1.0 create_stateyears(mry=TRUE) ends the frame at current year - 1; run unchanged code under libfaketime at 2025-05-06 (authors' LOG.pdf date) to get the authors' 1816-2024 frame (17511 rows). No authors' file edited."],
    proposed_class="A",
    class_reason=("With the clock set to the authors' run date, the unchanged code reproduces all five targets to the paper's rounding (identical to LOG.pdf and to the shipped RData). "
                  "Run as-is in 2026, T1-T3 still match exactly and T4/T5 drift (date-dependent state-year frame) but stay within 5% with the same conclusion."),
    confidence="medium",
    confidence_reason=("Numbers matched by script and the shortcut and full routes agree, but one environment fix (system date) was needed, the CI digits (T2, T3, T5) could not be read directly from the paper by B, "
                       "and code review found that the dispute variable does not measure what the text describes."),
    time_minutes=None, uncertainties=[])

res["supplementary_notes"] = dict(
    S1=f"pub_def >= 1: r={float(s1['estimate']):.4f}, 95% CI [{float(s1['ci_lo']):.4f}, {float(s1['ci_hi']):.4f}], p={float(s1['p_value']):.3g}, n={s1['n']}",
    S2=f"pub_def == 1 and year <= 2014: r={float(s2['estimate']):.4f}, 95% CI [{float(s2['ci_lo']):.4f}, {float(s2['ci_hi']):.4f}], p={float(s2['p_value']):.3g}, n={s2['n']}",
    rebuilt_vs_shipped_d=f"rebuilt {facts['rebuilt_dim']} vs shipped {facts['shipped_dim']}; per-column identical: " + ", ".join(f"{k[len('identical_col_'):]}={v}" for k, v in facts.items() if k.startswith("identical_col_")),
    diagnostics_file="outputs/code_review_diagnostic_correlations.csv (not pre-registered)")
# time from LOG.md first and last timestamps
import re
log = open(os.path.join(B, "LOG.md")).read()
ts = re.findall(r"^\- (\d\d):(\d\d) IST", log, re.M)
if ts: res["time_minutes"] = (int(ts[-1][0]) * 60 + int(ts[-1][1])) - (int(ts[0][0]) * 60 + int(ts[0][1]))
unc = json.load(open(os.path.join(B, "outputs", "uncertainties.json")))
res["uncertainties"] = unc["uncertainties"]
res["code_review_observations"] = unc["observations"]
json.dump(res, open(os.path.join(B, "results.json"), "w"), indent=1)
print(json.dumps(res, indent=1)[:6000])
