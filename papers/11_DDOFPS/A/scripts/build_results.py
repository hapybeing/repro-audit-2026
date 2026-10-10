"""Builds results.json for 11_DDOFPS agent A from files in outputs/ and the frozen targets.json."""
import csv, json, re, os
from datetime import datetime

A = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAPER = os.path.dirname(A)
O = os.path.join(A, "outputs")

def load_csv(label):
    with open(os.path.join(O, f"targets_extracted_{label}.csv"), encoding="utf-8") as f:
        return {r["key"]: r["value"] for r in csv.DictReader(f)}

v1, v2 = load_csv("v1"), load_csv("v2")
targets_frozen = json.load(open(os.path.join(PAPER, "targets.json"), encoding="utf-8"))
rob = json.load(open(os.path.join(O, "robustness.json"), encoding="utf-8"))
share = list(csv.DictReader(open(os.path.join(O, "party_share_check.csv"), encoding="utf-8")))
coer = list(csv.DictReader(open(os.path.join(O, "import_coercion_check_v1.csv"), encoding="utf-8")))

keymap = {"T1": "T1_sum_df_programas", "T2": "statcor_r_2002", "T3": "statcor_r_2018",
          "T4": "T4_obs_2018_Sim", "T5": "T5_obs_13_Sim", "T6": "T6_exp_13_Sim"}

def f(d, k): return float(d[k])

# same-conclusion rules from PREREG section 1
def concl(d):
    c = {}
    c["T1"] = abs(f(d, "T1_sum_df_programas") - 9439) <= 6
    t23 = (f(d, "statcor_r_2002") > 0 and f(d, "statcor_p_2002") < 0.05 and
           f(d, "statcor_r_2018") > 0 and f(d, "statcor_p_2018") < 0.05 and
           f(d, "cortest_r_2018") > f(d, "cortest_r_2002"))
    c["T2"] = c["T3"] = t23
    c["T4"] = f(d, "T4_obs_2018_Sim") > f(d, "T4_exp_2018_Sim") and f(d, "chisq_ano_APE4_p") < 0.001
    c["T5"] = c["T6"] = f(d, "T5_obs_13_Sim") > f(d, "T6_exp_13_Sim")
    return c

def build_targets(d, label):
    cc = concl(d); out = []
    for t in targets_frozen:
        tid = t["id"]; pv = t["paper_value"]; dec = t["paper_rounding_decimals"]
        rv = f(d, keymap[tid])
        ad = rv - pv; rd = ad / pv if pv else None
        note = f"{label} mapping; key {keymap[tid]}."
        if tid in ("T2", "T3"):
            yr = "2002" if tid == "T2" else "2018"
            note += (f" stat_cor rounds r to 2 decimals; unrounded cor.test r = {d['cortest_r_'+yr]}, "
                     f"stat_cor p = {d['statcor_p_'+yr]}, n = {d['cortest_n_'+yr]}. "
                     f"Conclusion rule: r>0, p<0.05 both years and r(2018) > r(2002) (cor.test, unrounded).")
        if tid == "T4":
            note += (f" Expected 2018 Sim = {d['T4_exp_2018_Sim']} (paper note 9 prints 16); chisq = {d['chisq_ano_APE4_stat']}, "
                     f"df = {d['chisq_ano_APE4_df']}, p = {d['chisq_ano_APE4_p']} (reading (1) p < 0.001 holds; literal reading 'p > 0.001' does not). "
                     f"2018 share = {d['APE4_share_2018']}, overall share = {d['APE4_share_all']}.")
        if tid in ("T5", "T6"):
            note += (f" Parties in table: {d['party_rows_in_partidos_sel']} (45 absent, see code observation). "
                     f"MDB(15) observed {d['obs_15_Sim']}, expected {d['exp_15_Sim']}; chisq p = {d['chisq_party_APE3_p']}.")
        out.append({"id": tid, "description": t["description"], "paper_value": pv,
                    "paper_rounding_decimals": dec, "reproduced_value": rv,
                    "source_file": f"outputs/targets_extracted_{label}.csv",
                    "abs_diff": ad, "rel_diff": rd,
                    "match_to_rounding": round(rv, dec) == pv,
                    "within_5pct": abs(rd) <= 0.05 if rd is not None else None,
                    "same_conclusion": cc[tid], "note": note})
    return out

