# DATA_STATEMENT: 20_SINIYU (Wu et al. 2025, QJRMS 151(770) e4964, doi 10.1002/qj.4964)

Written 2026-10-11 about 00:20 IST (2026-10-10 about 18:50 UTC), during pre-registration, before any analysis code was run. No sign-in, no author contact. Rule: CHANGELOG_METHOD.md #4 (materials = deposit plus every location the article's own statement names) and #5(a) (absence claims backed by a repeatable search log).

## Source read
- Article HTML full text, https://doi.org/10.1002/qj.4964 (Wiley Online Library), read with web_fetch 2026-10-10 about 18:25 UTC. Not saved as a file (no sha256). The PDF could not be saved (a browser attempt failed; curl returns a Cloudflare challenge page). Short excerpt: `data_statement_raw/statement_excerpt.txt`.

## Verbatim statement (section "DATA AVAILABILITY STATEMENT", after ACKNOWLEDGEMENTS)
"The ERA5 reanalysis data were downloaded from the website of ECMWF ( <https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels> ), and Feng Yun 3G (FY-3G) spaceborne Ku-band radar observations were downloaded from the website of the National Center for Space Weather ( <https://satellite.nsmc.org.cn/FY3G/html/IOTDATASET.html> ). Other data used or produced in this study have been archived at the Harvard data server ( <https://doi.org/10.7910/DVN/SINIYU> )."

The statement names data only; it does not mention code. The code is in the Dataverse deposit (codes.tar.gz, 1DVAR.py). The article does not name a code repository, the CMA-MESO model or 3D-Var system as obtainable, or the ZJU-AERO operator release used.

## Locations named and what was checked (reachability: `data_statement_raw/das_location_checks.txt`, 2026-10-10 18:33 to 18:34 UTC)
1. ERA5 on the Copernicus Climate Data Store, https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels : HTTP 200 (landing page). Downloads need a CDS account, so nothing was downloaded (no sign-in rule). ERA5 is used only for Figures 1 and 10 (`era5_data/...`, `ERA/era5_uv.nc`; pressure-level fields, while the statement links the single-levels dataset). No target reads ERA5.
2. NSMC FY-3G in-orbit test dataset page, https://satellite.nsmc.org.cn/FY3G/html/IOTDATASET.html : HTTP 200, 41,680 bytes; it describes PMR L1 HDF5 half-orbit files (`FY3G_PMR--_ORBA/D_L1_YYYYMMDD_HHmm_5000M_Vn.HDF`). Not downloaded from there: the deposit already holds the FY-3G PMR file the code reads (`FY3G_PMR.HDF4` inside the 7-volume rar, HDF5 format, with every HDF path that 1DVAR.py and O_B_Ku.py read).
3. Harvard Dataverse doi:10.7910/DVN/SINIYU : HTTP 200, version 1, 18 files, all downloaded, all MD5 match (sha256 in PREREG.md and `prereg_download_checksums.sha256`).

