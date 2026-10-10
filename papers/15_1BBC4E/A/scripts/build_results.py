# Builds results.json from files in outputs/ (no typed numbers except fixed pre-registered rules).
import csv, json, re, datetime
P = "/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/15_1BBC4E/"
A = P + "A/"
tg = json.load(open(P + "targets.json"))
ex = {r["id"]: float(r["value"]) for r in csv.DictReader(open(A + "outputs/targets_extracted.csv"))}
rob = json.load(open(A + "outputs/robustness.json"))
t3 = list(csv.DictReader(open(A + "outputs/table3_full_comparison.csv")))
BENCH = 0.73  # PREREG section 1 conclusion criterion
targets = []
for t in tg:
    i = t["id"]; pv = t["paper_value"]; dec = t["paper_rounding_decimals"]; rv = ex[i]
    ad = rv - pv; rd = ad / pv
    if i in ("T1", "T2", "T3"):
        same = (rv > 0) and (rv < BENCH)
        if i == "T1": same = same and (ex["max21"] == ex["T1"] or ex["max21"] < BENCH)
    elif i == "T4": same = abs(rd) <= 0.05
    elif i == "T5": same = rv < 0.05 * ex["T4_cand2"]
    else: same = abs(rd) <= 0.05
    note = ""
    if i == "T4": note = "T4 candidate 2 (sum of ead2 tally, Figure 3 sample) = %d, same as candidate 1." % ex["T4_cand2"]
    if i == "T5": note = "share of common sample = %.4f" % (rv / ex["T4_cand2"])
    if i == "T6": note = "T4_cand2 minus n at coded_by==0, from the same ead2 tally as T5"
    targets.append(dict(id=i, description=t["description"], paper_value=pv, paper_rounding_decimals=dec,
        reproduced_value=rv if dec else int(rv),
        source_file="outputs/targets_extracted.csv (from " + {"T4": "outputs/share_nrow_ead.txt"}.get(i, "outputs/agreement_ead2_tally.csv" if i in ("T5","T6") else "outputs/corr_ea_fullprec.csv") + ")",
        abs_diff=ad, rel_diff=rd, match_to_rounding=round(rv, dec) == pv, within_5pct=abs(rd) <= 0.05, same_conclusion=same, note=note))
