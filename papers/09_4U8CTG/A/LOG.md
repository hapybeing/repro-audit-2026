<!-- status-note:start -->
> **Status note added 2026-10-10, after this run; not part of the agent's record.** This file keeps the agent's run-time wording, which may call an item a "bug". Under CHANGELOG_METHOD.md #4d, the status in `batches/batch2_code_observations.csv` applies. For 09_4U8CTG: out of scope: not reproducibility: 09-6; unverified agent observation: 09-2, 09-3, 09-4, 09-5; verified finding: 09-1. Only "verified finding" items are findings; "unverified agent observation" items are unverified and are not claims about the paper. Nothing here says the paper is wrong.
<!-- status-note:end -->

# LOG, agent A, paper 09_4U8CTG (run date 2026-10-10, times IST)

Brief: REPO/batches/batch2_run_brief.md. Read AGENT_RUNBOOK.md, PROTOCOL.md, PREREG.md, targets.json, DATA_STATEMENT.md, batch2_class_decisions.md before running anything. Did not read B/ or any other paper's folders. Scratch: /workspace/audit_runs/09_4U8CTG/A/ (dl/ = untouched download, run/ = working copy, rlib/ = per-run R library).

- [18:01 IST] Start. `Rscript` missing. Ran `bash REPO/scripts/setup_env.sh`: failed, "Could not get lock /var/lib/apt/lists/lock. It is held by process 1882 (apt-get)" (another agent installing R system-wide). Waited instead of looping.
- [18:03 IST] Downloaded all 64 files listed by the Dataverse API (doi:10.7910/DVN/4U8CTG, version 1.0) with curl -A "repro-audit-2026"; the three ingested .tab files via `?format=original` (CSV). All HTTP 200. sha256 in checksums.sha256. All 37 non-image files match the sha256 values in PREREG.md. Note: API lists 64 files / 27 PNG; PREREG says 66 / 29.
- [18:05 IST] Read README and 02 in full around data import, preparation, models, Tables D3 to D10, F1 to F3; read the 01 model block (same baseline models as 02).
- [18:07 IST] R 4.5.0 now present (system install by shared setup). Missing from the 02 package list: texreg, stargazer, vtable, jtools, binom (no Debian binaries). Installed from CRAN source into R_LIBS_USER=rlib with Ncpus=1. pdflatex present (system TeX Live). `tinytex::tinytex_root()` errors: "/usr/share/texlive does not seem to be the root directory of TeX Live (no "bin/" dir under it)", so 02 lines 108 to 117 would stop the script.
- [18:08 IST] Made run/replication_scripts/02 copy with only the PREREG-allowed skips (LaTeX block and Study 1 lines). Diff: diffs/02_supplementary_materials.R.diff, reasons in diffs/README.md. Parse OK.
- [18:06 to 18:12 IST] Run 1: scripts/extract_targets.R (source 02, then write outputs/targets_extracted.csv). 02 finished; extraction CSV written. The script then ended with "Error: object 't0' not found" (my own timer variable, removed by 02's `rm(list = ls())`). Also found the regenerated texreg tables (D3 to D7, D10, E1) were empty: `source(echo = FALSE)` does not auto-print, so `texreg()` inside `sink()` wrote nothing. Log: outputs/run_02_attempt1_log.txt.
- [18:13 IST] Robustness script scripts/robustness.R (written before the run 1 output was inspected beyond the target CSV; it implements PREREG section 3 as written) run. R_c diagnostic before fitting: 0 rows with swd_ch != swd_w2 - swd_w1, 0 for LREM (outputs/R_c_diagnostic.txt). Outputs: outputs/robustness.csv, outputs/robustness_log.txt.
- [18:12 to 18:15 IST] Run 2: fixed my extraction script only (timer kept in an env var; `source(..., print.eval = TRUE)`, the same as running 02 top level with Rscript). Elapsed 177 s. targets_extracted.csv byte-identical to run 1. Log: outputs/run_02_log.txt (only warnings: "Use of `data$m_check3` is discouraged", twice).
- [18:16 IST] Compared the 22 regenerated Study 2 tables with the deposited copies after stripping CR line endings: all 22 identical (outputs/table_comparison_summary.txt; regenerated copies in outputs/tables_regenerated/). Tables B4, F1, F2, F3 were not regenerated (Study 1 skipped).
- [18:16 IST] Code review check scripts/mht_label_check.R -> outputs/mht_label_check.csv: in make_mht_table (02 line 1729) the hard-coded labels do not follow the coefficient order; rows 2, 3, 5 of Tables D8 and D9 are mislabelled; the Out-group row is correct.
- [18:18 IST] Wrote environment.txt, checksums.sha256, diffs/README.md, outputs/uncertainties.txt.

## Results (numbers from outputs/targets_extracted.csv, outputs/robustness.csv; results.json built by scripts/build_results.py)
- T1 Out-group ATE on SWD change, Model 1: reproduced -1.26603 (SE 0.62820, p 0.04614); paper -1.27 (0.63) *. Match to rounding.
- T2 N: 123 = 123. T3 Out-group ATE on LREM change, Model 1: -0.51130 (SE 0.34180, p 0.1374); paper -0.51 (0.34). Match. T4 N: 120 = 120.
- T5, T6 (Study 1): not run, FES inputs registration-only at ELIPSS.
- Context numbers also match Table D3/D5 Models 2 to 4 (regenerated tables identical to deposit).
- R_a bootstrap: -1.266, percentile 95% CI [-2.789, 0.205], p 0.086: CI includes 0 (not same significance as paper). LREM secondary CI [-1.045, -0.010].
- R_b |z| > 3: 2 control rows dropped; estimate -0.542 (SE 0.548), p 0.325: not significant. LREM secondary: 3 dropped, -0.511, p 0.058.
- R_c ANCOVA: -0.819 (SE 0.592), p 0.170: not significant. LREM secondary: -0.375, p 0.266.

## Decisions
- Proposed class C (batch2_class_decisions.md item 2: Study 1 targets behind registration). Alternative on open targets T1 to T4: A.
- 01 and 00 not run (not required; 00 cannot run without ELIPSS data).
- [18:20 IST] Built results.json with scripts/build_results.py. End.
