# PREREG: 08_SQRZR8

Written 2026-10-10, about 17:30 IST, before any analysis code was run. No analysis code from the deposit was executed to write this file (the R scripts and README were read as text; the data files were only opened to read their column headers).

- Paper: Guo, Danqi and Genia Kostka (2025/2026). "Knowing Is Disturbing: Emotions and Public Attitudes toward Digital Control under Autocracy". Perspectives on Politics 24(3): 966-987 (September 2026 issue; OpenAlex publication date 2025-11-24). DOI https://doi.org/10.1017/S1537592725103551 . Open Access, CC BY 4.0.
- Text source read: Cambridge Core publisher PDF, https://www.cambridge.org/core/services/aop-cambridge-core/content/view/42AEE2A628849EC66A948C140CBB93F6/S1537592725103551a.pdf/div-class-title-knowing-is-disturbing-emotions-and-public-attitudes-toward-digital-control-under-autocracy-div.pdf (HTTP 200, 22 pages, 1,919,132 bytes, sha256 f221f4cabeb620dab030a6a6504c01a69181edcb5650947e56f93f777d81cd08). Note: Cambridge stamps each page with the download time and IP, so a re-download will have a different sha256; the text content is the same.
- Online appendix (supplementary material) read: https://static.cambridge.org/content/id/urn%3Acambridge.org%3Aid%3Aarticle%3AS1537592725103551/resource/name/S1537592725103551sup001.pdf (HTTP 200, 49 pages, 2,185,952 bytes, sha256 0ed5f4a6898c4f9b48842b73986e6c3c6ac1912d7e250903afcc16e72a10ae56). Used for Table C1 (PCA loadings) and Tables D1/D2 (context only).
- Table 3 was read from a rendered image of PDF page 13 (journal p. 978), saved as `data_statement_raw/paper_p978_table3.png`, because the table is rotated and pdftotext scrambles star placement.
- Dataset: "Replication Data for: Knowing is Disturbing: Emotions and Public Attitudes Toward Digital Control under Autocracy", Harvard Dataverse, https://doi.org/10.7910/DVN/SQRZR8 , version 1.0 (only version), released 2025-10-28, licence CC0 1.0. Metadata: https://dataverse.harvard.edu/api/datasets/:persistentId/?persistentId=doi:10.7910/DVN/SQRZR8 (saved as `data_statement_raw/dataverse_SQRZR8.json`). No file is restricted.

Dataset files (downloaded 2026-10-10 ~11:50 UTC with `curl -A "repro-audit-2026"`, scratch copies in /workspace/audit_runs/08_SQRZR8/prereg/, all checksums in checksums.sha256 there):

| file | datafile id | URL | bytes | sha256 |
|---|---|---|---|---|
| ReadMe.txt | 12134915 | https://dataverse.harvard.edu/api/access/datafile/12134915 | 4151 | 81e723aca5c5822f29c6e4950afa216af5c019e3fc711c732ae363a4fb17d9f7 |
| main_rep.R | 12134913 | https://dataverse.harvard.edu/api/access/datafile/12134913 | 20742 (449 lines) | 4782d605915600b45e7e13a3f58e945c3f3b363612e3e814684d3fcab95b7c79 |
| append_rep.R | 12134912 | https://dataverse.harvard.edu/api/access/datafile/12134912 | 28763 (673 lines) | 25dbed58d2f728716ae77697760bdcb3ad4d2bf5017dbb969f87f33989401310 |
| data_raw_rep.csv | 12134914 | https://dataverse.harvard.edu/api/access/datafile/12134914 | 739447 | 0cb06582f605c74db1076998596a33e4a140a1ebe6bf95f52b48337d2c1178f4 |
| data_cleaned_rep.csv (ORIGINAL format, the file the code reads) | 12134916 | https://dataverse.harvard.edu/api/access/datafile/12134916?format=original | 1252043 | 09089df85d3db59a5609be9be4e8a5e0c3aa5aa2f98571441fcdad207589eb22 (md5 281de2db29ce09fdf6b4f79d31c6f88d = Dataverse-listed md5) |
| data_cleaned_rep.tab (Dataverse ingested archival copy, default download) | 12134916 | https://dataverse.harvard.edu/api/access/datafile/12134916 | 1306127 | 44e7b691b83228311a7617d4c28b1761ee6dba69150205a44cb25fe02b52c7a6 |

Important: the scripts read `read.csv("data_cleaned_rep.csv", sep=",")` (main_rep.R line 22, append_rep.R line 27). The default Dataverse download is the tab-separated ingested `.tab`; agents must download with `?format=original` and save it as `data_cleaned_rep.csv`. Check its md5 equals 281de2db29ce09fdf6b4f79d31c6f88d.