def cls(ts):
    if all(t["match_to_rounding"] for t in ts): return "A"
    if all(t["within_5pct"] and t["same_conclusion"] for t in ts): return "B"
    return None

T1 = build_targets(v1, "v1"); T2 = build_targets(v2, "v2")
c1, c2 = cls(T1), cls(T2)
identical = v1 == v2

ra, rb, rc, ex = rob["R_a"], rob["R_b"], rob["R_c"], rob["exploratory_party45"]
robust = [
    {"id": "R_a", "description": "Stratified (by ano) case bootstrap of teste_2, 2000 resamples, set.seed(20261010); Pearson r(2018), percentile 95% CI",
     "ran": True, "estimate": ra["estimate_r2018"],
     "se_or_ci": f"95% percentile CI [{ra['ci_low']}, {ra['ci_high']}], bootstrap SE {ra['boot_se']}",
     "p_value": ra["p_boot"],
     "same_direction_and_significance_as_paper": ra["estimate_r2018"] > 0 and ra["ci_low"] > 0,
     "source_file": "outputs/robustness.json",
     "note": f"Secondary: share of resamples with r(2018) > r(2002) = {ra['share_r2018_gt_r2002']}; r(2018)-r(2002) = {ra['diff_2018_2002']}, CI {ra['diff_ci']}. Draws in outputs/R_a_bootstrap_draws.csv."},
    {"id": "R_b", "description": "Drop rows with |z| > 3 on VR_RECEITA_total within each year (year mean and sd), Pearson r and cor.test per year",
     "ran": True, "estimate": rb["by_year"]["2018"]["r"],
     "se_or_ci": f"95% CI {rb['by_year']['2018']['ci']}", "p_value": rb["by_year"]["2018"]["p"],
     "same_direction_and_significance_as_paper": rb["by_year"]["2018"]["r"] > 0 and rb["by_year"]["2018"]["p"] < 0.05,
     "source_file": "outputs/robustness.json",
     "note": "Rows dropped per year: " + ", ".join(f"{y}: {rb['by_year'][y]['dropped']}" for y in rb["by_year"]) +
             ". r per year: " + ", ".join(f"{y}: {rb['by_year'][y]['r']}" for y in rb["by_year"]) +
             f". Secondary r(2018)-r(2002) = {rb['diff_2018_2002']}."},
    {"id": "R_c", "description": "Spearman rank correlation per year on teste_2 (cor.test method='spearman', exact=FALSE)",
     "ran": True, "estimate": rc["by_year"]["2018"]["rho"], "se_or_ci": "not reported by cor.test for Spearman",
     "p_value": rc["by_year"]["2018"]["p"],
     "same_direction_and_significance_as_paper": rc["by_year"]["2018"]["rho"] > 0 and rc["by_year"]["2018"]["p"] < 0.05,
     "source_file": "outputs/robustness.json",
     "note": "rho per year: " + ", ".join(f"{y}: {rc['by_year'][y]['rho']}" for y in rc["by_year"]) +
             f". Secondary rho(2018)-rho(2002) = {rc['diff_2018_2002']} (the increase over time seen with Pearson is not seen with Spearman)."},
]

dep = [r for r in share if r["filter"].startswith("deposited")][0]
w45 = [r for r in share if r["filter"] == "with 45"][0]
lost = [r for r in coer if int(r["values_lost"]) != 0]

bugs = []  # no verified bug; observations go to uncertainties
observations = [
    (f"Code observation, unverified as to intent (Análise dos Dados Nota Técnica.R line 177): the filter entry with an acute accent before 45 "
     f"matches {dep['rows_matching_literal_entry_with_accent']} rows, so party 45 ({v1['party45_rows_in_full_data']} programs) is not in the Figura 5 table. "
     f"The paper's Figura 5 legend also omits 45, so printed T5/T6 equal the deposited code's output. Deposited filter covers "
     f"{dep['share_of_all_rows']} of rows; with '45' it covers {w45['share_of_all_rows']} (text says the selected parties exceed 50%). "
     f"EXPLORATORY rerun with '45' (not pre-registered): PT expected {ex['exp_13_Sim']} vs observed {ex['obs_13_Sim']}; "
     f"chisq p {ex['p']}. Sources: outputs/party_share_check.csv, outputs/robustness.json."),
    ("Not affecting results: rio::import (readxl) guesses column types from the first rows and turns every value of "
     + ", ".join(f"{r['column']} ({r['values_lost']} values)" for r in lost)
     + " into NA; the script never uses these columns. Source: outputs/import_coercion_check_v1.csv."),
]

