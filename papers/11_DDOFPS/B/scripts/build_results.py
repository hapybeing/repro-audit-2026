"""Agent B: build results.json for 11_DDOFPS from files in outputs/ (no hand-typed estimates)."""
import csv, json, re, os, datetime
B = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(B)))
O = lambda f: os.path.join(B, "outputs", f)
def load(v):
    return {r["quantity"]: r["value"] for r in csv.DictReader(open(O(f"targets_extracted_{v}.csv")))}
v1, v2 = load("v1"), load("v2")
tg = json.load(open(os.path.join(REPO, "papers/11_DDOFPS/targets.json")))
rob = json.load(open(O("robustness.json")))
f = lambda d, k: float(d[k])
src = {"T1": "T1_sum_df_programas", "T2": "statcor_r_2002", "T3": "statcor_r_2018", "T4": "T4_obs_2018_Sim", "T5": "T5_obs_13_Sim", "T6": "T6_expected_13_Sim"}
# same-conclusion criteria (PREREG section 1)
def concl(d):
    r02, r18 = f(d, "statcor_r_2002"), f(d, "statcor_r_2018")
    corr_ok = r02 > 0 and f(d, "statcor_p_2002") < 0.05 and r18 > 0 and f(d, "statcor_p_2018") < 0.05 and r18 > r02
    return {"T1": abs(f(d, "T1_sum_df_programas") - 9439) <= 6, "T2": corr_ok, "T3": corr_ok,
            "T4": f(d, "T4_obs_2018_Sim") > f(d, "T4_expected_2018_Sim") and f(d, "T4_chisq_p") < 0.001,
            "T5": f(d, "T5_obs_13_Sim") > f(d, "T6_expected_13_Sim"), "T6": f(d, "T5_obs_13_Sim") > f(d, "T6_expected_13_Sim")}
c1, c2 = concl(v1), concl(v2)
notes = {
 "T1": "nrow(bd_doxa_programas) = %s; per year 1998..2018 = %s" % (v1["T1_nrow_bd_doxa_programas"], ", ".join(v1["T1_programas_%d" % y] for y in range(1998, 2019, 4))),
 "T2": "stat_cor r is itself rounded to 2 decimals by ggpubr; cor.test cross-check r = %s, p = %s, n = %s" % (v1["cortest_r_2002"], v1["cortest_p_2002"], v1["n_teste_2_2002"]),
 "T3": "cor.test cross-check r = %s, p = %s, n = %s" % (v1["cortest_r_2018"], v1["cortest_p_2018"], v1["n_teste_2_2018"]),
 "T4": "expected 2018 Sim = %s (paper note 9 says 16); chisq = %s, df = %s, p = %s" % (v1["T4_expected_2018_Sim"], v1["T4_chisq_statistic"], v1["T4_chisq_df"], v1["T4_chisq_p"]),
 "T5": "MDB (15) observed %s; parties in table: %s" % (v1["tab_party_APE3_obs_15_Sim"], v1["parties_in_partidos_sel"]),
 "T6": "MDB (15) expected %s; test2 p = %s" % (v1["tab_party_APE3_exp_15_Sim"], v1["test2_chisq_p"]),
}
targets = []
for t in tg:
    i = t["id"]; pv = t["paper_value"]; dec = t["paper_rounding_decimals"]; rv = f(v1, src[i])
    ad = rv - pv; rd = ad / pv
    same_v2 = f(v2, src[i]) == rv
    targets.append({"id": i, "description": t["description"], "paper_value": pv, "paper_rounding_decimals": dec,
        "reproduced_value": rv, "source_file": "outputs/targets_extracted_v1.csv",
        "abs_diff": round(ad, 10), "rel_diff": round(rd, 10), "match_to_rounding": round(rv, dec) == pv,
        "within_5pct": abs(rd) <= 0.05, "same_conclusion": c1[i],
        "note": notes[i] + "; v2 programs file gives %s (outputs/targets_extracted_v2.csv)%s" % (v2[src[i]], "" if same_v2 else " DIFFERENT")})
