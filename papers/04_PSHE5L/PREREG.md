# PREREG: 04_PSHE5L

Written 2026-10-09 (IST), before any analysis code was run. No model has been fitted by the author of this file.

- Paper: Bryant, J. C., Mueller, J. T., and Burow, P. B. (2025). "Rural Populism and Tolerance for Political Violence". Socius: Sociological Research for a Dynamic World. https://doi.org/10.1177/23780231251317227 (gold OA, CC licence; full text read via https://journals.sagepub.com/doi/10.1177/23780231251317227 , the HTML version; direct curl to Sage returns HTTP 403, a text fetcher worked).
- Dataset (Harvard Dataverse): https://doi.org/10.7910/DVN/PSHE5L , "Replication Code for: Rural Populism and Tolerance for Political Violence", version 1, CC0 1.0, deposited 2024-11-07.
- Note: REPO/PROTOCOL.md does not exist in the repo at the time of writing (only AGENT_RUNBOOK.md, CHANGELOG_METHOD.md and META.md were present). This PREREG follows AGENT_RUNBOOK.md and the assignment brief.

## 0. Materials found (what is and is not in the deposit)

Harvard Dataverse PSHE5L contains ONE file and NO data:

| file | Dataverse file id | bytes | sha256 |
|---|---|---|---|
| `Rural Populism - Socius - Public Code.R` | 10695152 (https://dataverse.harvard.edu/api/access/datafile/10695152) | 14238 | 955871dc22416db62aa81173fbf7e81ba152f00c8546a7042f52782d7422e7a5 |

No README. The script reads `Downloads/320-942_Rural_West_COVID-19_Survey_4.5.21.csv` (line 9), which is not in the deposit.

The data ARE publicly downloadable elsewhere, without sign-in or request: the authors' OSF project "Impact of Covid-19 in Rural America" (https://doi.org/10.17605/OSF.IO/64EZG , licence CC-BY 4.0) has a public component "Rural Populism" (https://osf.io/mtd4z/ , last modified 2025-01-11) with two files:

| file | OSF download URL | bytes | sha256 |
|---|---|---|---|
| `Rural Populism - Socius - Public Code.R` | https://osf.io/download/6zsmv/ | 14238 | 955871dc22416db62aa81173fbf7e81ba152f00c8546a7042f52782d7422e7a5 (identical to the Dataverse file) |
| `Rural_Populism_Dataset.csv` | https://osf.io/download/wr3ve/ | 79755 | f839986a49ef5e107480803efd234789078d7a9a9b60efd50d21e74adb31b2ec |

The paper itself does not cite the OSF component; it was found by browsing the OSF project the same team cites for the PNAS 2021 paper. The link between the CSV and this paper rests on the component title, the identical code file, and matching variables (see below). Both were downloaded only to read the header and value codes; no model was run.

What the OSF CSV contains (descriptive inspection only): 1203 rows (matches the paper's 1,203 complete responses), 30 columns: `WTS, Q23A-Q23O (14 items), Q25B, Q25C, Q25D, QF, Q20, Q7C, Q10, QC, QE, QD, XQ14, URBAN_CODE, QB, Q15`. All variables the active code uses are present. No blank, "." or "NA" cells. It is a reduced extract, not the full 117-column survey file the script was written for (the script's comment at line 13 counts 117 columns; `RAW_Q24A-I` columns used at lines 17-20 are absent).

Facts that matter for reproduction (recorded now so they cannot be chosen after results):
- F1. `Q15` (conservatism, 1-7) contains code 8 in 64 rows. The script's recode `rural$Q15[rural$Q15 == 8] <- NA` is commented out (line 188), so as written, code 8 stays in the model as a value above "extremely conservative". 1203 - 64 = 1139, which equals the paper's structural-model n (1,139). This suggests (not established) that the authors' original file had these values missing.
- F2. `XQ14` codes 4 or 5 occur in 205 rows; the script sets them to NA (lines 134-135). 1203 - 205 = 998, which equals the paper's controls-model n (998). Rows with XQ14 in 4/5 OR Q15 == 8: 226. So the two reported n values are not jointly explained by one simple missingness rule; I could not determine which data state the authors used.
- F3. `WTS` is 0 for 11 rows (4 of them also have Q15 == 8).
- F4. Lines 17-20 call `mutate(across(all_of(paste0("RAW_Q24", LETTERS[1:9])), as.numeric))`. These columns are not in the OSF CSV, so this line will error as written. The created variables are never used afterwards.

## 1. Headline result(s)

Abstract claim: "populist attitudes are associated with reduced tolerance for political violence in rural areas"; "associations among economic grievances, conservatism, and populist attitudes"; "populism attenuates the link between economic grievance and tolerance for political violence".

Model: latent-variable SEM in lavaan (main structural model, no controls), n = 1,139, weights `WTS`, estimator MLR, FIML (`missing = "ML"`). Reported fit: chi2 = 516.954, df = 141, robust CFI = 0.911, robust TLI = 0.892, SRMR = 0.058, robust RMSEA = 0.062 (text, "Structural Model" section).

Targets (standardized coefficients, copied exactly from the tables; the paper prints them with 3 decimals and no leading zero):

| id | quantity | paper value | decimals | location |
|---|---|---|---|---|
| T1 | Populism -> violence, standardized coefficient (b1) | -0.202 (p = .006) | 3 | Table 2, row "Populism -> violence" |
| T2 | Economic grievance -> violence, direct, standardized (c) | 0.354 (p = .005) | 3 | Table 2, row "Economic grievance -> violence" |
| T3 | Economic grievance -> populism, standardized (a1) | 0.718 (p = .000) | 3 | Table 2, row "Economic grievance -> populism" |
| T4 | Indirect effect economic grievance -> populism -> violence, standardized (a1*b1) | -0.145 (p = .028) | 3 | Table 3, row "Economic grievance -> -> violence" |
| T5 | Total effect of economic grievance on violence, standardized (c + a1*b1) | 0.208 (p = .020) | 3 | Table 4, row "Economic grievance" |

p values are recorded as secondary information in each target's note, not as targets. The paper does not say whether its p values come from `summary()` (unstandardized z tests) or from `standardizedSolution()` (delta-method tests of standardized values); report both.

Not targets (reported for context only if produced): Table 1 reliability values (Cronbach alpha .771/.720/.856/.891, CR .769/.610/.769/.802, AVE .361/.300/.498/.577), measurement-model fit, n.

## 2. Exact reproduction plan

Environment: R 4.4.3 at `/workspace/mamba/envs/r/bin/Rscript`, clean `R_LIBS_USER`. Packages loaded by the script: lavaan, tidyverse, semTools, semPlot, xtable, gt, psych. No versions are pinned by the authors. Code was deposited 2024-11-07, so try lavaan 0.6-19 (released 2024-09) and semTools 0.5-6 first via `remotes::install_version`; if that fails, use current CRAN and record versions.

Inputs: `Rural_Populism_Dataset.csv` from https://osf.io/download/wr3ve/ (sha256 above). Record sha256 again on download.

Allowed environment fixes, each saved as a diff with reason:
1. Line 9: change the path `Downloads/320-942_Rural_West_COVID-19_Survey_4.5.21.csv` to the local path of `Rural_Populism_Dataset.csv` (file path fix; note in diffs/README.md that the public file is a 30-column extract with a different name).
2. Lines 17-22: the `RAW_Q24*` columns are absent from the public extract, so the `mutate(across(all_of(...)))` call and `class(rural$RAW_Q24C)` will error. Comment these lines out. Justification: the created variables are not used by any model (grep shows no later use of `RAW_Q24`). If the line does not error, leave it.
3. `library(semPlot)`, `library(xtable)`, `library(gt)`: no function from these packages is called in the script (no `semPaths`, `xtable(`, `gt(`). If any fails to install within 20 minutes, comment out that `library()` line and record it. Do not comment out lavaan, tidyverse, semTools or psych.
No other change. In particular, do NOT uncomment line 188 (Q15 == 8 recode) in the primary run.

Script and objects:
- Run the whole script `Rural Populism - Socius - Public Code.R` top to bottom, capturing console output to `outputs/full_script_output.txt`.
- Targets come from the object `structural`, fitted at line 321: `cfa(mediation_model_violence_ctrls2, data = rural, sampling.weights = "WTS", missing = "ML", estimator = "MLR")`.
- After the script finishes (same R session, or a separate extraction script that re-sources the patched script), write `standardizedSolution(structural)` to `outputs/structural_stdsol.csv` and `parameterEstimates(structural)` to `outputs/structural_pe.csv`, plus `lavInspect(structural, "nobs")` and `fitMeasures(structural, c("chisq.scaled","df.scaled","cfi.robust","tli.robust","srmr","rmsea.robust"))` and `fitMeasures(...,"chisq")` to `outputs/structural_fit.csv`.
- Mapping (use `est.std` from `standardizedSolution`):
  - T1: row lhs = `violence`, op = `~`, rhs = `polgriev` (label b1).
  - T2: lhs `violence`, op `~`, rhs `econgriev` (label c).
  - T3: lhs `polgriev`, op `~`, rhs `econgriev` (label a1).
  - T4: lhs `indirect1_econgriev`, op `:=`.
  - T5: lhs `total_effect_econgriev`, op `:=`.
- Compare to paper values with rounding to 3 decimals. Also report the n lavaan used and compare to 1,139 (context, not a target).

Pre-registered diagnostic run (labelled DIAGNOSTIC, does not determine the class, run only after the primary run is saved): the same patched script with the authors' own commented line 188 (`rural$Q15[rural$Q15 == 8] <- NA`) re-enabled, nothing else changed. Save as `outputs/diag_q15na_stdsol.csv` and its n. Reason: fact F1 above; this tests whether the published n = 1,139 and estimates correspond to Q15 code 8 being treated as missing. Report both runs side by side. Class is proposed from the primary (as-deposited) run, with the diagnostic described in the note.

Secondary (context only): the controls model `structural_ctrl` (line 335) should report n = 998 and chi2 = 779.793, df = 201; record what the script prints.

## 3. Robustness checks (main result = T1, populism -> violence; also report T4)

All three use the primary-run data preparation (as deposited, Q15 code 8 kept), the `mediation_model_violence_ctrls2` model, and the same `cfa(..., sampling.weights = "WTS", missing = "ML", estimator = "MLR")` call unless stated. Report est.std of `violence ~ polgriev` and of `indirect1_econgriev`, with SE / CI and p value. "Same direction and significance" means the same sign as the paper and p < .05 (paper: T1 p = .006, T4 p = .028).

- R_a. Nonparametric case bootstrap, 1000 replicates, `set.seed(20261009)` once before the loop. Each replicate: sample `nrow(rural)` rows with replacement, refit the model with identical options, store est.std for b1 and `indirect1_econgriev` from `standardizedSolution()`. Reason for a manual loop: lavaan's built-in `se = "bootstrap"` is not used because it is not combined here with `sampling.weights`; resampling rows and keeping each row's weight is the nearest version. Report the bootstrap median, percentile 95% CI (2.5th, 97.5th), the share of replicates with b1 < 0, and the number of non-converged or erroring replicates (excluded and counted). "Significant" for R_a means the 95% percentile CI excludes 0; p_value field = null. Expected compute: about 1 to 3 s per fit, so 20 to 50 minutes; write results incrementally to `outputs/R_a_boot.csv` so it can resume.
- R_b. Outlier exclusion on the outcome. The outcome is latent, so use its indicators: compute `viol_mean = rowMeans(rural[, c("Q25B","Q25C","Q25D")], na.rm = TRUE)` on the prepared data, then the unweighted z score `(viol_mean - mean(viol_mean)) / sd(viol_mean)`. Drop rows with |z| > 3. Refit the model on the remaining rows. Report the number of rows dropped. Note in advance: the items are heavily skewed toward 1, so this rule removes only respondents with the highest violence tolerance; if it removes 0 rows, report "no rows met the rule" and the estimate equals the primary one.
- R_c. Unweighted: identical call without `sampling.weights = "WTS"` (all rows, including the 11 with weight 0), everything else unchanged.

## 4. Feasibility notes

- Compute: small (1203 x 30 data; single SEM fits in seconds). Bootstrap R_a is the only long step (tens of minutes); split into chunks under the 600 s background cap and make it resumable.
- Dependencies: lavaan, semTools, psych, tidyverse are the real requirements. semPlot has a heavy dependency tree (it may pull OpenMx and qgraph, source builds on aarch64 can be slow); it is not used, see env fix 3. `reliability()` at line 317 is deprecated in recent semTools versions and may warn or be removed; if it errors under the installed semTools, try semTools 0.5-6, and if still failing record it (it only affects Table 1, not the targets). The `rel()` helper calls `semTools::htmt` with raw data and `psych::alpha`; also Table 1 only.
- Data access: public, no sign-in (OSF, CC-BY 4.0). The Dataverse deposit alone is code only (CC0). Because the public CSV is a 30-column extract and not the file named in the code, and because of fact F1/F2, some divergence in n and estimates is possible from the data state alone.
- Licence: code CC0 1.0 (Dataverse); OSF project CC-BY 4.0; article open access.
- Supplementary material (https://journals.sagepub.com/doi/suppl/10.1177/23780231251317227/suppl_file/sj-docx-1-srd-10.1177_23780231251317227.docx) returned HTTP 403 to curl and was not read; the paper says it holds full model results and survey wording.
- Uncertainties: which p value type the paper reports; whether the paper's standardized values are std.all (assumed: std.all, the lavaan default `est.std`); the data state used by the authors (F1, F2).
