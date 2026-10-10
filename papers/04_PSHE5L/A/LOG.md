# LOG: 04_PSHE5L, Agent A

All times IST (Asia/Kolkata).

## 2026-10-09 21:10 Start
- Read PROTOCOL.md, AGENT_RUNBOOK.md, META.md, PREREG.md, targets.json.
- Verified PREREG.md sha256 = 99ac5e41e87def5056b8268a797a69b3bada761c05bf3d5fb1010fe58797289b, equal to batches/batch1_prereg_hashes.txt. Not edited.
- Did not read papers/*/B/, other papers' runs, or /workspace/audit_runs/04_PSHE5L/prereg/.

## 21:11 Downloads (fresh, into /workspace/audit_runs/04_PSHE5L/A/raw)
- Dataverse file 10695152 (`Rural Populism - Socius - Public Code.R`) via https://dataverse.harvard.edu/api/access/datafile/10695152 -> dataverse_code.R
- Dataverse dataset metadata JSON: confirms the deposit has one file only (the R script), no data, no README.
- OSF code https://osf.io/download/6zsmv/ -> osf_code.R (byte identical to the Dataverse file).
- OSF data https://osf.io/download/wr3ve/ -> Rural_Populism_Dataset.csv (79755 bytes).
- All sha256 equal those in PREREG.md section 0. See checksums.sha256.
- Data source note: the data are NOT in the Dataverse deposit; they come from the authors' OSF component https://osf.io/mtd4z/ (CC-BY 4.0), which the paper does not cite. The script reads a differently named 117-column file (line 9) that is not public.

## 21:13 Package installs (fresh library /workspace/audit_runs/04_PSHE5L/A/rlib)
- `remotes::install_version` lavaan 0.6-19 and semTools 0.5-6 into the fresh library: both installed (outputs/install_core_lavaan_semtools.log). First attempt failed because `lib=Sys.getenv("R_LIBS_USER")` returned a colon-joined path list; reran with the explicit path.
- 21:16 started gt + semPlot install (current CRAN, single thread, 20-minute cap per PREREG fix 3). gt failed in 0.6 min: dependency V8 needs system libv8 ("fatal error: v8.h: No such file or directory"). semPlot built its source deps (qgraph etc.).
- About 21:19 the sandbox was recycled: `Rscript: command not found`. Ran REPO/scripts/setup_env.sh (R 4.5.0 back). The semPlot install had been killed mid-way; removed its 00LOCK, reinstalled semPlot: OK in 0.2 min.
- 21:22 tried `sudo apt-get install libnode-dev` (V8's alternative system lib): failed, unresolvable dependencies (outputs/apt_libnode_attempt.log). `libv8-dev` has no apt candidate. Decision: PREREG env fix 3 for `library(gt)` only (gt is never called). semPlot and xtable left as written.

## 21:15-21:22 Environment fixes (diffs/, see diffs/README.md)
- Fix 1 line 9 data path. Fix 2: confirmed lines 19-20 error on the public extract (outputs/envfix2_error_before_fix.txt), commented out lines 17, 19, 20, 22. Fix 3 library(gt).

## 21:23 Primary run (as deposited, Q15 code 8 kept)
- `Rscript scripts/run_and_extract.R scripts/patched_primary.R outputs structural`, whole script top to bottom, console in outputs/full_script_output.txt. Ran without error in about 10 s; lavaan 0.6-19 and semTools 0.5-6 loaded from the fresh library (first lines of the output file).
- Only warning: controls model "205 cases were deleted due to missing values in exogenous variable(s)".
- est.std (3 dp) T1 -0.202, T2 0.354, T3 0.718, T4 -0.145, T5 0.208: all equal to the paper. Unstandardized z-test p values 0.0055, 0.0054, <.001, 0.0279, 0.0200 equal the paper's p values (.006, .005, .000, .028, .020); the standardizedSolution p values do not (e.g. T2 0.002).
- lavaan nobs = 1203 (paper 1,139). Structural fit chi2.scaled 519.886 df 141, robust CFI 0.909, robust TLI 0.890, SRMR 0.058, robust RMSEA 0.062 (paper 516.954 / .911 / .892 / .058 / .062).
- Controls model: chi2.scaled 779.793, df 201, n 998, equal to the paper.

## 21:24 DIAGNOSTIC run (authors' line 188 re-enabled, nothing else changed)
- Structural fit now equals the paper exactly (chi2.scaled 516.954, CFI .911, TLI .892); nobs still 1203; coefficients move away from the paper (T1 -0.203, T2 0.363, T3 0.761, T4 -0.155, T5 0.208); controls chi2 794.407 (paper 779.793). Side by side: outputs/primary_vs_diagnostic.csv (scripts/compare_primary_diag.py).
- Reading: the paper's coefficients and controls model correspond to code 8 kept; its structural fit statistics correspond to code 8 as missing; its n = 1,139 equals the count of Q15 != 8. Not resolved.

## 21:25 Robustness
- scripts/prep_for_checks.R saves the primary-run prepared data and model syntax.
- 21:26 R_a started in background (scripts/run_boot_chunks.sh calling scripts/R_a_bootstrap.R with 500 s budgets, single-threaded, appending to outputs/R_a_boot.csv). About 2-3 s per fit on the shared machine.
- R_b (scripts/R_b_R_c.R): 17 rows had |z| > 3 (max 3.733), refit on 1186 rows: b1 est.std -0.205, p 0.010 (unstd). Indirect -0.146.
- R_c unweighted: b1 est.std -0.118, p 0.041 (unstd); indirect -0.064, p 0.070 (not significant).

## Code review (whole script read, 409 lines; active code lines 1-22, 47-49, 122-123, 134-137, 177-180, 201-409)
- Q15 code 8 used as a numeric value (commented-out recode at line 188); see results.json bugs. Meaning of code 8: searched for a public codebook (web search; OSF parent project 64ezg files: README_covid_rural_us.docx and covid_data_cleaning.do are for the 2020 wave, where Q15 is a housing question). Not determinable.
- n mismatch: described in uncertainties, not a code bug.
- Controls-model dummies code non-substantive codes as 0 (comment lines 118-119 states this); observation only.
- No other problems found in the model syntax or the rel() helper that affect the targets.

## 21:46 R_a finished
- 1000 replicates in 3 chunks (driver log copied to outputs/R_a_driver.log). Summary by scripts/R_a_summary.py -> outputs/R_a_summary.json.
- b1 est.std bootstrap median -0.198, percentile 95% CI [-0.358, -0.066], 99.8% of replicates below 0, 0 failed replicates. Indirect effect median -0.140, CI [-0.305, -0.043]. Same direction and significance as the paper.

## 21:48 Classification and results.json
- results.json built by scripts/build_results.py from outputs/ and ../targets.json.
- Proposed class A (all five targets equal the paper to 3 decimals), confidence medium. Caveat recorded in class_reason: the Dataverse deposit is code only; the data come from the authors' unlinked OSF component, so on the deposit alone the materials are incomplete (PROTOCOL section 7, C). Left for the batch decision rather than silently choosing.
- Times: start 21:10 IST, end 21:50 IST.
TIME_MINUTES: 40