Ra, Rb, Rc, Ex = rob["R_a"], rob["R_b"], rob["R_c"], rob["exploratory_party45"]
robust = [
 {"id": "R_a", "description": "Stratified (by ano) case bootstrap of teste_2, seed 20261010, 2000 resamples; Pearson r(2018)", "ran": True,
  "estimate": Ra["estimate"], "se_or_ci": "95%% percentile CI [%.4f, %.4f]; bootstrap SE %.4f" % (Ra["ci_low"], Ra["ci_high"], Ra["boot_se"]),
  "p_value": Ra["p_value"], "same_direction_and_significance_as_paper": Ra["estimate"] > 0 and Ra["ci_low"] > 0,
  "source_file": "outputs/robustness.json", "note": "p is min(2*share r<=0,1) over 2000 draws, i.e. < 1/2000 when 0. Share of resamples with r(2018) > r(2002): %s. Original r(2018)-r(2002) = %.4f" % (Ra["share_r2018_gt_r2002"], Ra["diff_2018_2002"])},
 {"id": "R_b", "description": "Drop rows with |z| > 3 of VR_RECEITA_total within year; Pearson r(2018)", "ran": True,
  "estimate": Rb["estimate"], "se_or_ci": "95%% CI (cor.test) [%.4f, %.4f]" % tuple(Rb["ci"]), "p_value": Rb["p_value"],
  "same_direction_and_significance_as_paper": Rb["estimate"] > 0 and Rb["p_value"] < 0.05, "source_file": "outputs/robustness.json",
  "note": "Rows dropped per year: " + ", ".join("%s: %d" % (y, v["n_dropped"]) for y, v in Rb["by_year"].items()) + "; r by year: " + ", ".join("%s: %.3f" % (y, v["r"]) for y, v in Rb["by_year"].items()) + "; r(2018)-r(2002) = %.4f" % Rb["diff_2018_2002"]},
 {"id": "R_c", "description": "Spearman rank correlation (exact = FALSE) per year on teste_2; rho(2018)", "ran": True,
  "estimate": Rc["estimate"], "se_or_ci": "", "p_value": Rc["p_value"],
  "same_direction_and_significance_as_paper": Rc["estimate"] > 0 and Rc["p_value"] < 0.05, "source_file": "outputs/robustness.json",
  "note": "rho by year: " + ", ".join("%s: %.3f" % (y, v["rho"]) for y, v in Rc["by_year"].items()) + "; rho(2018)-rho(2002) = %.4f (secondary: the increase over time seen with Pearson is not seen with Spearman)" % Rc["diff_2018_2002"]},
]
log = open(os.path.join(B, "LOG.md")).read()
st = re.search(r"START: (\S+ \S+)", log).group(1); en = re.search(r"END: (\S+ \S+)", log).group(1)
mins = (datetime.datetime.strptime(en, "%Y-%m-%d %H:%M") - datetime.datetime.strptime(st, "%Y-%m-%d %H:%M")).seconds // 60
allA = all(t["match_to_rounding"] for t in targets)
res = {"paper_id": "11_DDOFPS", "agent": "B", "run_date_ist": st.split()[0], "ran": True, "could_not_run_reason": "",
 "targets": targets, "robustness": robust,
 "bugs": [],
 "code_review": "none found. Read all 270 lines of 'Análise dos Dados Nota Técnica.R'. Unverified observation: line 177 entry '´45' (byte 0xB4 + '45') matches no row; %s rows have numpartido 45 and are left out of Figura 5. The paper's Figura 5 legend also omits 45 (per PREREG), so intent cannot be confirmed. Exploratory (not pre-registered) run with '45': PT observed %s vs expected %.2f, observed > expected still holds (outputs/robustness.json, exploratory_party45)." % (v1["n_rows_party45_in_bd"], Ex["obs_13_Sim"], Ex["expected_13_Sim"]),
 "env_fixes": ["diffs/file_name_mapping_v1.diff: script reads bd_doxa_programas.xlsx / bd_doxa_candidatos.xlsx, deposited as bd_doxa_programas_HGPE.xlsx / bd_doxa_candidatos_HGPE.xlsx; copied under script names (pre-registered path fix)",
               "diffs/file_name_mapping_v2_alternative.diff: labelled alternative run with bd_doxa_programas_HGPE_v2.xlsx",
               "diffs/analise_dos_dados_theme_ipsum_tw.diff: theme_ipsum_tw() absent from hrbrthemes 0.9.3 and 0.8.7 (CRAN); cosmetic call on line 53 made non-fatal via tryCatch, as PREREG allows (Figura 1, no target)",
               "Script sourced with encoding = 'latin1' via scripts/run_authors.R (wrapper, no edit)"],
 "proposed_class": "A" if allA else "B",
 "class_reason": ("All six targets match the paper to its printed rounding with the pre-registered primary file (bd_doxa_programas_HGPE.xlsx); the v2 programs file gives identical values, so the alternative class is the same. Only path and cosmetic environment fixes were needed." if allA else "Not all targets match to rounding; see targets."),
 "alternative_class_v2": "A" if all(round(f(v2, src[t["id"]]), t["paper_rounding_decimals"]) == t["paper_value"] for t in tg) else "B",
 "same_conclusion_v2": c2,
 "confidence": "medium",
 "confidence_reason": "Numbers matched by script and v1/v2 agree; judgement remains on whether the renamed input files count as an environment fix (batch decision #1 says yes) and on Agent A agreement, which B cannot see; package versions are current CRAN, not the authors' (unpinned).",
 "time_minutes": mins,
 "uncertainties": [
   "Input files are not deposited under the names the script reads; class A rests on batch3_class_decisions.md #1 treating the mapping as a path-only fix. A reading of the materials as unclear would give C.",
   "theme_ipsum_tw() could not be found in CRAN hrbrthemes 0.9.3 or 0.8.7; Figura 1 styling differs from the authors' (no target affected).",
   "T2/T3 pre-registered statistic is ggpubr stat_cor's r, which ggpubr rounds to 2 decimals; the full-precision cor.test values (0.4475, 0.7152) also round to the printed values.",
   "Paper note 9 expected 2018 APE4 count 16 vs code 16.87 (rounds to 17); secondary, not a target.",
   "Figura 4 p-value wording 'p-valor > 0,001': code p = %s, consistent with reading (1) p < 0.001." % v1["T4_chisq_p"],
   "Robustness R_b and R_c keep r(2018) positive and significant, but the secondary claim of a stronger correlation over time is weaker after outlier exclusion and reversed under Spearman.",
   "The paper text was not re-read by Agent B (SciELO blocks scripted access); paper values taken from PREREG.md.",
   "Package versions are current CRAN / Debian (ggplot2 4.0.3, ggpubr 0.6.0, rio 1.2.3); the deposit pins none."]}
json.dump(res, open(os.path.join(B, "results.json"), "w"), indent=1, ensure_ascii=False)
print(json.dumps({k: res[k] for k in ["proposed_class", "alternative_class_v2", "time_minutes"]}))
for t in targets: print(t["id"], t["paper_value"], t["reproduced_value"], t["match_to_rounding"], t["same_conclusion"])
for r in robust: print(r["id"], r["estimate"], r["p_value"], r["same_direction_and_significance_as_paper"])