## Files the code reads compared with files present (target-relevant scripts first)
| script | reads | present? |
|---|---|---|
| codes/figure6/O_B_Ku.py (T1, T2) | `./FY3G_PMR.HDF` (h5py) | yes, as `FY3G_PMR.HDF4` in the rar set (path-only rename) |
| | `./gep00/postvar.nc` | yes, as top-level `postvar.nc` (path-only) |
| | `./gep00/swath_spaceborn.nc` | yes, as `swath_spaceborn_mu3.nc` (path-only; the figure7 script names the _mu3 file explicitly) |
| | `from interp_radar import interp_radar_ppi` (line 17; f2py Fortran, signature in comments lines 448 to 453) | **no** (searches below) |
| | `plt.style.use(['science','no-latex'])` | public PyPI package SciencePlots (not a deposit file) |
| 1DVAR.py (no paper number) | FY3G_PMR.HDF, gep00/postvar.nc, gep00/swath_spaceborn.nc | yes (same mapping) |
| | `from interp_radar import interp_radar_shift` (line 21) | **no** |
| | writes `tmp.nc` | deposited result appears as `1DVAR_output.nc` (same variable and dims) |
| Table 1 (T3 to T6) | no script exists | **no code**; inputs Z9092.bin, Z9230.bin, FY3G HDF are present |
| codes/figure8 | FY3G_PMR.HDF, gep00 files, `./2023072800.000`, `./57328.csv`, CTRL/KuRH postvar files, interp_radar | 57328.csv yes; 2023072800.000 present as 57516.csv (inferred from station id); KuRH/CTRL series and interp_radar no |
| codes/figure7 | FY3G_PMR.HDF, swath_spaceborn_mu3.nc, `temp_inno202307280000_o_b_thin.dat` (3D-Var innovations) | innovation file no |
| codes/figure3, figure4 | FY3G_PMR.HDF (incl. `/Geolocation/Ku/elevation`), `Z_RADR_I_Z9230_20230728000900_O_DOR_SA_CAP.bin.bz2`, `Z_RADR_I_Z9092_20230728000743_O_DOR_SAD_CAP_FMT.bin.bz2` (pycwr) | radar volumes present as Z9230.bin and Z9092.bin (renamed, not bz2); `elevation` dataset absent from the HDF |
| codes/figure5, 9, 10, 11 | CTRL and KuRH postvar series (figure5, 10, 11 under `/public/home/zhwu/ncl/grapes/postvar/{CTRL,KuRH_melting_warm_thin,MCR}/`, figure9 under `./CTRL`, `./KuRH`), `RADAMCR_*.nc`, `era5_uv.nc`, `Province.shp`, `VAR_COLOR` module (figure5) | one postvar.nc only (its role as a series member is not documented); others no |
| codes/figure12 (NCL) | CTRL and `KuRH_melting_thin_err13` postvar series, hourly gauge files `2023072809.000` to `2023072815.000` | no |
| codes/figure13 | MET outputs under `/public/home/zhwu/MET/meso2grib/met_out/...` | no (acc01h.tar.gz has MET inputs obs.txt / obs_met.nc only) |
| codes/figure2 (NCL) | `2023072808.006`, `2023072814.006` | first yes, second no |
| codes/figure1 (NCL) | ERA5 file under `/public/home/ssrafs/...`, CTRL postvar | ERA5 at the CDS (named location, sign-in needed); postvar no |

## Searches for the missing module and the Table 1 code (CHANGELOG #5)
Script: `data_statement_raw/absence_searches_20.py` (re-runnable, public APIs, no sign-in); raw records: `data_statement_raw/absence_searches.json`. Hit rule: a file or repository whose name (or for GitHub, name or description) contains `interp_radar`, or for the volume-matching queries an item about FY-3G. Record 18 was done by hand (download, `tar tzf`, `grep -rli interp_radar` on the extracted sources) and appended to the JSON with its details.

