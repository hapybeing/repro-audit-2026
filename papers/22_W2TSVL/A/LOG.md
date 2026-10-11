<!-- status-note:start -->
> **Status note added 2026-10-11, after this run; not part of the agent's record.** This file keeps the agent's run-time wording, which may call an item a "bug". Under CHANGELOG_METHOD.md #4d, the status in `batches/batch5_code_observations.csv` applies. For 22_W2TSVL: unverified agent observation: 22-2; verified finding: 22-1. Only "verified finding" items are findings; "unverified agent observation" items are unverified and are not claims about the paper. Nothing here says the paper is wrong.
<!-- status-note:end -->

# LOG: 22_W2TSVL, agent A

All times IST (UTC+05:30). Scratch: /workspace/audit_runs/22_W2TSVL/A/ (dl/, orig/, run/, rlib/).

- 2026-10-11 02:35 IST. Read batch5_run_brief.md, AGENT_RUNBOOK.md, PROTOCOL.md, PREREG.md, targets.json, DATA_STATEMENT.md, batch5_class_decisions.md. Rscript present (R 4.5.0). MemAvailable about 2.6 GB. Did not read B/ or any other paper's folders.
- 2026-10-11 02:35 IST. Downloaded the 4 code/doc files and `OA23 Base UT-TEC.dta` (`?format=original`, curl -L, UA repro-audit-2026) plus the publisher supplement PDF into dl/. All sha256 equal the PREREG values (checksums.sha256).
- 2026-10-11 02:36 IST. stargazer and tableone not installed; no Debian r-cran-stargazer / r-cran-tableone package in trixie. Installed stargazer, gmodels, tableone from CRAN source into rlib with Ncpus=1 (one R process, MemAvailable about 2.6 GB). All other packages from the system library.
- 2026-10-11 02:36 IST. Environment fixes (diffs/): line 14 absolute path to relative in both scripts; install.packages() lines commented out (appendix 4-6, 138, 282; main 4-8). browseURL no-op in wrapper scripts/run_appendix.R. Note: the batch brief says "path line 15"; the absolute-path read_dta is on line 14 of both scripts (main line 15 is the commented alternative); line 14 was edited as PREREG.md describes.
- 2026-10-11 02:37 IST. Ran `Rscript scripts/run_appendix.R` in run/ (the authors' Appendix A1.R via source(echo=TRUE)). Exit 0. Stdout in outputs/appendix_stdout.txt. Warnings only: 4 x "non-integer #successes in a binomial glm!" (weighted polr start values, m2/m5/m8/m11) and 5 x dplyr "argument is not numeric or logical: returning NA" from the Table A4 means of the ordered factor `unions` (line 224). Copied table_1A_new.htm, table_A2_new.htm, table_A3_new.htm, models_appendix.rds to outputs/.
- 2026-10-11 02:37 IST. scripts/extract_targets.R wrote outputs/targets_extracted.csv (first run failed with "object 'dta' not found" inside drop1 for the secondary LR p; fixed by loading the prepared data in my script, no change to the authors' code). Values:
  - T1 (m1 anti_strike): -0.385804, SE 0.1795, Wald p 0.03162
  - T2 (m7 pro_strike): 0.473369, SE 0.1817, Wald p 0.009172
  - T3 (m1 pro_strike): 0.19359, SE 0.1811, Wald p 0.285
  - T4 (m4 anti_strike): -0.579392, SE 0.1791, Wald p 0.001216
  - T5 (m1 nobs): 976
  - T6 (m7 nobs): 961
- 2026-10-11 02:38 IST. Ran the authors' main script via scripts/run_main.R (polr traced to capture fits). Exit 0, no errors, 4 figure pages drawn (outputs/main_script_figures.pdf). scripts/crosscheck_main.R: the four figure models equal m1, m4, m7, m10 (outputs/crosscheck_main_vs_appendix.csv, max abs diff below 1e-14).
- 2026-10-11 02:38 IST. Robustness (scripts/robustness.R, MemAvailable about 1.65 GB, one R process): R_a 1000+1000 bootstrap refits in 108 s, draws saved every 100; R_b dropped 2 rows with |z(age)| > 3; R_c OLS with HC2. Results in outputs/robustness.json. T1 criterion met in all three checks; secondary T2 criterion met in R_b only (R_a 99% CI lower bound -0.0197; R_c p 0.02021).
- 2026-10-11 02:40 IST. scripts/check_supplement_cells.py re-read the six target cells from the publisher supplement PDF: all agree with targets.json (outputs/supplement_target_check.json).
- 2026-10-11 02:41 IST. Code review of both scripts in full; data facts in outputs/code_observations_check.json (education code 13 'No tiene estudios' set to NA, 17 rows; Table A4 means typed, consistent with the numeric means). No bug affecting the targets.
- 2026-10-11 02:41 IST. environment.txt written by scripts/make_environment.sh.
- 2026-10-11 02:42 IST. LOG.md written by scripts/make_log.py, then results.json by scripts/build_results.py. Proposed class read from results.json.
