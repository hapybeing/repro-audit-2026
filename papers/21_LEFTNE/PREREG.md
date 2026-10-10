# PREREG: 21_LEFTNE

Written 2026-10-11 (IST, about 02:15), before any analysis code was run. No R or Python analysis code was executed to write this file (the authors' scripts were only read; the five .RDS files were only listed and scanned for strings such as column names and factor levels, never loaded into R).

The main text was read in full (publisher PDF, open access). The supplementary information (SI) is a Word 97 .doc; it was read as extracted text (`strings` on the binary file), which gives table cells in reading order. Table values copied from the SI below were checked cell by cell against the row and column labels in that order; agents should re-check them against the SI file itself.

- Paper: DeMora, S. L., Merolla, J. L., Osorio, M. A., Lindke, C. and Long, S. (2025). "Gendered Political Contexts, Emotions, and Engagement: A Case Study of the 2016 US Presidential Election". British Journal of Political Science 55, e175, 1 to 22. DOI https://doi.org/10.1017/S0007123425101166 . Licence CC BY 4.0.
- Text sources read (downloaded 2026-10-10 about 20:39 UTC, no sign-in):
  - Publisher PDF: https://www.cambridge.org/core/services/aop-cambridge-core/content/view/3665F10236319D5BAB8ED639242B29A2/S0007123425101166a.pdf/gendered-political-contexts-emotions-and-engagement-a-case-study-of-the-2016-us-presidential-election.pdf (489,045 bytes, 23 pages, sha256 9e11f10eb7e3a761aa2cae5d9354ab4b5e6a480bb682e5a3ee28226a0ae48d60)
  - Cambridge Core HTML page (via https://doi.org/10.1017/s0007123425101166); the main-text Tables 1 to 3 are images there: tab1.png sha256 c3febe1f8fc3ec170fbad214ca5da5bbe54ddceebb1f8401a5e6aff947ec3bb6, tab2.png 60f57f82e93ed402ad3b709e56331a723f05d2c06522801511925aaa8cf4d0d9, tab3.png bf54677d22e53e0e91f9561c9bd8a9eb1d6377018ff02e52341dc43242debf0d (values identical to the PDF text layer).
  - SI: https://static.cambridge.org/content/id/urn%3Acambridge.org%3Aid%3Aarticle%3AS0007123425101166/resource/name/S0007123425101166sup001.doc (2,709,504 bytes, sha256 64165d965e1bb1072bd5caf7a43ceb501ac0008402400dc9c7d68c2988c42c3e). The .doc has no printed page numbers in the extracted text, so SI locations are given by table number and column.
- Dataset: "Replication Data for: Gendered Political Contexts, Emotions, and Engagement: A Case Study of the 2016 U.S. Presidential Election", Harvard Dataverse, https://doi.org/10.7910/DVN/LEFTNE , version 1.0 (only version), released 2025-10-30 (UTC), licence CC0 1.0. File list API: https://dataverse.harvard.edu/api/datasets/:persistentId/?persistentId=doi:10.7910/DVN/LEFTNE (saved: `data_statement_raw/dataverse_LEFTNE.json`, `data_statement_raw/versions.json`).

## Dataset files

| datafile id | file | URL | bytes | sha256 |
|---|---|---|---|---|
| 13101004 | `01- Replication_Text.R` (434 lines) | https://dataverse.harvard.edu/api/access/datafile/13101004 | 19511 | 80261e7a37aedae55e0cdfd9066240c38e5a45fe1b8b0fcbe933754d7f93bcb7 |
| 13101005 | `02- Replication_Appendix.R` (457 lines) | https://dataverse.harvard.edu/api/access/datafile/13101005 | 24868 | 6cab25664aff17d0576e6b72046bfc68f67566b68ec6b35573157d3601694e85 |
| 13101006 | `Data.zip` | https://dataverse.harvard.edu/api/access/datafile/13101006 | 140055 | 26c2837511e0480133066d5c5cf7bb03596a5ceea4509ebec6be553aca5a6c97 |

Contents of `Data.zip` (plus `__MACOSX/._*` resource-fork files, to be ignored):

| file | bytes | sha256 |
|---|---|---|
| ANES16.RDS | 61350 | 49eebe2047cf03d872bf45136986a95e1932af4646bc4d83c727edf5070a241a |
| ANES18.RDS | 25812 | b81baefb2d9e2bbf9701c087bd060be2cca6d813374c54a47dc920597c88727e |
| CES2020.RDS | 10108 | 2decdf34860cf312c9c3bbe911a6d3db02ac242b7f1b6691af621e4c1b0401c2 |
| NORC.RDS | 11617 | 88fac1986bb82a1ec56f0bff16e09549cb49f261a8a8bbbdfdbb7e8ab89a7306 |
| Qualtrics_2019.RDS | 30283 | 628f646531e7386604a391c0e966cc691c749d37007739889fa57e8c172b8d41 |

Total deposit 184,434 bytes (matches META.md). No README, no codebook, no sessionInfo, no renv.lock. Scratch copies and `checksums.sha256`: /workspace/audit_runs/21_LEFTNE/prereg/.

## 1. Headline results and targets

Main claim (abstract): in two vignette experiments (Study 1: Qualtrics panel, Feb 2019; Study 2: NORC panel of highly educated white women, 2019), reading about Trump's treatment of women raised anger, "especially among Democratic women and men", and "these elevated emotions increased intended future engagement"; a third study (2020 CES module) that induced anger about Trump's treatment of women "led to greater intended engagement". The text supports the anger effect with SI Table A5 (text p. 10: Figure 1 means 0.28 vs 0.13), the engagement claim with main-text Table 1 (SEM indirect effects through anger, p. 13), and the third study with Table 3 (p. 16). The enthusiasm claim for highly educated women is a marginal one-tailed result in Study 1 (b = 0.099, p = 0.082 one-tailed, p. 14) and is not a target.

Targets (copied exactly from the paper):

| id | quantity | paper value | decimals | location | code object (pre-registered first) |
|---|---|---|---|---|---|
| T1 | Study 1 indirect effect of the Trump condition on the engagement scale through anger | 0.02 | 2 | Main text Table 1 (p. 13), row "Trump", Study 1 "Indirect effect" (printed p-value 0.00) | `01- Replication_Text.R` lines 343 to 363: `lavaan::parameterEstimates()` of `lavaan:::sem(mix_mod, data=df, std.lv=TRUE)` on Qualtrics_2019.RDS, row `label == "indirTRUMPanger"`, column `est` (p from column `pvalue`). Candidate 2: SI Table A8 "Study 1 Trump" ACME 0.017 (p 0.004), `mediation::mediate(..., treat.value="Trump")`, `02- Replication_Appendix.R` lines 147 to 157 |
| T2 | Study 2 indirect effect of the Trump condition on the engagement scale through anger | 0.08 | 2 | Main text Table 1 (p. 13), row "Trump", Study 2 "Indirect effect" (printed p-value 0.00) | `01- Replication_Text.R` lines 366 to 387: same lavaan model on NORC.RDS, label `indirTRUMPanger`, `est`. Candidate 2: SI Table A8 "Study 2 Trump" ACME 0.080 (p 0.000), Appendix lines 160 to 168 |
| T3 | Study 1 OLS coefficient of the Trump condition on anger (no covariates) | 0.15 | 2 | SI Table A5, column "None", row "Trump" (SE 0.02, ***) | `02- Replication_Appendix.R` line 107: `coef(lm(anger ~ TREATMENT, data = df))["TREATMENTTrump"]` on the 3-arm Qualtrics data (lines 27 to 30). Same model also at `01- Replication_Text.R` line 61 (summary only) and line 83 |
| T4 | Study 1 OLS coefficient of Trump x Party (Democrat incl. leaners) on anger | 0.22 | 2 | SI Table A5, column "Party", row "Trump:Party" (SE 0.05, ***) | `02- Replication_Appendix.R` line 109: `coef(lm(anger ~ TREATMENT * party_leanersinc, data = df))["TREATMENTTrump:party_leanersinc"]` |
| T5 | Study 3 (CES 2020) OLS coefficient of the "Treatment of women" anger induction on engagement among compliers | 0.06 | 2 | Main text Table 3 (p. 16), row "Treatment of women", "Model 1" (SE 0.02, **) | `01- Replication_Text.R` lines 392 to 398: `coef(mod2)["TREATMENTTreatment of Women"]`, `mod2 <- lm(futureengage_novote ~ TREATMENT, data = df_compliers)` |
| T6 | N of the Table 3 model | 697 | 0 | Main text Table 3 (p. 16), row "N" | `nobs(mod2)` |

Statistics are unstandardized in all cases. For T1 and T2, `std.lv=TRUE` has no effect on the estimates because the model has no latent variables; the pre-registered statistic is `est`, not `std.all`. lavaan uses its default ML estimator, listwise deletion and normal-theory standard errors in this call (no bootstrap), so T1 and T2 are deterministic.

Conclusion criterion for `same_conclusion`:
- T1, T2: estimate > 0 and lavaan `pvalue` < 0.05 (the paper prints p = 0.00 for both and calls them significant). Also record whether p rounds to 0.00 at 2 decimals.
- T3, T4: coefficient > 0 and p < 0.001 (Table A5 marks both ***), using the default lm standard errors as printed by `export_summs`.
- T5: coefficient > 0 and p < 0.01 (Table 3 marks it **).
- T6: same conclusion if N is within 5 of 697 (an N-only mismatch with matching estimates is classed under CHANGELOG #6(a)).

Secondary context (not targets; agents may report): Table A5 column "None" N = 584 and R2 0.07; Table A5 column "Party" N = 489; Table 1 Clinton rows (Study 1 0.00, p 0.48; Study 2 -0.00, p 0.98); Table 2 (enthusiasm) Trump -0.03 (p 0.00) and -0.02 (p 0.02), Clinton 0.01 (p 0.31) and 0.11 (p 0.00); Table 3 Treatment of minorities 0.07** (0.02), Trump 0.05** (0.02), intercept 0.40*** (0.01), R2 0.02; SI Table A8 ACMEs 0.002 (p 0.475), 0.017 (0.004), -0.000 (0.982), 0.080 (0.000).

Inconsistencies noticed while reading (described, not judged):
1. Which code produces Table 1 is ambiguous. The text (p. 13) and the code section header "Tables 1 & 2" (Text script line 339) point to the lavaan SEM. The Clinton p-values printed in Table 1 (0.48, 0.98) equal, at 2 decimals, the ACME p-values in SI Table A8 (0.475, 0.982), which come from the bootstrapped `mediation::mediate` calls, not from lavaan. Both candidates are listed for T1 and T2; the lavaan object is pre-registered.
2. Table 1 and Table 2 titles say "through anger" and "through enthusiasm", but the code fits one SEM with all three mediators (anxiety, anger, hope) at once and reads both tables' indirect effects from it.
3. The Study 1 SEM (Text script line 343) re-reads `Qualtrics_2019.RDS` without the filter to the Alexa, Trump and Clinton conditions applied at lines 42 to 44, so it includes the MeToo and Marches arms (as dummies in the model). Footnote 8 says those two treatments are analysed in another paper. The figures and Table A5 use the 3-arm data. The NORC SEM likewise uses all arms present in NORC.RDS (levels include March and MeToo).
4. Study 1 sample size: text p. 8 says n = 586 (footnote 10, p. 9: 94.52% of 620); SI Table A5 prints N = 584 for the no-covariate anger model. The deposited data hold no manipulation-check or complier variable for Study 1, so whether the RDS is already restricted to the 586 cannot be told without loading it.
5. The combined multiple-mediator indirect effects in the text (p. 14: 0.010, p = 0.370; 0.080; 0.015, p = 0.082; 0.096) and the Democratic-women subgroup values (p. 15: 0.066, 0.170) and footnote 18 values: the lavaan model defines only single-path indirect effects (no sum of paths, no subgroup fits), and no other deposited code computes them.
6. Cohen's d values in the Conclusion (p. 17: 0.58, 1.37, 0.94, 2.21, 1.4, 1.91): `effectsize` is loaded (Text script line 11) but no call computing d was found in either script.
7. SI Table C1 and Figures C1 to C3 (ANES time series 2000 to 2020, DIME candidate counts): no code in the deposit produces them. ANES16.RDS and ANES18.RDS are read (Text script lines 53 to 54) but never used afterwards. Footnote 20's 2024 college-student experiment has no data or code in the deposit.
8. The main text cites "S.I. Figures A1 and A2" (footnote 15) and "Figure A3" (p. 15); the SI labels these figures B1, B2 and B3.
9. SI Table A10 is titled "enthusiasm" but its inner header reads "Fear mediation by treatment on political engagement". The Appendix script header is dated August 19, 2022 and the Text script October 27, 2025.

## 2. Reproduction plan

Run directory: `/workspace/audit_runs/21_LEFTNE/<AGENT>/`. Unzip `Data.zip` into `RUNDIR/data/` (140 KB, no memory concern) and copy both R scripts there. Working directory = `RUNDIR/data/` for both scripts; the scripts read the five .RDS files by bare file name, and the deposited names match the read calls exactly, so no path fix is needed (`here` is loaded but unused).

Script order (each in a fresh R session, logging stdout and stderr to `outputs/`):
1. `01- Replication_Text.R` via `Rscript -e 'source("01- Replication_Text.R", echo=TRUE, max.deparse.length=Inf)'` > `outputs/text_log.txt`. Gives T1 and T2 (printed `summary()` of the two lavaan fits, "Defined Parameters" block) and T5, T6 (`export_summs(mod2)`).
2. `02- Replication_Appendix.R` the same way > `outputs/appendix_log.txt`. Gives T3, T4 (`export_summs(anger1, ..., anger7)` at line 114) and the Table A8 candidates for T1 and T2 (`set.seed(20241130)` at line 147, then `mediate(..., boot=TRUE, sims=1000)`).

Target extraction: the authors' scripts print but do not keep the fitted objects (`anger1` is overwritten at Appendix line 120; the lavaan fits are never assigned). `scripts/extract_targets.R` therefore re-executes, in a fresh session, only the authors' own data-loading lines and model lines for each target, copied verbatim (Text script lines 343 to 363, 366 to 387, 392 to 398; Appendix lines 27 to 30 and 107 to 109), and writes `outputs/targets_extracted.csv` with estimate, SE, statistic, p and nobs for each target (lavaan via `parameterEstimates()`, lm via `summary()$coefficients` and `nobs()`). `scripts/build_results.py` cross-checks each value against the printed log at the printed precision and builds `results.json`. Any mismatch between the re-executed value and the log is reported, not resolved.

Allowed environment fixes (each saved as a diff with a reason):
- Packages: none pinned anywhere in the deposit, so current CRAN versions are tried first. Needed beyond `scripts/setup_env.sh`: here, survey, margins (+ prediction), interplot, aod, Rmisc, dotwhisker, janitor, qualtRics, jtools, mediation, gtools, gridExtra, huxtable, DT, ggsci, hrbrthemes, effectsize, emmeans, ggpubr, lavaan, ggeffects. All were on CRAN on 2026-10-10 (`data_statement_raw/cran_check.txt`). `lavaan` is called as `lavaan:::sem` but is not in the `Packages` vector; installing it is an environment fix, not a code change.
- lavaan fallback: the treatment dummies passed to lavaan are built with `car::recode` on the TREATMENT factor (Text script lines 344 to 347, 367 to 370) and are therefore 2-level factors. If current lavaan (0.7-3) refuses them or treats them differently, the fallback is lavaan 0.6-20 (the CRAN release current on 2025-10-27, the Text script's date; CRAN archive dated 2025-09-21), then 0.6-19. The model lines are not changed in any case. If all versions refuse the factor input, record it and stop; do not convert the variables.
- Plot-only failures: `hrbrthemes::theme_ipsum_rc` (lines 18 to 39) needs Roboto Condensed fonts (expected to give warnings only). If a figure, theme or table-printing line stops the script, the allowed fix is to make that line non-fatal (`try()`), or, if `hrbrthemes` cannot be installed, to replace `hrbrthemes::theme_ipsum_rc(...)` with `ggplot2::theme_minimal()` in the theme definitions only. No estimation line may change.
- `mediate()` for Study 2 (Appendix lines 160 to 168 onward) is run on `df_TESS` without the NA filtering applied to Study 1; if `mediate` stops because the mediator and outcome models have different numbers of observations, record the error verbatim. It does not affect T1 to T6 (the lavaan objects are pre-registered), only the candidate-2 values; do not filter the data.

Expected sources of small differences: none for T1 to T6 (closed-form OLS and ML SEM on fixed data). The Table A8 bootstrap values depend on the `mediation` version and RNG; the script comment (Appendix line 142) says they "may differ slightly each time".

Compute and memory: data are about 0.5 MB uncompressed in total and each study has a few hundred rows. Peak memory well under 1 GB; no fallback needed under the 3 GB rule. Wall time: the Appendix script's 12 `mediate` calls with 1000 bootstrap draws each are the slowest part, expected a few minutes in total on 2 CPUs; everything else runs in seconds. Package installation (about 20 packages from source on aarch64) is the longest step; install into `RUNDIR/rlib` and keep it, so a sandbox restart only needs `setup_env.sh` and a re-run of the scripts.

## 3. Robustness checks (pre-registered)

Inference conventions: lavaan default standard errors for SEM quantities; default lm (OLS) standard errors for T3. All checks use the authors' data-loading lines unchanged and are run from `scripts/` copies, never by editing the authors' files.

R_a. Case bootstrap of T1 (primary). Data: the rows lavaan actually used in the Study 1 SEM (rows of `df` from Text script lines 343 to 350 that are complete on Engage, anxiety, anger, hope, TRUMP, CLINTON, MARCH, METOO; check that their count equals `lavInspect(fit, "nobs")`). Call `set.seed(20261011)` once, draw K = 1000 resamples of these rows with replacement (`sample(n, n, replace = TRUE)`), refit the identical `mix_mod` with the identical `sem()` call on each, and record `est` for `indirTRUMPanger`. Report the original-sample estimate as `estimate`, the 2.5th and 97.5th percentiles as `se_or_ci`, the SD of the bootstrap estimates, and as `p_value` the two-sided bootstrap proportion min(2 x share of draws <= 0, 1). Non-converged or erroring fits are counted and reported, not replaced. Same direction and significance = estimate > 0 and the percentile 95% CI excludes 0. Secondary: the same quantity for Study 2 (T2) with the same seed reset before its loop. Expected wall time about 1 to 2 minutes per study; if one study's loop exceeds 5 minutes, reduce to K = 500 with the same seed and say so. Save draws every 100 resamples to `outputs/Ra_draws_<study>.csv` so a restart resumes rather than repeats.

R_b. Outlier exclusion on the outcome, applied to T3 (primary) and T1 (secondary). T3: on the 3-arm Study 1 data (Appendix lines 27 to 30), take the rows used by `lm(anger ~ TREATMENT, data = df)`; compute z = (anger - mean) / sd over those rows; drop rows with |z| > 3; refit the identical formula; report the Trump coefficient, SE, p and the number of rows dropped. T1 secondary: in the lavaan estimation sample, compute z on the final outcome `Engage` the same way, drop |z| > 3, refit the identical SEM, report `indirTRUMPanger` est, SE, p and rows dropped. Both outcomes are 0 to 1 scales and z is meaningful on them. If no row exceeds |z| > 3, the check is reported as run with 0 rows dropped (estimate identical to the original), not replaced by another rule. Same direction and significance: T3 coefficient > 0 and p < 0.001; T1 est > 0 and p < 0.05.

R_c. Alternative reasonable analysis choice: estimate the Study 1 SEM on the three conditions the article analyses (T1, primary). Take `df` as built at Text script lines 343 to 350, keep only rows with TREATMENT in Alexa, Trump, Clinton, and fit `mix_mod` with the MARCH and METOO terms (and their labelled paths c3, c4, a98, a97, a298, a297, a398, a397) removed, because they are constant 0 in this subset; everything else (labels for the remaining paths, defined indirect effects, `std.lv=TRUE`, default estimator) is unchanged. Report `indirTRUMPanger` est, SE, p and nobs. Secondary: the same for Study 2 (NORC, keeping Alexa, Trump, Clinton). Same direction and significance = est > 0 and p < 0.05.

## 4. Known risks

- Table 1 ambiguity (inconsistency 1): if the lavaan values do not match Table 1 but the `mediate` ACMEs do (or the reverse), this is reported per candidate; the class uses the pre-registered lavaan object first and reports the other as an alternative. This could produce C ("code cannot produce the reported table") if neither matches.
- Results in the text with no code in the deposit (inconsistencies 5 to 7) are not targets and do not affect the class, but are listed as code observations.
- Package installs: about 20 CRAN packages from source on aarch64 Debian R 4.5; `margins`, `interplot` and `qualtRics` are old-style but currently on CRAN. A hard stop at `lapply(Packages, library, ...)` (Text script line 14, Appendix line 12) would stop the whole script, so every listed package must install or be handled by the plot-only fix above. Only figure and table-printing packages may be stubbed; `lavaan`, `car`, `mediation`, `jtools`/`huxtable` (for the printed tables used in the log cross-check) are required. If lavaan cannot be made to run, T1 and T2 cannot be produced and the paper would be E for those targets.
- lavaan factor input (see section 2): the most likely technical blocker.
- No proprietary dependencies (no Stata, no SPSS run needed; CES2020.RDS carries a `format.spss` attribute but is read with base `readRDS`).
- Compute and memory: negligible.
