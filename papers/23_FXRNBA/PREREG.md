# PREREG: 23_FXRNBA

Written 2026-10-11 02:15 IST, before any analysis code was run. No analysis code (the authors' or our own) was executed to write this file; only downloads, checksums, `head`/`tail` of CSV headers and reading of the R scripts and the paper.

The main text of the paper was read in full (publisher PDF, below). The Supplementary Information (SI, tables B1 to B14) could not be read: every IOPscience route returned a bot-check captcha (attempts in `data_statement_raw/si_access_attempts.json`). No target depends on the SI.

- Paper: Kircheis, L. (2026). "Wildfire smoke increases assaults: evidence from Seattle". Environmental Research Letters 21, 044020. DOI https://doi.org/10.1088/1748-9326/ae436c . Open access, CC BY 4.0. Received 2025-09-17, published 2026-02-26.
- Text source read: publisher PDF https://iopscience.iop.org/article/10.1088/1748-9326/ae436c/pdf (HTTP 200, 887,006 bytes, 10 PDF pages = IOP download cover + journal pp. 1-9, sha256 88218ab352b3caa0a5ce24505c9724d13a9cf5ac6869e4539703adbab6844e06), downloaded 2026-10-10 20:39 UTC; also the IOPscience HTML full text (same numbers). Page numbers below are journal page numbers (PDF page = journal page + 1).
- Dataset: "Replication Data for: Wildfire Smoke Increases Assaults: Evidence from Seattle", Harvard Dataverse, https://doi.org/10.7910/DVN/FXRNBA , version 1.1, released 2026-02-20, licence CC BY-NC 4.0 (META.md). Metadata: `data_statement_raw/dataverse_FXRNBA.json`. 14 files, none restricted. All downloaded 2026-10-10 20:38-20:39 UTC to `/workspace/audit_runs/23_FXRNBA/prereg/files/`; sha256 list also in `data_statement_raw/deposit_checksums.sha256`.

| datafile id | Dataverse folder / name (as served) | URL | bytes | sha256 |
|---|---|---|---|---|
| 13436966 | wildfire_data_analysis.R | https://dataverse.harvard.edu/api/access/datafile/13436966 | 95153 | 69407b415effc5123aad99e1d6bcba08d7a88d2363af2429e15aeef232115be5 |
| 13436969 | wildfire_plots.R | https://dataverse.harvard.edu/api/access/datafile/13436969 | 37102 | df577fa09941a7c8cafb244df0337332569ee35c169255374d15e316bac8148b |
| 13436965 | README.md | https://dataverse.harvard.edu/api/access/datafile/13436965 | 6291 | 4a236bb367a9674b3b7242eb29b367a42d2eb84f48486de57b30614266b05ee7 |
| 13436964 | Data Analysis/merged_final_combined_data_13km.csv (original, `?format=original`) | https://dataverse.harvard.edu/api/access/datafile/13436964?format=original | 1330165 | c7a31d4d88b5b4e4538703b186e7c6daca92718b9bfd96cfd3a801b57991119f |
| 13436970 | Data Analysis/merged_final_combined_data_10km.csv (original) | https://dataverse.harvard.edu/api/access/datafile/13436970?format=original | 1325981 | 43959a7017e266163268c58708b5b71ace052c857864e10047a003f193b6e925 |
| 13436967 | Data Analysis/merged_final_combined_data_21km.csv (original) | https://dataverse.harvard.edu/api/access/datafile/13436967?format=original | 1341988 | c4be04d6e5d697c277eadfbc8675dfbdafe19cb17d60aa53927139c6c4eac21b |
| 13436958 | Data Analysis/merged_final_combined_data_7km.csv (original) | https://dataverse.harvard.edu/api/access/datafile/13436958?format=original | 1321110 | 353e1b48a2f66119b549d7c6689d060ae4bd129f568449e921f563f47ee67afc |
| 13436963 | Crime Data/crime_by_beat_2008_2023.csv (original) | https://dataverse.harvard.edu/api/access/datafile/13436963?format=original | 55656300 | 15ab9a149d116ff8b7897ae656bbb69c51a84286da1a08b8ed1ddaf2cacac3a7 |
| 13436960 | Beats/Beats_WM.shp | https://dataverse.harvard.edu/api/access/datafile/13436960 | 292176 | 93ebbf523649d258b41ff49676347a05d7b1b15df0f40679546f12e84ca12880 |
| 13436971 | Beats/Beats_WM.shx | https://dataverse.harvard.edu/api/access/datafile/13436971 | 540 | 4667324b039a41da98a7a4ac82b7ca77a7a435f82b5db41dde2b739b0de8a02f |
| 13436968 | Beats/Beats_WM.dbf | https://dataverse.harvard.edu/api/access/datafile/13436968 | 3155 | 4ebd95af1260ade1b6b86c64c0942641e8e7a83a9cf3e987f576828f412ace1d |
| 13436961 | Beats/Beats_WM.prj | https://dataverse.harvard.edu/api/access/datafile/13436961 | 569 | 5fbc29423f6a9b70dca9527795d953a03c2f33a2c278eaa1a65bc0f7b08f9819 |
| 13436962 | Beats/Beats_WM.cpg | https://dataverse.harvard.edu/api/access/datafile/13436962 | 5 | 3ad3031f5503a4404af825262ee8232cc04d4ea6683d42c5dd0a2f2a27ac9824 |
| 13436959 | Beats/Beats_WM.shp.xml | https://dataverse.harvard.edu/api/access/datafile/13436959 | 250 | e5bc083d88a7c0455f41166d5f76c8b9b6173a6c999c8cbec5719825020fefd8 |

The five CSVs are ingested by Dataverse as `.tab`; the default access URL (no `?format=original`) returns the ingested tab-separated version (13km: 1078378 bytes, sha256 15df5610de778d52b80cfca82f83d45cfe8b9e927e1019682e27e833847d4b24; the other `.tab` hashes are in `data_statement_raw/deposit_checksums.sha256`). The code reads `.csv` with `read.csv(..., dec = ",")`, so the originals are the files to use. The four buffer CSVs each have 8034 data rows (2 stations x 4017 days, 2013-01-01 to 2023-12-31) and identical headers; crime CSV 279316 data rows.

File-name mapping (path-only fix): the code reads `Data Analysis/merged_final_combined_data_{21,13,10,7}km.csv` (analysis line 245, plots line 316), `Beats/Beats_WM.shp` and `Crime Data/crime_by_beat_2008_2023.csv` (plots lines 34-35), all relative to the working directory. The Dataverse `originalFileName` and `directoryLabel` match these exactly, so the only fix is to place the files in those sub-folders (or use the dataset zip, which keeps the folders) and set the working directory to the folder that holds them. Alternative files: the ingested `.tab` versions; do not use them unless the originals become unavailable (then log it, since `dec=","` and quoting behave differently on tab files).

## 1. Headline and targets

Main claim (abstract, journal p. 1): using ground-level wildfire smoke presence as an instrument for PM2.5 in Seattle 2013-2023, "an average smoke-impacted day increased mean ambient PM2.5 by 7.0 ug m-3, which corresponds to 3.6% more assaults". Section 3.1 (p. 4) names Model 3 of Table 1 as the preferred specification: "a one ug m-3 increase in PM2.5 is associated with a 0.5% increase in assaults". Table 1 (p. 6): IV-Poisson, two-stage residual inclusion (2SRI), SEs clustered by calendar date.

Table 1 values as printed (secondary context, not all targets): PM2.5 (instrumented) Model 1 0.009* (0.002) p = 0.000; Model 2 0.010* (0.003) p = 0.000; Model 3 0.005* (0.002) p = 0.027; Model 4 0.012* (0.005) p = 0.021. First-stage F 46.79 / 42.36 / 42.72 / 74.97. Partial R2 0.064 / 0.054 / 0.056 / 0.035. N 7163 / 7163 / 7163 / 5623.

| id | quantity (statistic and code object) | paper value | decimals | location |
|---|---|---|---|---|
| T1 | Model 3 2SRI coefficient on PM2.5: `r3$pm25_mean$beta` = `iv3$est["pm25_mean"]` (analysis lines 577-584) | 0.005 | 3 | Table 1, p. 6, row "PM2.5 (instrumented)", Model (3); text p. 4 ("0.5%") |
| T2 | p-value of T1: `r3$pm25_mean$p` = `2*pnorm(-abs(beta/se))`, se from `iv3$vcov` (ivglm, clusterid = "date") (lines 393-404) | 0.027 | 3 | Table 1, p. 6, Model (3), "p = 0.027" |
| T3 | N of main sample, Models 1-3: `N_main` = `nrow(seattle_main)` (lines 263-291, 550) | 7163 | 0 | Table 1, p. 6, row "N", Model (3) (also Models 1, 2) |
| T4 | Model 3 first-stage F: `d3$F` = b^2 / clustered var of `z_smoke` from `feols(pm25_mean ~ z_smoke + W | station + year + month + dow, cluster = ~date)` (lines 364-374, 582-583) | 42.72 | 2 | Table 1, p. 6, row "First-stage F", Model (3) |
| T5 | Model 3 first-stage coefficient on smoke presence: `coef(d3$fs)["z_smoke"]` (printed at line 667) | 7.0 | 1 | Abstract p. 1; text p. 4; Discussion p. 7 ("7 ug m-3") |
| T6 | % more assaults on an average smoke day: `100*(exp(T1 * T5) - 1)` using the unrounded objects, computed in our extraction script | 3.6 | 1 | Abstract p. 1; text p. 4; Discussion p. 7 |

Printed N: Table 1 prints one N per model (7163 for Models 1-3, 5623 for Model 4). The analysis script also prints `N_main` in the Table 1 footnote and at line 340; all should be the same object.

Candidate statistics where the paper is not explicit (first listed is pre-registered):
- T2: (1) `2*pnorm(-abs(b/se))` from `grab_by_name` (the code that fills Table 1); (2) the `Pr(>|z|)` column of `summary(iv3)`. They should be identical; if not, report both.
- T5: (1) `coef(d3$fs)["z_smoke"]`, Model 3 first stage by `feols` on `seattle_main`; (2) the first-stage coefficient `b_fs` in `wildfire_plots.R` (lines 822-826, Figure 3(b) top row), which is fit on the plots script's own main sample (see inconsistency 1); (3) `coef(iv3$fitX.LZ)` / `coef` of the `glm` first stage inside `run_ivglm` for Model 3 (should equal (1)).
- T6: no deposited script computes 3.6% (grep for `exp(`, `7.0`, `3.6`, percent conversions: only the IQR scaling in `wildfire_plots.R` line 881 and the event-time conversion at analysis line 2418 exist). Candidates: (1) `100*(exp(b3 * fs3) - 1)` with unrounded T1 and T5; (2) `100 * b3 * fs3` (linear approximation); (3) `100*(exp(b3 * 7.0) - 1)` with the rounded 7.0. The extraction script writes all three; (1) is the target.

Conclusion criterion for `same_conclusion`:
- T1: estimate > 0 and T2 p < 0.05 (Table 1 star rule, p < 0.05).
- T2: p < 0.05 (same bucket as the paper's star).
- T3: reproduced N equals 7163. An N-only mismatch with matching estimates is read under CHANGELOG #6(a) (C, not D).
- T4: F > 10 (paper: "the instrument is sufficiently strong"; conventional weak-instrument threshold).
- T5: estimate > 0 and its date-clustered p (from `d3$fs`) < 0.05.
- T6: value > 0 and T1 same_conclusion true.

Inconsistencies noticed (described, not judged):
1. Two definitions of the "main sample". In `wildfire_data_analysis.R` (lines 264-280) `seattle_main` applies `na.omit()` after selecting, besides the Model 3 variables, `smokepm_pred`, `tmax_sq`, `tmin_sq`, `high_temp`, `wind_8bin`, `wind_4bin`, `wdf2`, `week_of_year`, and the other crime counts (robbery, burglary, theft_of_veh, theft_from_veh, intimidation, person, property). `wildfire_plots.R` (lines 341-353, comment "This matches Models 1-3 in the analysis") applies `na.omit()` to a shorter list without wind direction or other crimes. If any of those extra columns has missing values, Table 1 (N 7163) and Figure 3 / the "2.2% per IQR" figure (computed in the plots script) are fit on different samples. Not checked (no data analysis before the run).
2. The abstract's 3.6% and 7.0 are not printed in any table, and no deposited code computes 3.6% (see T6).
3. The paper describes raw smoke-day vs non-smoke-day mean PM2.5 of 14.04 vs 6.26 ug m-3 (difference 7.78, p. 4) and a conditional first-stage effect of 7.0; these are different quantities, consistent with the text's "conditional on covariates".
4. `wildfire_plots.R` comments "same as Python" (line 40) and "matching Python logic" (line 46): the merged station-day CSVs were built by a pre-processing step (apparently Python) that is not in the deposit. The README lists the raw sources (EPA AQS, Childs et al. 2022 smoke data, SPD crime, NOAA, Seattle 911 / use-of-force / SDOT). The audit starts from the merged CSVs, as the deposited code does.
5. `wildfire_plots.R` line 145 loads `ragg`, which is not in the README's install list.
6. In the deposited CSVs `smokePM_pred` is empty on the rows inspected (first and last rows of the 13km file; not counted); the code sets missing `smokepm_pred` to 0 (line 200-203). The Table 1 models use only `smokepm_dummy`, so this does not touch T1 to T6, but `smokepm_pred` is in the `na.omit` list after it has been zero-filled, so it drops nothing.
7. Table 1 note says first-stage diagnostics are clustered by date; the code's partial R2 uses an unclustered restricted `feols` (only RSS, so clustering does not matter for it). No conflict, noted for completeness.

## 2. Reproduction plan

Scripts and order:
1. RUNDIR = `/workspace/audit_runs/23_FXRNBA/<AGENT>/run/`. Download the deposit (per-file originals or the dataset zip `https://dataverse.harvard.edu/api/access/dataset/:persistentId/?persistentId=doi:10.7910/DVN/FXRNBA`, User-Agent "repro-audit-2026"), verify sha256 against the table above, and lay out `RUNDIR/Data Analysis/`, `RUNDIR/Beats/`, `RUNDIR/Crime Data/`. Working directory = RUNDIR. The zip is about 60 MB; unzip to disk with `unzip`, never into memory.
2. `wildfire_data_analysis.R`, top to bottom, unchanged, in one `Rscript` session with stdout/stderr logged to `outputs/analysis_log.txt`. Wrap it so that the objects needed for the targets are saved right after the script ends, e.g. `Rscript -e 'source("wildfire_data_analysis.R", echo=TRUE, max.deparse.length=Inf); saveRDS(list(iv3=iv3, r3=r3, d3_F=d3$F, d3_pr2=d3$pr2, fs3_coef=coef(d3$fs), fs3_vcov=vcov(d3$fs), N_main=N_main, N_copoll=N_copoll, r1=r1, r2=r2, r4=r4, d1F=d1$F, d2F=d2$F, d4F=d4$F), "outputs/table1_objects.rds")'`. Note the script starts with `rm(list = ls())`, so anything defined before `source()` is wiped; the save must come after.
3. Restart safety: the script is deterministic (no `set.seed`, no bootstrap, no random draws in the Table 1 path), so a restart costs only a rerun. To protect the targets, also run a second, short wrapper that sources only lines 1-668 (through `save_kable(main_tbl, ...)` and the Model 3 print) into a separate session and saves `outputs/table1_objects_part.rds` before the full run. This uses the authors' lines unchanged; it is a subset run, not an edit.
4. `wildfire_plots.R` is not needed for any target. Run it afterwards only if time allows (it reads the 55.7 MB crime CSV with `read.csv`, peak a few hundred MB; needs `sf`, `ragg`, cairo). Its failure does not affect the class.
5. `scripts/extract_targets.R`: reads `outputs/table1_objects.rds` and writes `outputs/targets_extracted.csv` with: T1 beta, its SE, T2 p (both candidates), T3 N, T4 F, partial R2, T5 first-stage coefficient with clustered SE and p, T6 candidates (1)-(3), plus the Model 1, 2 and 4 rows as secondary. Also copy `table_1_main_results.html` into `outputs/`. `scripts/build_results.py` builds `results.json` from the CSV.

Where each target comes from: T1, T2 from `r3` (Model 3, `run_ivglm` + `grab_by_name`); T3 from `N_main`; T4 from `d3$F`; T5 from `coef(d3$fs)["z_smoke"]`; T6 computed from T1 and T5 objects.

Allowed environment fixes (each as a diff in `diffs/` with a reason):
- Working directory / folder layout (path-only fix as mapped above).
- `kableExtra::save_kable` or `print(kable)` failing for a missing system library: make that export call non-fatal (`try(...)`). It does not touch estimates.
- Locale: the script uses `lubridate::wday(label = TRUE)` and `month(label = TRUE)`; labels follow `LC_TIME`. Run with `LC_ALL=C.UTF-8` (or `en_US.UTF-8`) and record it. FE levels are the same in any locale, so estimates are unaffected; Section 12 (line 1530 onward) has German-weekday handling that might need an English locale to match its `dow` names.

Packages (README, no versions pinned; README says R >= 4.0; script header dated December 2025): haven, tidyverse, fixest, ivtools, sandwich, lmtest, weathermetrics, lubridate, knitr, kableExtra, MASS, splines (plots: sf, viridis, scales, patchwork, colorspace, ragg). All on CRAN on 2026-10-10 (index pages checked: ivtools 2.3.0 published 2020-02-24, weathermetrics 1.2.2 published 2016-05-19, fixest 0.14.2 published 2026-06-26, kableExtra and sf present). No pin exists, so current CRAN is tried first. Version note for fixest (it produces T4 and T5): the CRAN release current when the script was dated (December 2025) was fixest 0.13.2 (archive date 2025-09-08; 0.14.0 dated 2026-03-18). If T4 or T5 differs beyond rounding with current fixest, re-run with fixest 0.13.2 via `remotes::install_version("fixest", "0.13.2")` as an allowed package-version fix and report both (as in CHANGELOG #6(b)); if 0.13.2 fails to compile under R 4.5, try 0.12.1. ivtools 2.3.0 has been unchanged since 2020, so no ivtools fallback is needed; its dependency `ahaz` compiles from source.

Memory and time: the four analysis CSVs are 1.3 MB each (8034 rows); models have about 7000 rows and fewer than 40 parameters. Peak memory for `wildfire_data_analysis.R` is expected well under 1 GB, so no reduced-memory fallback is needed. Expected wall time: a few minutes up to about 20 minutes (dozens of `glm`/`ivglm`/`feols`/`fepois` fits; `ivglm` with `clusterid` computes a sandwich vcov). If one foreground call cannot finish in the shell limit, run it as a background job with the log written to disk.

## 3. Robustness checks (pre-registered)

All three checks target the preferred Model 3 PM2.5 coefficient (T1). Each check reports estimate, SE or CI, p, N. "Same direction and significance as the paper" means: estimate > 0 and p < 0.05 (or, for R_a, a 95% interval that excludes 0), matching Table 1's Model 3 (0.005, p = 0.027).

R_a. Date-cluster bootstrap of the full 2SRI estimator. The paper's estimator is deterministic, so this is the resampling check. Starting from `seattle_main` exactly as built by the authors' code (N 7163), call `set.seed(20261011)` once and draw B = 999 bootstrap samples of calendar dates with replacement (sample of `unique(date)` of the same length; each drawn date brings both station rows for that date; duplicates kept). Generate all B index vectors first and save them to `outputs/Ra_boot_indices.rds`. In each replicate, refit Model 3 exactly as `run_ivglm` does (`droplevels`, `glm` first stage `pm25_mean ~ z_smoke + holiday + awnd + tmax + tmin + prcp + station + year + month + dow`, Poisson second stage `assault ~ pm25_mean + same controls and FE`, `ivtools::ivglm(estmethod = "ts", ctrl = TRUE)`), without `clusterid` and with `vcov.fit = FALSE` (point estimate only), and record `est["pm25_mean"]`. Write results to `outputs/Ra_boot.csv` every 50 replicates and skip replicates already present on restart. Report the original T1 as estimate, the bootstrap SE (sd of the replicates), the 95% percentile interval, and as p the two-sided bootstrap share min(2 x share of replicates <= 0, 1). Failed or non-converged replicates are counted and reported, not replaced. Reduced-K rule: time the first 20 replicates; if the projected time for 999 exceeds 30 minutes, use B = 499; if 499 would exceed 60 minutes, use B = 199. Record which B was used and why. Same direction and significance: estimate > 0 and the percentile interval excludes 0.

R_b. Outlier exclusion on the outcome (default rule). On `seattle_main` (the Model 3 sample), compute z = (assault - mean(assault)) / sd(assault) over all 7163 station-days pooled; drop rows with |z| > 3; refit Model 3 with the authors' `run_ivglm` (`clusterid = "date"`, `vcov.fit = TRUE`) and `grab_by_name`, and `fs_diag` for the first-stage F. Report beta, SE, p, F, N, and the number of rows dropped overall and by station. The outcome is a count with a station-specific level; the pooled z rule is the pre-registered default and is applied as written even if most dropped rows come from one station (report the split).

R_c. Alternative estimator: linear IV (2SLS) on log assaults. The paper contrasts its 2SRI Poisson with classic 2SLS (p. 3). Fit, on `seattle_main`, `fixest::feols(log(1 + assault) ~ holiday + awnd + tmax + tmin + prcp | station + year + month + dow | pm25_mean ~ z_smoke, data = seattle_main, cluster = ~date)` with the fixest version used for the main run. Report the `fit_pm25_mean` coefficient (approximately a proportional change per ug m-3), clustered SE, p, first-stage F (`fitstat(..., "ivwald")`), and nobs. Same direction and significance: coefficient > 0 and p < 0.05.

Exploratory only (not pre-registered, never changes the class, must be labelled as such if run): Model 3 on the sample defined by listwise deletion over the Model 3 variables only (see inconsistency 1), and a count of rows dropped by the extra `na.omit` columns.

## 4. Known risks

- Supplementary Information unread (captcha). Targets are all from the main text; SI tables (B1 to B14) cannot be compared.
- Upstream construction of the merged CSVs from raw sources (EPA, Childs et al., SPD, NOAA) is not deposited (inconsistency 4). The deposited code itself reads only deposited files, so this does not by itself make the reproduction incomplete under rule #4, but the data-building step cannot be audited.
- T5 and T6 are prose values; T6 is not computed by any deposited script. A mismatch there may reflect the formula the author used rather than the code.
- fixest version sensitivity for T4/T5 (small-sample correction of the clustered vcov). Fallback 0.13.2 pre-registered above.
- `read.csv(dec = ",")` on files whose decimals use "." (quoted, e.g. "8.7"): the code converts these columns with `as.numeric` afterwards, so it should work; if a numeric column used in Model 3 stays character or becomes NA, record it (it would be a data-reading issue, not an environment fix).
- `kableExtra` pulls `svglite`/`systemfonts` (needs fontconfig/freetype headers on aarch64). If it cannot be installed, Debian `r-cran-kableextra` is the first fallback; the export calls can be made non-fatal, but `kable()`/`pack_rows()` are called while building tables, so the package must load for the script to reach line 668.
- No Stata or proprietary dependency. No long compute expected. Classes C or E are most likely only if an R package cannot be installed on aarch64 (E) or if the code cannot produce the printed Table 1 values (C/D per PROTOCOL.md section 7 and CHANGELOG #6).
