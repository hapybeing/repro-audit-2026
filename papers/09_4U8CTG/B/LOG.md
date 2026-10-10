<!-- status-note:start -->
> **Status note added 2026-10-10, after this run; not part of the agent's record.** This file keeps the agent's run-time wording, which may call an item a "bug". Under CHANGELOG_METHOD.md #4d, the status in `batches/batch2_code_observations.csv` applies. For 09_4U8CTG: out of scope: not reproducibility: 09-6; unverified agent observation: 09-2, 09-3, 09-4, 09-5; verified finding: 09-1. Only "verified finding" items are findings; "unverified agent observation" items are unverified and are not claims about the paper. Nothing here says the paper is wrong.
<!-- status-note:end -->

# LOG: 09_4U8CTG, agent B (blind second pass)

All times IST (UTC+05:30), 2026-10-10. Scratch: /workspace/audit_runs/09_4U8CTG/B/ (deposit/ = pristine download, run/ = working copy, rlib/ = fresh R library). Did not open, list or read papers/09_4U8CTG/A/, /workspace/audit_runs/09_4U8CTG/A/, any batch report or any other paper's folders. No sign-in, registration or author contact.

- 18:14 Read batch2_run_brief.md, AGENT_RUNBOOK.md, PROTOCOL.md, PREREG.md, targets.json, DATA_STATEMENT.md, META.md, batch2_class_decisions.md.
- 18:15 Environment: Rscript present (R 4.5.0, Debian 13 aarch64). Of the 02 package list, texreg, stargazer, vtable, jtools, binom were missing; `apt-cache policy r-cran-<pkg>` showed no candidates, so installed from CRAN source into R_LIBS_USER=rlib with Ncpus=1 (outputs/install_*.log).
- 18:16 Downloaded dataset metadata (API) and the 35 non-image files. First loop attempt produced empty files (my shell loop: missing `-L`, Dataverse answers 303 redirect; and curl reading the loop's stdin). Fixed with `curl -sfL ... </dev/null`. CSV originals via `?format=original` as PREREG says. All 35 sha256 equal the PREREG table (checksums.sha256). API lists 64 files (PREREG says 66; see uncertainties).
- 18:18 Read 02_supplementary_materials.R end to end. Built run/ copy; inserted `if (FALSE) {` wrappers around the Study 1 blocks named in PREREG plan item 1 (exact deposited ranges confirmed: 146-149, 162-192, 253-286, 1218-1262, 1455-1468, 1789-1815, 1819-1861). File has CRLF endings; first diff attempt rewrote every line (Python universal newlines), redone byte-wise so the diff has only added lines.
- 18:21 Attempt 1 (outputs/run_02_attempt1_log.txt) stopped: `Error in root_dir(normalizePath(path), "..", "..", "..") : /usr/share/texlive does not seem to be the root directory of TeX Live (no "bin/" dir under it)` from `tinytex::tinytex_root()` (02 line 114). pdflatex exists, so lines 108-112 pass. Skipped lines 114-117 (LaTeX package install only; PREREG plan item 2). diffs/02_supplementary_materials.R.diff, diffs/README.md.
- 18:23 Attempt 2 (outputs/run_02_attempt2_log.txt): 02 ran to the end; my extraction script then failed with `object 't0' not found` because 02 starts with `rm(list = ls())`. Fixed my script (dot-named variable). Not an author issue.
- 18:26 Attempt 3 (outputs/run_02_attempt3_log.txt): 02 finished in 2.59 min; targets extracted. Comparing tables showed every texreg-produced .tex file empty: `texreg()` inside `sink()` only writes when its value is auto-printed, which `source(echo = FALSE)` does not do. stargazer/st/kable tables were fine.
- 18:30 Attempt 4 (final, outputs/run_02_log.txt): same modified 02, sourced with `print.eval = TRUE` from a fresh copy of the deposit. 02 finished in 2.58 min; only warnings were ggplot "Use of data$m_check3 is discouraged". outputs/targets_extracted.csv byte-identical to attempt 3 (outputs/targets_extracted_attempt3_echoFALSE.csv).
  - T1 model_1_ez Out-group: -1.266026 (SE 0.628203, classical p 0.046144), N 123. T3 model_1_ez_lrem Out-group: -0.511304 (p 0.137412), N 120. Model 2 (HC2) SWD p 0.0967; LREM p 0.0582.
- 18:33 scripts/compare_tables.py: all 22 regenerated Study 2 / descriptive tables (A1-A6, B1-B3, C1-C2, D1-D10, E1) identical to the deposited .tex files ignoring line endings (outputs/table_compare.json, outputs/tables_regenerated/). B4, F1, F2, F3 not regenerated (Study 1).
- 18:34 Robustness (scripts/robustness.R, outputs/robustness.csv, run twice, identical). R_c diagnostic: rows with swd_ch != swd_w2 - swd_w1: 0; same for LREM: 0. Recorded before reading R_c output (both printed by the same script; the diagnostic line is computed and logged first).
  - R_a (seed 20261010, B=2000, stratified): T1 estimate -1.2660, boot SE 0.7458, 95% CI [-2.7885, 0.2054], p 0.086. Not same significance as paper.
  - R_b (|z|>3): T1 drops 2 rows (both control, swd_ch = 10); estimate -0.5417, SE 0.5476, p 0.325, N 121. Not same.
  - R_c (ANCOVA): T1 -0.8188, SE 0.5925, p 0.170, N 123. Not same.
  - Secondary LREM: R_a -0.5113, CI [-1.0453, -0.0103], p 0.041 (differs from paper's 'not significant'); R_b drops 3 rows, -0.5113, p 0.058; R_c -0.3746, p 0.266.
- 18:35 Code checks (scripts/extra_checks.R): Tables D8/D9 label order (outputs/mht_label_check.csv) and figure label order for D1, D2, D4 (outputs/figure_label_check.csv). See results.json "bugs".
- 18:37 environment.txt, checksums.sha256, figures copied to outputs/figures_regenerated/. scripts/build_results.py -> results.json.
- 18:39 Done. Wall time about 25 min (18:14 to 18:39); compute about 12 min.

Decisions:
- 01_manuscript.R not run (PREREG: optional cross-check of T1/T3; 02 and the deposited tables already agree).
- T5/T6: reproduced_value null; not attempted (registration-only data).
- Class: C by batch2_class_decisions.md #2; alternative on T1-T4 alone: A.
