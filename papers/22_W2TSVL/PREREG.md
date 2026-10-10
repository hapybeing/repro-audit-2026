# PREREG: 22_W2TSVL

Written 2026-10-11 02:15 IST, before any analysis code was run. No analysis code (authors' or own) was executed to write this file; the deposit files were only downloaded and read (code as text, docx text, first lines of the .tab for column names). The main text was read in full from the publisher PDF. The main text reports its results only as coefficient plots (Figures 1 to 4); the printed numbers are in the online Appendix A (Tables A1 to A6), which was read in two identical-looking copies (publisher supplement PDF and the deposit's Appendix_Final.docx). Targets are copied from Appendix Tables A1 and A2.

- Paper: Chambers-Ju, C., and Trasberg, M. (2025). "Framing Labor Action: Experimental Evidence from Teachers in Mexico". Perspectives on Politics 24(3), 1253-1270 (issue dated September 2026; published online 2025-06-10). DOI https://doi.org/10.1017/S1537592725000660 . Open access, CC BY 4.0.
- Text sources read (downloaded 2026-10-10 20:39 UTC, no sign-in):
  - Publisher PDF (18 pages): https://www.cambridge.org/core/services/aop-cambridge-core/content/view/6FA86B96F76F1A17BD7DF6E7B28910FD/S1537592725000660a.pdf/div-class-title-framing-labor-action-experimental-evidence-from-teachers-in-mexico-div.pdf , 473,342 bytes, sha256 f92d18a5a84b22551a1ffd3b6e1b76ae39cb6f4ff9092ba50529f28b4db50d96 (Cambridge stamps a download time into each copy, so a re-download will have a different hash).
  - Publisher supplementary material (Appendix A and B, 8 pages): https://static.cambridge.org/content/id/urn%3Acambridge.org%3Aid%3Aarticle%3AS1537592725000660/resource/name/S1537592725000660sup001.pdf , 240,181 bytes, sha256 b72cfccc1bd5e0ca829a03f1ff0fc6548aa36e8394fe4f3815feb716087d2456. Tables A1 and A2 in it carry the same numbers as the deposit's Appendix_Final.docx (compared by eye, every cell of A1 and A2).
- Dataset: "Replication Data for: Framing Labor Action: Experimental Evidence from Teachers in Mexico", Harvard Dataverse, https://doi.org/10.7910/DVN/W2TSVL , version 1, released 2025-04-23, CC0 1.0, no restricted files. File list API: https://dataverse.harvard.edu/api/datasets/:persistentId/?persistentId=doi:10.7910/DVN/W2TSVL (saved as data_statement_raw/dataverse_W2TSVL.json).

| datafile id | file | URL | bytes | sha256 |
|---|---|---|---|---|
| 10905681 | Appendix_Final.docx | https://dataverse.harvard.edu/api/access/datafile/10905681 | 46586 | cf4f30948d5b34e6734300066edcdee8ef4d9fb5889d94f0288ef1bd7a024f94 |
| 10903647 | Chambers-Ju and Trasberg_Read_me.txt | https://dataverse.harvard.edu/api/access/datafile/10903647 | 793 | 046ba28ff9dcd3f3628e405f116c13dd54e19c5b35d52fa3e1e11461471d1a21 |
| 10903649 | Framing Labor Action_Appendix A1.R | https://dataverse.harvard.edu/api/access/datafile/10903649 | 9739 | 72d139742fddc0c5449ff441f825454c77f535c696519091268a1290013af223 |
| 10903646 | Framing Labor Action_R script.R | https://dataverse.harvard.edu/api/access/datafile/10903646 | 11232 | b55b035ab4d28635c55d8e76207fa8dc7cad30ea57d3c1802f76738831ea0785 |
| 10903648 | OA23 Base UT-TEC.dta (original upload, Stata 118) | https://dataverse.harvard.edu/api/access/datafile/10903648?format=original | 1080751 | 2678501b572867bc34378ce1b8fc9c2500d72f8080bc3125c31c4c75243c8ef1 |
| 10903648 | OA23 Base UT-TEC.tab (Dataverse ingest of the same file) | https://dataverse.harvard.edu/api/access/datafile/10903648 | 384025 | 40aac3ed93a197d4b6316eae62c0481cf1b66d6879e6aae1d6a190840bd56e63 |

Notes: Dataverse lists the data file as `OA23 Base UT-TEC.tab` (384,025 bytes); its stored md5 (dc0d4d5db841d52846eb76a724db3b99) matches the `.dta` original, which is the file the code reads. Use the `.dta` (`?format=original`). The access API answers with an HTTP 303 redirect to S3, so use `curl -L`. The data has 1011 rows and 69 columns; every variable the code uses is present (Entidad, d1, d2, d3, d12, TratUT2, UT2_1, UT2_2, PartyID, EdadRec, Ponderador). All sha256 values are also in `prereg_download_checksums.sha256` (this folder).

