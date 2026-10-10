# PREREG: 20_SINIYU

Written 2026-10-11 about 00:15 IST (2026-10-10 about 18:45 UTC), before any analysis code was run. No analysis code by the authors was executed to write this file. I only downloaded the deposit, unpacked archives (codes.tar.gz listing and extraction, the FY3G_PMR rar volumes), and read file headers (HDF5 and netCDF variable names and shapes), code and column headers.

The main text was read in full, including Table 1 and the Data Availability Statement. Source: the HTML full text at https://doi.org/10.1002/qj.4964 (resolves to https://rmets.onlinelibrary.wiley.com/doi/10.1002/qj.4964), read with web_fetch on 2026-10-10 about 18:25 UTC. The HTML was not saved as a file, so it has no sha256. The PDF could not be saved: a browser attempt by an earlier agent failed, and a plain curl of the Wiley page returned only a Cloudflare challenge page (`/workspace/audit_runs/20_SINIYU/prereg/t.bin`, 5683 bytes, "Just a moment..."). The equations (1) to (9) do not render in the HTML text, but no target depends on them. Short excerpts of the target rows and the statement: `data_statement_raw/statement_excerpt.txt`.

- Paper: Wu, Z., Han, W., Xie, H., Ye, M. and Gu, J. (2025). "Assimilation of FY-3G Ku-band radar observations with 1D Bayesian retrieval and 3DVAR in CMA-MESO". Quarterly Journal of the Royal Meteorological Society, 151(770), e4964. DOI https://doi.org/10.1002/qj.4964 . Open access, CC BY 4.0. Version of record online 06 March 2025 (author-name correction 20 March 2025).
- Dataset: "Replication Data for: Assimilation of FY-3G Ku-band radar observations with 1D Bayesian retrieval and 3DVAR in CMA-MESO", Harvard Dataverse, https://doi.org/10.7910/DVN/SINIYU , version 1, released 2025-02-14 18:34 UTC, CC0 1.0, 18 files, none restricted. Metadata: https://dataverse.harvard.edu/api/datasets/:persistentId/?persistentId=doi:10.7910/DVN/SINIYU (saved as `/workspace/audit_runs/20_SINIYU/prereg/dsmeta.json`).
- No README, no requirements file, no environment file and no version pins in the deposit. No Python version is stated anywhere.
- An earlier pre-registration attempt crashed before writing anything. Its downloads in `/workspace/audit_runs/20_SINIYU/prereg/` were reused only after checking: 17 files matched the Dataverse MD5 values; `FY3G_PMR.part1.rar` was truncated (34,660,352 of 104,857,600 bytes, MD5 mismatch) and was re-downloaded. All 18 files now match the Dataverse MD5. sha256 below and in `prereg_download_checksums.sha256`.

## Dataset files (all downloaded 2026-10-10 from https://dataverse.harvard.edu/api/access/datafile/<id>, User-Agent "repro-audit-2026")

