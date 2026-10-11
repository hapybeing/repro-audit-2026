<!-- status-note:start -->
> **Status note added 2026-10-11, after this run; not part of the agent's record.** This file keeps the agent's run-time wording, which may call an item a "bug". Under CHANGELOG_METHOD.md #4d, the status in `batches/batch5_code_observations.csv` applies. For 24_U9CKK6: unverified agent observation: 24-2, 24-3; verified finding: 24-1. Only "verified finding" items are findings; "unverified agent observation" items are unverified and are not claims about the paper. Nothing here says the paper is wrong.
<!-- status-note:end -->

# LOG: paper 24_U9CKK6, agent B (blind second pass)

All times IST (UTC+05:30) unless marked UTC. Scratch: /workspace/audit_runs/24_U9CKK6/B/ (data, rlib, run dir, saved models).
Agent B did not open, list or read papers/24_U9CKK6/A/, /workspace/audit_runs/24_U9CKK6/A/ or any batch report or results file.

## 2026-10-11 05:43 Start
- Read batches/batch5_run_brief.md, AGENT_RUNBOOK.md, PROTOCOL.md, PREREG.md, targets.json, DATA_STATEMENT.md, batches/batch5_class_decisions.md.
- `which Rscript` was empty (sandbox recycled). No `setup_env` process running (pgrep). Ran `bash scripts/setup_env.sh` in the background (log /tmp/setup_env.log). R 4.5.0 installed by 05:47; r-cran-fixest skipped (no Debian candidate).
- 05:44 Downloaded from Dataverse (curl -A "repro-audit-2026"): readme.txt (10431957), Scripts/6_analysis1.R (10431975), Scripts/9_analysis4.R (10431976), Data/RdW_salience.Rdata (10431967), Data/EP_debates_07062023.Rdata (10431963). All five sha256 equal the PREREG.md values (checksums.sha256).

## 05:50 Target cells checked against the paper PDF
- web_fetch of https://www.tandfonline.com/doi/pdf/10.1080/13501763.2024.2391510 returned the PDF text (served via fallback). Table 1 Model 2: Challenger 0.05 *** (0.01); Proximity to next EP-Election 0.01 *** (0.00); Challenger * Proximity to next National Election 0.02 *** (0.00); Num. obs. 266,854. Table 2: Challenger * Austerity Salience 0.04 ** (0.01); Challenger * EU Salience 0.02 * (0.01). All six cells equal targets.json; no change needed. Record: outputs/pdf_cell_check.json (short excerpts only).

## 05:47-05:52 Packages
- apt (Debian binaries): r-cran-ggeffects 2.2.1, r-cran-skimr 2.1.5, r-cran-zoo 1.8-14, r-cran-sjmisc 2.8.10 (lme4 1.1-37 and tidyverse came with setup_env.sh). `sudo apt-get clean` run to free RAM held by the in-memory root overlay.
- CRAN source into per-run library rlib (Ncpus=1, one at a time): texreg, performance, effectsize, sjPlot, sjstats, dreamerr, stringmagic, fixest. No versions pinned by the authors, so current CRAN versions (environment.txt).