ra, rb, rc = rob["R_a"], rob["R_b"], rob["R_c"]
f = lambda x: "%.4f" % x
robust = [
 dict(id="R_a", description="Country-cluster bootstrap (Final_Code), 1000 resamples, set.seed(20261010), pairwise-complete Pearson matrix; T1 primary", ran=True,
      estimate=ra["estimate"], se_or_ci="95%% percentile CI [%s, %s]; bootstrap SE %s" % (f(ra["ci_lo"]), f(ra["ci_hi"]), f(ra["boot_se"])),
      p_value=ra["p_value"], same_direction_and_significance_as_paper=ra["same"], source_file="outputs/robustness.json; outputs/R_a_bootstrap_draws.csv",
      note="%d clusters (123 rows with missing Final_Code excluded from the pool; they enter no pair). Undefined T1 resamples: %d. Share of resamples with T1 >= 0.73: %s. p = min(2 x share T1 <= 0, 1). Secondary CIs: T2 [%s, %s], T3 [%s, %s], largest pair [%s, %s] (share >= 0.73: %s), median [%s, %s]." % (
        ra["n_clusters"], ra["n_undefined"], ra["share_T1_ge_0.73"], f(ra["T2_ci"][0]), f(ra["T2_ci"][1]), f(ra["T3_ci"][0]), f(ra["T3_ci"][1]),
        f(ra["max21_ci"][0]), f(ra["max21_ci"][1]), ra["share_max21_ge_0.73"], f(ra["median21_ci"][0]), f(ra["median21_ci"][1]))),
 dict(id="R_b", description="Influential-country exclusion: drop top 1% (ceiling, min 1) of countries by |leave-one-country-out change in T1|, recompute 7x7 matrix", ran=True,
      estimate=rb["estimate"], se_or_ci="cor.test 95%% CI [%s, %s]" % (f(rb["ci_lo"]), f(rb["ci_hi"])), p_value=rb["p_value"],
      same_direction_and_significance_as_paper=rb["same"], source_file="outputs/robustness.json; outputs/R_b_loco_T1.csv",
      note="%d of %d countries dropped: %s (Final_Code %s), %d country-years in total, %d with an ARD-AoW pair; n = %d. T2 %s, T3 %s, largest pair %s (%s), median %s. p printed as 0 means below double precision." % (
        rb["n_dropped"], rb["n_countries_ranked"], ", ".join(rb["dropped_names"]), ", ".join(str(x) for x in rb["dropped_Final_Code"]),
        rb["dropped_country_years_all_rows"], rb["dropped_country_years_with_ARD_AoW_pair"], rb["n"], f(rb["T2"]), f(rb["T3"]), rb["max_pair"], f(rb["max21"]), f(rb["median21"]))),
 dict(id="R_c", description="Listwise common sample (all seven PDA dummies non-missing) instead of pairwise-complete observations", ran=True,
      estimate=rc["estimate"], se_or_ci="cor.test 95%% CI [%s, %s]" % (f(rc["ci_lo"]), f(rc["ci_hi"])), p_value=rc["p_value"],
      same_direction_and_significance_as_paper=rc["same"], source_file="outputs/robustness.json; outputs/R_c_listwise_matrix.csv",
      note="N = %d. T2 %s, T3 %s, median %s. Largest pair here is %s (%s), not ARD-AoW; still below 0.73. p printed as 0 means below double precision." % (
        rc["N"], f(rc["T2"]), f(rc["T3"]), f(rc["median21"]), rc["max_pair"], f(rc["max21"]))),
]
n3 = sum(r["match_3dp"] == "True" for r in t3)
log = open(A + "LOG.md").read()
ts = re.findall(r"(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}) IST", log)
t0 = datetime.datetime.strptime(" ".join(ts[0]), "%Y-%m-%d %H:%M"); t1 = datetime.datetime.strptime(" ".join(ts[-1]), "%Y-%m-%d %H:%M")
allA = all(t["match_to_rounding"] for t in targets)
res = dict(paper_id="15_1BBC4E", agent="A", run_date_ist="2026-10-10", ran=True, could_not_run_reason="",
  targets=targets, robustness=robust, bugs=[],
  env_fixes=["none: no author file changed (see diffs/README.md); corrr 0.4.5 and pacman 0.5.1 installed from CRAN into the per-run library"],
  proposed_class="A" if allA else "B",
  class_reason=("All six targets reproduced exactly at the paper's printed precision by running the authors' three scripts unmodified on the deposited Measures_merged.rds; all %d Table 3 cells also match to 3 dp." % n3) if allA else "Not all targets match to rounding.",
  confidence="high", confidence_reason="Deterministic computation, unmodified code, deposited input file with matching checksum; final confidence also depends on agent B agreeing.",
  time_minutes=int((t1 - t0).total_seconds() // 60),
  uncertainties=[
   "Code review: none found (bugs list empty). Read Comparison.R fully, Share_Common_Sample.R and Agreement across all.R fully; other scripts not reviewed. Unverified observation: Comparison.R lines 105, 176 and 183 relabel alphabetically ordered factor levels by position, so Figure 1 and Figure 4 labels depend on the collation locale; correct in this run (C.UTF-8, outputs/label_locale_check.csv), not tested under a locale that sorts upper case before lower case; consistent with the author's comment at line 104. Not on any target.",
   "Input is the deposited merged file; the data preparation (Merging_measures.R, needs democracyData from GitHub) was not re-run, as the PREREG plan states.",
   "Paper values come from PREREG.md, which read Table 3 from PDF-extracted text; the PDF bytes and the supplemental appendix were not available to this run.",
   "Prose values noted in PREREG (highest correlation '.63', median '.39') differ from the rounded reproduced values 0.636 and median %.4f (outputs/targets_extracted.csv); Table 3 itself matches. Consistent with truncation in the prose; not a target." % ex["median21"],
   "R_a judgment call: 123 rows with missing Final_Code (only RoW non-missing, so they enter no correlation) were left out of the bootstrap cluster pool; with them as an extra cluster the random draws would differ.",
   "R_b/R_c p-values are below double precision and stored as 0; R_a p = 0 means no bootstrap resample had T1 <= 0.",
   "No version pins in the deposit; current CRAN/Debian versions used (corrr 0.4.5)."])
json.dump(res, open(A + "results.json", "w"), indent=1)
print(json.dumps({k: res[k] for k in ("proposed_class", "time_minutes")}), [(t["id"], t["paper_value"], t["reproduced_value"], t["match_to_rounding"], t["same_conclusion"]) for t in targets])
