# PREREG: 19_KH0SQ2

Written 2026-10-10, 23:00 IST, before any analysis code was run. None of the authors' scripts (`main_text_figs_JEPP_FINAL.R`, `Appendix_plus.R`) was executed, in whole or in part, to write this file. The main text and the Online Appendix were both read; the appendix tables are images and were read from page renders at 200 and 300 dpi.

Disclosure of data inspection done before writing (no model was fitted): the five `.RData` files were loaded in R only to list object names, column names, factor levels, row counts by country and treatment, counts of non-missing `Support`, `Masculine` and `Weight`, and the z-score ranges of `Support`, `Weight` and `Masculine` in the treated samples. These counts were used only to check feasibility of the checks below; they are reported where used.

## Paper and sources read

- Paper: Coffé, H., Saha, S., & Catalano Weeks, A. (2024, online 16 Sep 2024; issue 2025). "Quotas or parity? How the framing of positive action measures impacts public support and backlash". Journal of European Public Policy, 32(10), 2409-2438. DOI https://doi.org/10.1080/13501763.2024.2402864 . Open access (CC BY).
- Main text read: publisher full-text HTML https://www.tandfonline.com/doi/full/10.1080/13501763.2024.2402864 , copy obtained 2026-10-10 through the agent's web_fetch tool (direct curl gets HTTP 403 from Cloudflare). Scratch copy `/workspace/audit_runs/19_KH0SQ2/prereg/tandf_page.txt`, 169,418 bytes, sha256 22b24847e43104b2a8425d20294279d6435ed1bc8e364fff5efda2d53a2e016e (an HTML-to-text extraction, not the publisher file itself). The publisher PDF (31 pages incl. cover) was also viewed in a browser without sign-in on 2026-10-10 to confirm the abstract N and the absence of a data statement; it was not downloaded, so it has no hash.
- Online Appendix read: `rjpp_a_2402864_sm5162.pdf`, the T&F supplement, downloaded from its figshare copy (https://doi.org/10.6084/m9.figshare.27036622.v1 , file https://ndownloader.figshare.com/files/49219486 ), 4,962,072 bytes, md5 017b34d5face365160473a12c7d5c20d (matches figshare's computed_md5), sha256 4f00b351cb593c5bd90d85a88df93b66c9c7f607414cbd03d2c9e7bab28040f2. 34 PDF pages; Tables S1 to S26 are embedded images.
- Dataset: "Replication Data for: QUOTAS OR PARITY? ...", Harvard Dataverse, https://doi.org/10.7910/DVN/KH0SQ2 , version 2 (released 2024-07-11), licence CC0 1.0. File list API: https://dataverse.harvard.edu/api/datasets/:persistentId/?persistentId=doi:10.7910/DVN/KH0SQ2 . Downloaded 2026-10-10 with `curl -A "repro-audit-2026"` from `https://dataverse.harvard.edu/api/access/datafile/<id>?format=original`. Every md5 matches the Dataverse record. Checksums also in `/workspace/audit_runs/19_KH0SQ2/prereg/checksums.sha256`.

| file | datafile id | URL | bytes | sha256 |
|---|---|---|---|---|
| `all_merged.RData` | 10380211 | https://dataverse.harvard.edu/api/access/datafile/10380211 | 67514 | 7225bc8cf56c04924ee9ab791129c43e9d6202506550630a247100072235b423 |
| `Appendix_plus.R` | 10380209 | https://dataverse.harvard.edu/api/access/datafile/10380209 | 39230 | 01788e0fa7a8105ebcc0001006266f66111bf63f76b6df9d0b398f708ef77571 |
| `dataset.RData` | 10380207 | https://dataverse.harvard.edu/api/access/datafile/10380207 | 75278 | 1deaa2cef858cecc9123bb3d46f73b3a4815ee10c2572ea23ed4c12cd1d34289 |
| `FRCONJdataset.RData` | 10380208 | https://dataverse.harvard.edu/api/access/datafile/10380208 | 66711 | 052455f1a1e60f6a95986547c27827cccb6fba4f59e2a12de9a0670b8f94bd73 |
| `FRdataset.RData` | 10380210 | https://dataverse.harvard.edu/api/access/datafile/10380210 | 45047 | ea9e8400dfc2f700359d8a8f7257ff8b73f04e604e6c1a14662bbf3ff57b9231 |
| `main_text_figs_JEPP_FINAL.R` | 10380213 | https://dataverse.harvard.edu/api/access/datafile/10380213 | 34487 | 4352209547dbc51634b7cc4ace17c21af8e60abd1c39779a27d1c5bd85331301 |
| `yougov_uk_conjoint.RData` | 10380212 | https://dataverse.harvard.edu/api/access/datafile/10380212 | 116945 | 82e4766bf9dc931e959d43b2d9372da84b2d7111161df85e7c90713464850f59 |

Contents (from loading, see disclosure above): `all_merged.RData` holds data.frame `all` (2772 rows x 27 cols; UK 1734, FR 1038; `Treatment` factor Control|Parity|Quota; `resp_gender` factor Female|Male|Other/Prefer not to answer, the last level empty). `dataset.RData` and `FRdataset.RData` each hold `df` (UK 1734 x 73, FR 1038 x 72). `yougov_uk_conjoint.RData` and `FRCONJdataset.RData` each hold `long` (3468 and 2076 rows). No README or codebook in the deposit; the Dataverse description reads "Please find replication code for all figures in the main text and tables in the Appendix, with corresponding datasets."

## 1. Headline results and targets

Main claim (abstract): in a YouGov survey experiment in the UK and France ("combined N = 2677"), "Parity is more supported than quotas in France, but no such framing effects emerge in the UK. Respondents' gender also matters, with men less supportive of both measures than women." The framing comparison is reported in Online Appendix Table S1 (treated respondents, survey-weighted OLS of Support on Treatment, Parity = reference) and the text ("3.46 for quota compared with 3.64 for parity, difference significant at p < 0.05; see Table S1"; UK "3.02 for quota compared with 2.98 for parity; difference not statistically significant"). The gender claim in its plain additive form is Table S10 (Support ~ Treatment + gender), columns (UK) and (FR).

Targets (copied exactly from the appendix tables; OLS coefficients with weights = `Weight`; standard errors in the tables are the default `summary.lm` SEs that stargazer prints):

| id | quantity | paper value | decimals | location | code object |
|---|---|---|---|---|---|
| T1 | FR, coefficient on Quota (vs Parity), Support ~ Treatment | -0.188 | 3 | Table S1 (appendix p. 12), row Quota, col 4 (FR); SE 0.089, ** | `Appendix_plus.R` l. 948 `res4`, `coef(res4)["TreatmentQuota"]` |
| T2 | UK, coefficient on Quota (vs Parity), Support ~ Treatment | 0.047 | 3 | Table S1 (p. 12), row Quota, col 1 (UK); SE 0.076, no star | l. 906 `res1`, `coef(res1)["TreatmentQuota"]` |
| T3 | UK, coefficient on Male (vs Female), Support ~ Treatment + resp_gender | -0.312 | 3 | Table S10 (p. 20), row Male, col (UK); SE 0.076, *** | l. 915 `resg1`, `coef(resg1)["resp_genderMale"]` |
| T4 | FR, coefficient on Male (vs Female), Support ~ Treatment + resp_gender | -0.280 | 3 | Table S10 (p. 20), row Male, col (FR); SE 0.088, *** | l. 957 `resg2`, `coef(resg2)["resp_genderMale"]` |
| T5 | UK, observations in the treated-sample Support models | 1099 | 0 | Table S1 (p. 12) cols 1-3, and Table S10 (p. 20) col (UK): 1,099 in each | `nobs(res1)` (also `res2`, `res3`, `resg1`) |
| T6 | FR, observations in the treated-sample Support models | 623 | 0 | Table S1 (p. 12) cols 4-6, and Table S10 (p. 20) col (FR): 623 in each | `nobs(res4)` (also `res5`, `res6`, `resg2`) |

Cross-check for T1 and T2 (not separate targets): `main_text_figs_JEPP_FINAL.R` fits the same models as `res1b` (l. 363, FR) and `res1` (l. 325, UK) on `subset(T1, country==...)` where `T1` keeps Quota and Parity rows; `lm` drops the empty Control level, so the Quota coefficient should equal the Appendix one. Agents report both; the Appendix object is the target.

Which statistic, where the paper is ambiguous:
- p-value: the tables give stars only (*p<0.1; **p<0.05; ***p<0.01). Candidates: (1) the t-test p-value from `summary(lm(..., weights = Weight))`, which is what stargazer prints and what the code computes (pre-registered); (2) a design-based p-value from `survey::svyglm`, which the code does not compute for these models. Only (1) is used.
- Gender effect: the abstract's "men less supportive of both measures" could map to (1) the additive Table S10 Male coefficients (pre-registered: T3, T4) or (2) the Table S1 Male coefficients from the interaction models (UK col 2: -0.381, SE 0.108, ***; FR col 5: -0.267, SE 0.124, **; `res2`, `res5`, `coef(.)["resp_genderMale"]`), which are the gender gap under Parity only. Agents report (2) as secondary context, not as targets.

Conclusion criterion for `same_conclusion`:
- T1: estimate < 0 and 0.01 <= p < 0.05 (the ** bucket). If p < 0.01 the direction and significance at 0.05 still hold; record as same_conclusion = true with a note (the paper's claim is "p < 0.05").
- T2: p >= 0.10 (no star; "not statistically significant"). Sign recorded but not part of the criterion.
- T3, T4: estimate < 0 and p < 0.01.
- T5, T6: reproduced N equal to the printed N. Under CHANGELOG #6(a) an N-only mismatch with matching estimates is class C, not D.

Secondary context agents may report (not targets): Table S1 constants 2.977 (UK) and 3.643 (FR); Table S1 FR col 6 Quota:Male:Masculine -0.185 (SE 0.075, **), the basis of the H4 claim; R2 values; the main-text weighted means 2.98/3.02 (UK) and 3.64/3.46 (FR), which the script comments at l. 321, 323, 359, 361 also give.

Inconsistencies noticed while reading (described, not judged):
- Sample size: abstract and design section say combined N = 2677 (UK N = 1,708; France N = 969). `all_merged.RData` has 2772 rows (UK 1734, FR 1038), and `dataset.RData` / `FRdataset.RData` have 1734 and 1038 rows. No line in either script produces 1,708, 969 or 2677. These are descriptive Ns, not model Ns, and are not targets; agents report `table(all$country)`.
- Sensitivity-check text says the social desirability subset has "N = 401 in UK; 180 in France" and the FMC subset "387 in the UK ... and 169 in France". Table S10 prints SDS N 702 (UK) and 351 (FR) and FMC N 387 and 169. In `Appendix_plus.R` the comments `#401` and `#180` (l. 1154, 1157) sit on the FMC subset rows, and the SDS subset comments say 1108 and 591 (l. 1057, 1098).
- In Table S10, the printed SE of Male equals the SE of Quota in both full-sample columns (UK 0.076 and 0.076; FR 0.088 and 0.088). Recorded only; agents compare the reproduced SEs.
- `Appendix_plus.R` l. 2 says "For Figure S12, please see 'main_text_figs_JEPP_R1'"; the deposited file is `main_text_figs_JEPP_FINAL.R`, which contains the Fig S12 code (l. 699-752). Path-only mapping, see section 2. L. 636 says "use appendix.r code to create this sample"; no file of that name is deposited, and the objects it needs (`uksd`, `frsd`) are created later in `Appendix_plus.R` itself (l. 1059 and 1100). Not needed for any target.
- The deposit contains no `stargazer` call that prints Table S1 or Table S10; the models are fitted at l. 906-957 and printed only with `summary()`. Values are read from the model objects.

## 2. Reproduction plan

Environment: fresh R library `R_LIBS_USER=/workspace/audit_runs/19_KH0SQ2/<AGENT>/rlib`, system R 4.5.x. The authors give no R or package versions (no renv.lock, no sessionInfo, no README), so there is no pin to try first; current CRAN versions are used and recorded. CRAN versions seen on 2026-10-10: cjoint 2.1.3, interactions 1.2.0, collapse 2.1.8, rstatix 1.1.0, ggpubr 1.0.0, sjPlot 2.9.0, stargazer 5.2.3, effects 4.2-5, survey 4.5, ggthemes 7.0.0, patchwork 1.3.2, cowplot 1.2.0, psych 2.6.9.

Inputs: put all seven deposit files in `RUNDIR/deposit/` and use it as the working directory (both scripts say "Set working directory here" and use bare file names).

Step A (targets). `Appendix_plus.R` is not a top-to-bottom script: its first three `load()` lines are commented out (l. 6, 18, 183; the only active one is l. 1248, in the list-experiment section), sections expect the user to load other datasets by hand (comments at l. 363, 391, 1111, 1125), and l. 638 uses `uksd`, created further down. The block that fits Tables S1 and S10 is l. 892-958 ("using merged all data / creating main table 1"), which uses only `all`. Run it in a fresh session with a driver `scripts/run_S1_S10.R`:
```
setwd("RUNDIR/deposit"); load("all_merged.RData")
src <- readLines("Appendix_plus.R"); eval(parse(text = src[892:958]))
saveRDS(list(res1=res1,res2=res2,res3=res3,resg1=resg1,res4=res4,res5=res5,res6=res6,resg2=resg2), "../outputs/S1_S10_models.rds")
```
The driver adds the `load("all_merged.RData")` the script itself has commented out at l. 18 and says "using merged all data" at l. 892 (also "use all merged data" at l. 1200); record it as an environment fix (missing load / working directory) in `diffs/` with a README line. No line in 892-958 is changed. Loading a fresh `all` is equivalent to the state the script reaches at l. 892: the only earlier change to `all` is l. 426-430 (`subset(all, country != "US")`, no US rows exist; `droplevels(resp_gender)`, which l. 904 and 946 repeat on the subsets).
Then `scripts/extract_targets.R` writes `outputs/targets_extracted.csv` with, for each of the 8 models: term, estimate, SE, t, p (from `summary()`), nobs. `scripts/build_results.py` builds `results.json` from that CSV.

Step B (completeness and cross-check). Run `main_text_figs_JEPP_FINAL.R` whole with `Rscript`, logging stdout/stderr to `outputs/main_text.log` and writing plots to `outputs/Rplots.pdf`. It reads `all_merged.RData` (l. 41), `yougov_uk_conjoint.RData` (l. 634), `FRCONJdataset.RData` (l. 666); all are deposited. Allowed environment fixes: (a) l. 17-18 call `install.packages()` with no repository, which fails under non-interactive Rscript if a package is missing: pre-install the packages in the per-run library (preferred, no diff) or prepend `options(repos = "https://cloud.r-project.org")` (record as diff); (b) if a plotting-only package cannot be installed on aarch64, comment out only its `library()` line and the plot lines that need it (record as diff; no estimate line touched). Extract `coef(res1)` (l. 325) and `coef(res1b)` (l. 363) for the T2/T1 cross-check.

Mapping of the deposited name: references to `main_text_figs_JEPP_R1` (Appendix_plus.R l. 2) map to `main_text_figs_JEPP_FINAL.R`. No other file-name mismatch: every `load()` call in either script names a deposited file.

Randomness: none in the target models (closed-form weighted OLS). No `set.seed` in either script.

## 3. Robustness checks (pre-registered)

All checks use the exact estimation samples of the target models: `uk2` and `fr2` from the driver, restricted to rows used by the fit (`model.frame`), i.e. treated respondents with non-missing `Support` (UK 1099, FR 623 expected). The primary quantity for every check is T1 (FR Quota coefficient, `res4`); each check also reports T2, T3 and T4 as secondary, with p-values from `summary.lm`. "Same direction and significance as the paper" for the primary = estimate < 0 and two-sided p < 0.05 (or, for R_a, 95% CI entirely below 0). For the secondaries: T2 same = p >= 0.10 (for R_a, 90% percentile CI contains 0); T3, T4 same = estimate < 0 and p < 0.01 (for R_a, 99% percentile CI entirely below 0).

R_a. Nonparametric case bootstrap. `set.seed(20261010)` once, then for each model separately in the order res4, res1, resg1, resg2: draw 2000 resamples of the estimation-sample rows with replacement (`sample(n, n, replace = TRUE)`), each row keeping its own `Weight`, refit the identical `lm(..., weights = Weight)` and store the coefficient. Report the original-sample estimate, the bootstrap SE, and the 90%, 95% and 99% percentile CIs; p-value = min(1, 2 * min(share of draws <= 0, share >= 0)). Resamples where a coefficient is not estimable (NA) are counted and reported, not replaced.

R_b. Outlier exclusion. The default rule, |z| > 3 on the outcome, cannot drop anything here: `Support` is 1-5 and in the estimation samples its z-scores range from about -1.60 to 1.55 (UK) and -2.37 to 1.28 (FR) (pre-run data inspection, see top). The main predictors (Treatment, gender) are binary. The rule is therefore applied to the continuous quantity that enters every estimate, the survey weight: within each country's estimation sample compute z = (Weight - mean(Weight)) / sd(Weight) (unweighted mean and sd, `sd()` with n-1), drop cases with |z| > 3, refit res4, res1, resg1, resg2 with weights on the remaining cases, and report estimate, SE, p and the number dropped (pre-run inspection suggests about 29 UK and 16 FR cases; agents recompute and report their own count). Agents also report, as a confirmation, that |z| > 3 on `Support` drops 0 cases.

R_c. Alternative analysis choice: unweighted OLS. Refit the same four models on the same estimation samples without `weights = Weight` (plain `lm`), report estimate, SE and p. Rationale: the paper uses YouGov weights throughout (footnote 4); an unweighted estimate of a randomised treatment contrast is a standard alternative and shows whether the France framing effect depends on the weights.

## 4. Known risks

- Materials: no data availability statement in the article (see `DATA_STATEMENT.md`); the deposit holds the data and code that every target needs. No missing input file for any `load()` call.
- `Appendix_plus.R` is an interactive script that cannot run top to bottom; the targets come from one self-contained block run through a driver that adds the load line. A reviewer could see the driver as more than an environment fix; it changes no analysis line.
- The printed Table S1/S10 layout is not produced by any deposited code (no stargazer call for them); agents compare numbers from model objects to the printed tables.
- Descriptive Ns in the main text (1,708; 969; 2677) do not match the deposited data (1734; 1038; 2772). Not targets, but a reader may ask about them.
- Dependencies: Step A needs only base R (`stats`). Step B loads 14 packages plus `cowplot`; `ggpubr`/`rstatix` pull in `car` -> `lme4`/`nloptr`, and `cjoint` and `sjPlot` pull many more. On aarch64 Debian `nloptr` may need cmake or the system nlopt library; Debian `r-cran-*` binaries are acceptable and recorded. A failure here affects only figures and the T1/T2 cross-check, not the targets.
- Compute and memory: data under 0.5 MB, about 2,800 rows. Step A runs in seconds; R_a is 8,000 small `lm` fits, under 1 minute. Peak memory for Step B estimated well under 1 GB (plotting packages loaded), far below the 3 GB guard, so no fallback is needed; if Step B were to exceed it, Step A alone gives every target with the authors' estimation lines unchanged.
- No randomness and no version pins, so platform or package versions should not change OLS coefficients; differences beyond the third decimal would point to data or sample differences.