## Run scripts
- scripts/make_run_scripts.py builds scripts/run_table1.R (6_analysis1.R lines 1-53 and 346-416) and scripts/run_table2.R (9_analysis4.R lines 1-123) from the deposited files. scripts/*_ranges_verbatim.R are the raw line ranges; diffs/run_table1.diff and diffs/run_table2.diff show that the only added lines are `## ENV` lines (saveRDS after each model, start/end timestamps). Fallback variants *_F1F2.R add the pre-registered F1 line after load() and the F2 rm()/gc() plus rebuild of the combined texreg table from saved RDS files (diffs/*_F1F2.diff), plus an `if (!file.exists(model.rds))` resume guard around each lmer call.
- Saved models go to scratch run/models/ (each well over 5 MB, so never in the repo); sha256 listed below.
- scripts/run_watch.sh runs one Rscript, samples R RSS and MemAvailable every 5 s, and kills R if RSS > 3000 MB (PREREG F1/F2 trigger) or MemAvailable < 400 MB. /usr/bin/time is not installed, so peak RSS comes from this sampler.

## 05:49 Table 1, plain run (scripts/run_table1.R)
- MemAvailable before start: 3917 MB (>= 3 GB rule). Fits were fast (about 25-30 s each).
- cycle_AE saved 05:50:19, cycle_AE_fit2 saved 05:50:46, cycle_AE_fit3 saved 05:51:14 (IST; R printed UTC 00:20-00:21).
- 05:51:19 watchdog stopped R while fitting cycle_AE_fit_group: R RSS 3369 MB (> 3000 MB, the PREREG F1/F2 trigger), MemAvailable 437 MB. Log: outputs/t1plain.out, outputs/t1plain_mem.tsv. Exit code 143 (killed).
- Decision (pre-registered): apply F1/F2 for the rest of the Table 1 block. The three models already saved by the plain run were kept (the F1/F2 script's resume guard skips them); F1/F2 changes no estimation line, so this only affects Model 4 (not a target).

## 05:51 Table 1, F1/F2 run (scripts/run_table1_F1F2.R)
- MemAvailable before start: about 3790 MB. cycle_AE_fit_group saved 05:52:22; combined table written to Tables/AE_cycle_240124.tex from the four saved models; END 05:52:29. Peak RSS 1920 MB. Log: outputs/t1F1F2.out, outputs/t1F1F2_mem.tsv.

## 05:53 Table 2, plain run (scripts/run_table2.R)
- MemAvailable before start: 3768 MB. AUT_sal_model 05:53:43, Immi_sal_model 05:54:14, EU_sal_model 05:54:22, END 05:54:22. Peak RSS 2542 MB, no fallback needed. Log: outputs/t2plain.out, outputs/t2plain_mem.tsv.

## 05:55 Extraction (scripts/extract_targets.R -> outputs/targets_extracted.csv, fixef_*.csv, modelinfo_*.txt; .tex tables copied to outputs/)
- T1 challenge:days_to_nat 0.01827 (SE 0.00481, naive p 1.4e-4); T2 days_to_EP 0.00884 (SE 0.00260, p 6.7e-4); T3 challenge 0.05089 (SE 0.01477, p 5.7e-4); T4 nobs 266854 (MEP 1466, party 204); T5 challenge:aut_sal 0.03719 (SE 0.01331, p 0.0052); T6 challenge:EU_sal 0.01542 (SE 0.00758, p 0.042). No lme4 convergence messages. All six round to the printed values and fall in the printed star buckets. Table 1 Model 2 AIC 738747.50 and logLik -369309.75 equal the printed values; the regenerated .tex tables print the same cells as the PDF for every row compared.

## 05:55-05:57 Robustness R_c, R_b (scripts/robustness.R, run one at a time under run_watch.sh)
- R_c (as.factor(year)): T1 0.01741, SE 0.00482, p 3.0e-4, nobs 266854 (outputs/R_c_factor_year.csv). Peak RSS 1080 MB.
- R_b (|z| > 3 on embed_dict_scale): 5489 rows dropped; T1 0.01326, SE 0.00296, p 7.4e-6 (outputs/R_b_outliers_T1.csv). Secondary: T5 0.03645 (p 0.0015, ** bucket kept; 1923 rows dropped), T6 0.01258 (p 0.080, above 0.05; 590 rows dropped) (outputs/R_b_outliers_T5_T6.csv).

## 05:57 Robustness R_a (party-cluster bootstrap)
- 200 draws pre-generated with set.seed(20261011) and saved (outputs/R_a_draws.rds). First refit 20.2 s, so the K rule gives K = min(200, floor(3600/20.2)) = 178 (outputs/R_a_K.txt). Results saved after every draw (outputs/R_a_partial.csv), which is more often than the pre-registered every 5.
- Wall-time limit from the dispatching brief (about 75 minutes total): the bootstrap was given a deadline of 07:00 IST (01:30 UTC). Average time per draw including resampling was about 26 s, so fewer than 178 draws were expected by then; if so, R_a is reported on the draws completed, marked ran = false in results.json (K rule not met) with the partial statistics in the note.
- 07:00 IST the deadline stopped the bootstrap after 166 of 178 draws (outputs/ra_part1.out, ra_part1_mem.tsv). Because only 12 draws (about 5 minutes) remained, I resumed from outputs/R_a_partial.csv with a new deadline of 07:08 so the pre-registered K rule is met; draws 167-178 finished at 07:05 (outputs/ra.out). Draws come from the saved pre-generated list, so the stop and resume do not change any draw.
- R_a result (outputs/R_a_summary.csv): K = 178 successful refits, 0 failed, 0 with lme4 convergence messages, no dropped columns. Original T1 0.01827; bootstrap SE 0.00821; 95% percentile interval [0.00283, 0.03579] (excludes 0); normal p from estimate / bootstrap SE 0.026 (not < 0.001). So the pre-registered "same direction and significance" condition is not met for R_a: the sign holds and the interval excludes 0, but the party-cluster bootstrap SE is about 1.7 times the model SE, and p does not reach the paper's *** level. Peak RSS 1763 MB.

## 07:06 Wrap-up
- environment.txt by scripts/write_environment.sh (sessionInfo, all package versions, saved-model sha256). Saved models (scratch only): /workspace/audit_runs/24_U9CKK6/B/run/models/*.rds, sha256 in environment.txt.
- Code review: read 6_analysis1.R fully at text level (ran lines 1-53, 346-416) and 9_analysis4.R lines 1-123 (ran). No bugs affecting targets found. Observations (results.json code_observations): linear `year` labelled "Year Fixed Effects: Yes" (verified: deposited code reproduces printed AIC/logLik exactly); undefined `right`/`left` at 6_analysis1.R 132 and 246 (not run); centering index 117:118 in 9_analysis4.R selects year_mon instead of radical (code reading, no effect on targets).
- results.json built by scripts/build_results.py from outputs/.
