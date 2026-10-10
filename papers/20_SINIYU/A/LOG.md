<!-- status-note:start -->
> **Status note added 2026-10-11, after this run; not part of the agent's record.** This file keeps the agent's run-time wording, which may call an item a "bug". Under CHANGELOG_METHOD.md #4d, the status in `batches/batch4_code_observations.csv` applies. For 20_SINIYU: unverified agent observation: 20-1, 20-2. Only "verified finding" items are findings; "unverified agent observation" items are unverified and are not claims about the paper. Nothing here says the paper is wrong.
<!-- status-note:end -->

# LOG 20_SINIYU agent A

Paper: Wu et al. (2025) QJRMS 151(770) e4964, doi 10.1002/qj.4964. Dataset doi:10.7910/DVN/SINIYU (v1).
Scratch: /workspace/audit_runs/20_SINIYU/A/. Saved: REPO/papers/20_SINIYU/A/. All times IST (UTC+05:30).
Agent B folders were not opened.

## 2026-10-11

- 00:18 Start. Read batch4_run_brief.md, AGENT_RUNBOOK.md, PROTOCOL.md, PREREG.md, targets.json, DATA_STATEMENT.md, batch4_class_decisions.md, CHANGELOG_METHOD.md. Pre-registration frozen 2026-10-10 18:46:56 UTC; PREREG.md and targets.json not edited.
- 00:18 Read the file list (ids, MD5) from the pre-registration metadata copy (`/workspace/audit_runs/20_SINIYU/prereg/dsmeta.json`). Did not reuse the prereg downloads: re-downloaded all 18 files fresh into `/workspace/audit_runs/20_SINIYU/A/data/` from `https://dataverse.harvard.edu/api/access/datafile/<id>` with `curl -A "repro-audit-2026"`; the two radiosonde files with `?format=original` (57328.csv, 57516.csv) as PREREG says.
- 00:19 to 00:21 All 18 downloads match the Dataverse MD5 values.
- 00:21 `unrar-free -x FY3G_PMR.part1.rar` (unrar-free 1:0.3.1-1): "Extracting FY3G_PMR.HDF4 OK / All OK" (`outputs/unrar_free.log`). sha256 of all 18 files plus FY3G_PMR.HDF4 in `checksums.sha256`; byte-identical (sorted) to `prereg_download_checksums.sha256`.
- 00:21 Extracted codes.tar.gz into `/workspace/audit_runs/20_SINIYU/A/run/` (14 scripts in figure1..figure13).
- 00:22 Scanned the deposit for the `interp_radar` module or any Fortran/f2py/compiled module, and for volume-matching code (`scripts/check_deposit_for_module.py` -> `outputs/deposit_module_search.json`). 56 files scanned (18 deposit files plus tar members). Module found: no. Fortran/f2py/.so files: none. Volume-matching keyword hits (vmm, warren, corrcoef, pearson, .corr(, volume match): none. Three import lines: 1DVAR.py line 21 (`interp_radar_shift`), figure6/O_B_Ku.py line 17 (`interp_radar_ppi`), figure8/mult_plot_without_green.py line 23 (`interp_radar_shift`).
- 00:22 The DATA_STATEMENT search (18 public searches, pre-registration) found the module in none of the locations the article names; I did not repeat those searches. The article's statement names only data pages (ERA5 CDS, NSMC FY-3G page) and the Dataverse deposit, so PREREG step 4 has no location left to compile from. No replacement was written (brief; class decision 5).
- 00:23 Fresh venv `/workspace/audit_runs/20_SINIYU/A/venv` (Python 3.12.15); `pip install numpy pandas xarray netCDF4 h5py scipy matplotlib SciencePlots` (current releases, no pins exist). pip freeze in `environment.txt`.
- 00:24 Path-only fixes as symlinks in `run/figure6/` (PREREG steps 1 to 3): `FY3G_PMR.HDF`, `gep00/postvar.nc`, `gep00/swath_spaceborn.nc` (diffs/README.md). The authors' O_B_Ku.py was not edited (sha256 in `outputs/O_B_Ku_sha256_as_run.txt`).
- 00:24 First run attempt failed before Python started: `/bin/bash: line 5: /usr/bin/time: No such file or directory` (exit 127). Installed Debian package `time` (1.9-0.2+b1) with `sudo apt-get install -y time` (first try hit another agent's dpkg lock; retried with `-o DPkg::Lock::Timeout=60`, OK). Environment step only.
- 00:26 Run: `cd run/figure6; /usr/bin/time -v python O_B_Ku.py > outputs/O_B_Ku.log 2>&1`. Exit 1. Verbatim:
  ```
  Traceback (most recent call last):
    File "/workspace/audit_runs/20_SINIYU/A/run/figure6/O_B_Ku.py", line 17, in <module>
      from interp_radar import interp_radar_ppi
  ModuleNotFoundError: No module named 'interp_radar'
  ```
  Max RSS 85 MB; no data was read (the import is before line 130). No `o_b_pvp.csv`, no figure. Not retried: the cause is a missing deposit file, not something an environment fix can change.
- 00:27 `scripts/extract_targets.py` -> `outputs/targets_extracted.csv`: T1 and T2 not produced (ModuleNotFoundError); T3 to T6 not produced (no deposited code computes Table 1).
- 00:27 Robustness R_a, R_b, R_c not run: each starts from the `data` vector that O_B_Ku.py never builds (PREREG section 3). The output-only `np.save` line and the memory fallback were therefore not applied.
- 00:28 Code review. Read all of figure6/O_B_Ku.py (519 lines) and the import headers of 1DVAR.py and figure8. Static check `scripts/code_observation_checks.py` -> `outputs/code_observation_checks.json`. Two unverified observations (effect on any paper number cannot be shown without the missing module):
  1. O_B_Ku.py lines 419 to 420: line 419 sets `radar_Z_out` to NaN where > 6000; line 420 then tests `radar_Z_out>6000.` to mask `obs_mesh_meso`, which is False for NaN, so line 420 masks nothing (toy-array check: 0 cells masked). Whether the 6000 m cut still acts depends on how the undeposited `interp_radar_ppi` treats NaN heights. Already flagged in PREREG.
  2. O_B_Ku.py lines 343 to 345: line 344 builds `B_value` with ZH < 0 set to 0, and line 345 overwrites `B_value` with raw `ZH/Rvar`, so the clip on line 344 has no effect. In the deposited swath file 7,489,094 of 7,887,000 ZH values are below 0. Lines 479 to 480 later drop interpolated background values below 18 dBZ, so any effect would come only through the interpolation, which cannot be run.
  No confirmed bug.
- 00:29 Proposed class C (materials incomplete: the only script that computes a target imports a module that is not deposited and not in any location the data statement names; no deposited code for Table 1). `scripts/build_results.py` -> `results.json`.