## 1. Headline results and targets

Abstract claim: in a vignette experiment in a nationally representative in-person survey in Mexico, "mentioning the political interest of union leaders decreases support for unions, while informing voters about teacher grievances increases support for ongoing strikes." Results section (pp. 1261-1264): ordered logistic regressions of each outcome on treatment dummies, main models without weights or controls, run once with control and once with pro-strike as reference. Text p. 1262: the anti-strike treatment "has a negative effect on union support (H2)"; the pro-strike effect on union support "is insignificant (p = 0.28)"; support for striking teachers differs between control and pro-strike "at the 0.01 level". Figures 1 to 4 plot these coefficients; Appendix Tables A1 (union influence) and A2 (support for strike) print them.

| id | quantity | code object | paper value | decimals | location |
|---|---|---|---|---|---|
| T1 | Anti-strike coefficient, DV union influence, control as reference | `coef(m1)["anti_strike"]` | -0.386 | 3 | Table A1 col (1), row Anti-strike (SE 0.180, **); Figure 1 |
| T2 | Pro-strike coefficient, DV support for striking teachers, control as reference | `coef(m7)["pro_strike"]` | 0.473 | 3 | Table A2 col (1), row Pro-strike (SE 0.182, ***); Figure 3; text p. 1262 |
| T3 | Pro-strike coefficient, DV union influence, control as reference | `coef(m1)["pro_strike"]` | 0.194 | 3 | Table A1 col (1), row Pro-strike (SE 0.181, no star); text p. 1262 "p = 0.28" |
| T4 | Anti-strike coefficient, DV union influence, pro-strike as reference | `coef(m4)["anti_strike"]` | -0.579 | 3 | Table A1 col (4), row Anti-strike (SE 0.179, ***); Figure 2 |
| T5 | Observations, union influence simple model | `nobs(m1)` (also `m1$n`) | 976 | 0 | Table A1 cols (1) and (4); Figure 1 and 2 notes "N = 976" |
| T6 | Observations, support-for-strike simple model | `nobs(m7)` (also `m7$n`) | 961 | 0 | Table A2 cols (1) and (4); Figure 3 and 4 notes "N = 961" |

`m1`, `m4`, `m7` are the objects in `Framing Labor Action_Appendix A1.R` (lines 143, 155, 171): `MASS::polr(..., Hess = TRUE)`, unweighted, no controls. The main script's Figure 1 to 4 models (`polr(as.factor(unions) ~ Treatment)` etc., lines 77-79, 124-126, 194-196, 234-236) are the same models with a factor coding and should give identical coefficients; they are a cross-check, not the target source.

Statistic used for significance (pre-registered): the Wald z from `summary(m)` (coefficient / Hessian-based SE), two-sided normal p-value `2 * pnorm(-abs(t value))`. This is the convention stargazer uses for its stars and is the only reading that reproduces the printed "p = 0.28" from 0.194 / 0.181. The table notes state "*** p<0.01, ** p<0.05, * p<0.1". Candidate alternative (listed second, not pre-registered): a likelihood-ratio or profile-likelihood p-value (e.g. from `broom::tidy(conf.int = TRUE)` profile CIs, which the main script uses for the figure bars).

Printed Ns: each model prints one N in Table A1/A2 and the figures repeat it. The same DV also has other Ns in other columns (Table A1: weighted 975, controls 754; Table A2: weighted 962, controls 747; Table A3 without Tamaulipas: 947 and 931). Only the simple-model Ns are targets.

Conclusion criterion for `same_conclusion`:
- T1 to T4: same sign as the paper and the pre-registered two-sided Wald p falls in the same star bucket as printed: T1 0.01 <= p < 0.05 (**); T2 p < 0.01 (***); T3 p >= 0.10 (no star; paper text p = 0.28); T4 p < 0.01 (***).
- T5, T6: same conclusion if the reproduced N is within 5 of the printed N (as for earlier papers). An N-only mismatch with matching estimates is read under CHANGELOG_METHOD #6(a).

Secondary context only (not targets): SEs above; Table A1 col (1) Strike -0.242 (0.179), Double frame -0.121 (0.183); Table A2 col (1) Strike -0.113, Anti-strike 0.030, Double frame 0.057; Table A2 col (4) Anti-strike -0.444 (0.183) **; weighted and control columns; Table A3 (2 decimals); Table A4 means.

