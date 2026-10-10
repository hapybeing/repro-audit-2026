<!-- status-note:start -->
> **Status note added 2026-10-10, after this run; not part of the agent's record.** This file keeps the agent's run-time wording, which may call an item a "bug". Under CHANGELOG_METHOD.md #4d, the status in `batches/batch2_code_observations.csv` applies. For 10_6MLKJZ: unverified agent observation: 10-2, 10-3; verified finding: 10-1. Only "verified finding" items are findings; "unverified agent observation" items are unverified and are not claims about the paper. Nothing here says the paper is wrong.
<!-- status-note:end -->

# LOG: 10_6MLKJZ, agent B (blind second pass)

All times 2026-10-10, UTC (IST = UTC+05:30). I did not open, list or read papers/10_6MLKJZ/A/ or /workspace/audit_runs/10_6MLKJZ/A/, or any batch report or results file. (The workspace tooling printed names of files changed by other agents, including A's; I did not open them.) Read: AGENT_RUNBOOK.md, PROTOCOL.md, batch2_run_brief.md, PREREG.md, targets.json, DATA_STATEMENT.md, META.md, batch2_class_decisions.md. PREREG.md and targets.json were not edited.

Scratch: /workspace/audit_runs/10_6MLKJZ/B/ (files/ = clean download, run/ = working copy, rlib/ = per-run R library).

## 12:47 Download
- Fetched Dataverse metadata API (version 1.0, 71 files; copy outputs/dataverse_metadata_api_6MLKJZ.json).
- Downloaded all 71 files per file with `curl -A "repro-audit-2026"`, ingested tabular files with `?format=original` (scripts/download.py). All 71 HTTP 200 (outputs/download_log.tsv).
- sha256 of all 71 files identical to prereg_download_checksums.sha256 (diff empty). Checksums: checksums.sha256.

## 12:48-12:53 Environment
- System R 4.5.0 present (no setup_env.sh needed). tidyverse, data.table, Hmisc, here, rvest 1.0.4, survey, sandwich, lmtest, DT, shiny, shinyjs already installed system-wide. Missing: cregg, ebal, cobalt, cjoint, ggstance.
- First install attempt in the foreground hit the 120 s tool limit (outputs/install1.log); rerun detached (scripts/install_packages.R, outputs/install2.log): ebal 0.2.1, ggstance 0.3.7, cobalt 5.0.0 (pulled ggplot2 4.0.3, scales 1.4.0, arg 0.2.1, rlang, cli), cjoint 2.1.3, cregg 0.4.0 from the CRAN archive tarball. Ncpus = 1.
- Run copy: lower-case symlinks data_uhh.csv, data_hsvn.csv (diffs/00). Deposited PNGs moved to run/figures_authors/, deposited prep CSVs to prep_data_deposited/, so the code regenerates both.

## 12:54 Run 1 (cjoint 2.1.3): failed
- scripts/run_authors.R sources 01-04 unchanged in run/analysis with LANG=C.UTF-8. Error in 03 (prep_data via purrr::map_df) inside cjoint::read.qualtrics, verbatim: "Caused by error in `$<-.data.frame`: ! replacement has 0 rows, data has 2048" (outputs/run_authors_log_attempt1_cjoint213.txt).
- Read the 2.1.3 source: it renames the ID column to `respondent` and makes respondentIndex an integer; the authors' code (01 lines 151, 154) expects `Response.ID` and `respondent`. Decision: version pin, not a code change. cjoint 2.1.0 was the CRAN release current at the authors' last revision (2023-07-11; 2.1.1 came 2023-08-22).
- Installed cjoint 2.1.0 from the CRAN archive; first attempt failed ("dependency 'shinyBS' is not available"), then installed shinyBS 0.61.1 from the archive and cjoint 2.1.0 (outputs/install3.log). diffs/01.

## 12:58-13:00 Run 2 (cjoint 2.1.0): completed
- 01-04 ran to the end (outputs/run_authors_log.txt, warnings in outputs/run_authors_warnings.txt). Notable warnings: dplyr "Detected an unexpected many-to-many relationship between `x` and `y`" (03 line 133), rvest repair_encoding deprecation, 8 "NAs introduced by coercion" (Progress column), 101 "svyglm not fitted by maximum likelihood" (cregg), ggplot2 `size` deprecation. No ggplot "Removed rows" warning.
- table(match_data$D) = 2570 / 666 (outputs/table_match_data_D.txt): profile rows at task 1, i.e. 1285 / 333 respondents x 2.
- All 7 cj() results saved as CSV; regenerated PNGs in outputs/figures_regenerated/. Regenerated figure_02 compared by eye with the deposited one: same points and intervals, different font rendering.
- Attribute check: all 8 attributes have the expected level counts and no NA (outputs/attribute_levels_check.csv). No encoding fix needed.

## 13:01-13:03 Targets and figure claims (scripts/targets_and_fc.R)
- First run: my FC script filtered features by variable name, but cj() reports Hmisc labels ("Household\nComposition", "Nationality", ...), so FC1 counted nothing and FC2/FC3 were wrong. Fixed my script (label-to-variable map with a stopifnot), reran. Only my script changed.
- T1 1285, T2 333, T4 510, T5 636, T6 123: exact. T3 2482 vs 1849 (outputs/sample_sizes.csv).
- FC1: 0 of the FC1 levels have mm_diff CIs excluding 0 (holds). Since: 2 levels exclude 0 ("1 Year", "3 Years"); Education 0. FC2: Composition has the largest MM range in both sectors (holds). FC3: Syria < 0.5 and Germany > 0.5 with CIs excluding 0.5 in both sectors (strict holds). outputs/figure_claims.json.

## 13:03-13:06 Robustness (scripts/robustness.R)
- First run stopped at R_b: my label map rejected variable-name features (subsetting dropped the Hmisc labels). Made the map accept both; reran. R_a reran from the same seed.
- R_a, R_b, R_c results in outputs/robustness.json and results.json.

## 13:06-13:09 Code checks
- scripts/code_checks.R: confirmed the many-to-many join duplicates 1614 respondents' rows (87936 rows vs 62112 distinct respondent-task-profile). De-duplicated Figure 1/2 reruns: max MM change 0.0009, FC1 unchanged. Reported as a bug with file, line, evidence.
- scripts/t3_decomposition.R: civic respondents 2482 = 1285 Private + 333 Public + 231 empty sector + 545 sector ".b" + 88 not in survey_data.csv. Private + Public + empty = 1849 = paper's Table 2 total. No step in the deposited code removes the ".b" and absent respondents.
- Code read: all of 01, 03, 04 and the plot functions in 02 used by 04. Fig 1 formula lists Citizenship twice (04 line 31); cregg output has 32 levels per sector, no duplicate, so not a bug.

## 13:10-13:13 Write-up
- environment.txt, diffs/, checksums.sha256, results.json built by scripts/build_results.py from outputs/.
- Proposed class C (T3 not produced by the code; undocumented sample step), alternative A on T1, T2, T4-T6 + FC1-FC3. Confidence medium.
