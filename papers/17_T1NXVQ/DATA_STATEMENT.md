# DATA_STATEMENT: 17_T1NXVQ (Shaping states into nations, AJPS 2024, doi 10.1111/ajps.12838)

Written 2026-10-10 (IST), before any analysis code was run. Checks run 2026-10-10 between about 17:20 and 17:35 UTC (22:50 to 23:05 IST). No sign-in, no author contact.

## Source read
- Published version (CC BY-NC-ND 4.0) from LSE Research Online: http://eprints.lse.ac.uk/120409/1/American_J_Political_Sci_2024_M_ller_Crepon_Shaping_states_into_nations_The_effects_of_ethnic_geography_on_state.pdf , HTTP 200, 4,391,122 bytes, sha256 67e1f23d126112145766273bd7645a2bdfb7f94d0712f570ffad59b152dc3516 (same file as PREREG.md). Short excerpt: `data_statement_raw/statement_excerpt.txt`. OpenAlex record: `data_statement_raw/openalex_work.json`. The Wiley pdfdirect URL returned HTTP 403 to a scripted request.
- The Supporting Information was not opened.

## Verbatim statement (p. 1, first-page footnote block, "Verification Materials")
"Verification Materials: The materials required to verify the computational reproducibility of the results, procedures, and analyses in this article are available on the American Journal of Political Science Dataverse within the Harvard Dataverse Network, at: http://doi.org/10.7910/DVN/T1NXVQ."

Related line (p. 2, footnote 4, on the software): "Available at https://github.com/carl-mc/pspm and https://github.com/carl-mc/SpatialLattice."

## Locations named
1. Harvard Dataverse doi:10.7910/DVN/T1NXVQ (the audited deposit): the data and code location.
2. GitHub carl-mc/pspm and carl-mc/SpatialLattice: software (the PSPM package and its Python lattice code), named in footnote 4, not as a data location.

## Checks per location
1. Dataverse T1NXVQ (`data_statement_raw/dataverse_T1NXVQ.json`): checked. Version 1.0, 167 files, 1,988,578,335 bytes, none restricted, custom terms of use. Holds README.txt, codebook.pdf, replication.R, all scripts, the analysis data (`data/analysis_data/`), the fitted models and bootstrap results (`data/models/`), Monte Carlo results, logs and the replication version of the pspm package (`pspm/pspm_1.0.tar.gz`). README states that only the data for the analysis step are included: the data-preparation code "depend[s] on (large, geographical) data not included in this replication repository" and the Monte Carlo simulations are not re-run by replication.R.
2. GitHub carl-mc/pspm and carl-mc/SpatialLattice: checked with the unauthenticated GitHub API (searches 11 and 12 below); both public. They hold the current package code; the deposit's README and libraries.R install the deposited tarball for replication, so the GitHub copies are not needed for any target.

## Script read calls compared with files present
Method: `grep` for readRDS, load, read.csv, readOGR, raster, readLines, st_read in `replication.R` and every script under `scripts/analysis/` (106 calls; list in `data_statement_raw/read_calls_analysis.txt`), and for quoted data paths in `scripts/data_prep/`, `scripts/functions/`, `scripts/monte_carlos/`. Compared with the Dataverse file list.