## 1. Headline results and targets

Main claim (abstract): in a survey experiment in China (n = 4,507), exposure to revealing information about digital control "slightly amplifies negative emotions but profoundly reduces positive emotions and significantly undermines public support for authoritarian digital governance. These effects are more pronounced in the context of digital surveillance than censorship and are most severe when individuals perceive control measures as personally targeted."

The table that reports the surveillance-versus-censorship and personalized-versus-public comparison with the paper's main specification is Table 3 (p. 978, "Main Effects of Digital Surveillance and Digital Censorship on Emotions and Public Attitudes"): OLS with controls, robust SEs, N = 4,057. Column (1) of each outcome (main effects, no interaction) is the specification the targets use. In the code it is `all_models$<outcome>.mod2` = `lm_robust(<outcome> ~ surveillance_fac + censorship_fac + <18 covariates>, data = data)` (main_rep.R lines 340-369; `estimatr::lm_robust` default se_type HC2). Coefficient names in R: `surveillance_facPersonalized`, `censorship_facPersonalized`.

Targets (copied exactly from Table 3, read from the page image):

| id | quantity | paper value | decimals | location |
|---|---|---|---|---|
| T1 | Coefficient of Surveillance [Personalized] on positive emotions (`positive_emo_rv`), column (1) | -0.201 (SE 0.058, ***) | 3 | Table 3, p. 978, row "Surveillance [Personalized]", column Positive (1) |
| T2 | Coefficient of Surveillance [Personalized] on negative emotions (`negative_emo`), column (1) | 0.211 (SE 0.079, **) | 3 | Table 3, p. 978, row "Surveillance [Personalized]", column Negative (1) |
| T3 | Coefficient of Surveillance [Personalized] on attitude, fictive scenario (`general_attitude_fic`), column (1) | -0.532 (SE 0.099, ***) | 3 | Table 3, p. 978, row "Surveillance [Personalized]", column Attitude (fictive) (1) |
| T4 | Coefficient of Surveillance [Personalized] on attitude, real-life (`general_attitude_real`), column (1) | -0.237 (SE 0.079, **) | 3 | Table 3, p. 978, row "Surveillance [Personalized]", column Attitude (real-life) (1) |
| T5 | Coefficient of Censorship [Personalized] on attitude, fictive scenario (`general_attitude_fic`), column (1) | -0.352 (SE 0.096, ***) | 3 | Table 3, p. 978, row "Censorship [Personalized]", column Attitude (fictive) (1) |
| T6 | Number of observations in the Table 3 models (`nobs` of each column (1) model) | 4057 | 0 | Table 3 note, p. 978: "N = 4,057 across all models" |

T3 and T5 together carry the "surveillance stronger than censorship" comparison; T1 to T4 carry "slightly amplifies negative, profoundly reduces positive, undermines support", for the personalized level.