Inconsistencies noticed while reading (described, not judged):
- Sample size: text p. 1261 says "The sample size consists of 1,010 respondents"; Table A5 gives sample N 1011, the Table A6 group Ns sum to 1011 (210+200+206+201+194), and the data file has 1011 rows.
- Weighted-model Ns differ from unweighted ones on the same rows: Table A1 col (2) 975 vs col (1) 976; Table A2 col (2) 962 vs col (1) 961 (a weighted N larger than the unweighted one). `MASS::polr` stores `nobs` as the sum of weights, which may explain this; to be observed, not assumed.
- Figure 3 note says the bars "represent 90% and 95% confidence intervals"; the main script draws one bar per term from `tidy(conf.int = TRUE, conf.level = 0.95)` (lines 194-224).
- Main script descriptive CIs use `qt(0.95, ...)` for union support (lines 63-64, a 90% two-sided interval) and `qt(0.975, ...)` for teacher support (lines 176-177), with `length()` including missing values; these feed no printed table.
- Table A4 means are typed into the code as constants (Appendix A1.R lines 234 and 264), not computed from the data in that step; the computed means are printed just before (lines 224-228, 253-257).
- Table A5 census column comes from an external INEGI / Data OPM document (code comment lines 301-302), not from the deposit.
- Table A6 has an "Income (mean (SD))" row with p and SMD, but `CreateTableOne` at Appendix A1.R lines 312-317 lists only woman, age_levels, education_levels; Table A6 prints "4.40 (1.37%)" for the Strike income SD.
- Text p. 1261: union influence mean 3.17 (SD 1.4) and teacher support mean 4.46 (SD 2.4); not produced by an explicit line in either script.
- README calls the appendix file "Appendix A1 and A2"; the deposit file is `Appendix_Final.docx`. README lists the data as `OA23 Base UT-TEC.dta`; Dataverse displays it as `.tab`.

## 2. Reproduction plan

Run directory RUNDIR = /workspace/audit_runs/22_W2TSVL/<AGENT>/run. Place `OA23 Base UT-TEC.dta` (the `?format=original` download) in RUNDIR and set the working directory to RUNDIR.

Script order:
1. `Framing Labor Action_Appendix A1.R` (primary; produces m1 to m12, Tables A1 to A3 via stargazer html, A5/A6 via tableone). All targets come from here.
2. `Framing Labor Action_R script.R` (secondary; Figures 1 to 4). Used only as the cross-check that its polr coefficients equal m1, m4, m7. Its failure would not block the targets.

Allowed environment fixes (each as a unified diff under `diffs/`):
- Path only: line 14 of both scripts reads `read_dta("C:/Users/L03538527/OneDrive - .../Analysis/OA23 Base UT-TEC.dta")`. Replace with `read_dta("OA23 Base UT-TEC.dta")`, which is the authors' own commented alternative (main script line 15). Mapping: code name `OA23 Base UT-TEC.dta` = Dataverse datafile 10903648 original. Alternative file: the ingested `OA23 Base UT-TEC.tab`; use it only if the `.dta` cannot be read, and log it (value labels are lost in the .tab; the code uses numeric codes only, so estimates should not depend on labels, but this is unverified).
- Comment out the `install.packages(...)` lines (main 4-8; appendix 4-6, 138, 282) and install the packages beforehand into the per-run library.
- `browseURL()` (appendix lines 166, 190, 216) may fail non-interactively: define `browseURL <- function(...) invisible(NULL)` in a wrapper before sourcing.
- Run with a wrapper: `Rscript -e 'source("Framing Labor Action_Appendix A1.R", echo=TRUE, max.deparse.length=Inf); saveRDS(list(m1=m1,m4=m4,m7=m7,m10=m10), "outputs/models_appendix.rds")'`, logging stdout/stderr to `outputs/`. Copy the stargazer htm files (`table_1A_new.htm`, `table_A2_new.htm`, `table_A3_new.htm`) to `outputs/`.
- Then `scripts/extract_targets.R` reads `outputs/models_appendix.rds` and writes `outputs/targets_extracted.csv` with, for T1 to T4: coef, SE, z, two-sided Wald p; for T5, T6: `nobs()` and `$n`. `scripts/build_results.py` builds results.json from that CSV.

Packages needed (no versions pinned; README gives only "R version 4.4.2 and R Studio Version 2024.09.1"): haven, foreign, plyr, dplyr, MASS, broom, ggplot2, stargazer, tableone. All are current CRAN packages; no pin to try. MASS ships with R. Note: the main script loads plyr after dplyr, and both scripts use `dplyr::summarize` explicitly where it matters; masking does not touch the polr calls.