| scripts | file read | present in deposit? |
|---|---|---|
| analysis_globals.R `load_data()` (line 154), used by analysis_pool.R and main_plots_tables.R (Table 1) | `data/analysis_data/maindata.Rdata` | yes (datafile 6980033) |
| analysis_pool.R, main_plots_tables.R (Table 1 path) | package `pspm` | yes, `pspm/pspm_1.0.tar.gz` |
| main_plots_tables.R lines 26-27 (Table 1 printing) | `data/models/pool_model.ls.rds`, `pool_se.ls.rds` (written by analysis_pool.R, also deposited) | yes |
| all other scripts called by analysis_all.R | `data/models/*.rds` (all 40+ names read), `data/analysis_data/graph_*.rds`, `sdm_*.rds`, `compare_heg_df.rds`, `graph_austhung.rds`, `uch_cam_12_georef.tif`, `data/geography/continents` shapefile, `cshapes_2_cow.geojson`, `heg_full.geojson`, `heg_extent.geojson`, `data/monte_carlo_res/*/results.rds`, `parameters.rds` | yes |
| analysis_descriptives.R, meta_data_table.R, analysis_bymap.R | `data/geography/HEG/heg_meta.csv`, `heg_langmatch.csv`, `heg_author_nationalities.csv` | yes as ingested `.tab` files; originals (`?format=original`) are CSV with the same content. Path/format fix only. |
| analysis_shift_notrun.R line 41, sdm/analysis_shiftcheck_notrun.R line 46 (both marked "Do not run" and commented out in analysis_all.R), data_prep/prepare_networks.R line 106 | `data/analysis_data/res_optim.rds` | no |
| data_prep/* and functions/data_mgt/* (data preparation, not called by replication.R) | e.g. `data/geography/geosdm_subset/gsdm.rds`, `sdm_claims.csv`, `data/geography/EPR/epr_sec.geojson`, `epr_sec.csv`, `data/geography/census_austhung/Final_df_complete`, `data/geography/GREG`, `geography/elevation/globe_30sec.tif`, `/nastac/data/abramsonmax`, `/nastac/data/euratlas`, FAO GAEZ and HydroSHEDS layers, LEDA matching tables | no; README lists the third-party sources for these and says GeoSDM is "Available from the authors" |

## Searches for missing files (repeatable)
Script: `data_statement_raw/absence_searches_17.py` (run from repo/); full output with per-query UTC time, HTTP status, totals and notes: `data_statement_raw/absence_searches.json`. Hit rule: a file with exactly the missing name in a dataset or repository linked to these authors or this article. Counts below are copied by script from the JSON.

| # | source | query | URL | time (UTC) | HTTP | results | hits (exact missing file name) |
|---|---|---|---|---|---|---|---|
| 1 | Harvard Dataverse Search API | `fileName:"res_optim.rds" type=file` | https://dataverse.harvard.edu/api/search?q=fileName%3A%22res_optim.rds%22&type=file&per_page=100 | 2026-10-10T17:29:03Z | 200 | 0 | 0 |
| 2 | Harvard Dataverse Search API | `fileName:"gsdm.rds" type=file` | https://dataverse.harvard.edu/api/search?q=fileName%3A%22gsdm.rds%22&type=file&per_page=100 | 2026-10-10T17:29:03Z | 200 | 0 | 0 |
| 3 | Harvard Dataverse Search API | `fileName:"sdm_claims.csv" type=file` | https://dataverse.harvard.edu/api/search?q=fileName%3A%22sdm_claims.csv%22&type=file&per_page=100 | 2026-10-10T17:29:03Z | 200 | 0 | 0 |
| 4 | Harvard Dataverse Search API | `fileName:"epr_sec.geojson" type=file` | https://dataverse.harvard.edu/api/search?q=fileName%3A%22epr_sec.geojson%22&type=file&per_page=100 | 2026-10-10T17:29:04Z | 200 | 0 | 0 |
| 5 | Harvard Dataverse Search API | `fileName:"epr_sec.csv" type=file` | https://dataverse.harvard.edu/api/search?q=fileName%3A%22epr_sec.csv%22&type=file&per_page=100 | 2026-10-10T17:29:04Z | 200 | 0 | 0 |
| 6 | Harvard Dataverse Search API | `fileName:"Final_df_complete.shp" type=file` | https://dataverse.harvard.edu/api/search?q=fileName%3A%22Final_df_complete.shp%22&type=file&per_page=100 | 2026-10-10T17:29:05Z | 200 | 0 | 0 |
| 7 | Harvard Dataverse Search API | `authorName:"Müller-Crepon" type=dataset` | https://dataverse.harvard.edu/api/search?q=authorName%3A%22M%C3%BCller-Crepon%22&type=dataset&per_page=100 | 2026-10-10T17:29:05Z | 200 | 13 | 0 |
| 8 | Harvard Dataverse Search API | `authorName:"Muller-Crepon" type=dataset` | https://dataverse.harvard.edu/api/search?q=authorName%3A%22Muller-Crepon%22&type=dataset&per_page=100 | 2026-10-10T17:29:06Z | 200 | 13 | 0 |
| 9 | Harvard Dataverse Search API | `authorName:"Schvitz" type=dataset` | https://dataverse.harvard.edu/api/search?q=authorName%3A%22Schvitz%22&type=dataset&per_page=100 | 2026-10-10T17:29:07Z | 200 | 3 | 0 |
| 10 | GitHub REST API (unauthenticated) | `repositories of user carl-mc (named in article footnote 4)` | https://api.github.com/users/carl-mc/repos?per_page=100 | 2026-10-10T17:29:07Z | 200 | 13 | 0 |
| 11 | GitHub REST API (unauthenticated) | `full file tree of carl-mc/pspm (main)` | https://api.github.com/repos/carl-mc/pspm/git/trees/main?recursive=1 | 2026-10-10T17:29:08Z | 200 | 46 | 0 |
| 12 | GitHub REST API (unauthenticated) | `full file tree of carl-mc/SpatialLattice (main)` | https://api.github.com/repos/carl-mc/SpatialLattice/git/trees/main?recursive=1 | 2026-10-10T17:29:08Z | 200 | 46 | 0 |
| 13 | GitHub repository search API (unauthenticated) | `Shaping states into nations` | https://api.github.com/search/repositories?q=Shaping+states+into+nations | 2026-10-10T17:29:09Z | 200 | 5 | 0 |

Notes: #7 and #8 return 13 datasets each (other articles by the first author; the stored note lists the first eight names, truncated at 1500 characters, and none of those is a second deposit of this article); #9 returns 3 datasets (T1NXVQ itself and two other articles). #10 lists the 13 public repositories of carl-mc; only the two named in the article (pspm, SpatialLattice) had their full file trees checked (#11, #12); the repository `hegdata` (not named in the article) was not inspected. #13 returned 5 unrelated repositories. GitHub code search needs sign-in and was not used.

## Finding
Complete for the headline (Table 1) and for every script that replication.R runs: the article's statement points to the Dataverse deposit, and the deposit holds every file those scripts read (three HEG CSVs only under Dataverse's `.tab` ingest name, a format/path matter).
Not complete for the whole pipeline: `data/analysis_data/res_optim.rds` (read only by two scripts marked "Do not run" and by data preparation) and the raw inputs of the data-preparation step are not in the deposit, and the searches above found no copy at any location linked to the authors or the article. README says so itself and names the third-party sources. No target depends on these files. Under CHANGELOG rule #4 the materials for the targets are complete.