Conclusion criterion for `same_conclusion` (stars in Table 3: * p < 0.05, ** p < 0.01, *** p < 0.001; robust SE as computed by the authors' `lm_robust` call):
- T1, T3, T5: same sign as the paper (negative) and p < 0.001.
- T2: same sign (positive) and p < 0.01.
- T4: same sign (negative) and p < 0.01.
- T6: reproduced N within 5 of 4057.
The significance bucket is read from the reproduced p-value of the same `lm_robust` model; the SE values above are context, not targets.

Secondary numbers agents may report as context only (not targets): Figure 2 / text p. 975 b = -0.55 ("personal both"), b = -0.52 (personalized surveillance) and b = -0.28 (public surveillance) on positive emotions, which are the no-control condition-dummy models (main_rep.R lines 77 and 110; same coefficients appear in online Table D1 as -0.549, -0.524, -0.285 with Observations 4507); Table 3 R2 for column (1): Positive 0.100, Negative 0.131, Attitude (fictive) 0.288, Attitude (real-life) 0.400.

Inconsistencies noticed while reading (described, not judged):
- N: abstract/methods say the final sample is 4,507 (p. 967, p. 972); Table 1 cell sizes sum to 4,507; online Tables D1/D2 (no controls) report Observations 4507. Table 3 (with controls) reports N = 4,057. This may be listwise deletion of missing covariates in `lm_robust`, or a digit transposition; I did not check it (that would require running the analysis).
- main_rep.R line 371 comments the Table 3 block as "models without control, with and without interaction Table D2", but the models in that block (lines 352-361) include `covariates_str`. The table object is named `tab_3`, and the paper's Table 3 is the with-controls table.
- The Table 3 note lists controls as "age, gender, education, income, rural residence, ethnic minority, CCP membership, overseas experiences, political ideology, VPN familiarity, personal values, and personality traits". The code's `covariates_str` (lines 156-162) also includes `LifeSat_1` (life satisfaction), not named in the note.
- ReadMe.txt says analyses used R 4.3.2 on macOS 15.6.1 and lists a code file `data_preparation_rep.R` that builds `data_cleaned_rep.csv` from `data_raw_rep.csv`; that file is not in the deposit (see DATA_STATEMENT.md). The targets need only `data_cleaned_rep.csv`, which is deposited.
- main_rep.R calls `mediation::mediate` (line 238) without `library(mediation)`; this works only if the package is installed. main_rep.R sets no seed, so Figure 3 (mediation bootstrap) is not seed-fixed; this does not touch the targets.

## 2. Reproduction plan

Script: `main_rep.R` only (append_rep.R reproduces appendix tables; not needed for targets). Working directory = a folder holding `main_rep.R` and `data_cleaned_rep.csv` (original-format download).

Pipeline (line numbers of the deposited main_rep.R):
1. Lines 14-19: load tidyverse, ltm, coefplot, ggpubr, estimatr, sjPlot. Line 22: read `data_cleaned_rep.csv`.
2. Lines 37-64: PCA with `princomp()` on 10 emotion items (covariance matrix); `negative_emo` = Comp.1, `positive_emo_rv` = -1 x Comp.2, `neutral_emo_rv` = -1 x Comp.3. Lines 67-68: attitude indices = row sums of the four items.
3. Lines 73-146: Figure 2 models (no controls). Lines 156-162: `covariates_str` (needed by Table 3). Lines 185-331: mediation (Figure 3), commented as taking 15-20 minutes.
4. Lines 340-389: Table 3. Factors `surveillance_fac`, `censorship_fac` (baseline "No Mention"); `fit_models()` fits `mod2` (main effects) and `mod4` (interactions) with `lm_robust` for 5 outcomes; `tab_3 <- tab_model(...)` builds an HTML table (not written to disk).

Run: `Rscript -e 'source("main_rep.R", echo=TRUE, max.deparse.length=Inf); save(all_models, pca_emotion, data, file="outputs/session_models.RData")'` with stdout/stderr logged to `outputs/`. Then `scripts/extract_targets.R` loads the saved objects and writes `outputs/targets_extracted.csv` with, for each of the 5 outcomes, the `mod2` coefficient, SE, p-value and nobs for `surveillance_facPersonalized`, `surveillance_facPublic`, `censorship_facPersonalized`, `censorship_facPublic`, plus `summary(pca_emotion, loadings = TRUE)` loadings to `outputs/pca_loadings.csv`. `scripts/build_results.py` builds `results.json` from those CSVs. Optionally also write `tab_3` to `outputs/tab_3.html` with `sjPlot` (`file=` argument via a separate call in the extraction script, not by editing the authors' file).

Where each target comes from: T1 `all_models$positive_emo_rv.mod2`, T2 `all_models$negative_emo.mod2`, T3 and T5 `all_models$general_attitude_fic.mod2`, T4 `all_models$general_attitude_real.mod2`; T6 `nobs()` of each of these (all should be equal; report all five).

Allowed environment fixes (each saved as a diff with a reason): installing missing packages (including `mediation`, which line 238 needs); path or working directory; if the full script cannot finish inside one background-shell window (mediation step), running the authors' unchanged lines in their original order across segments in one saved session (`save.image()` / `load()` between segments) is an execution arrangement, logged in LOG.md, not a code change. If a plotting call fails only for a missing system font/graphics library, making that line non-fatal is allowed (diff), since no target depends on plots.

PCA sign rule (decided now): eigenvector signs from `princomp` can differ by platform/LAPACK. Agents record the loadings and compare signs with online Table C1 (Comp.1: Sadness +0.400; Comp.2: Happiness -0.659, Secured -0.586; Comp.3: Curiosity -0.635, Surprised -0.558). The as-is run is the reproduction result. If any of Comp.1 to Comp.3 has the opposite sign to Table C1, the agent also reports a sign-aligned run (multiply that component's scores by -1 so loadings match Table C1, then rerun Table 3) as a logged deviation in the spirit of CHANGELOG #4(c), with both results shown; the as-is class is reported alongside. T3 to T5 do not depend on the PCA; T1 and T2 do.

Expected sources of small differences (recorded, not fixed): R 4.5.x on aarch64 Debian here vs R 4.3.2 on macOS for the authors; `estimatr` version (HC2 is the default throughout recent versions). The targets are deterministic OLS; no random numbers are involved in T1 to T6.

## 3. Robustness checks (pre-registered)

Primary quantity for all checks: T1, the Surveillance [Personalized] coefficient on positive emotions in Table 3 column (1) (`all_models$positive_emo_rv.mod2`), which carries the abstract's "profoundly reduces positive emotions" and "personally targeted surveillance" claims. Secondary (reported, not primary in results.json): T3, the same coefficient on `general_attitude_fic`. Inference uses `lm_robust` HC2 as in the paper. "Same direction and significance as paper" = negative coefficient and p < 0.001 (as in Table 3 for both T1 and T3), unless stated otherwise below.

R_a. Nonparametric case bootstrap. Take the estimation sample of the T1 model (rows of `data` with no missing value in `positive_emo_rv`, the two factors and the 18 covariates, i.e. the rows `lm_robust` used). Keep the PCA scores as computed on the full data (do not re-run PCA inside the bootstrap). Call `set.seed(20261009)` once, draw 1000 resamples of rows with replacement (`sample(n, n, replace = TRUE)`), refit the identical formula with `lm()` (point estimates equal `lm_robust`'s), and record the `surveillance_facPersonalized` coefficient. Report the original-sample estimate, the bootstrap SE, the percentile 95% CI (2.5th and 97.5th percentiles), and as p-value min(2 x share of draws >= 0, 1). Resamples where a factor level is absent or a coefficient is NA are counted and reported, not replaced. Same direction and significance = estimate negative and the percentile CI excludes 0. Repeat for T3 (secondary) with the same seed reset.

R_b. Outlier exclusion on the outcome. In the T1 estimation sample, compute z = (positive_emo_rv - mean) / sd over that sample; drop rows with |z| > 3; refit the identical `lm_robust` call on the remaining rows; report the coefficient, HC2 SE, p-value and the number of rows dropped. For T3 (secondary), apply the same rule to `general_attitude_fic` in its own estimation sample. If no row has |z| > 3, report "0 dropped" and the unchanged estimate.

R_c. Alternative outcome construction for positive emotion. Instead of the PCA score, define the positive-emotion outcome as the row mean of the two items the paper describes as positive valence ("security and happiness", p. 974): `pos_mean = (Secured + Happiness) / 2`, then standardize it to mean 0, SD 1 over the T1 estimation sample. Refit the identical `lm_robust` formula (same factors, same 18 covariates, same data rows) with `pos_mean_z` as outcome; report the `surveillance_facPersonalized` coefficient, HC2 SE and p-value. This check does not use PCA signs, so it is unaffected by the sign issue. Same direction and significance = negative and p < 0.001. Secondary for T3: none (attitude indices are already simple sums).

All three checks are written as the agent's own scripts in `scripts/` that load the saved session objects; the authors' file is not edited.

## 4. Known risks

- Data file format: the default Dataverse download is `.tab`; the code reads `.csv`. Use `?format=original` (see above). Using the `.tab` with `sep=","` would read one column and fail.
- Missing file: `data_preparation_rep.R` (named in ReadMe.txt) is not deposited, so the step from `data_raw_rep.csv` to `data_cleaned_rep.csv` cannot be reproduced or checked. The targets need only the cleaned file, which is present. Whether this makes the paper C is for the class rules (CHANGELOG #4) to decide; the README itself says the preparation step can be skipped "to directly start the analytical part".
- N = 4,057 vs 4,507: if the reproduced Table 3 models use 4,507 rows (no missing covariates), T6 will not match while T1 to T5 may also differ; this would be recorded as found.
- PCA sign/platform dependence for T1 and T2 (handled by the sign rule above).
- Compute: small (4,507 rows). The mediation block (32 `mediate()` calls with 1000 bootstrap sims each) is commented as 15 to 20 minutes on the authors' machine; on 2 CPUs it may take longer and exceed one 600 s background window, hence the segmented-run allowance. R_a is 2 x 1000 small `lm` fits, about a minute.
- Dependencies: CRAN packages tidyverse, ltm (needs msm, polycor), coefplot, ggpubr, estimatr, sjPlot, mediation (for line 238). No Stata, MATLAB or proprietary dependency. No version pins besides "R 4.3.2" in ReadMe.txt. `sjPlot`/`ggpubr` pull many dependencies; they only affect tables/plots, but the script stops at the first error, so they must install or be handled as env fixes.
- Licence: deposit CC0 1.0; article CC BY 4.0. Public downloads, no sign-in.
