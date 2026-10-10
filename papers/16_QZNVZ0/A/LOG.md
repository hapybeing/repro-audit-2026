<!-- status-note:start -->
> **Status note added 2026-10-11, after this run; not part of the agent's record.** This file keeps the agent's run-time wording, which may call an item a "bug". Under CHANGELOG_METHOD.md #4d, the status in `batches/batch4_code_observations.csv` applies. For 16_QZNVZ0: unverified agent observation: 16-1, 16-2. Only "verified finding" items are findings; "unverified agent observation" items are unverified and are not claims about the paper. Nothing here says the paper is wrong.
<!-- status-note:end -->

# LOG: 16_QZNVZ0, agent A

All times UTC with IST in brackets (IST = UTC + 5:30).

## 2026-10-10 18:46 UTC (2026-10-11 00:16 IST) start
- Read batch4_run_brief.md, AGENT_RUNBOOK.md, PROTOCOL.md, PREREG.md, targets.json, DATA_STATEMENT.md, batch4_class_decisions.md. Did not read B/ or other papers' folders.

## 18:48 UTC (00:18 IST) download
- Re-downloaded all 6 deposit files (version 2.0) from Dataverse with `curl -A "repro-audit-2026"` into /workspace/audit_runs/16_QZNVZ0/A/data, plus `timelines.csv` via `?format=original` (datafile 10577539) and the ingested `timelines.tab`.
- sha256 of every file matches PREREG.md and data_statement_raw/prereg_download_checksums.sha256. Saved in checksums.sha256.

## 18:49 UTC (00:19 IST) environment
- `python3 -m venv /workspace/audit_runs/16_QZNVZ0/A/venv`; `pip install pandas numpy statsmodels nbconvert ipykernel`. The first command hit the 120 s foreground cap (nbconvert/ipykernel deps); re-ran `pip install --prefer-binary pandas numpy statsmodels`, which completed. Current releases installed: pandas 3.0.6, numpy 2.5.3, statsmodels 0.15.0, scipy 1.18.1 (full pip freeze in environment.txt). nbconvert was not completed, so the PREREG's second route (cells extracted verbatim into a script) is used.

## 18:51 UTC (00:21 IST) verbatim script
- `scripts/regression_verbatim_orig.py`: the 13 notebook code cells concatenated verbatim (cell markers added as comments only).
- `scripts/regression_verbatim.py`: the same plus an appended extraction block (writes outputs/regression_estimates.csv, outputs/regression_summaries.txt, Model 1 and Model 4 estimation row labels). Diff: diffs/regression_verbatim_extraction.diff. No author line changed.
- Run from the data directory (working directory fix: the CSV is read by bare filename).

## 18:52 to 19:03 UTC (00:22 to 00:33 IST) main run
- Attempt at 18:52 UTC killed by the system with exit 137 after about 75 s (machine available memory had fallen to about 200 MB because of other agents; our process RSS was about 350 to 500 MB). A second attempt with `timeout 100` was also cut (timeout plus another 137). No code change for memory (the PREREG usecols fallback applies only above about 3 GB peak, which was not the case).
- Re-ran detached through scratch wrapper `run_wrap.sh` that waits for at least 1,800 MB available and retries after exit 137. Run 19:02:08 to 19:03:24 UTC, exit 0, peak RSS 622 MB, 74.4 s. Log: outputs/run_regression.log. Only warning: pandas DtypeWarning for column 5 Journal_Rank (mixed types; not used in any model). `Top10_Inst`/`Top50_Inst` parsed as bool.
- Outputs: outputs/regression_estimates.csv (all 8 models: B, SE, t, p, nobs, adj R2), outputs/regression_summaries.txt (statsmodels summaries), outputs/model1_row_labels.csv, outputs/model4_row_labels.csv.
- Quick read: Model 1 N 68,558; FA_Female 0.0393; FA_Hispanic/Latino -0.0746; FA_South -0.0240; International 0.0875; Model 4 FA_African -0.0906 (exact values in the CSV; results.json is built from it by script).

## 19:04 to 19:07 UTC (00:34 to 00:37 IST) robustness R_b and R_c
- scripts/robustness.py (rb, rc, ra), run through the same wrapper, sequentially.
- R_b: 129 of 68,558 Model 1 rows dropped (|z| > 3; all on the upper side, z min -1.58). Output outputs/R_b_outlier_exclusion.csv.
- R_c: GLM Poisson HC1 converged with default settings (9 iterations). Output outputs/R_c_poisson.csv. Primary FA_Hispanic/Latino coefficient negative but p about 0.008, i.e. not p < .001 as pre-registered for "same significance".

## 19:07 UTC (00:37 IST) R_a started
- 1,000 case-bootstrap draws, default_rng(20261010), numpy lstsq on the resampled design; resumable draws file outputs/R_a_bootstrap_draws.csv. About 100 draws per 2 minutes on the shared machine.

## 19:11 UTC (00:41 IST) R_a done
- 1,000 draws finished 19:11:56 UTC, exit 0, 0 rank-deficient resamples, 0 of 1,000 FA_Hispanic/Latino draws >= 0. Outputs outputs/R_a_bootstrap_draws.csv and outputs/R_a_bootstrap_summary.csv.

## 19:13 UTC (00:43 IST) code checks
- scripts/code_checks.py (descriptive counts only) -> outputs/code_checks.json. FA_South is 0 for all 8,805 Top10 first-author rows, so its absence from the Model 3 regressor list matches a constant column (it would be collinear with Const). Model 2's lower N (39,690) follows from missing values in team variables (Team_Female, Team_Author_Reputation, Team_South, Team_Affliation_Weight) within the FA_Ethnicity row filter.
- Code review: read all 13 cells of Regression.ipynb. No real bug found. Visualizations.ipynb not run (not needed for targets, per PREREG).

## 19:14 UTC (00:44 IST) results
- scripts/build_results.py reads outputs/ and writes results.json.
