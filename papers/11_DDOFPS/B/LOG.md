<!-- status-note:start -->
> **Status note added 2026-10-10, after this run; not part of the agent's record.** This file keeps the agent's run-time wording, which may call an item a "bug". Under CHANGELOG_METHOD.md #4d, the status in `batches/batch3_code_observations.csv` applies. For 11_DDOFPS: unverified agent observation: 11-1, 11-2. Only "verified finding" items are findings; "unverified agent observation" items are unverified and are not claims about the paper. Nothing here says the paper is wrong.
<!-- status-note:end -->

# LOG: 11_DDOFPS, Agent B (blind second pass)

All times IST (UTC+05:30), 2026-10-10. Agent B did not open, list or read papers/11_DDOFPS/A/, /workspace/audit_runs/11_DDOFPS/A/, any batch report, or any other paper's folder. (The sandbox tool printed names of files other agents changed after some commands; none of those files were opened.)

START: 2026-10-10 21:20

- 21:20 Read batch3_run_brief.md, AGENT_RUNBOOK.md, PROTOCOL.md, PREREG.md, targets.json, DATA_STATEMENT.md, META.md, batch3_class_decisions.md. The paper itself was not re-read; targets and page numbers taken from PREREG.md (SciELO blocks scripted downloads, as PREREG notes).
- 21:20 `Rscript` present (R 4.5.0), so setup_env.sh not needed. `free -g`: about 3 GB available.
- 21:20 Re-downloaded all 9 files from Harvard Dataverse (`/api/access/datafile/<id>?format=original`, User-Agent "repro-audit-2026") plus the dataset JSON into /workspace/audit_runs/11_DDOFPS/B/raw. All HTTP 200; every md5 matched Dataverse; every sha256 equals the value in PREREG.md (checksums.sha256).
- 21:21 Read the R script as text (270 lines, Latin-1, CRLF). Line 177 filter contains byte 0xB4 before "45", as PREREG says.
- 21:21 Package check: tidyverse, rio, patchwork, openxlsx, gplots, corrplot, vcd, ggpubr already in the system library. Missing: pacman, janitor, paletteer, directlabels, hrbrthemes. Installed from CRAN into per-run library rlib/ with Ncpus=1: pacman, janitor, paletteer (+prismatic), directlabels, hrbrthemes 0.9.3 (pulled ggplot2 4.0.3 and scales 1.4.0 into rlib). No apt installs.
- 21:22 Created run_v1 (programs file = bd_doxa_programas_HGPE.xlsx) and run_v2 (programs file = bd_doxa_programas_HGPE_v2.xlsx), copying deposited files under the names the script reads (pre-registered path fix; diffs/file_name_mapping_*.diff).
- 21:22 First run v1 via scripts/run_authors.R (source with encoding = "latin1", echo). Failed at line 53: `Error in theme_ipsum_tw() : could not find function "theme_ipsum_tw"`.
- 21:23 Attempt 2: `remotes::install_version("hrbrthemes", "0.8.7")` (plus extrafont, extrafontdb, Rttf2pt1). Still no `theme_ipsum_tw`. Stopped trying package versions (two attempts) and applied the PREREG-allowed fix: line 53 wrapped in tryCatch falling back to an empty `ggplot2::theme()` (Figura 1 only, no target). Byte-level edit, line 177 verified identical with cmp. diffs/analise_dos_dados_theme_ipsum_tw.diff.
- 21:24 Run v1 completed (exit 0, "RUN_COMPLETED"; only warnings: "There were 50 or more warnings", from plots). Console: outputs/console_authors_v1.log. Run v2 completed the same way: outputs/console_authors_v2.log. Plots: outputs/Rplots_v1.pdf, Rplots_v2.pdf.
- 21:25 scripts/extract_targets.R on both saved sessions -> outputs/targets_extracted_v1.csv and _v2.csv. The two CSVs are identical apart from the version label (checked with diff), so v1 and v2 give the same target values and the alternative class equals the main class.
  - T1 = 9439 (per year 1071, 1778, 1351, 1610, 2703, 926, same as the paper's text).
  - T2 stat_cor r(2002) = 0.45, p = 2.6e-17; cor.test cross-check r = 0.44754, identical p.
  - T3 stat_cor r(2018) = 0.72, p = 6.1e-138; cor.test r = 0.71516.
  - T4 = 40; expected 16.874; chisq = 113.98, df 5, p = 5.9e-23 (< 0.001, reading (1)).
  - T5 = 602; T6 expected = 524.249 (MDB: observed 417, expected 342.151).
  - Other years: r = 0.61 (2006), 0.61 (2010), 0.69 (2014), matching the secondary numbers in PREREG.
- 21:26 scripts/robustness.R -> outputs/robustness.json, R_a_bootstrap_draws.csv, console_robustness.log. Also one clearly labelled exploratory (not pre-registered) table with party 45 included.
- 21:27 Wrote environment.txt, diffs/README.md, scripts/build_results.py -> results.json.

## Observations
- Note 9 of the paper (per PREREG) gives the expected 2018 APE4 count as 16; the code gives 16.874, which rounds to 17. Secondary number, not a target; could be truncation in the text. Not judged.
- Line 177: the entry "´45" (0xB4 + "45") matches no row, while 711 rows of the programs file have numpartido 45, so party 45 is left out of Figura 5. The paper's Figura 5 legend (per PREREG) also omits 45, so the printed numbers correspond to the code as run. Whether leaving 45 out was intended cannot be confirmed from a run: recorded as an unverified observation, not a bug. Exploratory run with "45": PT observed 602 vs expected 557.76, so observed > expected still holds.
- R_b and R_c: r(2018) stays positive and significant, but the secondary claim that the correlation grows over time weakens (R_b: r(2018) - r(2002) = 0.037) or reverses (R_c Spearman: rho falls from 0.69 in 2002 to 0.50 in 2018).

END: 2026-10-10 21:28
