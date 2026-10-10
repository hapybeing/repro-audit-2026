<!-- status-note:start -->
> **Status note added 2026-10-10, after this run; not part of the agent's record.** This file keeps the agent's run-time wording, which may call an item a "bug". Under CHANGELOG_METHOD.md #4d, the status in `batches/batch3_code_observations.csv` applies. For 15_1BBC4E: unverified agent observation: 15-1. Only "verified finding" items are findings; "unverified agent observation" items are unverified and are not claims about the paper. Nothing here says the paper is wrong.
<!-- status-note:end -->

# LOG: 15_1BBC4E, agent B (blind second pass)

Start: 2026-10-10 21:20 IST (15:50 UTC)

All times IST, 2026-10-10. Agent B did not open, list or read papers/15_1BBC4E/A/ or /workspace/audit_runs/15_1BBC4E/A/ or any batch report. (The workspace tool printed file names of A's outputs as change notices while I worked; I did not open any of them.)

1. 21:20 Read batch3_run_brief.md, AGENT_RUNBOOK.md, PROTOCOL.md, CHANGELOG_METHOD.md, PREREG.md, targets.json, DATA_STATEMENT.md, META.md, batch3_class_decisions.md.
2. 21:21 Fetched dataset metadata from the Dataverse API (49 files, none restricted). The API reports versionNumber 1, versionMinorNumber 1 (PREREG.md says version 1.0); see uncertainties. First download loop failed: curl without -L saved the 303 redirect bodies; a bash `read` with tab IFS also collapsed empty fields. Both fixed in a Python download loop (curl -sSL, User-Agent "repro-audit-2026"; `?format=original` for the four ingested tabular files as PREREG.md says).
3. 21:22 All 49 downloads HTTP 200, md5 of every file matches the Dataverse metadata, and all 49 sha256 values equal the values in PREREG.md (checksums.sha256; outputs/download_log.tsv).
4. 21:23 R 4.5.0 (Debian). Missing: corrr, pacman (no Debian binary). Installed from CRAN source into /workspace/audit_runs/15_1BBC4E/B/rlib with Ncpus=1: corrr 0.4.5, pacman 0.5.1. tidyverse, knitr, kableExtra (Debian 1.4.0), RColorBrewer, psych (Debian 2.4.12) already present.
5. 21:24 Ran the three target scripts unmodified, each in a fresh Rscript session from the R project folder (scripts/run_authors.sh): Comparison.R, Share_Common_Sample.R, Agreement across all.R. All exit 0. Only ggplot2 deprecation / removed-rows warnings (figures). Saved corr.ea (rds and full-precision csv), nrow(ead) and the ead2 tally.
6. 21:25 scripts/extract_targets.R -> outputs/targets_extracted.csv. T1 0.6363706, T2 0.1772635, T3 0.5390712, T4 6067 (candidate 2 also 6067), T5 144, T6 3093. All 21 Table 3 cells match the printed values to 3 decimals (outputs/table3_full_comparison.csv). Median and mean of the 21 pairs: 0.398 and 0.405 (console log lines 96-101), as PREREG.md computed from the printed table.
7. 21:26 scripts/robustness.R (R_a, R_b, R_c exactly as pre-registered) -> outputs/robustness.json, about 2 minutes. Note: 123 rows have missing Final_Code; they have values only for RoW (no other PDA dummy), so they contribute no pair to any correlation. The bootstrap resamples the 223 non-missing country codes. R_b dropped 2 of 172 eligible countries (codes 571 Botswana, 651 Egypt; 372 rows).
8. 21:27 Code review of Comparison.R (full), Share_Common_Sample.R and Agreement across all.R (full). No bug on the target path. One exploratory, not pre-registered observation (figures only): Comparison.R lines 105, 176 and 183 relabel factor levels by position after as.factor(), so the labels depend on the collation locale. scripts/factor_label_locale_check.R -> outputs/factor_label_locale_check.csv: correct in this run's locale (C.UTF-8), wrong under LC_COLLATE=C. Not on any target; the author's own comment at line 104 mentions the level order switching.
9. 21:28 environment.txt, checksums.sha256, diffs/README.md (no diffs: no author file changed), scripts/build_results.py -> results.json.

End: 2026-10-10 21:30 IST (16:00 UTC)
