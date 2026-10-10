# PREREG: 13_DX5T9G

Written 2026-10-10 (IST), about 21:10 IST, before any analysis code was run. No analysis code from the deposit was executed to write this file. The deposit was downloaded and its files were read as text (code, README, log, CSV column headers, row counts and treatment-value counts read with a short Python reader, not with the authors' code).

The main text was read in full (publisher version of record, 18 pages). The paper's numbers below are copied from that PDF.

- Paper: Kobayashi, Y., Cilizoglu, M., Heinrich, T., and Christiansen, W. (2024). "No Entry in a Pandemic: Public Support for Border Closures". American Journal of Political Science 68(2), 372-389. First published online 2023-04-24. DOI https://doi.org/10.1111/ajps.12790 . Open access, CC BY.
- Text source read: publisher version of record deposited at White Rose eprints, https://eprints.whiterose.ac.uk/194407/15/American%20J%20Political%20Sci%20-%202023%20-%20Kobayashi%20-%20No%20Entry%20in%20a%20Pandemic%20%20Public%20Support%20for%20Border%20Closures.pdf (762,558 bytes, 18 pages, sha256 29a878be7af3352678da2ced5a8bd653faa8725fc95a1a0e2e2a5035c8691085). The Wiley pdfdirect URL (https://onlinelibrary.wiley.com/doi/pdfdirect/10.1111/ajps.12790) returned a 5,531-byte HTML page instead of a PDF to a scripted request, so it was not used. Page numbers below are the journal's printed page numbers. Table 2 was also checked against a rendered image of printed p. 379.
- The online supporting information (SI) was not read; no target comes from it.
- Dataset: "Replication Data for: No Entry in a Pandemic: Public Support for Border Closures", Harvard Dataverse, https://doi.org/10.7910/DVN/DX5T9G , version 1.0, released 2023-02-21, 23 files, 847,156,282 bytes, none restricted. Licence field empty; terms of use: "This dataset is made available with limited information on how it can be used. You may wish to communicate with the Contact(s) specified before use." (no sign-in needed to download).
- Scratch copies and checksums: /workspace/audit_runs/13_DX5T9G/prereg/ (`checksums.sha256`, `files_sha.json`); copy of the per-file table in `papers/13_DX5T9G/data_statement_raw/files_sha256.json`.

## Dataset files

Downloaded 2026-10-10 around 15:28 to 15:31 UTC with `curl -A "repro-audit-2026"` from `https://dataverse.harvard.edu/api/access/datafile/<id>`. Four tabular files were ingested by Dataverse and are served as `.tab` by default; their original uploads were fetched with `?format=original`. The original-format files match the MD5 that Dataverse records for each file. The code reads the original names (`.csv`, `.dta`), so agents must use the `?format=original` downloads.

| datafile id | path in deposit | bytes | sha256 |
|---|---|---|---|
| 6911550 | replication/code/00_Run it all.R | 4315 | bb4df219008eaac03f29da310f9c47eda18f483e3b3dc7e2294631bb5c417914 |
| 6911552 | replication/code/01_Prepare data.R | 6186 | 92794c4d4a915ea847545ac74c274ab10ffe7bd6fc1e960b8ad025420c44fec8 |
| 6911541 | replication/code/02_Descriptives.R | 5938 | 93015a353ed7cdd9cbb70b1ddb3381de3392de7a186f689dfb9bef15d7917c0c |
| 6911557 | replication/code/03_Estimate main models.R | 8161 | 7a578a41c0ce65cbcf0f66937250eecaf437df1601b6ed362eb9a4acb1606dfb |
| 6911540 | replication/code/04_Make main graphs.R | 7613 | ef939e9c5ba10d6896da660f81bc76b5748c924d801174071451784e8d0fa9dc |
| 6911547 | replication/code/05_Make main tables.R | 4842 | 378ff3c35fae457f8f14c474e06d6a8ed01e12f85bd273552fcb868ffcf441eb |
| 6911558 | replication/code/06_Estimate Open.R | 9994 | 2afcfdd41c42765413cb52c38eafe670119695320baf5d6c05a8a3fdb81ee632 |
| 6911542 | replication/code/07_Causal moderation for Open.R | 4797 | 397184217d30eab93fea37bbe70db455ba4e58874d1c901909029c3e60265124 |
| 6911545 | replication/code/08_Newspaper analysis.R | 3041 | 0d36271ca63a9b76138e2627ad02e06469552279c66b064110a18041b9cf950f |
| 6911560 | replication/code/X_Auxiliary functions.R | 1668 | 5334fad543ab7cdd20800b01749970bc11963fa2df7bac439f28d671c144edd7 |
| 6911561 | replication/ReadMe.txt | 3557 | ff240d623426fdf389e64c4343ade594649e4e77d1fd2141c4e2be2701037a13 |
| 6911537 | replication/log/PandemicBorder.log | 8487 | eb6c835e3947d5b678ddd908138a79c6a663c7179ca3728091cd2eeb95db6160 |
| 6911553 | replication/data/ViralBorders - US.csv (original of .tab) | 1169429 | 3b348166bb2b104aed18017eafbb7d964f6401f7950f9cb1f147d18d40790f1d |
| 6911559 | replication/data/ViralBorders - UK.csv (original of .tab) | 1168013 | 25b452348c82191c9c1877cdf965f781bbedd7dd6a45589a09e68d8bd4cffe1f |
| 6911546 | replication/data/CCES/cces18_common_vv.dta (Stata 14, release 118; not ingested) | 839424284 | 3282e5c40228f32876460ffe34da5131fa6acd2b390fc9093d02e03d8691285a |
| 6911551 | replication/data/BES/bes_f2f_2017_v1.5.dta (original of .tab; Stata format 115) | 1845588 | 2bbcc7e1bd8263938064bc6881ae92528d8b8bf5aee9bb12e92d02f865016340 |
| 6911556 | replication/data/News Queries/News.csv (original of .tab) | 2570 | 02af87ce84f7497db4aa9e6cc5a05e75c40792aca307bf0ac0f48cfb4e77aa08 |
| 6911548 | replication/data/cascara_geo_trimmed.png | 707747 | e09eeaab5dbdb25515c1a98e0da6a40e762321da67a444491d2e9aae9ce038a6 |
| 6911549 | replication/data/Codebook.pdf | 90268 | a915142f0470b00b40efc95510e0e449d6a52b64b0ac32218243ece0948421ef |
| 6911562 | replication/data/Sample flow of survey - UK.pdf | 727356 | 428776ac2e7c4d2b6afba2fdf13381946a28974d98a4e2f6f36f3ed1488781ac |
| 6911544 | replication/data/BES/BES-2017-F2F-codebook.pdf | 1277586 | 846f6de7b72cb614adea91f2ce4c1272d901cf96111b33e0a33f8d5db6afb7a7 |
| 6911543 | replication/data/CCES/CCES+Guide+2018.pdf | 497715 | 194e87c2aa2c0ea4e5b0aa21bf8e8c7ce40968836d61811c4528df1f07d492cd |
| 6911539 | replication/data/News Queries/News Codebook.pdf | 96522 | bd081f4ec08c2557c2aa14ad3810ef202d805cf5c63b125d5729622aaf17ee85 |

Ingested `.tab` versions, for the record only (not used by the code): US .tab 1,221,018 bytes sha256 def222e5e296007172003483894f1ceb458a42f64dc83ee61045827387df09e2; UK .tab 1,219,576 bytes c2aeb554c18725573f1ea0ba2f63990dafc446ac40ccf7e9ab64eb87ce490abe; BES .tab 1,822,710 bytes 84978c8317ecdc3df675018345156705446aa34309e92718aae4267f3d6ed50a; News .tab 2,901 bytes e322e9d6ed4c0594b0da97ddecdd256ec5e5dfdf1c0fbf4538c26e8717324dbc.

## 1. Headline results and targets

Main claim (abstract, p. 372): survey experiments in the UK and the US show "that a greater pandemic threat mildly increases support for border closures, but the World Health Organization's (WHO) guidance against border closures and reminders about international legal obligations to follow the guidance substantially weaken support for border closures." The tables that report it are Table 2 (UK, p. 379) and Table 3 (US, p. 380): weighted multinomial-logit coefficients, reference category "leave borders open", one column per border-closure option. The text (p. 379) says "both WHO-related treatments are negative and statistically significant". Figure 5 and the text on p. 381 give the same claim as changes in probability (0.13 [0.10, 0.17] UK and 0.11 [0.08, 0.15] US for the WHO recommendation); those are simulation outputs read from a figure and prose, so per the batch 2 lesson the printed table estimates are preferred as targets.

Targets are the two WHO treatment coefficients in the first outcome column ("Close border(s) to: Infected neighbor", i.e. close the border to Marshovia, outcome level Y = 2), for each country, plus each table's printed N. The first column is chosen because it is the most frequently chosen closure option in both samples and the first printed column; the other four columns are secondary context only.

| id | quantity | paper value | decimals | location |
|---|---|---|---|---|
| T1 | UK, coefficient on "WHO (recommendation)", outcome "Infected neighbor" vs leave open | -1.53 | 2 | Table 2, p. 379, row "WHO (recommendation)", column "Infected neighbor" (printed -1.53**, SE 0.28) |
| T2 | UK, coefficient on "WHO (recommendation, ratification)", outcome "Infected neighbor" | -2.01 | 2 | Table 2, p. 379, row "WHO (recommendation, ratification)", column "Infected neighbor" (printed -2.01**, SE 0.27) |
| T3 | US, coefficient on "WHO (recommendation)", outcome "Infected neighbor" | -1.06 | 2 | Table 3, p. 380, row "WHO (recommendation)", column "Infected neighbor" (printed -1.06**, SE 0.24) |
| T4 | US, coefficient on "WHO (recommendation, ratification)", outcome "Infected neighbor" | -1.52 | 2 | Table 3, p. 380, row "WHO (recommendation, ratification)", column "Infected neighbor" (printed -1.52**, SE 0.23) |
| T5 | UK estimation sample size | 1599 | 0 | Table 2 note, p. 379 ("based on 1,599 observations"); also text p. 376 ("We recruited 1,599 participants from the United Kingdom") |
| T6 | US estimation sample size | 1625 | 0 | Table 3 note, p. 380 ("based on 1,625 observations"); also text p. 376 ("... and 1,625 from the United States") |

Each N is printed twice for the same sample (table note and recruitment sentence), with the same value both times. The table note is the pre-registered location.

### Exact statistic and code object for each target

The tables are written by `05_Make main tables.R` from `output/Estimates-Main.Rdata` (object `store_estimates`, a list from `foreach(v=1:2)` in `03_Estimate main models.R`; element 1 is the US, element 2 is the UK). Within `run_models(i)`, model `m = 1` is the main model (all respondents, formula `form_raw` plus the two WHO indicators), fitted with `nnet::multinom(..., weights = tmp$w, Hess = TRUE, maxit = 500)` after `set.seed(1230)`, followed by `theta <- mvrnorm(n = 5000, mu = c(t(coef(mod))), vcov(mod))`.

- T1: `store_estimates[[2]]$Coefficients`, row with `X1 == '2:I(T_who == "WHO")TRUE'` and `Subset == 1`, column `Mean`.
- T2: same object, `X1 == '2:I(T_who == "WHO.Ratified")TRUE'`, `Subset == 1`, column `Mean`.
- T3, T4: same rows in `store_estimates[[1]]$Coefficients`.
- T5, T6: column `N` (= `nrow(tmp)`) of those rows, which is what the table caption prints (`NN_vec[1]`).
- Cross-check: the printed strings in `output/table_main_UK_1.tex` (copied to `output/named_items/Table_2.tex`) and `output/table_main_US_1.tex` (`Table_3.tex`).

Ambiguity about the statistic, listed in order; the first is pre-registered:
- Estimate. (1) The printed number is `Mean`, the mean of the 5000 parametric simulation draws (this is what the code prints). (2) The maximum-likelihood coefficient `coef(mod)["2", 'I(T_who == "WHO")TRUE']`. The two should agree to about 0.01; agents report both, but match is judged on (1).
- Standard error in parentheses. (1) `SD`, the standard deviation of the 5000 draws (what the code prints). (2) `sqrt(diag(vcov(mod)))`. Not a target.
- p-value behind the stars. (1) The code's `pvalue = 2 * pt(-abs(Mean / SD), df = nrow(data))`, where `data` inside `run_models` is the global combined UK+US data frame, not the country subset. (2) Wald normal p from `coef(mod)` and `vcov(mod)`. The conclusion criterion uses (1).

### Conclusion criterion (same_conclusion)

- T1 to T4: same conclusion if the reproduced estimate is negative and its pre-registered p-value is below .01 (the paper prints ** for all four, legend "** p < .01").
- T5, T6: same conclusion if the reproduced N is within 5 of the printed N. Under CHANGELOG #6, a mismatch only in N while T1 to T4 match is read as C, not D.

### Secondary context (not targets)

Other WHO coefficients in Tables 2 and 3 (columns Threatened neighbors, All neighbors, Entire region, Entire world): UK -1.36, -2.26, -1.90, -1.36 (recommendation) and -2.72, -2.62, -2.56, -2.06 (ratification); US -2.15, -1.31, -1.40, -1.25 and -1.83, -2.05, -1.84, -1.95, all printed with **. Proportions choosing "leave open" 0.16 [0.13, 0.18] UK and 0.16 [0.14, 0.18] US (p. 378). Verisimilitude subsample sizes 354 (UK) and 370 (US) (p. 382).

### Inconsistencies noticed while reading (described, not judged)

1. The ReadMe lists `data/ViralBorders - US.csv`, `... - UK.csv`, `data/BES/bes_f2f_2017_v1.5.dta` and `data/News Queries/News.csv`. Dataverse serves these four as ingested `.tab` files by default; the original uploads are available with `?format=original` and match the recorded MD5.
2. The deposited log's header says "Log Path: output/log/test.log"; `00_Run it all.R` writes `output/test.log`. The log contains the code echo, `sessionInfo()` and warnings, but no estimates, so it is not a numeric reference.
3. The ReadMe and code comments describe an Apple M1 MacBook Air; the log reports "Platform: x86_64-apple-darwin17.0" with a Darwin ARM64 kernel (an x86_64 R build on Apple silicon).
4. The log ends with 16 warnings "non-integer #successes in a binomial glm!", which come from the weighted binomial models in scripts 06 and 07, not from the target models.
5. Raw row counts read from the deposited CSVs: 1,628 rows (US) and 1,605 rows (UK); 2 rows in each have an empty outcome (Q59). The paper prints 1,625 and 1,599 both as "recruited" participants (p. 376) and as estimation N (table notes). The code drops rows with age outside 18 to 100 and rows with any missing value before estimation.
6. Table 2 (UK), column "All neighbors": Gender (male) -0.47 (0.21) and Ideology (left-right) 1.76 (0.57) are printed without a star, while cells with a smaller estimate-to-SE ratio carry stars (e.g. Health capacity, Threatened neighbors, 0.60 (0.31) with *). Confirmed on a rendered image of p. 379. Not a target.
7. Table 3 (US), row "Ideology (do not know)", column "Threatened neighbors": -7.81** with SE printed as (0.00). Not a target.
8. Table notes say "Standard errors are reported in parentheses"; the code prints the mean and SD of 5000 parametric simulation draws rather than the MLE and its analytic SE (see the statistic list above).
9. `06_Estimate Open.R`, footnote 20 models (`mod_UK`, `mod_US`): weights are passed as `...$w1`; `01_Prepare data.R` creates only a weight column `w`. Not a target; for the code review to assess.
10. Paper and code label "Ideology (do not know)" vs "Ideology (don't know)": wording only.

## 2. Reproduction plan

Run directory `RUNDIR = /workspace/audit_runs/13_DX5T9G/<AGENT>/replication`, laid out as the deposit (`code/`, `data/`, `data/BES/`, `data/CCES/`, `data/News Queries/`, `log/`), with the original-format files saved under the names the code reads: `data/ViralBorders - US.csv`, `data/ViralBorders - UK.csv`, `data/BES/bes_f2f_2017_v1.5.dta`, `data/CCES/cces18_common_vv.dta`, `data/News Queries/News.csv`, `data/cascara_geo_trimmed.png`. Working directory = RUNDIR (the `setwd` line is already commented out).

Script order (only `00_Run it all.R` is called; it sources the rest):
1. `00`: `set.seed(10002)`, `logr` log, loads plyr, foreign, ggplot2, readstata13, stringr, tmvtnorm, reshape2, arm, nnet, ebal, lubridate, scales, doMC; `registerDoMC(cores=7)`.
2. `01_Prepare data.R`: reads both survey CSVs, recodes (outcome `Y` 1 to 6, `Authoritarianism`, `T_who`, `T_health_cap`, `T_cases`, age, gender, ideology `LR` with -99 for "not sure", university), drops ages outside 18 to 100 and incomplete rows; reads CCES (`read.dta13`, 4 columns used) and BES (`foreign::read.dta`) as target populations; entropy balancing per country (`set.seed(1230)`, 10,000 target rows sampled with replacement, `ebalance` then `ebalance.trim`), weight `w` normalised to the country N; writes `output/Prepped_survey_data.csv` and `output/Target_data.csv`.
3. `02_Descriptives.R`: bootstrap proportions (Figure 2, Figure A1). Not needed for targets but run as deposited.
4. `03_Estimate main models.R`: `run_models` for US and UK, five models each (m = 1 main); writes `output/Estimates-Main.Rdata` and `output/Estimates_numbers.csv`. Targets come from here.
5. `04` graphs, `05` tables (`output/table_main_UK_1.tex` = Table 2, `output/table_main_US_1.tex` = Table 3), `06`, `07`, `08`, then copies to `output/named_items/`.

Extraction: `scripts/extract_targets.R` loads `output/Estimates-Main.Rdata`, writes `outputs/targets_extracted.csv` with, for each target row: country, X1, Mean, SD, pvalue, N, and also the MLE coefficient and analytic SE (refit not needed if agents save `mod` objects; otherwise the MLE candidate may be obtained in a separate labelled script that re-fits the same `multinom` call). `scripts/build_results.py` builds `results.json` from that CSV. Copy the two `.tex` tables into `outputs/`.

Allowed environment fixes (each saved as a diff):
- `registerDoMC(cores=7)` to `registerDoMC(cores=1)` (or 2). Estimates do not depend on the number of workers because `run_models` calls `set.seed(1230)` itself before the only random draws in the estimation. Strongly recommended for memory, see risks.
- Package versions: the log records R 4.2.2 and, among others, ebal 0.1-8, nnet 7.3-18, MASS 7.3-58.1, arm 1.13-1, plyr 1.8.8, readstata13 0.10.0, foreign 0.8-83, ggplot2 3.4.0, logr 1.3.3. Current CRAN (checked 2026-10-10): ebal 0.2.1, nnet 7.3-21, MASS 7.3-66, arm 1.15-3, readstata13 0.11.0, ggplot2 4.0.3, logr 1.4.0. Try `remotes::install_version("ebal", "0.1-8")` first (ebalance weights feed every estimate); record which version was used. Older ggplot2 or logr may be installed if exports fail.
- If reading the 839 MB CCES file exhausts memory, reading only the four columns the script keeps (`read.dta13(..., select.cols = c("commonweight","birthyr","gender","ideo5"))`, if supported by the installed readstata13) is allowed, because line `CCES <- CCES[, c("commonweight", "birthyr", "gender", "ideo5")]` immediately discards the rest. Row order must be unchanged.
- Making a purely cosmetic export (ggsave, logr) non-fatal if it fails for a system-library reason.

Fallback if the full `03` script cannot finish (memory or the 2-hour limit), labelled as a deviation and reported with the as-is outcome: a script that runs `00` preliminaries and `01` unchanged, then executes, for m = 1 and each country, the authors' lines from `03` unchanged: the subset, `set.seed(1230)`, `multinom(...)`, `mvrnorm(n=5000, ...)` and the `store_coefficients` `adply` block, skipping the simulation of substantive effects. Nothing between `set.seed(1230)` and `mvrnorm` consumes random numbers, so the draws, and hence `Mean`, `SD` and `pvalue`, are the same as in the full run.

Expected sources of small differences (recorded, not fixed): ebal version (weights), BLAS/LAPACK and platform (multinom optimisation path, `mvrnorm` eigen decomposition), R 4.5.x vs 4.2.2. Differences at the second decimal are possible.

## 3. Robustness checks (pre-registered)

All three checks use the main model (m = 1) and the prepared data `output/Prepped_survey_data.csv` from the agent's own run (including its weights `w`), with the authors' formula `form_raw + I(T_who == "WHO") + I(T_who == "WHO.Ratified")` fitted by `nnet::multinom(..., Hess = TRUE, maxit = 500)`. The primary estimate written to `results.json` for every check is the T2 quantity (UK, WHO recommendation plus ratification, outcome "Infected neighbor"); the T1, T3 and T4 quantities are reported in the note field and in the output CSV as secondary. "Same direction and significance as paper" = estimate negative and the check's p-value below .01 (the paper prints ** for T1 to T4).

R_a. Nonparametric case bootstrap (different resampling scheme from the authors' parametric draws). Within each country, using the country's rows of the prepared data with their weights `w` attached and held fixed (weights are not re-estimated), call `set.seed(20261010)` once, then for the UK and then the US draw 1000 resamples of rows with replacement (`sample(n, n, replace = TRUE)`), refit the identical weighted multinom on each, and record the coefficient on each WHO indicator in the Y = 2 equation. Report as estimate the original-sample MLE coefficient, as `se_or_ci` the bootstrap SE and the 95% and 99% percentile intervals, and as p-value the two-sided bootstrap proportion `min(2 * mean(b >= 0), 1)` (for a negative estimate). Fits with `mod$convergence != 0` are counted and reported, not replaced, and excluded from the percentiles. Same direction and significance = estimate negative and the 99% percentile interval excludes 0 (equivalently bootstrap p < .01).

R_b. Extreme-weight exclusion. The outcome is a six-category nominal choice, so a z rule on the outcome is meaningless. The rule for binary outcomes (apply to the main continuous predictor) does not bite either: the only continuous treatment, log cases, takes 12 fixed design values and its z-scores in the deposited CSVs range from -2.18 to 1.12, so |z| > 3 would drop nothing. The continuous quantity that enters every estimate and can have a heavy tail is the entropy-balancing weight. Rule: within each country, compute z of `w` (mean and SD of `w` within that country) and drop rows with |z| > 3. If this drops no row in a country, drop instead the rows in the top 1% of `w` in that country (`w > quantile(w, 0.99)`, type 7). Refit the main model on the remaining rows exactly as the authors do (`set.seed(1230)`, weighted multinom, `mvrnorm(n = 5000)`, `Mean`, `SD`, `pvalue = 2*pt(-abs(Mean/SD), df = nrow of the combined post-exclusion data)`). Report the estimate (`Mean`), SD, p, rows dropped per country and which rule was used. Also report, for information only, the number of rows with |z| > 3 on log(T_cases) and on Age.

R_c. Alternative analysis choice: unweighted estimation. The paper reweights its opt-in Prolific samples to population targets by entropy balancing (p. 376); a reasonable alternative is the unweighted sample. Refit the main model with the identical formula and data but without `weights`, using `set.seed(1230)` and `mvrnorm(n = 5000)` and the authors' `Mean`, `SD` and `pvalue` definitions. Report estimate (`Mean`), SD, p, and the MLE. Same direction and significance = negative and p < .01.

## 4. Known risks

- Memory: in `03`, each `run_models` call allocates `store_cases_tmp` and `store_cases` arrays of about nrow(tmp) x 5000 x 3 x 6 doubles (about 1.1 to 1.2 GB each for N near 1,600) plus `raw_exp` (about 0.4 GB). With `registerDoMC(cores=7)` two forked workers would run at once on a 7 GB machine shared with other agents. Use cores = 1. If it still fails, use the labelled fallback above.
- Reading the 839 MB CCES `.dta` with `read.dta13` may need several GB; see the allowed column-selection fix.
- Package drift: ebal 0.1-8 vs 0.2.1 could change the weights and so every estimate; ggplot2 4.x may reject or warn on old theme arguments (export only). `doMC` uses forking and works on Linux.
- Compute time: the authors' log shows about 21 minutes on their machine with parallel workers; sequential on 2 aarch64 CPUs may take one hour or more, mostly in the simulation part of `03` and the bootstrap in `02`. The 600 s background cap means the run must be split or resumable (e.g. run `00` to `03` in one background job that saves its outputs, then `04` to `08`).
- No Stata or proprietary software needed: Stata files are read by readstata13 and foreign.
- The deposit's terms of use ask users to consider contacting the authors; no contact is made, per protocol.
- Materials appear complete (see DATA_STATEMENT.md): every file the code reads is in the deposit.
