<!-- status-note:start -->
> **Status note added 2026-10-10, after this run; not part of the agent's record.** This file keeps the agent's run-time wording, which may call an item a "bug". Under CHANGELOG_METHOD.md #4d, the status in `batches/batch3_code_observations.csv` applies. For 11_DDOFPS: unverified agent observation: 11-1, 11-2. Only "verified finding" items are findings; "unverified agent observation" items are unverified and are not claims about the paper. Nothing here says the paper is wrong.
<!-- status-note:end -->

# LOG 11_DDOFPS, agent A (2026-10-10, IST)

Scratch: /workspace/audit_runs/11_DDOFPS/A (raw/, run_v1/, run_v2/, rlib/). Saved results: this folder.

- 21:20 Read batch3_run_brief.md, AGENT_RUNBOOK.md, PROTOCOL.md, PREREG.md, targets.json, DATA_STATEMENT.md, batch3_class_decisions.md. Did not open B/ or any other paper's folder.
- 21:20 Downloaded all 9 files from https://dataverse.harvard.edu/api/access/datafile/<id> (User-Agent repro-audit-2026), renamed by datafile id to the Dataverse names. All 9 sha256 equal the PREREG table (checksums.sha256).
- 21:20 Read the full script (270 lines, Latin-1, CRLF). Line 177 byte check with `od -c`: `"\264 4 5"`, i.e. 0xB4 before 45, as PREREG says.
- 21:20 R check: Rscript present (R 4.5.0). Missing: pacman, janitor, hrbrthemes, paletteer, directlabels. Not in Debian apt. Installed from CRAN into the per-run library with Ncpus=1 (this also pulled CRAN ggplot2 4.0.3 into rlib, which masks system ggplot2 3.5.1).
- 21:23 Run 1 of the authors' script (v1 mapping), via scripts/run_authors.R (source with encoding = "latin1"): stopped at line 53: `Error in theme_ipsum_tw() : could not find function "theme_ipsum_tw"`. hrbrthemes 0.9.3 does not export it.
- 21:24 Tried hrbrthemes 0.8.7 (CRAN Archive): `remotes::install_version` failed with a lib path error ("not writable", lib string concatenated); installed by `R CMD INSTALL` after installing extrafont. 0.8.7 also lacks theme_ipsum_tw. Checked the 0.8.0 NAMESPACE: it exports theme_ipsum_tw. Installed hrbrthemes 0.8.0. Package-version environment fix.
- 21:25 Run 2: stopped while drawing Figura 1: `Error in grid.Call.graphics(C_text, ...) : invalid font type` (pdf device, Titillium Web not installed). Switched my wrapper's device to cairo PNG (diffs/run_authors_graphics_device.diff). Cosmetic only, no author code changed.
- 21:25 Run 3 (v1): SCRIPT_COMPLETED_OK. Run v2 mapping: SCRIPT_COMPLETED_OK. 21 plots each.
- 21:26 scripts/extract_targets.R on both sessions -> outputs/targets_extracted_v1.csv and _v2.csv. The two files are identical (diff shows no difference). Note: the saved session contains the wrapper's `args`, so scripts that load the session must read their own arguments before `load()`; party_share_check.R first failed on this ("cannot open file 'NA/party_share_check.csv'") and was fixed.
- 21:27 Re-ran both with a warnings summary. 50 warnings: one ggplot2 deprecation from hrbrthemes, one element_blank label warning, and readxl "Expecting logical in DL.../R...C116". scripts/check_import_coercion.R (outputs/import_coercion_check_v1.csv, _v2.csv): readxl's type guess turns every value of `sequencial_tse` (6959 values) and `raca_tse` (2800 values) into NA. Neither column is used by the script. Target columns ano, numpartido, APE3, APE4 lose nothing.
- 21:27 scripts/robustness.R (R_a, R_b, R_c as pre-registered, plus one EXPLORATORY party-45 check) -> outputs/robustness.json, outputs/R_a_bootstrap_draws.csv.
- 21:28 scripts/party_share_check.R -> outputs/party_share_check.csv (evidence for the line 177 code observation). scripts/fig7_recode_check.R -> outputs/fig7_recode_check.csv (all resultado values recoded; no unmatched category).
- 21:29 environment.txt written. diffs/README.md written. scripts/build_results.py builds results.json.

## Results in brief (values are in the output files; results.json is built from them)
- All six targets match the paper at its printed rounding with the primary v1 mapping, and the v2 mapping gives identical extracted values.
- T2 and T3: ggpubr::stat_cor reports r already rounded to 2 decimals; the unrounded cor.test cross-check rounds to the same values.
- Secondary (not targets): `test$expected["2018","Sim"]` is 16.87; note 9 of the paper prints 16 (rounding to 0 decimals would give 17). Labelled context only.
- Robustness: R_a, R_b, R_c each keep r(2018) positive and significant. Secondary quantity r(2018) - r(2002): positive under R_a, near zero under R_b, negative under R_c (Spearman), see robustness.json.

## Code review
Read all 270 lines. No change of any target value was traced to a coding error.
- Code observation (line 177): the filter entry "´45" (0xB4 before 45) matches no row (0 rows), so the 711 programs of party 45 are not in Figura 5's table. Mechanically verified by run (outputs/party_share_check.csv, outputs/targets_extracted_v1.csv key party45_rows_in_full_data). The paper's Figura 5 legend also lists seven parties without 45, so the printed numbers match the code as deposited. The deposited filter covers 49.0% of programs; the text says the selected parties together exceed 50% (56.6% with 45). Whether 45 was meant to be in the table cannot be confirmed by a run: unverified observation on intent. EXPLORATORY (not pre-registered) rerun with "45": expected PT count 557.8 instead of 524.2; observed 602 still above expected (outputs/robustness.json, exploratory_party45).
- Not a bug for the results: readxl type guessing empties two unused columns (see 21:27).