# time from LOG.md timestamps
log = open(os.path.join(A, "LOG.md"), encoding="utf-8").read()
times = re.findall(r"^- (\d\d:\d\d) ", log, flags=re.M)
tm = [datetime.strptime(t, "%H:%M") for t in times]
minutes = int((max(tm) - min(tm)).total_seconds() // 60)

res = {
    "paper_id": "11_DDOFPS", "agent": "A", "run_date_ist": "2026-10-10",
    "ran": True, "could_not_run_reason": "",
    "targets": T1,
    "robustness": robust,
    "bugs": bugs,
    "code_observations": observations,
    "env_fixes": [
        "diffs/file_name_mapping_v1.diff: script reads bd_doxa_programas.xlsx and bd_doxa_candidatos.xlsx; deposited bd_doxa_programas_HGPE.xlsx and bd_doxa_candidatos_HGPE.xlsx copied byte-identical under those names (pre-registered path-only fix)",
        "diffs/file_name_mapping_v2_alternative.diff: labelled alternative using bd_doxa_programas_HGPE_v2.xlsx",
        "diffs/run_authors_graphics_device.diff: wrapper only; cairo PNG device instead of pdf() because pdf() stops with 'invalid font type' on theme_ipsum_tw() (cosmetic, Figura 1 has no target)",
        "Package version (diffs/README.md item 5): hrbrthemes 0.8.0 from CRAN Archive, since 0.9.3 and 0.8.7 do not export theme_ipsum_tw()",
        "Encoding: script sourced with encoding='latin1' (line 177 byte 0xB4 kept as U+00B4)",
    ],
    "alternative_v2": {"proposed_class": c2, "targets_identical_to_v1": identical, "targets": T2},
    "proposed_class": c1,
    "class_reason": ("All six targets match the paper at its printed rounding after the pre-registered path-only file-name mapping "
                     "(primary file bd_doxa_programas_HGPE.xlsx); the v2 programs file gives identical values (alternative class "
                     f"{c2}). Whether the renamed files make the materials unclear (C) is a lead reading under PREREG section 4."),
    "confidence": "medium",
    "confidence_reason": "Numbers matched by script, but the class rests on the file-name mapping judgment and B's run is not yet compared.",
    "time_minutes": minutes,
    "uncertainties": [
        "The script reads two file names that are not in the deposit; the mapping to the _HGPE files is a pre-registered path-only fix, but nothing in the deposit says which programs file the authors used (v1 and v2 give identical target values here).",
        "T2/T3 come from ggpubr::stat_cor, which rounds r to 2 decimals; the match is also checked with unrounded cor.test values in the notes.",
        "Paper note 9 prints an expected 2018 APE4 count of 16; the code gives 16.87 (secondary number, not a target).",
        "The paper prints 'p-valor > 0,001' for Figura 4; the code gives p far below 0.001 (pre-registered reading (1)).",
        "CRAN ggplot2 4.0.3 was pulled into the per-run library as a dependency and masks system ggplot2 3.5.1; stat_cor output was read via layer_data under 4.0.3.",
        "Secondary robustness quantity r(2018)-r(2002) is not stable: near zero after outlier exclusion and negative under Spearman (robustness.json). Primary checks all pass.",
    ] + observations,
}
json.dump(res, open(os.path.join(A, "results.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print(json.dumps({"class": c1, "alt_v2": c2, "identical": identical, "minutes": minutes,
                  "targets": [(t["id"], t["paper_value"], t["reproduced_value"], t["match_to_rounding"], t["same_conclusion"]) for t in T1],
                  "robust": [(r["id"], r["estimate"], r["p_value"], r["same_direction_and_significance_as_paper"]) for r in robust]}, indent=1))
