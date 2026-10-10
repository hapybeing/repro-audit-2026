# DATA_STATEMENT: 23_FXRNBA (Wildfire smoke increases assaults: evidence from Seattle, Environ. Res. Lett. 21 044020 (2026), doi 10.1088/1748-9326/ae436c)

Written 2026-10-11 (IST), checks run 2026-10-10 20:38 to 20:40 UTC. No sign-in, no author contact, no analysis code run.

## Source read
- Publisher PDF, https://iopscience.iop.org/article/10.1088/1748-9326/ae436c/pdf : HTTP 200, 887,006 bytes, sha256 88218ab352b3caa0a5ce24505c9724d13a9cf5ac6869e4539703adbab6844e06 (same file as in PREREG.md). Short excerpt: `data_statement_raw/statement_excerpt.txt`.
- IOPscience HTML full text (https://doi.org/10.1088/1748-9326/ae436c), read with a fetch tool: same statement in its "Open science / Data availability statement" box and at the end of the article.
- Crossref record (`data_statement_raw/crossref.json`): licence CC BY 4.0, VOR links only to the IOPscience HTML and PDF.

## Verbatim statement (journal p. 8, PDF p. 9, "Data availability statement")
"The data that support the findings of this study are openly available at the following URL/DOI: https://doi.org/10.7910/DVN/FXRNBA [83].
Supplementary Information available at http://doi.org/10.1088/1748-9326/ae436c/data1."

## Locations the statement names
1. Harvard Dataverse doi:10.7910/DVN/FXRNBA (the audited deposit).
2. Supplementary Information, http://doi.org/10.1088/1748-9326/ae436c/data1 (publisher SI; the article cites "SI A" and "SI B", e.g. tables B3, B5 and B14). It is named as supplementary information, not as a data or code location.

No other location (OSF, GitHub, "on request") is named in the article. The deposit README names the original public sources (EPA AQS, Childs et al. 2022 smoke data, Seattle Police Department crime data, NOAA station WBAN 24234, Seattle 911 call, use-of-force and SDOT collision data); the article cites these as references but its data statement does not point to them as locations of the analysis data.

## Check of each location
1. Dataverse (checked, `data_statement_raw/dataverse_FXRNBA.json`): status released, version 1.1 (released 2026-02-20), 14 files, none restricted, related publication "IsSupplementTo" https://doi.org/10.1088/1748-9326/ae436c . All 14 files downloaded with HTTP 200 and sha256 recorded (`data_statement_raw/deposit_checksums.sha256`).
2. Supplementary Information (attempted, not readable): every route hit a Radware bot-check captcha or HTTP 403; attempts with UTC times in `data_statement_raw/si_access_attempts.json`. Whether the SI contains any data or code could not be determined. No deposited script reads a file that would come from the SI.

## Script read calls compared with files present

| script, line | read call | file in deposit? |
|---|---|---|
| wildfire_data_analysis.R 245, 251 | `read.csv("Data Analysis/merged_final_combined_data_{21,13,10,7}km.csv")` | yes, all four (datafiles 13436967, 13436964, 13436970, 13436958; originals are .csv, Dataverse folder "Data Analysis") |
| wildfire_plots.R 34, 38 | `st_read("Beats/Beats_WM.shp")` (+ .shx, .dbf, .prj, .cpg sidecars) | yes (13436960, 13436971, 13436968, 13436961, 13436962; plus .shp.xml 13436959) |
| wildfire_plots.R 35, 44 | `read.csv("Crime Data/crime_by_beat_2008_2023.csv")` | yes (13436963, original .csv, Dataverse folder "Crime Data") |
| wildfire_plots.R 316, 322 | same four buffer CSVs as above | yes |

Search method: `grep -n -E "read|source\(|load\(|st_read"` over both R scripts; no `source()`, `load()`, `readRDS()`, `haven::read_*` or other file reads exist. Neither script sources a helper file. The analysis script writes `seattle_21km.csv` (line 420) and HTML tables; these are outputs, not inputs.

Not in the deposit, and not read by any deposited script: the step that built the merged station-day CSVs from the raw sources (the plots script comments "same as Python" and "matching Python logic", lines 40 and 46). Because no deposited script reads a missing file, no absence search was needed under rule #4/#5(a).

## Finding
Deposit alone complete for the deposited code: every file the two R scripts read is in the Dataverse deposit, under the folder names the code expects. The second named location (publisher SI) could not be read because of a captcha; it is not needed by the code. The upstream data-construction code (raw sources to merged CSVs) is not deposited and is not referenced by the data statement.
