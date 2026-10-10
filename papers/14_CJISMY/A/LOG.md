<!-- status-note:start -->
> **Status note added 2026-10-10, after this run; not part of the agent's record.** This file keeps the agent's run-time wording, which may call an item a "bug". Under CHANGELOG_METHOD.md #4d, the status in `batches/batch3_code_observations.csv` applies. For 14_CJISMY: out of scope: not reproducibility: 14-2; unverified agent observation: 14-1. Only "verified finding" items are findings; "unverified agent observation" items are unverified and are not claims about the paper. Nothing here says the paper is wrong.
<!-- status-note:end -->

# LOG: 14_CJISMY, agent A

All times IST (UTC+05:30).

- 2026-10-10 21:20 Start. Read batch3_run_brief.md, AGENT_RUNBOOK.md, PROTOCOL.md, PREREG.md, targets.json, DATA_STATEMENT.md, batch3_class_decisions.md. Free RAM about 2-3 GB. Rscript present (/usr/bin/Rscript).
- 2026-10-10 21:20 Downloaded funs_and_constants.R (10360800), 01_make_directories.R (10360785), crosssection_linear.R (10360798), readme.txt (10360788) into scratch orig/, and the original CSVs (`?format=original`, `curl -L`) of epro_data_h1/h2 and epro_geo_data_h3 into RUNDIR/data/. Sizes 1,839,633 / 25,185,448 / 82,037,766 bytes as expected; h1 sha256 equals the PREREG value; MD5 of the three .R files and readme equal the Dataverse MD5s. sha256 in checksums.sha256.
- 2026-10-10 21:21 Started background source install into clean R_LIBS_USER (Ncpus=1): dreamerr 1.2.3, fixest 0.11.1, texreg 1.38.6 via remotes::install_version. All built (outputs/install_logs/install1.log). No r-cran-fixest/texreg/specr apt candidates were available.
- 2026-10-10 21:25 Installed vctrs 0.5.1 and dplyr 1.0.9 (both built; install2.log).
- 2026-10-10 21:27 Run 1 (only library(specr) commented out). Failed: "package or namespace load failed for 'broom.mixed' ... namespace 'vctrs' 0.5.1 is already loaded, but >= 0.6.3 is required".
- 2026-10-10 21:27 Run 2 (broom.mixed also commented out). Failed: "package or namespace load failed for 'patchwork' ... namespace 'vctrs' 0.5.1 is already loaded, but >= 0.6.0 is required". Second failure from the vctrs pin, so the pin was dropped (vctrs moved to rlib_unused; system vctrs 0.6.5) and the broom.mixed edit reverted.
- 2026-10-10 21:28 Run 3 (specr only). Failed: "package or namespace load failed for 'broom.mixed' ... namespace 'dplyr' 1.0.9 is already loaded, but >= 1.0.10 is required". library(broom.mixed) commented out (allowed by PREREG step 4; no broom.mixed call in the script), dplyr 1.0.9 pin kept.
- 2026-10-10 21:28 Run 4: `Rscript -e 'source("crosssection_linear.R", echo=TRUE, ...); save(...)'` exit 0, no errors or warnings in the log. Produced tables/h1,h2,h3 .tex and both plot PDFs (marginaleffects 0.25.0 worked, so no plot edit). h1 table matches printed Table 1 (coefficients, SEs, stars, N 138, 62 countries, R2 0.70/0.72, adj. R2 0.39).
- 2026-10-10 21:29 scripts/extract_targets.R: T1 0.506545, T2 0.190686, T3 -0.475310, T4 -0.499608, T5 138. Factor levels in order Both|None|Single, so reference = Both as in the paper; no relevelled refit needed (targets_releveled.csv not produced, by design).
- 2026-10-10 21:30 scripts/robustness.R as pre-registered (seed 20261010, 1000 draws, 0 failed). R_a CI excludes 0; R_b 16 cases dropped (20 non-finite Cook's kept, |z|>3 would drop 0), estimate stays positive and p<0.001; R_c (no FE) positive but p 0.143.
- 2026-10-10 21:31 Exploratory, not pre-registered: scripts/figure2_check.R on the Figure 2 left-panel model (prose on p. 824 says 0.2 point change).
- 2026-10-10 21:32 Code review of crosssection_linear.R (all 221 lines), funs_and_constants.R, 01_make_directories.R. No bug affecting Table 1. Unverified observations recorded in results.json. Current CRAN fixest not run (optional per PREREG; 0.11.1 built).
- 2026-10-10 21:31 Wrote environment.txt, diffs/README.md, checksums.sha256; built results.json with scripts/build_results.py.
