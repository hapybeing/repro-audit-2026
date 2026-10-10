# PREREG: 05_FNTC1J

Written 2026-10-09 (IST), before any analysis code was run. No analysis code was executed to write this file.

- Paper: Wintterlin, F. (2025). "Not so different after all? Antecedents of believing in misinformation and conspiracy theories on COVID-19". Harvard Kennedy School (HKS) Misinformation Review, 6(5). DOI https://doi.org/10.37016/mr-2020-188
- Open PDF read: https://misinforeview.hks.harvard.edu/wp-content/uploads/2025/10/wintterlin_not-so-different-after-all_20251030.pdf (27 pages, sha256 fcc1b66cbc5f89d86cc588c56618eef1561cb212bf40866d888b04620f477357)
- Dataset: "Replication Data for: Not so different after all? ...", Harvard Dataverse, https://doi.org/10.7910/DVN/FNTC1J , version 1.0, licence CC0 1.0
  - File list API: https://dataverse.harvard.edu/api/datasets/:persistentId/?persistentId=doi:10.7910/DVN/FNTC1J
  - `MisinfoCT_HSK.r` (datafile id 12135073, https://dataverse.harvard.edu/api/access/datafile/12135073 , 162115 bytes, 3703 lines, sha256 fd86537ea9b98b2e69e06c0e353264bf3fbc1ad19c4d737e7afaddfa77dcf157)
  - `raw_data_CTvsMisinfo.rds` (datafile id 12135074, https://dataverse.harvard.edu/api/access/datafile/12135074 , 389085 bytes, sha256 c78b5ca25759263deececc8b563122894a183396364de732eb46dd235495687f)
  - No README in the deposit. The R script is the only documentation.
- Note: REPO/PROTOCOL.md does not exist in the repo at the time of writing (only AGENT_RUNBOOK.md, CHANGELOG_METHOD.md, META.md were found). This PREREG follows the assignment brief and AGENT_RUNBOOK.md.

## 1. Headline results and targets

Main claim (abstract, essay summary, Finding 1): in a German survey (March 2024), conspiracy mentality and the attitude that "truth is political" are the strongest predictors of believing both COVID-19 conspiracy theories (CT) and COVID-19 misinformation, each with p < .001, in two binary logistic regressions with 18 predictors. Text (p. 5): "a one-point increase was associated with a 1.30- (conspiracy theories) and a 1.20- (misinformation) point increase in the odds ... A one-point increase in the attitude that truth is political was associated with a 1.33 and 1.20 increase in the odds". The text adds that intuitive thinking and actively open-minded thinking were not significant (Bonferroni-adjusted p).

Targets (copied exactly from the paper; all odds ratios = exp(log-odds), unstandardized, as in the "Odds Ratios" column):

| id | quantity | paper value | decimals | location |
|---|---|---|---|---|
| T1 | Odds ratio, Conspiracy Mentality (`ConspMent_index`), CT belief model | 1.30 | 2 | Table A1 (p. 16), row "Conspiracy Mentality", column "Odds Ratios"; also text p. 5 |
| T2 | Odds ratio, Conspiracy Mentality, misinformation belief model | 1.20 | 2 | Table A2 (p. 17), row "Conspiracy Mentality", column "Odds Ratios"; also text p. 5 |
| T3 | Odds ratio, Truth is Political (`EpistBel_Truth_index`), CT belief model | 1.33 | 2 | Table A1 (p. 16), row "Truth is Political", column "Odds Ratios"; also text p. 5 |
| T4 | Odds ratio, Truth is Political, misinformation belief model | 1.20 | 2 | Table A2 (p. 17), row "Truth is Political", column "Odds Ratios"; also text p. 5 |
| T5 | Observations (N) in the CT logistic model | 2962 | 0 | Table A1 (p. 16), row "Observations" (Table A2 also reports 2962) |

Conclusion criterion for `same_conclusion`: T1 to T4 have OR > 1 and Bonferroni-adjusted (19 terms incl. intercept) HC3 p < .001 for T1, T3 and the CT model; for T2 and T4 OR > 1 with adjusted p < .01 (Table A2 marks T2 with *** and T4 with **). For T5, same conclusion if N is within 5 of 2962.

Other numbers in the paper that agents may report as secondary context only (not targets): Table A1 log-odds 0.26 (SE 0.03) and 0.29 (SE 0.05); Table A2 0.18 (0.03) and 0.18 (0.04); chi2(18) = 1573.84 and Nagelkerke R2 = .56 (A1); chi2(18) = 1226.09 and R2 = .45 (A2). Figure 1 (standardized odds ratios) is figure only, no numeric value in text beyond those tables.

Inconsistencies noticed while reading (described, not judged):
- Essay summary says N = 2,953; Methods and Tables A1/A2 say 2,962; linear Tables A3/A4 say 2963.
- Methods: removed n = 28 (more than 30% missing) and n = 14 (straightlining). Code comments say n = 24 and n = 28 respectively (lines 337 and 364).
- Code comment line 1842 says chi2(18) = 1571.41 and line 1975 says 1224,20; Table A1/A2 notes say 1573.84 and 1226.09.
- Text: 41.05% (n = 1,216) CT believers; code comment line 3154 mentions 1553 CT believers.
- Text says results are robust to a 2-or-more-items threshold; no code for that check was found in `MisinfoCT_HSK.r`.

## 2. Reproduction plan

Everything is in one script, `MisinfoCT_HSK.r`, which must be run top to bottom in one R session because the multiple-imputation step depends on the RNG state left by earlier calls.

Pipeline in the script (line numbers of the deposited file):
1. Line 18: `set.seed(2000)`; lines 17-66 load ~50 packages (line 17 needs `pacman`).
2. Line 73: `readRDS("published/raw_data_CTvsMisinfo.rds")`. Place the downloaded rds at `RUNDIR/published/raw_data_CTvsMisinfo.rds` and create `RUNDIR/_tables`, `RUNDIR/_figures`, `RUNDIR/_data` (the script writes there). Working directory = RUNDIR.
3. Lines 82-1152: filtering (LASTPAGE == 18), recoding, cleaning (>30% missing, IRV < 1.26), item dummies, PCA (`psych::fa.parallel` at lines 516, 558, 596, 637 consumes random numbers), index construction (line 1029 onward), outcome dummies (`COVID_CTB_dummy`, `misinfo_covid_beliefs_dummy`, lines 893-956).
4. Lines 1179-1220: MCAR test, then `mice(data = imp, m = 5)` (no seed argument, so it uses the global stream), imputed values averaged across the 5 imputations per `id` and written back into the single analysis dataset.
5. Lines 1647-1770: build `ds_analysis_paper2_CTBs_Ant`, fit preliminary model, drop row named "1400" (line 1770).
6. Lines 1814-1823: `model_CTB` (glm binomial, 18 predictors). Lines 1949-1957: `model_misinfo` (same predictors, same data).
7. Lines 2011-2110 (CT) and 2203 onward (misinfo): HC3 robust SEs (`sandwich::vcovHC`, `lmtest::coeftest`), OR = exp(coef), robust CIs, Bonferroni p, y-standardized coefficients (`parameters::standardize_parameters`), fit stats; exported via `flextable::save_as_docx` to `_tables/2_glm_CTBs_final.docx` and `_tables/2_glm_misinfo_final.docx`.

Target sources:
- T1, T3, T5: `model_CTB` (`exp(coef(model_CTB))["ConspMent_index"]`, `["EpistBel_Truth_index"]`, `nobs(model_CTB)`), also the `results` / `final_table` data frame built at lines 2024-2120 and the docx `_tables/2_glm_CTBs_final.docx`.
- T2, T4: `model_misinfo`, same extraction; `_tables/2_glm_misinfo_final.docx`.

Recommended way to run (environment fixes only, each saved as a diff):
- Run `Rscript -e 'source("MisinfoCT_HSK.r", echo=TRUE, max.deparse.length=Inf); save.image("outputs/session.RData")'` or equivalent, logging stdout/stderr to `outputs/`.
- `utils::View()` is called at lines 1159 and 1225 and fails in a non-interactive session. Allowed fix: define `View <- function(...) invisible(NULL)` before sourcing (record as env fix). `tibble::view()` is a no-op when non-interactive.
- If a purely cosmetic export (docx, html, ggsave) fails because of a missing system library, the allowed fix is to make that export line non-fatal (record as diff); it does not touch estimates.
- An extraction script `scripts/extract_targets.R` loads the session (or the models) and writes `outputs/targets_extracted.csv` with OR, log-odds, HC3 SE, raw and Bonferroni p, and nobs for both models. `scripts/build_results.py` builds `results.json` from that CSV.

Expected sources of small differences (to be recorded, not fixed): R 4.4.3 here vs 4.4.2 (macOS, x86_64) for the authors; package versions for `mice` and `psych` are not pinned and both affect the random stream and imputed values. Missingness is about 1% of values, so differences in the 2nd decimal are possible but not expected.

## 3. Robustness checks (pre-registered)

All three checks target the main result: the conspiracy mentality odds ratio in the CT model (`model_CTB`, T1). Each check also reports the same quantity for Truth is Political (T3) and for the misinformation model (T2, T4) as secondary, but the primary estimate written to `results.json` is the T1 quantity. Inference: HC3 robust SE as in the paper; p-value reported raw and Bonferroni-adjusted over the 19 model terms. "Same direction and significance" = OR > 1 and Bonferroni-adjusted p < .001 (as in Table A1).

R_a. Nonparametric case bootstrap. Using the exact data frame `model_CTB` was fit on (`model.frame(model_CTB)` rows of `ds_analysis_paper2_CTBs_Ant` after the row "1400" removal), call `set.seed(20261009)` once, draw 1000 resamples of rows with replacement (`sample(n, n, replace = TRUE)`), refit the identical glm formula on each, and record exp(coef) for `ConspMent_index`. Report the original-sample OR as the estimate, the bootstrap percentile 95% CI (2.5th and 97.5th percentiles of the 1000 ORs) as `se_or_ci`, the bootstrap SE of the log-odds, and as p-value the two-sided bootstrap proportion min(2 * share of log-odds <= 0, 1). Resamples where glm fails to converge are counted and reported, not replaced. Same direction and significance = OR > 1 and percentile CI excludes 1.

R_b. Influential-case exclusion. From the final `model_CTB`, compute `cooks.distance(model_CTB)`; drop every case with Cook's distance > 4/N where N = `nobs(model_CTB)`; refit the identical glm on the remaining cases; report OR, HC3 SE, raw and Bonferroni p for `ConspMent_index`, and the number of cases dropped. (A |z| > 3 rule is not used: the outcome is binary, and on the 1-11 conspiracy mentality scale with mean 6.85 and SD 2.69 (Table B1b) no value can lie more than 3 SD from the mean, so it would drop nothing.) For the misinformation secondary estimate, apply the same rule using `model_misinfo`'s own Cook's distances.

R_c. Alternative scale construction for social dominance orientation (a control). In the deposited script, line 1035 builds `SDO_index = rowMeans(dplyr::select(., starts_with("SDO")), na.rm = TRUE)`; at that point the data contain `SDO1, SDO2, SDO3, SDO4` and the reversed copies `SDO1_r, SDO3_r` created at lines 377 and 387, so `starts_with("SDO")` would average six columns, including each reversed item together with its unreversed original. The paper describes a 4-item scale, and the script's own reliability check (line 982) uses `SDO1_r, SDO2, SDO3_r, SDO4`. Check: in a copy of the script saved under `scripts/` (not the authors' file), replace that line with `SDO_index = rowMeans(dplyr::select(., c("SDO1_r", "SDO2", "SDO3_r", "SDO4")), na.rm = TRUE)`, change nothing else, rerun the whole copy from the top with the authors' `set.seed(2000)`, and report the T1 quantity from the resulting `model_CTB` with HC3 SE and Bonferroni p. Note that mice receives a different `SDO_index`, so imputed values of other variables may shift slightly; that is part of this check. Before running R_c, agents should confirm (by printing `names(dplyr::select(ds, starts_with("SDO")))` just before line 1029 in their own diagnostic script) which columns the original line actually averaged, and record that in LOG.md; whether this is a real bug is for the code review to decide on that evidence.

## 4. Feasibility notes

- Compute: tiny. Raw data 389 KB, about 3000 rows. Heaviest parts are two `car::Boot(..., R = 5000)` linear-model bootstraps (lines 3431, 3678) and `fa.parallel`; expected well under 15 minutes on 2 CPUs. R_a (1000 glm refits) about 1-2 minutes.
- Dependencies: about 55 CRAN packages, all currently on CRAN (checked index pages 2026-10-09: MissMech 1.0.4, blorr 0.3.1, tidycomm 0.4.2, MVN 6.3, plus careless, descr, olsrr, report, correlation, finalfit, naniar, DescTools, arm, sjPlot, parameters, flextable, officer, mice, pacman, DT, GPArotation). Not in the base env and needing install into a per-run library: at least pacman, descr, tidycomm, sjmisc, sjlabelled, psych, report, naniar, correlation, Hmisc, MVN, lavaan, writexl, GPArotation, stargazer, MissMech, finalfit, careless, labelled, skimr, blorr, arm, sjPlot, ggridges, DescTools, viridis, patchwork, multcomp, car, olsrr, kableExtra, cowplot, mice, flextable, officer, parameters, DT, htmlTable. Risks on aarch64: `flextable`/`gdtools` need cairo/freetype/fontconfig headers; `MVN` and `sjPlot` pull many dependencies. These only affect exports; the models can still be extracted. No version pins in the deposit besides the header "R version 4.4.2 (2024-10-31), x86_64-apple-darwin20, macOS Ventura 13.7.1".
- Randomness: `set.seed(2000)` once at the top; imputation draws depend on every RNG call before line 1201, on `mice` and `psych` versions, and on platform. Exact bit-for-bit imputation equality with the authors' run is not guaranteed.
- Licence: dataset CC0 1.0 (Dataverse metadata); script header says CC BY 4.0; article CC BY 4.0. Public downloads, no sign-in.
- Data access: both files downloaded without authentication via the Dataverse access API with User-Agent "repro-audit-2026".
