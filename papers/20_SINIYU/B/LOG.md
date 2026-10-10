<!-- status-note:start -->
> **Status note added 2026-10-11, after this run; not part of the agent's record.** This file keeps the agent's run-time wording, which may call an item a "bug". Under CHANGELOG_METHOD.md #4d, the status in `batches/batch4_code_observations.csv` applies. For 20_SINIYU: unverified agent observation: 20-1, 20-2. Only "verified finding" items are findings; "unverified agent observation" items are unverified and are not claims about the paper. Nothing here says the paper is wrong.
<!-- status-note:end -->

# LOG: 20_SINIYU, agent B (blind)

All times IST (UTC+05:30).

- 2026-10-11 00:27 Start. Read batch4_run_brief.md, AGENT_RUNBOOK.md, PROTOCOL.md, PREREG.md, targets.json, DATA_STATEMENT.md, batch4_class_decisions.md, CHANGELOG_METHOD.md. Did not open REPO/papers/20_SINIYU/A/ or /workspace/audit_runs/20_SINIYU/A/ (a directory listing of papers/20_SINIYU/ showed that an `A` entry exists; it was not opened). Scratch dir /workspace/audit_runs/20_SINIYU/B. Machine shared; `free -g` at start showed 0 GB available.
- 2026-10-11 00:28 Re-downloaded all 18 deposit files from https://dataverse.harvard.edu/api/access/datafile/<id> (curl -A "repro-audit-2026", `?format=original` for 57328 and 57516). All 18 match the Dataverse MD5 values and the PREREG sha256 list (checksums.sha256). Took about 4 minutes.
- 2026-10-11 00:29 `tar xzf codes.tar.gz`: 14 scripts in figure1 to figure13 (11 .py, 3 .ncl). `unrar-free -x FY3G_PMR.part1.rar`: "Extracting FY3G_PMR.HDF4 OK / All OK" (28 s); sha256 b86dc63e... matches PREREG.
- 2026-10-11 00:30 grep of all deposited code: `interp_radar` appears only as `from interp_radar import interp_radar_ppi` (O_B_Ku.py line 17), its call (line 473) and signature comment (line 448), and `interp_radar_shift` imports/calls in 1DVAR.py (21, 518) and figure8 (23, 818, 1042). No grep hit for vmm, warren, corrcoef, pearson, .corr(, volume match in any script: no Table 1 code.
- 2026-10-11 00:30 Clean venv /workspace/audit_runs/20_SINIYU/B/venv. First `pip install` of numpy pandas xarray netCDF4 h5py scipy matplotlib SciencePlots hit the 120 s shell cap (pip upgrade in the same command); second call completed. Versions in environment.txt (numpy 2.5.3, xarray 2026.9.0, h5py 3.16.0, netCDF4 1.7.4, scipy 1.18.1, matplotlib 3.11.2, SciencePlots 2.2.2). No pins exist in the deposit.
- 2026-10-11 00:32 Built rundir with path-only symlinks (diffs/paths_symlinks.txt): FY3G_PMR.HDF -> extracted FY3G_PMR.HDF4; gep00/postvar.nc; gep00/swath_spaceborn.nc -> swath_spaceborn_mu3.nc. O_B_Ku.py copied unchanged (sha256 identical). `free -m`: 1612 MB available.
- 2026-10-11 00:32 Ran `/usr/bin/time -v ../venv/bin/python O_B_Ku.py` from rundir (outputs/O_B_Ku.log). Verbatim:
  ```
  Traceback (most recent call last):
    File "/workspace/audit_runs/20_SINIYU/B/rundir/O_B_Ku.py", line 17, in <module>
      from interp_radar import interp_radar_ppi
  ModuleNotFoundError: No module named 'interp_radar'
  ```
  Exit status 1, 9.6 s wall, max RSS 92 MB. Nothing else ran; no o_b_pvp.csv.
- 2026-10-11 00:33 scripts/deposit_module_search.py: every deposit file and every archive member (64 entries) searched by name for interp_radar / .f90 / .f / .so / .pyf, and every text member by content. No module source or binary. PyPI `interp_radar` and `interp-radar`: HTTP 404 (PyPI is not a location the article cites; checked for information only). Output outputs/deposit_module_search.json. The cited locations (Copernicus CDS ERA5 page, NSMC FY-3G dataset page) are data pages; their check is in DATA_STATEMENT.md and I did not repeat it. Per PREREG step 4 and batch4 decision 5, no replacement module was written; the run stops at line 17.
- 2026-10-11 00:33 scripts/check_inputs.py (metadata only): every HDF path, postvar.nc variable and swath variable that O_B_Ku.py reads exists at the symlinked paths with the expected shapes (outputs/input_check.json). So the missing module is the only material blocker found. Second issue found: with SciencePlots 2.2.2, line 20 `plt.style.use(['science','no-latex'])` raises OSError ("'science' is not a valid package style") unless `import scienceplots` runs first; it works after that import. Not reached in the run (line 17 fails first), so not changed.
- 2026-10-11 00:34 scripts/code_observation_demo.py: toy arrays showing (a) lines 419 to 420 (second mask tests NaN > 6000, masks 0 cells) and (b) lines 343 to 345 (clip of negative ZH to 0 is overwritten by line 345; same at 1DVAR.py 310 to 312). Output outputs/code_observation_demo.json. Effect on any paper number cannot be shown without the module, so both are unverified observations. 1DVAR.py has the 6000 m cap commented out (lines 473 to 474) while O_B_Ku.py keeps it.
- 2026-10-11 00:34 scripts/extract_targets.py: ob_data.npy and o_b_pvp.csv not produced, so T1 and T2 are null (outputs/targets_extracted.csv). T3 to T6: no deposited code, null. Robustness R_a, R_b, R_c not run: all need the `data` vector that only O_B_Ku.py builds (R_c also needs the script to run). Not attempted: 1DVAR.py (not planned in PREREG; needs the same missing module), figure scripts (not targets).
- 2026-10-11 00:36 scripts/build_results.py writes results.json from outputs/. Proposed class C. End.
