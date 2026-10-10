<!-- status-note:start -->
> **Status note added 2026-10-10, after this run; not part of the agent's record.** This file keeps the agent's run-time wording, which may call an item a "bug". Under CHANGELOG_METHOD.md #4d, the status in `batches/batch3_code_observations.csv` applies. For 12_CYBR7L: unverified agent observation: 12-1, 12-2, 12-3. Only "verified finding" items are findings; "unverified agent observation" items are unverified and are not claims about the paper. Nothing here says the paper is wrong.
<!-- status-note:end -->

# LOG: 12_CYBR7L, agent B

All times IST, 2026-10-10. Blind agent: did not open, list or read papers/12_CYBR7L/A/ or /workspace/audit_runs/12_CYBR7L/A/.

- 21:20 Read batch3_run_brief.md, AGENT_RUNBOOK.md, PROTOCOL.md, PREREG.md, targets.json, DATA_STATEMENT.md, META.md, batch3_class_decisions.md.
- 21:20 Downloaded the 4 deposit files to /workspace/audit_runs/12_CYBR7L/B/raw with curl -A "repro-audit-2026", no sign-in: README.txt (datafile 13436794), replication_code.ipynb (13436793), Data.csv (13378108?format=original), CitingCited.csv (13378106?format=original). All four sha256 equal the PREREG table (checksums.sha256).
- 21:21 Created venv (/workspace/audit_runs/12_CYBR7L/B/venv, Python 3.12.15). First combined pip install hit the 120 s foreground cap; reran in pieces. Installed numpy 2.4.1, pandas 3.0.0, scipy 1.17.0, matplotlib 3.10.8, networkx 2.8.8 (README versions, exact), then nbconvert 7.17.1, nbclient 0.11.0, ipykernel 7.4.0. Python 3.14.2 (README) not available; 3.12 recorded as a deviation.
- 21:25 While checking whether pip was still running, `ps aux | grep "pip install"` printed an agent A process command line (a pandas reinstall in A's venv). Noted for transparency; no A file was read. Stopped using ps.
- 21:26 Read all 10 notebook cells. Made run copy with two pickle-only cells (see diffs/README.md). Note: PREREG says "an added final cell"; I inserted the first pickle cell right after Table 1 because the Table 2 cell overwrites G_citation.
- 21:27 Started `MPLBACKEND=Agg jupyter nbconvert --to notebook --execute replication_code_audit.ipynb --output executed.ipynb --ExecutePreprocessor.timeout=-1` in /workspace/audit_runs/12_CYBR7L/B/run (detached with setsid nohup). Unseeded, as deposited.
- 21:30 Table 1 written. 21:33 Table 2 written; notebook finished, no error outputs (only nbformat MissingIDFieldWarning and an IPKernel TCP warning in nbconvert.log). Copied tables, PNGs, executed notebook to outputs/.
- 21:31 Ran scripts/robustness.py (R_a, R_b, R_c) on the pickled Table 1 networks: outputs/robustness.json, outputs/R_a_seeds.csv, console_robustness.log. Only FutureWarnings from networkx (adjacency_matrix).
- 21:34 Ran scripts/extract_targets.py: outputs/targets_extracted.csv, outputs/boundary_authority_scores.csv.
- 21:35 Code-review check scripts/location_coding_check.py: outputs/location_coding_check.json.
- 21:36 Wrote environment.txt (pip freeze), built results.json with scripts/build_results.py.

## Outcome
- T1 8.89 (paper 9), T2 4.44 (4), T3 27.27 (27), T4 78.53 (78.5), T5 55.36 (55.4), T6 903 (903). All match to rounding; all same-conclusion rules hold. Other Table 1 and Table 2 cells also equal the paper's printed values quoted in PREREG (2000 top share 16.67 vs 17; 2010 complete 23.04 vs 23; Table 2 1956-2010 64.29 and 40.74).
- R_a: primary seed and all 20 seeds give the same top-45 set as the main run (8.89% African, 4.44% Africa-based).
- R_b: 10 authors with |z|>3 dropped (none African or Africa-based); African share in new top 45 is 13.33% vs 17.36% complete set; direction kept.
- R_c: weighted in-degree, cutoff 15, 46 authors with ties: 8.70% African vs 17.17%; strict first 45: 6.67%. Direction kept.
- Boundary: no ties at rank 45 (2021) or rank 22 (2010).
- Code review: none found (all cells read). Observation: complete-set share uses first-row raw location vs mode-based for top set; 117 vs 120 Africa-based in 2021, both 13% rounded.
- Proposed class A, confidence medium.
- Wall time about 25 minutes (21:20 to about 21:45).