| datafile id | file | bytes | sha256 | what it is (from reading) |
|---|---|---|---|---|
| 10886577 | 1DVAR.py | 22081 | 14bbafb21f486328a3c001355d5b8d9b18cc5bf055439775f93e800e52a289c5 | 1D Bayesian retrieval script; writes `tmp.nc` |
| 10886580 | 1DVAR_output.nc | 26636408 | c3694d85f772386549f76c5dbef48bd1462ba0bb25824eebb01dbaab2ddef037 | variable `D1_out(bt=27, var=4, sn=144, we=214)`: same layout as the `tmp.nc` that 1DVAR.py writes |
| 10886576 | codes.tar.gz | 51664 | 043c095077fb42860d3c49e659fd6b7068690a853006a7052958cd6f61391cac | 14 plotting/analysis scripts in folders figure1 to figure13 (11 Python, 3 NCL) |
| 10886655 | postvar.nc | 196118587 | 0a26bcb62d175b6380f6bcdc9e5bedc620bf97dbfc0c916b2b7dc31b3d2d42d5 | CMA-MESO post-processed fields, 1 time, 27 pressure levels (1000 to 200 hPa), 301 x 601 grid (25 to 34 N, 96 to 114 E); variables u v w t Qv Qc Qr Qi Qs Qg ps |
| 10886665 | swath_spaceborn_mu3.nc | 378724932 | 08c8df8c845e00ec178a60b4f9dccdcaf528aa8d4df81571e0601d0df85a0f30 | ZJU-AERO simulated Ku swath, dims nscan 150, nray 220, nbin 239; ZH, heights, etc. |
| 10886811 | FY3G_PMR.part1.rar | 104857600 | f473e172ab8ac369558e387946209b6982c91de4e61e68ade80211ea2440e221 | RAR5 multi-volume archive, 7 volumes |
| 10886810 | FY3G_PMR.part2.rar | 104857600 | 529f9a9323d2095fc8b193263e6895c103f53720c06a9759bb865a4bba2359a5 | |
| 10886812 | FY3G_PMR.part3.rar | 104857600 | e45158f120cb0f7ffd9fc2496dff0eebc503f016604d22624fe4647d4c6edc11 | |
| 10886814 | FY3G_PMR.part4.rar | 104857600 | e18193475f791a844118b827a99c4126e502368a09a6f2359ef40401c53f82c1 | |
| 10886818 | FY3G_PMR.part5.rar | 104857600 | f95726c7ac331abad11e36df0f7a37a8c3fdfb73bb3b3f76747f4313b770743b | |
| 10886819 | FY3G_PMR.part6.rar | 104857600 | 90686c138ba80667583d9a7b8fec572ee01da2e6d9ca9ec1081c9c4ba0ed8cdb | |
| 10886820 | FY3G_PMR.part7.rar | 21052367 | ab550acc54ebc982282e1c0feb8371d731b327729e220005813da40ac1b4718b | |
| (extracted) | FY3G_PMR.HDF4 | 650468713 | b86dc63e4b55de72e577bd0f894facb649570e215c486aaac6ac6451ad24b32c | the single member of the rar set. Despite the name it is HDF5 (signature 89 48 44 46). Holds /PRE/Ku/zFactorMeasured (3884, 59, 500), /Geolocation/Ku/height, Latitude, Longitude, flagPrecip, binClutterFreeBottom, dayCount, msCount. /Geolocation/Ku/elevation is absent |
| 10886575 | Z9092.tar.gz | 8267304 | b0c72d3a3c066b2c64d4dac835645fcd94f373bfd8aeb4bb53f77af738d4fd1d | contains Z9092.bin (36,051,888 bytes), Yongchuan S-band radar volume |
| 10886574 | Z9230.tar.gz | 1359539 | 1d4ca157cd63f933a38e967497222a4814d65baa6116be7b6acc5d6e86167ad0 | contains Z9230.bin (9,718,272 bytes), Chongqing S-band radar volume |
| 10886573 | acc01h.tar.gz | 1879984 | b84b5308ffaa002718f30ce76379db1734422e3063544b682261a05f663b0b67 | hourly gauge observations for MET (obs.txt, obs_met.nc, ascii2nc.log per hour) |
| 10886583 | 2023072808.006 | 208113 | 053699c254d7b87a390602c8cca79465cc688cdf0993b2340b725e35d87f52f5 | 6-h gauge accumulation, 7850 station rows (read by the figure2 NCL script) |
| 10886582 | 57328.tab (original 57328.csv) | 390006 (tab 394073) | 34e4131e20764759eb56d289c9a571a31e78dd4a3d551407a6e9ac0a100546ad | radiosonde 57328 (downloaded in original format) |
| 10886581 | 57516.tab (original 57516.csv) | 446601 (tab 451211) | 0a863e563816a1fe6e29e28e50fbbb5f63b33933df0f1a52e3b76d113261ff47 | radiosonde 57516 (original format) |

Download note for agents: use `?format=original` for the two .tab files. Debian's `7z` (7zip 25.01+dfsg) cannot decompress this RAR5 set ("Unsupported Method"); `unrar-free -x FY3G_PMR.part1.rar` (Debian package unrar-free) extracted it with "All OK" (CRC checked).