| # | source | query | UTC time | HTTP | total results | relevant hits |
|---|---|---|---|---|---|---|
| 1 | Harvard Dataverse Search API (type=file) | `fileName:interp_radar*` | 2026-10-10T18:32:55Z | 200 | 0 | 0 |
| 2 | Harvard Dataverse Search API (type=file) | `"interp_radar_ppi"` | 2026-10-10T18:32:56Z | 200 | 0 | 0 |
| 3 | Harvard Dataverse Search API (type=file) | `"interp_radar_shift"` | 2026-10-10T18:32:57Z | 200 | 0 | 0 |
| 4 | Harvard Dataverse Search API (type=file) | `fileName:VAR_COLOR*` | 2026-10-10T18:32:59Z | 200 | 0 | 0 |
| 5 | Harvard Dataverse Search API (type=file) | `fileName:temp_inno*` | 2026-10-10T18:33:00Z | 200 | 0 | 0 |
| 6 | Harvard Dataverse Search API (type=file) | `fileName:*o_b_thin*` | 2026-10-10T18:33:01Z | 200 | 0 | 0 |
| 7 | Dataverse file list doi:10.7910/DVN/SINIYU | `all files (latest version)` | 2026-10-10T18:33:03Z | 200 | 18 | 0 |
| 8 | Zenodo records API | `"interp_radar_ppi"` | 2026-10-10T18:33:04Z | 200 | 0 | 0 |
| 9 | Zenodo records API | `"interp_radar_shift"` | 2026-10-10T18:33:06Z | 200 | 0 | 0 |
| 10 | Zenodo records API | `interp_radar` | 2026-10-10T18:33:08Z | 200 | 0 | 0 |
| 11 | Zenodo records API | `FY-3G Ku-band volume matching` | 2026-10-10T18:33:09Z | 200 | 263698 | 3 |
| 12 | Zenodo records API | `FY-3G 1D Bayesian retrieval CMA-MESO` | 2026-10-10T18:33:12Z | 200 | 84354 | 3 |
| 13 | GitHub repository search API (unauthenticated) | `interp_radar` | 2026-10-10T18:33:15Z | 200 | 15 | 0 |
| 14 | GitHub repository search API (unauthenticated) | `interp_radar_ppi` | 2026-10-10T18:33:19Z | 200 | 0 | 0 |
| 15 | GitHub repository search API (unauthenticated) | `FY3G PMR` | 2026-10-10T18:33:22Z | 200 | 0 | 0 |
| 16 | GitHub repository search API (unauthenticated) | `FY-3G radar assimilation` | 2026-10-10T18:33:26Z | 200 | 0 | 0 |
| 17 | GitHub repository search API (unauthenticated) | `Ku-band 1D Bayesian retrieval` | 2026-10-10T18:33:29Z | 200 | 0 | 0 |
| 18 | Zenodo record 10.5281/zenodo.11307123 (ZJU-AERO software, Xie, Bi, Han 2024; NOT cited by the article's data statement) | `file names and file contents matching 'interp_radar' (case-insensitive) in ZJU_AERO-0.6.1.tar.gz` | 2026-10-10T18:42:59Z | 200 | 239 | 0 |

URLs:
1. https://dataverse.harvard.edu/api/search?q=fileName%3Ainterp_radar%2A&type=file&per_page=100
2. https://dataverse.harvard.edu/api/search?q=%22interp_radar_ppi%22&type=file&per_page=100
3. https://dataverse.harvard.edu/api/search?q=%22interp_radar_shift%22&type=file&per_page=100
4. https://dataverse.harvard.edu/api/search?q=fileName%3AVAR_COLOR%2A&type=file&per_page=100
5. https://dataverse.harvard.edu/api/search?q=fileName%3Atemp_inno%2A&type=file&per_page=100
6. https://dataverse.harvard.edu/api/search?q=fileName%3A%2Ao_b_thin%2A&type=file&per_page=100
7. https://dataverse.harvard.edu/api/datasets/:persistentId/versions/:latest/files?persistentId=doi:10.7910/DVN/SINIYU
8. https://zenodo.org/api/records?q=%22interp_radar_ppi%22&size=25
9. https://zenodo.org/api/records?q=%22interp_radar_shift%22&size=25
10. https://zenodo.org/api/records?q=interp_radar&size=25
11. https://zenodo.org/api/records?q=FY-3G+Ku-band+volume+matching&size=25
12. https://zenodo.org/api/records?q=FY-3G+1D+Bayesian+retrieval+CMA-MESO&size=25
13. https://api.github.com/search/repositories?q=interp_radar&per_page=100
14. https://api.github.com/search/repositories?q=interp_radar_ppi&per_page=100
15. https://api.github.com/search/repositories?q=FY3G+PMR&per_page=100
16. https://api.github.com/search/repositories?q=FY-3G+radar+assimilation&per_page=100
17. https://api.github.com/search/repositories?q=Ku-band+1D+Bayesian+retrieval&per_page=100
18. https://zenodo.org/api/records/11307123/files/ZJU_AERO-0.6.1.tar.gz/content

Reading of the hits: the 3 "relevant" Zenodo items for queries 11 and 12 are FY-3G records from other studies (10.5281/zenodo.19562313 "Data for Enhancing Typhoon Precipitation Forecasts via Vertical Moisture Refinement ... FY-3G Ku/Ka ...", data.zip, not opened; 10.5281/zenodo.12200147 FY-3G PMR sample data; 10.5281/zenodo.10699613 FY-3G imager cloud phase). None is this article's code. GitHub code search needs sign-in, so only repository names and descriptions were searched; the 15 repositories returned for `interp_radar` are unrelated (listed in the JSON note). The ZJU-AERO 0.6.1 release (not cited by the article) has its own `ZJU_AERO/interp/` Cython/SWIG module but no `interp_radar`. Version 0.4.1 (the version in a hard-coded path in the figure7 script), `zju_aero_env.tar.gz` and the uncited typhoon-study data.zip were not checked.

## Finding
Incomplete. The statement's three locations hold the data that the target scripts read (the deposit alone covers them; ERA5 is not needed for any target). Two things are missing from the deposit and the cited locations: (1) the module `interp_radar` (`interp_radar_ppi`, `interp_radar_shift`) imported by O_B_Ku.py, 1DVAR.py and figure8, so the one script that computes a paper number (Figure 6a, T1 and T2) cannot run; (2) any code for Table 1 (T3 to T6). Many figure-only inputs (forecast series, 3D-Var innovations, MET outputs, radar mosaics) are also absent, but those belong to results already out of scope (CMA-MESO / 3D-Var). Under rule #4 this points to class C. No uncited location was found that would supply the module, so no alternative class is expected at this point.
