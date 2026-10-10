# PREREG: 06_VSV5DM

Written 2026-10-10 (IST, about 17:55), before any analysis code was run. No analysis code of the authors was executed to write this file. The two .Rdata files were opened only to list object names and column headers (Python `rdata` reader, no model fitted, no statistic computed).

Read for this pre-registration: REPO/PROTOCOL.md (sections 5 to 7), REPO/AGENT_RUNBOOK.md, REPO/CHANGELOG_METHOD.md (#4 and #5 apply), REPO/papers/06_VSV5DM/META.md, REPO/batches/batch2_prereg_brief.md; format model REPO/papers/05_FNTC1J/PREREG.md and targets.json.

## Paper and text sources

- Paper: Strawbridge, M., Masuoka, N., Brown, N. E., and Hanson, E. (2025). "Leadership in a Pandemic: State Legislator Constituent Outreach in Response to COVID-19". Political Research Quarterly 78(2), 437-452. First published online 2024-12-03. DOI https://doi.org/10.1177/10659129241301785 . Open access, CC BY-NC 4.0.
- Main article PDF read (16 pages, journal pp. 437-452): obtained 2026-10-10 about 12:23 UTC by the Hark browser agent from https://journals.sagepub.com/doi/pdf/10.1177/10659129241301785 opened in Chrome's PDF viewer and saved (direct curl gets HTTP 403 from Cloudflare). 1,295,791 bytes, sha256 ae02f4271a1cafefe627895cacb963763997fbba280ee2ae6408b3412e639081. PDF metadata Subject "Political Research Quarterly 2025.78:437-452". Because it came through a browser save, a direct download by another agent may have different bytes; the text is what matters. Text extracted with `pdftotext -layout`; the target passage is saved in `data_statement_raw/article_targets_excerpt_p8.txt`.
- The publisher HTML full text (https://journals.sagepub.com/doi/full/10.1177/10659129241301785, read 2026-10-10 about 11:55 UTC via a text fetcher) gives the same target sentences.
- Online appendix (Sage supplement `sj-pdf-1-prq-10.1177_10659129241301785.pdf`, 49 pages, PDF metadata Creator "Microsoft Word 2010", author "Michael Strawbridge", created 2024-11-14): obtained 2026-10-10 about 12:07 UTC by the browser agent via https://journals.sagepub.com/action/downloadSupplement?doi=10.1177%2F10659129241301785&file=sj-pdf-1-prq-10.1177_10659129241301785.pdf (the /doi/suppl/... link and the Google Docs viewer were blocked). 568,638 bytes, sha256 9db99f76a93334cdd993edca78eb9a84d80255c899275893dc40f6efce788dd6. Text extracted with `pdftotext -layout`; Tables A8, A9, A10 are saved in `data_statement_raw/appendix_A8_A9_A10_excerpt.txt`. Appendix PDF page numbers equal the printed "Appendix Page N" footers.
- Source NOT used: an earlier browser transcription of the appendix (notes under /workspace/web/notes/.../sage-prq-06-tu_mpomucixp3vn2zlo344jck3qar/) disagrees with the appendix PDF text in many cells (for example Table A10 entirely, and the A8 COVID value for Democratic White Men). Every appendix number below was copied from the `pdftotext` output of the PDF itself, not from that transcription.
- Local copies and hashes: /workspace/audit_runs/06_VSV5DM/prereg/ (`article.pdf`, `appendix_sj-pdf-1.pdf`, `checksums.sha256`, copied to `data_statement_raw/prereg_downloads.sha256`).

## Dataset

"Replication Data for: Leadership in a Pandemic: State Legislator Constituent Outreach in Response to COVID-19", Harvard Dataverse, https://doi.org/10.7910/DVN/VSV5DM , version 1.0, released 2024-11-06, licence CC0 1.0. File list API: https://dataverse.harvard.edu/api/datasets/:persistentId/?persistentId=doi:10.7910/DVN/VSV5DM (saved as `data_statement_raw/dataverse_VSV5DM.json`). No file restricted. Downloaded 2026-10-10 about 11:49 UTC with `curl -L -A "repro-audit-2026"`; every MD5 matches the Dataverse metadata.

| datafile id | file | URL | bytes | sha256 |
|---|---|---|---|---|
| 10692911 | Multivariate Analysis.Rmd | https://dataverse.harvard.edu/api/access/datafile/10692911 | 68539 | 29ad88f0381fa357114ecedf8cbc920563140939e6f946081df926046e02421c |
| 10692910 | Time-Series Analysis.Rmd | https://dataverse.harvard.edu/api/access/datafile/10692910 | 40867 | fb4d5ebadcc6e871ca7f54a9265c3ca19239ac1908be26a0ed59514f0b82668e |
| 10692909 | StateLeg_COVIDFacebookActivity.Rdata | https://dataverse.harvard.edu/api/access/datafile/10692909 | 158004 | 9fa44dba34f83290c4e4ee3609ce2d3bbf1403f8a1efecbbc8a1ef61961ca9d4 |
| 10692912 | StateLeg_WeeklyCOVIDFacebookActivity.RData | https://dataverse.harvard.edu/api/access/datafile/10692912 | 459760 | cad5d921212c6766e838a6dfc80d9f937e280589113a27ac38c065116005d07b |
| 10692913 | ReadMe File.txt | https://dataverse.harvard.edu/api/access/datafile/10692913 | 1460 | a4094246ff0db327ba9d72a4f47a297279f0d74f571258c47d3a410d94be70b4 |

Contents seen (headers only): `StateLeg_COVIDFacebookActivity.Rdata` holds one data frame `by_leg`, 654 rows x 82 columns, including every variable in the model formula (`covid`, `rpg`, `senator`, `age_rescaled`, `leader_or_chair`, `X.voteTrump2016_resclaed`, `Last.Vote.Share`, `Bill.Sponsor.2019_rescaled`, `COVID.Rate.per.100.000_rescaled`, `perc_white`, `Population.Density..Per.sq.mile._rescaled`, `College_Educated_rescaled`, `median_income_rescaled`, `State`, `general_rescaled`). `StateLeg_WeeklyCOVIDFacebookActivity.RData` holds `by_week`, 25451 x 78. Both are processed counts; the README says the raw Facebook post text is restricted (used under licence) and is not deposited.

## 1. Headline results and targets

Main claim (abstract): "This study finds there to be important variation by partisanship, but within party, we find important differences depending on both the race and gender of the legislator. Democratic women of all races were those legislators most actively providing information and outreach related to COVID-19 to their constituents in 2020." The abstract gives no numbers. The quantitative result behind it is the multivariate analysis of total COVID posts per legislator (January to September 2020): quasi-Poisson regression with a six-level race-gender-party factor (reference Republican white men) plus controls and state, turned into differences in expected counts (Figure 4, Appendix Table A8). Article p. 444 (PDF p. 8): "we find that Democratic white women made, on average, 10.21 more posts about COVID in our period of interest compared to Republican white men; however, this finding is only significant at p = .054. Similarly, Democratic men of color and women of color averaged 17.28 and 15.05 more posts about COVID relative to Republican white men."

Targets (copied exactly from the paper):

| id | quantity | paper value | decimals | location |
|---|---|---|---|---|
| T1 | AME, Democratic White Women vs Republican White Men, COVID count model | 10.21 | 2 | Article p. 444 (PDF p. 8) text; Appendix Table A8 (appendix p. 16), row "Democratic White Women", column "COVID": 10.21 (-0.3 20.72) |
| T2 | AME, Democratic Men of Color vs Republican White Men, COVID model | 17.28 | 2 | Article p. 444 text; Table A8, row "Democratic Men of Color", COVID: 17.28 (4.88 29.68), bold |
| T3 | AME, Democratic Women of Color vs Republican White Men, COVID model | 15.05 | 2 | Article p. 444 text; Table A8, row "Democratic Women of Color", COVID: 15.05 (2.69 27.42), bold |
| T4 | p-value of T1 | 0.054 | 3 | Article p. 444 text "only significant at p = .054" |
| T5 | Quasi-Poisson coefficient, Democratic White Women, COVID model | 0.16 | 2 | Appendix Table A10 (appendix p. 18), row "Democratic White Women", column "COVID": 0.16 (0.09)* |
| T6 | Num. obs., COVID model | 635 | 0 | Appendix Table A10 (appendix p. 19), row "Num. obs.", column "COVID" |

Conclusion criterion for `same_conclusion` (per target):
- T1: AME > 0 and 0.05 <= p < 0.10 (positive, not significant at .05, as the text says "only significant at p = .054" and A8 does not print it in bold).
- T2, T3: AME > 0 and p < 0.05 (A8 prints both in bold, "statistically significant (p < .05)", CIs exclude 0).
- T4: 0.05 <= p < 0.10.
- T5: coefficient > 0 and 0.05 <= p < 0.10 (one star in A10; legend "***p < 0.01; **p < 0.05; *p < 0.1"), p taken from `summary(covid)` (t test with estimated dispersion, which is what texreg uses for the stars).
- T6: N equal to 635 (deterministic; no imputation or randomness in this pipeline). If N differs, `same_conclusion` is false for T6 and the difference is reported.

The AME p-value and CI are the delta-method values from `summary(margins(...))` (columns `p`, `lower`, `upper`), as in the authors' code.

Secondary context numbers (not targets; agents may report them): Table A8 COVID column also has Democratic White Men 5.38 (-4.64 15.41) and Republican White Women 6.1 (-6.22 18.41). Table A10 COVID column: Constant 3.51 (0.19)***, Democratic White Men 0.09 (0.09), Republican White Women 0.10 (0.10), Democratic MOC 0.26 (0.10)***, Democratic WOC 0.23 (0.10)**, Total Posts 6.73 (0.17)***, Deviance 10622.6. Table A9 (Democratic White Women as reference) COVID column: Democratic Men of Color 7.07 (-4.67 18.82), Democratic Women of Color 4.84 (-6.85 16.54), Republican White Men -10.21 (-20.72 0.3).

Inconsistencies noticed while reading (described, not judged):
- Method wording vs code: the article (p. 444, and the notes of Figure 4 and Table A8) says expected counts are computed "hold[ing] all other covariates at their mean observed values". The code (Multivariate Analysis.Rmd line 521) uses `margins(covid, variables="rpg", data = by_leg2)`, whose default for a factor is the average over observed rows of the discrete change in predicted counts, not a prediction at covariate means. The targets are the numbers in A8 and the text, so agents reproduce the `margins` output as coded.
- Appendix Tables A14/A15 are titled "Fractional Logit Regression Models"; the code chunk that produces them ("##Fractional Logit Models", lines 995-1057) fits `betareg` (beta regression) on proportions + 0.00001, with a comment saying the constant is needed because "the lm function requires" it. Not a target.
- Sample counts: article says 654 legislators (335 white men, 101 white women, 114 men of color, 104 women of color); footnote 16 says "632 out of 653"; models report 635 observations. The Rmd hard-codes group sizes (lines 61/260 and 160/381: 335/101/114/104 and 242/91/38/63/108/101, sum 643 after dropping 11 legislators); the detailed-race chunk (line 1094) hard-codes White Women freq 102 while the label says n=101. Why 643 becomes 635 in the models is not stated (presumably missing covariates; not checked, no data were summarised).
- Deposit README describes "Main Analysis.Rmd" ("produces all of the tables and figures that appear in the time series analysis"); no file of that name is in the deposit; the time-series file is "Time-Series Analysis.Rmd". README also names an output folder "..._v2" that the code never writes to.
- Dataverse citation metadata gives the article title as "Leadership in a Pandemic: State Legislator Constituent Activities in Response to COVID-19" and author order Strawbridge, Brown, Hanson, Masuoka; the published article says "Constituent Outreach" and order Strawbridge, Masuoka, Brown, Hanson. The appendix PDF title says "Constituent Services".

## 2. Reproduction plan

Only `Multivariate Analysis.Rmd` and `StateLeg_COVIDFacebookActivity.Rdata` are needed for the targets. `Time-Series Analysis.Rmd` (glmer models, Table 1, A16 to A20) is not needed for any target; agents may run it for completeness if time allows, but its outcome does not affect the class.

Pipeline (line numbers of the deposited Rmd):
1. Lines 5-23: libraries (foreign, ggplot2, dplyr, tidytext, lubridate, readr, scales, broom, httr, rtweet, ggeffects, ggpubr, devtools, stringr, rio, eeptools); later chunks add xtable, texreg, margins, betareg.
2. Line 27: `load("StateLeg_COVIDFacebookActivity.Rdata")` gives `by_leg`. Lines 30-37: drop Independent White Men, Republican Men of Color, Republican Women of Color into `by_leg2`; set `rpg` levels with "Republican White Men" first; `rpg2` with "Democratic White Women" first.
3. Lines 481-709 (chunk "##Count Models -Republican White Men as a reference"): line 485 `covid = glm(covid ~ rpg + senator + age_rescaled + leader_or_chair + X.voteTrump2016_resclaed + Last.Vote.Share + Bill.Sponsor.2019_rescaled + COVID.Rate.per.100.000_rescaled + perc_white + Population.Density..Per.sq.mile._rescaled + College_Educated_rescaled + median_income_rescaled + State + general_rescaled, family = "quasipoisson", data = by_leg2)`; line 508 `htmlreg(...)` writes `Total Activity Analysis_RaceAndGenderAndParty_v1/CountModel_WhiteGOPmen_reference_racegenderparty.doc` (Table A10); line 521 `res2 <- margins(covid, variables="rpg", data = by_leg2)`; line 534 `covid_marg = as.data.frame(summary(res2))`; line 708 writes `marginaleffects_table_white_men_gop.doc` (Table A8, AME and CI rounded to 2 dp) and line 668 `ggexport` writes Figure 4 as `marginaleffects_white_men_gop.pdf`.
4. The object name `covid` is reused later (lines 715, 942, 973, betareg at 1008, lm at 1061), so targets must be extracted right after the chunk ending at line 709, not at the end of the file.

How to run:
- Working directory RUNDIR containing the two .Rdata files and the Rmd. Create the output folders the code writes to: `Total Activity Analysis_RaceAndGender/`, `Total Activity Analysis_RaceAndGenderAndParty_v1/` (and `..._v2/` for safety). Creating folders is an environment fix; record it.
- Extract the R code with `knitr::purl("Multivariate Analysis.Rmd", output = "multivariate.R", documentation = 0)` (no pandoc needed). Run the full `multivariate.R` with `source(..., echo = TRUE)`, logging to `outputs/`.
- Target extraction: `scripts/extract_targets.R` sources the purled code only up to and including the end of the chunk at Rmd line 709 (identify the cut point by the `rg_me` html export line, not by a hand-typed line number in the .R file), then writes `outputs/targets_extracted.csv` with: for each of the five `rpg` levels, unrounded AME, SE, z, p, lower, upper from `summary(res2)`; `coef`, SE, t, p from `summary(covid)$coefficients` for the five `rpg` terms; `nobs(covid)`; `deviance(covid)`. `scripts/build_results.py` builds `results.json` from that CSV. Also copy the authors' html outputs (`CountModel_WhiteGOPmen_reference_racegenderparty.doc`, `marginaleffects_table_white_men_gop.doc`) into `outputs/` as a cross-check.
- T1, T2, T3: `AME` for factor levels `rpgDemocratic White Women`, `rpgDemocratic Men of Color`, `rpgDemocratic Women of Color` in `summary(res2)`. T4: `p` for `rpgDemocratic White Women`. T5: `coef(covid)["rpgDemocratic White Women"]`. T6: `nobs(covid)`.

Allowed environment fixes (each saved as a diff with reason):
- Create the output directories.
- `rtweet` was archived on CRAN on 2025-04-07 (CRAN page checked 2026-10-10 12:23 UTC). Try `remotes::install_version("rtweet", ...)` from the CRAN archive first. No rtweet function is called anywhere in the Rmd (grep for `search_tweets|get_timeline|lookup_|rtweet::` finds nothing), so if it cannot be installed the allowed fix is to comment out `library(rtweet)` (line 15), saved as a diff with this grep as evidence.
- Comment out any other `library()` line only if the package cannot be installed and grep shows none of its functions is used; otherwise classify accordingly.
- If a purely cosmetic export (`ggexport`, `htmlreg(file=)`, `print(xtable(...), file=)`) fails for a system-library reason, make that line non-fatal with a diff; estimates are not affected.
- If an indexing line such as `basics2=basics[,c(25,2,4:11)]` errors because of a package-version difference in column order, record the error verbatim; do not edit the analysis; extraction of the targets only needs the code up to line 709, and the count-model chunk does not depend on `basics2`.

Randomness: none. The Rmd has no `set.seed`, no sampling, no bootstrap; quasi-Poisson fit and delta-method margins are deterministic. Small differences can only come from package versions (margins/prediction numerical derivatives) and platform. No R or package versions are given anywhere in the deposit.

## 3. Robustness checks (pre-registered)

All checks use the COVID count model as specified at Rmd line 485, on the exact rows it used (`model.frame(covid)`, expected n = 635). Primary estimate written to `results.json` for each check: the Democratic Women of Color AME (T3 quantity). Secondary, reported in the `note` field and in the check's output CSV: the Democratic Men of Color AME (T2) and the Democratic White Women AME (T1) with their p-values. "Same direction and significance as paper" for the primary estimate = AME > 0 and p < 0.05 (or, for R_a, percentile 95% CI excludes 0). For the secondary estimates the paper pattern is T2 > 0 with p < 0.05 and T1 > 0 with 0.05 <= p < 0.10; each is reported as matching or not.

R_a. Nonparametric case bootstrap (the analysis has no seed to vary). `set.seed(20261010)` once; B = 1000 resamples of the 635 rows of `model.frame(covid)` with replacement (`sample(n, n, replace = TRUE)`); refit the identical formula with `family = quasipoisson` on each resample; compute the AME for each of the three Democratic groups directly as `mean(predict(fit, newdata = d_with_rpg_set_to_level, type = "response") - predict(fit, newdata = d_with_rpg_set_to_"Republican White Men", type = "response"))` over the resample rows, where the factor keeps all six levels. Before the bootstrap, verify on the original data that this direct formula equals the `margins` AME for all five levels to within 1e-6 and write that check to `outputs/`. A resample in which any `rpg` or `State` level is absent or any coefficient is NA is counted and dropped (not replaced) and the count is reported. Report: original-sample AME as estimate, bootstrap percentile 95% CI as `se_or_ci`, bootstrap SE, and p = min(1, 2 * min(share of AME <= 0, share of AME >= 0)).

R_b. Outlier exclusion on the outcome (the outcome `covid` is a count, so the default rule applies). Within the 635 estimation rows compute z = (covid - mean(covid)) / sd(covid); drop rows with |z| > 3; refit the identical quasi-Poisson model on the remaining rows; recompute the AMEs with `margins(fit, variables = "rpg", data = <reduced data>)`. Report AME, delta-method SE, p and CI for the three Democratic groups, the number of rows dropped and their `rpg` groups. Same direction and significance as defined above.

R_c. Alternative reasonable analysis choice: negative binomial instead of quasi-Poisson for the overdispersed count (the paper cites Ver Hoef and Boveng 2007 on exactly this choice). Fit `MASS::glm.nb` with the identical formula on the 635 rows; compute AMEs with `margins(fit, variables = "rpg", data = <same rows>)`. Report AME, SE, p, CI for the three Democratic groups and theta. If `glm.nb` does not converge, report that (with the warning text) and do not substitute another model.

## 4. Known risks

- Missing files: none for the targets. The code reads two files (`load("StateLeg_COVIDFacebookActivity.Rdata")`, Multivariate line 27; `load("StateLeg_WeeklyCOVIDFacebookActivity.RData")`, Time-Series line 22) and both are in the deposit with the exact names. Raw post text and the keyword-counting step are not deposited (README: restricted, used under licence), so the construction of the counts cannot be checked; this does not block reproducing the reported models from the deposited counts.
- Package availability: `rtweet` archived from CRAN 2025-04-07 (loaded but unused; see allowed fix). `margins` 0.3.28 (published 2024-07-31) and `eeptools` are on CRAN. Time-Series file also needs lme4, performance, see, qqplotr, stargazer (all on CRAN). No proprietary or Stata dependency. `devtools`, `httr`, `tidytext` pull system libraries (curl, openssl, libxml2) on aarch64; they are unused for the targets, but a failed install would stop `library()`.
- Version drift: no sessionInfo or version pins in the deposit. `margins` computes numerical derivatives through `prediction`; differences in the 3rd decimal are possible.
- Compute: tiny for the targets (635 rows). R_a needs 1000 glm refits and 2 x 3 predictions each (about 1 to 3 minutes). The Time-Series glmer models (25,451 rows, Poisson GLMM, 36 models) may take long; they are not needed for any target.
- Text sources came through a browser because Sage blocks scripted downloads (Cloudflare, HTTP 403); a second agent may need the same browser route (`/action/downloadSupplement?...` for the appendix, `/doi/pdf/...` for the article).
- Main risk for class C: low on materials (all read files present). Main risk for a D-like discrepancy: T1/T4 sits near the .05 boundary (p = .054), so a small numerical difference could move it across .05; this is why the T1 criterion is a band, and it is reported, not resolved.