## 1. Headline results and targets

The abstract makes three kinds of claims. (i) Data quality: volume matching shows FY-3G Ku-band (KR) reflectivity agrees with two ground S-band radars (GRs); numbers in Table 1 and Section 2.2 ("correlation coefficients were greater than 0.82, and the standard deviations were less than 3.8 dB"). (ii) Retrieval: 1D Bayesian retrieval gives reasonable relative humidity (RH) profiles compared with radiosondes (Figure 8, qualitative), and the O-B distributions are near Gaussian (Figure 6, Section 4.1: Ku O-B mean 1.23, 31,161 points; RH O-B mean 2.58%, 7463 points). (iii) Forecast impact: assimilating the RH pseudo-observations in CMA-MESO 3D-Var improves echo and rainfall forecasts for about six hours; CSI and FBIAS increase (Figures 9 to 13, no numbers printed in the text).

What the deposit can and cannot produce (from reading the code and file lists):
- Claim (iii), Figures 9 to 13, and the RH O-B in Figure 6b are out of scope. They need the CMA-MESO model and its 3D-Var system (not public, not deposited, would not run on a 7 GB aarch64 machine), and the scripts read files that are not deposited: KuRH and CTRL forecast series (`postvar*.nc` under `/public/home/zhwu/...`, only one postvar.nc is deposited), MET point-stat outputs for CSI/FBIAS (`/public/home/zhwu/MET/.../met_out/...`; acc01h.tar.gz holds only the gauge inputs), the 3D-Var innovation file `temp_inno202307280000_o_b_thin.dat` (needed for Figure 6b and Figure 7), ERA5 `era5_uv.nc`, ground radar mosaics `RADAMCR_*.nc`, the gauge file `2023072814.006`, and a province shapefile. These would be class E for compute and C for materials; they are not targets.
- Table 1 (claim (i)) has no code in the deposit. None of the 15 scripts implements the volume-matching method (grep for vmm, warren, corrcoef, pearson, .corr(, volume, match: no hit; the only np.std call is the Figure 6 histogram in O_B_Ku.py line 501). The inputs exist (Z9092.bin, Z9230.bin, FY3G_PMR.HDF4), but there is nothing to run. Table 1 is the paper's only table and backs the abstract's first claim, so its key rows are pre-registered as T3 to T6. The expected outcome is that they cannot be reproduced from the deposited code (reproduced_value null). Agents must not write their own volume-matching code to fill these targets (that would be a new analysis, not a reproduction).
- Figure 6a (Ku O-B) is the one paper number that a deposited script computes: `codes/figure6/O_B_Ku.py`, on deposited data (FY3G_PMR, postvar.nc, swath_spaceborn_mu3.nc). It is T1 and T2. But the script imports `interp_radar_ppi` from a module `interp_radar` (line 17), an f2py-wrapped Fortran subroutine whose signature is quoted in comments at lines 448 to 453. That module is not in the deposit (DATA_STATEMENT.md has the searches). 1DVAR.py and figure8 need `interp_radar_shift` from the same missing module.

So no target is expected to be reproducible from the materials as deposited. I pre-register these targets anyway, as the brief requires, so the class is decided by what actually runs.

Targets (copied exactly from the HTML full text):

| id | quantity | paper value | decimals | location | maps to |
|---|---|---|---|---|---|
| T1 | Mean Ku-band reflectivity O-B (dBZ) | 1.23 | 2 | Section 4.1, paragraph 1 ("with a mean value of 1.23"); Figure 6a | `mu=np.mean(data)`, O_B_Ku.py line 500; equivalently the mean of `o_b_pvp.csv` (line 494) |
| T2 | Number of Ku O-B data points | 31161 | 0 | Figure 6 caption, panel (a) ("31,161 data points") | `len(data)` in O_B_Ku.py, i.e. rows of `o_b_pvp.csv` |
| T3 | Table 1, Z9230, 2.4 deg: sample size | 573 | 0 | Table 1, Section 2.2 | no deposited code |
| T4 | Table 1, Z9230, 2.4 deg: correlation coefficient | 0.90 | 2 | Table 1, Section 2.2 | no deposited code |
| T5 | Table 1, Z9092, 2.4 deg: correlation coefficient (lowest in table) | 0.82 | 2 | Table 1, Section 2.2; text "greater than 0.82" | no deposited code |
| T6 | Table 1, Z9092, 3.4 deg: standard deviation (dB) (largest in table) | 3.76 | 2 | Table 1, Section 2.2; text "less than 3.8 dB" | no deposited code |

Statistic ambiguity for T1: the paper says "mean value of 1.23" without units. O_B_Ku.py sets `Rvarname=np.array([1.0,1.0,1.0,1.0])` (line 114; the 1.5 version on line 113 is commented out), so `data` is in dBZ and there is one candidate: the arithmetic mean `np.mean(data)` of the values written to `o_b_pvp.csv`. Note that `o_b_pvp.csv` is written with `fmt='%.3f'`; the pre-registered value is `np.mean(data)` on the unrounded array (agents print it to a file with full precision), and the mean of the rounded csv is reported as a secondary number only.

Conclusion criteria for same_conclusion:
- T1: same conclusion if the reproduced mean is positive (the paper's reading is "a slight positive bias relative to the background") and within 5% relative of 1.23.
- T2: same conclusion if the count is within 1% of 31161 (it decides nothing by itself; a large gap would mean a different sample).
- T3: within 5% of 573. T4 and T5: correlation above 0.80 and within 0.02 of the printed value. T6: below 3.8 dB and within 5%. Since no code exists for T3 to T6, same_conclusion is expected to be null.

Other numbers in the paper, context only (not targets): the remaining Table 1 rows; Figure 6b RH O-B mean 2.58% and 7463 points ("over 14% ... slightly above 0, while nearly 8% are slightly below 0"); Figure 2 caption "7399 rain gauges"; Section 2.2 attenuation and DFR values quoted from other papers; 1.5 dB observation error and 17% RH error (settings).

Inconsistencies noticed (described, not judged):
- Section 2.2 text says the correlation coefficients "were greater than 0.82"; the lowest value in Table 1 is 0.82 (Z9092, 2.4 deg).
- The Introduction's outline says Section 2 describes "the 27 July 2023 rainfall case"; the abstract and Section 2.1 date the event and the FY-3G overpass to 28 July 2023 (the event spans 27 to 28 July, Section 2.1).
- Section 3.3 says retrieval runs "only if the number of valid observations in the centre column was at least 10"; 1DVAR.py line 510 tests `np.count_nonzero(tmpsr > dbz_threshold/Rvarname[0]) > 10`, that is at least 11.
- Section 3.3 says RH pseudo-observations span 850 to 400 hPa in 25-hPa steps. postvar.nc levels are 25 hPa apart only down to 500 hPa, then 450 and 400 (50 hPa apart); 1DVAR.py writes all 27 levels (1000 to 200 hPa) and the level selection and thinning happen outside the deposited code.
- O_B_Ku.py lines 419 to 420: line 419 sets `radar_Z_out` to NaN where it exceeds 6000 m, then line 420 tests `radar_Z_out>6000.` again to mask `obs_mesh_meso`; after line 419 those cells are NaN, so line 420 masks nothing. Whether the 6000 m cut still acts depends on how the missing `interp_radar_ppi` treats NaN heights. The 6000 m cut is not described in the paper. (For the code review to assess; not a judgement here.)
- 1DVAR.py and O_B_Ku.py read `./gep00/postvar.nc` and `./gep00/swath_spaceborn.nc`; the deposit has `postvar.nc` and `swath_spaceborn_mu3.nc` at the top level. The figure7 script reads a file named `swath_spaceborn_mu3.nc` by full path, which supports the mapping below.
- The HDF member is named `FY3G_PMR.HDF4` but is HDF5; the scripts read `./FY3G_PMR.HDF` with h5py.
- The figure3/4/7 scripts read `/Geolocation/Ku/elevation`, which is not in the deposited HDF file (not used by any target).
- figure8 reads `./2023072800.000` as the 57516 sounding; the deposit has `57516.csv` (first data row is station 57516). Not used by any target.

## 2. Reproduction plan

Only one deposited script can produce a target: `codes/figure6/O_B_Ku.py` (T1, T2). There is no script order beyond that one script. No seed is used anywhere in it (it is deterministic).

Inputs and path-only fixes (each saved as a diff or a symlink listed in diffs/README.md):
1. Extract `FY3G_PMR.part1.rar` with `unrar-free -x` (or any RAR5-capable unrar) and expose the member as `RUNDIR/FY3G_PMR.HDF` (symlink or rename of `FY3G_PMR.HDF4`). Path-only. No alternative file.
2. `RUNDIR/gep00/postvar.nc` -> deposited `postvar.nc`. Path-only. No alternative file.
3. `RUNDIR/gep00/swath_spaceborn.nc` -> deposited `swath_spaceborn_mu3.nc`. Path-only. No alternative file exists in the deposit (mu3 matches the rain shape parameter 3 in Section 3.2).
4. `interp_radar` (f2py module with `interp_radar_ppi`): not deposited. Allowed: if the module source is found in the deposit or in a location the data statement names, compile it with `numpy.f2py` and gfortran (an environment step, logged). Not allowed: writing a replacement from the signature comment. If it is not found there, the run stops at the import on line 17. Record the error verbatim, set `reproduced_value` null for T1 and T2, and propose class C ("code imports a module that is not deposited"). If the module is found only in a location the article does not cite, run it there too and report that as the alternative class under CHANGELOG #4(a); it does not set the main class.
5. Environment: clean venv `python3 -m venv RUNDIR/venv`; install numpy, pandas, xarray, netCDF4, h5py, scipy, matplotlib, SciencePlots (needed by `plt.style.use(['science','no-latex'])`, line 20). No pins exist, so current releases are used; record `pip freeze`. If SciencePlots fails to install, the allowed fix is to drop the style line (cosmetic; diff). `pt2temp` uses `np.float` (removed in NumPy 1.24) but is never called; leave it.
6. Run from RUNDIR: `/usr/bin/time -v python O_B_Ku.py > outputs/O_B_Ku.log 2>&1`. Keep `o_b_pvp.csv` and `O-B_pvsp.png` in outputs/. A separate script `scripts/extract_targets.py` reads `o_b_pvp.csv` and, in a re-run that saves the unrounded `data` array (add one `np.save('outputs/ob_data.npy', data)` line after line 492, logged as an output-only diff), writes `outputs/targets_extracted.csv` with mean (full precision), count, SD, median. `scripts/build_results.py` builds results.json from that csv.
7. T3 to T6: no code. Record `reproduced_value` null, note "no deposited code computes Table 1", and say so in class_reason.

Peak memory (estimated from array shapes, not measured). The FY3G file is the only large input: each of `zFactorMeasured` and `height` is 3884 x 59 x 500 float32 = 458 MB. The script keeps both raw arrays, builds a Dataset on them, makes two `xr.where` copies of zFactorMeasured (one transient), `obs_all` and a copy `radar_Z_out_all = np.array(ds['height'])`. Estimate 2.3 to 3.2 GB if float32 is kept, up to about 5 GB if `xr.where` with `np.nan` promotes to float64. postvar.nc (4 variables of 27 x 301 x 601 float32, about 20 MB each) and the swath (about 32 MB per variable) are small. The 150 x 220 nearest-neighbour loop and one interpolation call take seconds to a few minutes.

Fallback (pre-registered, used only if the full run fails for memory or would exceed about 3 GB with the other agent running): read only scans 2750 to 2899 from the HDF file (`f[path][2750:2900]` for zFactorMeasured, height, Latitude, Longitude, flagPrecip, binClutterFreeBottom) and set `js_slice=0`, `je_slice=150`, keeping `iscan=2800-2750` as the literal 50. Every operation before line 390 is element-wise per scan, and lines 390 to 393 take exactly these scans, so `obs`, `radar_Z_out_PMR`, `lat_gpm`, `lon_gpm` and `bin_res2` are identical. The authors' estimation lines (O-B, thresholds, mean) are unchanged and there is no seed. `datestart`/`dateend` (from dayCount[0] and [-1]) change but are never used afterwards. Save it as a diff marked "memory fallback". If both runs are possible, check that `o_b_pvp.csv` is byte-identical.

Expected sources of difference (record, do not fix): if `interp_radar` is ever found, its exact version and compiler; scipy/xarray versions; the `fmt='%.3f'` rounding of the csv.

Not planned (labelled exploratory, would never change the class): re-running 1DVAR.py to compare with the deposited `1DVAR_output.nc`. It needs the same missing module, and its 7 x 7 shift stack (`model_Value_base1`, about 239 x 49 x 144 x 214 float32, about 1.4 GB, plus the same for heights and concatenation copies) would need about 4 to 6 GB, which is over the memory budget.

## 3. Robustness checks (pre-registered)

All three apply to T1 (Ku O-B mean) and can only run if O_B_Ku.py runs (main or alternative-location run). Each starts from the unrounded `data` vector the script builds (saved as `outputs/ob_data.npy` per step 6). There are no robustness checks for T3 to T6 because no code exists. The paper reports no test for the O-B mean, so "same direction and significance as the paper" = mean > 0 and its 95% interval excludes 0.

R_a. Bootstrap resample. `rng = np.random.default_rng(20261010)`; 2000 resamples of `data` with replacement (size n = len(data)); record the mean of each. Report the original mean as the estimate, the 2.5th and 97.5th percentiles as `se_or_ci`, the bootstrap SE, and as p-value the two-sided bootstrap proportion min(2 x share of resample means <= 0, 1). Note in the output that the points are spatially correlated, so the i.i.d. interval is narrower than a block bootstrap would give; that limitation is accepted in advance.

R_b. Outlier exclusion. Compute z = (data - mean) / SD (np.std, ddof=0, as the script uses); drop |z| > 3; report the new mean, n dropped, a 95% t-interval and one-sample t-test p-value against 0.

R_c. Alternative analysis choice: no 6000 m height cap. In a copy of O_B_Ku.py under `scripts/` (not the authors' file), delete lines 419 and 420 (the `radar_Z_out>6000.` masks), which the paper does not describe, change nothing else, rerun, and report mean, n, 95% t-interval and p-value as in R_b. If the memory fallback was used for the main run, use it here too.

## 4. Known risks

- Missing module (decisive): `interp_radar` (`interp_radar_ppi`, `interp_radar_shift`) is imported by O_B_Ku.py, 1DVAR.py and figure8 and is not in the deposit or the cited locations (DATA_STATEMENT.md). Without it no target can be computed, so the expected class is C. It is not E: the data and compute are enough; the code is incomplete.
- No code for Table 1 (T3 to T6). The abstract's first claim cannot be reproduced from the deposited code.
- Out of scope by design: everything that needs CMA-MESO or its 3D-Var system (Figures 6b, 7, 9 to 13; the abstract's forecast-improvement and CSI/FBIAS claims). CMA-MESO/GRAPES is not publicly distributed and is not deposited. Even with it, a 3-km model over central and eastern China would far exceed 2 CPUs and 7 GB. If these claims had to be targets they would be E (compute and system dependency) as well as C (forecast outputs not deposited).
- NCL scripts (figures 1, 2, 12) need NCL, which has no maintained aarch64 package; none is used for a target.
- `wrf-python`, `pycwr`, `proplot`, `cartopy` and a local `VAR_COLOR` module are imported by other figure scripts (not targets). `VAR_COLOR` is not deposited.
- Memory: see section 2; fallback pre-registered.
- Hard-coded absolute paths (`/public/home/zhwu/...`, `/public/home/ssrafs/...`) in most figure scripts; O_B_Ku.py uses only relative paths.
- Compute for T1/T2 is small (minutes), if the module were available.