Peak memory: well under 500 MB (1011 rows, 69 columns, polr fits). Wall time: seconds for the scripts; R_a about 2000 polr refits, expected under 2 minutes. No reduced-K rule is needed; if one bootstrap of 1000 refits takes over 5 minutes, pre-registered fallback is K = 500 with the same seed, logged. Save bootstrap draws to `outputs/` every 100 resamples so a sandbox restart costs at most one chunk.

Expected sources of small differences (record, do not fix): R 4.5.x (Debian, aarch64) vs 4.4.2 (Windows, from the file path); MASS polr optimiser (optim BFGS) could differ in the last digit across versions. No random numbers are used by the authors' estimation code.

## 3. Robustness checks (pre-registered)

Primary quantity for every check: T1, the anti-strike coefficient for union influence with control as reference (model m1 specification). Secondary, reported in the same output file and in the results.json note with its own direction/significance verdict: T2, the pro-strike coefficient for support for striking teachers (m7 specification). The `same_direction_and_significance_as_paper` field refers to T1 only.

"Same direction and significance" (all checks): same sign as the paper, and significance at the paper's printed threshold: for T1 p < 0.05 (printed **), for T2 p < 0.01 (printed ***).

R_a. Nonparametric case bootstrap. Take the rows m1 was fit on (rows with non-missing `unions` and `Treatment`; check the count equals `nobs(m1)`). Call `set.seed(20261011)` once, draw 1000 resamples of rows with replacement (`sample(n, n, replace = TRUE)`), refit the identical `polr(unions ~ strike + pro_strike + anti_strike + double, Hess = TRUE)` on each, record the anti_strike coefficient. Do the same for m7 on its own rows (continuing the same RNG stream after the m1 loop). Report: original-sample estimate, bootstrap SE, percentile 95% CI and percentile 99% CI, and the two-sided bootstrap p = min(2 * min(share <= 0, share >= 0), 1). Failed or non-converged fits (error, or `convergence != 0`) are counted and reported, not replaced. Same direction and significance: T1 percentile 95% CI excludes 0 with the same sign; T2 percentile 99% CI excludes 0 with the same sign.

R_b. Outlier exclusion. The outcomes are ordinal (1 to 5 and 1 to 7) and the predictors are treatment dummies, so a |z| > 3 rule on the outcome or the predictor cannot drop anything (union influence: printed mean 3.17, SD 1.4, so the maximum |z| is about 1.6). The rule is therefore applied to the only continuous respondent variable in the data the code uses, age (`d2`, used as `age` in m3): compute z = (d2 - mean(d2)) / sd(d2) over all 1011 rows (na.rm = TRUE), drop rows with |z| > 3 (rows with missing age are kept, since the simple model does not use age), refit m1 and m7 exactly as specified on the remaining rows, and report the estimate, Wald SE and p as in section 1, plus the number of rows dropped. If no row has |z| > 3, the check is reported as run with 0 exclusions and identical estimates; it is not replaced by another rule.

R_c. Alternative analysis choice: linear model instead of ordered logit. Fit `lm(as.numeric(unions) ~ strike + pro_strike + anti_strike + double)` on m1's rows and `lm(Support_teachers ~ strike + pro_strike + anti_strike + double)` on m7's rows (the authors print linear models of the same form in the main script, lines 117, 185, 231), with HC2 heteroskedasticity-robust SEs (`sandwich::vcovHC(type = "HC2")`, `lmtest::coeftest`). Report the anti_strike (T1) and pro_strike (T2) coefficients in outcome units, HC2 SE and two-sided p. Only sign and significance are compared, not magnitude.

## 4. Known risks

- Paper numbers: the main text has no printed coefficients; targets come from the online appendix, which is part of the publisher's supplementary material and also in the deposit. If an agent reads the plotted figures only, it cannot check the targets.
- Absolute Windows path in both scripts (path-only fix above).
- `install.packages()` and `browseURL()` calls in a non-interactive run (environment fixes above).
- Main script: `aes(estimate, term, color)` (lines 212, 252) passes an undefined `color` as a third positional aesthetic and `geom_errorbarh` is deprecated in recent ggplot2; this may warn or fail when a plot is drawn. It affects figures only, not the targets.
- No Stata or proprietary dependency: the .dta is read with haven.
- Tables A4 (typed constants), A5 (census column external) and the Table A6 income row are not produced by the code from the deposit; none is a target.
- Weighted-model N (975, 962) may not match `nobs()` exactly; not a target.
- No randomness in the authors' code, so a match should be exact if package numerics agree.
