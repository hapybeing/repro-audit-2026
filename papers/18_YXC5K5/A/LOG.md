<!-- status-note:start -->
> **Status note added 2026-10-11, after this run; not part of the agent's record.** This file keeps the agent's run-time wording, which may call an item a "bug". Under CHANGELOG_METHOD.md #4d, the status in `batches/batch4_code_observations.csv` applies. For 18_YXC5K5: verified finding: 18-1, 18-2. Only "verified finding" items are findings; "unverified agent observation" items are unverified and are not claims about the paper. Nothing here says the paper is wrong.
<!-- status-note:end -->

# LOG: 18_YXC5K5, agent A

All times IST (UTC+05:30). Machine clock is UTC; converted here. Step times were checked against output file modification times.

## 2026-10-11 00:18 Start
- Read batch4_run_brief.md, AGENT_RUNBOOK.md, PROTOCOL.md, PREREG.md, targets.json, DATA_STATEMENT.md, META.md, batch4_class_decisions.md. Did not read B/ or any other paper's folder.
- `Rscript` missing at start. Another agent had already started `scripts/setup_env.sh` (apt lock held), so I waited for it instead of starting a second copy.

## 00:19 Download (scripts/download.py)
- Per-file Dataverse access API, User-Agent "repro-audit-2026", dataset version 1 (latest and only). 94 files into /workspace/audit_runs/18_YXC5K5/A/data. The 4 ingested `.tab` files were fetched with `?format=original` and saved under their original `.csv` names.
- md5 of every file matches the Dataverse metadata. All 94 sha256 values are identical to the pre-registration download list (`data_statement_raw/prereg_download_checksums.sha256`). sha256 list: `checksums.sha256`; manifest `outputs/downloads.json`.

## 00:19 to 00:23 Code reading while R installed
- Read Benchmarking_DataAnalysis.Rmd lines 1-420, 700-800, 1160-1185, 1355-1380, 1540-1660, 1890-2157 (setup, accuracy, precision, descriptives, F1, ICC, AUC, hamming loss, summary table, correlations). See Code review below.

## 00:22 to 00:24 Packages
- Debian binaries (apt, system library): r-cran-caret r-cran-gridextra r-cran-forcats r-cran-patchwork r-cran-proc r-cran-cowplot r-cran-reshape2 r-cran-knitr r-cran-sessioninfo r-cran-tidyverse r-cran-lpsolve (some already present from setup_env.sh).
- No Debian candidate for irr or stargazer: installed from CRAN source into R_LIBS_USER=/workspace/audit_runs/18_YXC5K5/A/rlib with Ncpus=1 (`outputs/install_cran.log`).
- No author pins exist (memo: R 4.3.3 on Windows, no package versions). Versions used are in environment.txt.

## 00:25 Main run, Rmd exactly as deposited (scripts/run_rmd.sh ... main)
- `knitr::purl(documentation = 1)` to `outputs/analysis_main.R`, then `source(..., echo = TRUE)` with working directory = data folder, plots to `outputs/plots_main.pdf`, `save.image` to scratch session_main.RData. Log `outputs/analysis_log_main.txt`.
- Confirmed: the `eval = F` chunk "filter switch" is commented out in analysis_main.R (line 147 header, line 153 `# filter_by_human <- function...`), as in a knit.
- Exit status 0. No errors. No edit to the authors' file, so no environment diff was needed (setting the working directory was done by `cd` in the runner, not by editing code).
- stargazer table in the log reproduces Table A1 LLM rows; GPT 4o 8 Few Shot row: AUC 0.50, Recall 0.87, F1 0.89, HammingLoss 0.18, Mean 12.75.

