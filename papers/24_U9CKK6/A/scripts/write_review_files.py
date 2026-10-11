#!/usr/bin/env python3
"""Write outputs/code_observations.json and outputs/uncertainties.json (numbers read from outputs/ files)."""
import csv, json, os
O = "/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/24_U9CKK6/A"
rd = lambda p: list(csv.DictReader(open(p, encoding="utf-8")))
rb = {r["check"] + "|" + r["target"]: r for r in rd(f"{O}/outputs/robustness_bc.csv")}
ex = {(r["model"], r["term"]): r for r in rd(f"{O}/outputs/targets_extracted.csv")}
fx = [r["term"] for r in rd(f"{O}/outputs/fixef_all_cycle_AE_fit2.csv")]
yr_terms = [t for t in fx if "year" in t]
t1 = float(ex[("cycle_AE_fit2", "challenge:days_to_nat")]["estimate"]); rc = float(rb["R_c_year_as_factor|T1"]["estimate"])
obs = [{"file": "Scripts/6_analysis1.R", "line": 410,
  "description": "Code observation (label vs specification, verified by run): the Table 1 texreg call hard-codes the row 'Year Fixed Effects' = Yes for all four models, but the four Table 1 models (lines 356, 365, 374, 384) enter `year` as a numeric column, i.e. one linear year slope, not year fixed effects. Other models in the same script and all Table 2 models use as.factor(year).",
  "evidence": f"outputs/fixef_all_cycle_AE_fit2.csv has year-related fixed-effect terms {yr_terms} (a single slope). Refitting with as.factor(year) (R_c, outputs/robustness_bc.csv) moves T1 from {t1:.5f} to {rc:.5f}; both round to {round(t1,2):.2f} with p < 0.001, so the printed Table 1 is what the deposited code produces and the conclusion is unchanged."}]
s9 = f"{O}/outputs/s9_column_index_check.csv"
if os.path.exists(s9):
    r = rd(s9); n9 = [x["column_name"] for x in r if x["script"].startswith("9_")]; n6 = [x["column_name"] for x in r if x["script"].startswith("6_")]
    used = any(x["used_in_table2_formulas"] == "TRUE" for x in r if x["script"].startswith("9_")) or r[0]["radical_in_table2_formulas"] == "TRUE"
    obs.append({"file": "Scripts/9_analysis4.R", "line": 43,
      "description": "Code observation (verified by run, no effect on any target): the centering index list `117:118` is copied from 6_analysis1.R line 35, where position 118 is `radical`; in script 9, after lines 30-32 (year_mon and the left_join), position 118 holds `EU_sal`, so a different column is centred and `radical` is not.",
      "evidence": f"outputs/s9_column_index_check.csv: in script 6 positions 117:118 are {n6}; in script 9 they are {n9}; `radical` sits at position {r[0]['radical_position_script9']} of {r[0]['ncol_script9']} in script 9. `radical` and `radical_scale` are in no Table 2 formula; `EU_sal` is mean-centred by the slip but then passed through scale() at line 61, which centres it again with the same mean, so the model input is unchanged. T5 and T6 are unaffected (also confirmed by the exact match of Table 2 AIC and log likelihood in outputs/model_gof.csv)."})
else:
    obs.append({"file": "Scripts/9_analysis4.R", "line": 43, "description": "Unverified observation: index 117:118 copied from script 6 while two columns are appended earlier in script 9; not checked by a run.", "evidence": "code reading only"})
obs.append({"file": "Scripts/6_analysis1.R", "line": 132,
  "description": "Unverified observation (not run by agent A, outside the target blocks): lines 132 and 246 use `right` and `left`, which no deposited script creates and which are not among the 117 columns of EP_debates_07062023.Rdata (PREREG.md Known risks), so a top-to-bottom run of the script would stop at line 132. Affects appendix models only, not T1 to T6.",
  "evidence": "grep of 6_analysis1.R: `chall_fact*right + chall_fact*left` (line 132), `challenge*right + challenge*left` (line 246); no assignment of right/left in any script. Not executed."})
json.dump(obs, open(f"{O}/outputs/code_observations.json", "w"), indent=1)
unc = [
 "Peak memory: the plain run stopped at 3199 MB RSS during the third Table 1 model, so the class rests on the pre-registered F1/F2 runs; the two models finished in the plain run are byte-identical to the F1/F2 ones (outputs/plain_vs_f1f2.csv). Table 2 was run with F1/F2 from the start (judgment call, LOG.md).",
 "Saved models (11 to 29 MB each) and estimation samples are in scratch /workspace/audit_runs/24_U9CKK6/A/models, not in outputs/ as PREREG section 2 says, because the brief keeps objects over 5 MB out of the repo; sha256 are in LOG.md.",
 "No package versions are pinned by the authors; run used lme4 1.1-37, Matrix 1.7-3, texreg 1.40, R 4.5.0. Exact AIC/logLik agreement suggests no material version effect.",
 "Satterthwaite p (lmerTest, exploratory candidate 2 in PREREG) was not computed; the pre-registered naive p sets the star buckets.",
 "R_a bootstrap: copy_index read as the k-th copy of a party within a draw (so the first copy of each party keeps cross-party MEP links); PREREG does not spell this out.",
 "R_a K rule used the time of the first refit (31.0 s) measured before a sandbox restart; the remaining draws ran after the restart with the same saved draws.",
 "Target cells were checked against the publisher PDF text layer fetched via web_fetch (outputs/pdf_target_cell_check.md), not a rendered page image.",
 "Data-statement findings carried from DATA_STATEMENT.md (not re-searched by agent A): parlgov CSVs for script 4 and the Eurobarometer .dta for script 10 are absent from the deposit; no target needs them (batch5_class_decisions.md #7)."]
json.dump(unc, open(f"{O}/outputs/uncertainties.json", "w"), indent=1)
print(len(obs), len(unc))
