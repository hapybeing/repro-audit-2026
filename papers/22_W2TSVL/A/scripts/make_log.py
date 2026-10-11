"""Writes LOG.md for 22_W2TSVL agent A. Step times are the IST times recorded during the run; the closing time is taken now."""
import json, os, datetime, csv
A = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); OUT = os.path.join(A, "outputs")
now = (datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)).strftime("%Y-%m-%d %H:%M")
ext = list(csv.DictReader(open(os.path.join(OUT, "targets_extracted.csv"))))
rob = json.load(open(os.path.join(OUT, "robustness.json")))
tl = "\n".join(f"  - {r['id']} ({r['model']} {r['term']}): {float(r['value']):.6g}" + (f", SE {float(r['se']):.4f}, Wald p {float(r['p_wald']):.4g}" if r['se'] not in ('', 'NA') else "") for r in ext)
log = f"""# LOG: 22_W2TSVL, agent A

All times IST (UTC+05:30). Scratch: /workspace/audit_runs/22_W2TSVL/A/ (dl/, orig/, run/, rlib/).

- 2026-10-11 02:35 IST. Read batch5_run_brief.md, AGENT_RUNBOOK.md, PROTOCOL.md, PREREG.md, targets.json, DATA_STATEMENT.md, batch5_class_decisions.md. Rscript present (R 4.5.0). MemAvailable about 2.6 GB. Did not read B/ or any other paper's folders.
- 2026-10-11 02:35 IST. Downloaded the 4 code/doc files and `OA23 Base UT-TEC.dta` (`?format=original`, curl -L, UA repro-audit-2026) plus the publisher supplement PDF into dl/. All sha256 equal the PREREG values (checksums.sha256).
- 2026-10-11 02:36 IST. stargazer and tableone not installed; no Debian r-cran-stargazer / r-cran-tableone package in trixie. Installed stargazer, gmodels, tableone from CRAN source into rlib with Ncpus=1 (one R process, MemAvailable about 2.6 GB). All other packages from the system library.
- 2026-10-11 02:36 IST. Environment fixes (diffs/): line 14 absolute path to relative in both scripts; install.packages() lines commented out (appendix 4-6, 138, 282; main 4-8). browseURL no-op in wrapper scripts/run_appendix.R. Note: the batch brief says "path line 15"; the absolute-path read_dta is on line 14 of both scripts (main line 15 is the commented alternative); line 14 was edited as PREREG.md describes.
- 2026-10-11 02:37 IST. Ran `Rscript scripts/run_appendix.R` in run/ (the authors' Appendix A1.R via source(echo=TRUE)). Exit 0. Stdout in outputs/appendix_stdout.txt. Warnings only: 4 x "non-integer #successes in a binomial glm!" (weighted polr start values, m2/m5/m8/m11) and 5 x dplyr "argument is not numeric or logical: returning NA" from the Table A4 means of the ordered factor `unions` (line 224). Copied table_1A_new.htm, table_A2_new.htm, table_A3_new.htm, models_appendix.rds to outputs/.
- 2026-10-11 02:37 IST. scripts/extract_targets.R wrote outputs/targets_extracted.csv (first run failed with "object 'dta' not found" inside drop1 for the secondary LR p; fixed by loading the prepared data in my script, no change to the authors' code). Values:
{tl}
- 2026-10-11 02:38 IST. Ran the authors' main script via scripts/run_main.R (polr traced to capture fits). Exit 0, no errors, 4 figure pages drawn (outputs/main_script_figures.pdf). scripts/crosscheck_main.R: the four figure models equal m1, m4, m7, m10 (outputs/crosscheck_main_vs_appendix.csv, max abs diff below 1e-14).
- 2026-10-11 02:38 IST. Robustness (scripts/robustness.R, MemAvailable about 1.65 GB, one R process): R_a 1000+1000 bootstrap refits in {rob['R_a']['seconds']:.0f} s, draws saved every 100; R_b dropped {rob['R_b']['rows_dropped_total']} rows with |z(age)| > 3; R_c OLS with HC2. Results in outputs/robustness.json. T1 criterion met in all three checks; secondary T2 criterion met in R_b only (R_a 99% CI lower bound {rob['R_a']['T2']['ci99'][0]:.4f}; R_c p {rob['R_c']['T2']['p']:.4g}).
- 2026-10-11 02:40 IST. scripts/check_supplement_cells.py re-read the six target cells from the publisher supplement PDF: all agree with targets.json (outputs/supplement_target_check.json).
- 2026-10-11 02:41 IST. Code review of both scripts in full; data facts in outputs/code_observations_check.json (education code 13 'No tiene estudios' set to NA, 17 rows; Table A4 means typed, consistent with the numeric means). No bug affecting the targets.
- 2026-10-11 02:41 IST. environment.txt written by scripts/make_environment.sh.
- {now} IST. LOG.md written by scripts/make_log.py, then results.json by scripts/build_results.py. Proposed class read from results.json.
"""
open(os.path.join(A, "LOG.md"), "w").write(log)