## 00:25 Extraction (scripts/extract_targets.R -> outputs/targets_extracted.csv)
- First attempt failed: `get_means` (restored from the saved session) calls `tibble()`, which was not attached in the extraction session. Fixed by loading tidyverse and caret at the top of my extraction script (my script only, not the authors' code). Second attempt wrote 148 rows.
- T1 0.18230050933786077; T2 0.15407470288624789; T3 0.28820033955857388; T4 0.89408064691807509; T5 12.754668930390492; T6 589 (pi10mat, gpt4o10mat_fewx and hum10matx all 589 rows).
- Secondary only: F1 with "1" as positive class for GPT 4o Few Shot 8 labels = 0.106 (mean over labels).
- Secondary only: undergrads8 "% 1s" in the script is 0.0972 (9.72%), Table A1 prints 9.68 for Undergraduate Coders 8. Not a target; recorded as an uncertainty.

## 00:25 R_a bootstrap (scripts/robustness.R, seed 20261010, 1000 resamples)
- Outputs: outputs/R_a_summary.csv, R_a_bootstrap_draws.csv, R_a_point_estimates.csv, R_a.log.
- T1 0.1823; D = 0.0282, 95% percentile CI of D [0.0187, 0.0378]; T1 CI [0.1687, 0.1957]; GPT 4o Few Shot 8 lowest of 18 in 100% of resamples. No resample had D <= 0, so the computed p = min(1, 2*0/1000) = 0 (meaning below 1/1000 resolution).

## 00:26 R_b outlier exclusion
- k = rowSums(pi10mat) takes values 0 to 4; z(k=4) = 3.69, z(k=3) = 2.59. 5 rows (k = 4) have |z| > 3 and were dropped from every matrix by position. Outputs outputs/R_b_*.csv.
- T1 0.1789; D 0.0278, CI [0.0173, 0.0383]; rank 1 of 18; same direction and significance: TRUE.

## 00:27 R_c pre-run diagnostic (recorded before running the copy)
- Original script session: `identical(pi$docid, gpt_data$gpt4o_10lab_fewshot$docid)` = FALSE and `identical(pi$docid, human_data$human_10lab$docid)` = FALSE (outputs/targets_extracted.csv, rows "diag"). The docid sets are equal (setequal TRUE), but only 1 of 589 rows (share 0.0017) has the same docid at the same row position.
- Copy (scripts/Benchmarking_DataAnalysis_Rc.Rmd, one line `pi = pi %>% arrange(docid)` inserted after line 108, diff diffs/R_c_Benchmarking_DataAnalysis_docid_sort.diff): expected TRUE for both, since every model and human file is docid-sorted. Checked after the run below.

## 00:27 R_c run (scripts/run_rmd.sh scripts/Benchmarking_DataAnalysis_Rc.Rmd Rc)
- Exit status 0. Log outputs/analysis_log_Rc.txt; extraction outputs/R_c_targets_extracted.csv.
- Diagnostics in the copy: both identical() checks TRUE, share of rows with matching docid = 1.
- Copy values: T1 0.1101, T2 0.0925, T3 0.1507, T4 0.9362, T5 12.75 (unchanged, it does not use the benchmark), T6 589. GPT 4o 8 Few Shot AUC 0.748 (0.497 in the original). GPT 4o Few Shot 8 is still the lowest hamming loss of the 18 LLM specs.
- R_c bootstrap (seed 20261010, 1000): D = 0.0176, CI [0.0079, 0.0267]; lowest of 18 in 100% of resamples; same direction and significance TRUE (outputs/R_c_summary.csv).

## 00:28 Code-review evidence scripts
- scripts/row_pairing_check.R -> outputs/row_pairing_confusion_counts.csv, outputs/model_files_docid_order.csv. Pooled 8-label counts for GPT 4o Few Shot: position pairing FP 539, FN 320; docid pairing FP 369, FN 150, which equal the Table A5 counts quoted in PREREG.md (computed in the Supplementary Rmd with a docid join). Undergraduates docid pairing FP 256, FN 180 vs printed Table A6 FP 254, FN 180. All 18 model and both human data frames share one docid order.
- scripts/undergrad_row_check.R -> outputs/undergrad_row_check.csv: undergrads8/4 AUC, Recall, F1 are identical to the GPT 4 Turbo Zero Shot rows (all six TRUE).

## Code review (read about 1,000 of 2,157 lines of Benchmarking_DataAnalysis.Rmd: setup, accuracy, precision, descriptives, F1, ICC and AUC function definitions, hamming loss, summary table, correlations; plotting chunks skimmed only)
1. Row pairing (line 108, with comparisons at lines 1552-1572, 124-128, 1358, 1168, 2050-2064): the author benchmark is compared with model and undergraduate codes by row position while the files are in different docid orders. Confirmed by run (see above). The printed Table A1 numbers match this position-paired computation.
2. Undergraduate AUC/Recall/F1 (lines 2051-2053 and 2059-2061) use gpt10mat / gpt4mat instead of the undergraduate matrices. Confirmed by run. Does not affect T2.
- Not counted as bugs: `read_and_process_human` names its keep-list argument `drop_ids` (line 85) but uses it as a keep filter, which is what the call intends; the Spanish file is tagged num_labels "4" (line 47) but that column is not used in any computation.
- Benchmarking_Supplementary.Rmd and Benchmarking_DataGeneration.Rmd not run (not needed for targets, per PREREG).

## 00:30 End
- scripts/build_results.py builds results.json from outputs/. Checksums in checksums.sha256; environment in environment.txt.
