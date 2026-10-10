# DATA_STATEMENT: 13_DX5T9G (No Entry in a Pandemic, AJPS 2024 68(2), doi 10.1111/ajps.12790)

Written 2026-10-10 (IST), about 21:10 IST. Checks run 2026-10-10 between 15:28 and 15:35 UTC. No sign-in, no author contact. No analysis code was run.

## Source read
- Publisher version of record (open access, CC BY), White Rose eprints copy: https://eprints.whiterose.ac.uk/194407/15/American%20J%20Political%20Sci%20-%202023%20-%20Kobayashi%20-%20No%20Entry%20in%20a%20Pandemic%20%20Public%20Support%20for%20Border%20Closures.pdf : 762,558 bytes, 18 pages, sha256 29a878be7af3352678da2ced5a8bd653faa8725fc95a1a0e2e2a5035c8691085 (same file as in PREREG.md). Found via OpenAlex (`data_statement_raw/openalex_work.json`). The Wiley pdfdirect URL returned an HTML page to a scripted request and was not used.
- Short excerpt saved: `data_statement_raw/statement_excerpt.txt`.

## Verbatim statement (p. 372, under the abstract, "Verification Materials")
"Verification Materials: The data and materials required to verify the computational reproducibility of the results, procedures, and analyses in this article are available on the American Journal of Political Science Dataverse within the Harvard Dataverse Network, at https://doi.org/10.7910/DVN/DX5T9G."

Other places in the article that point to materials:
- Footnote 19 (p. 382), about the Bernoulli-probit verisimilitude results: "These results are available from the authors and are also noted in the replication materials."
- Footnote 13 (p. 376) names the 2017 British Election Study and the 2018 Cooperative Congressional Election Study as benchmark data, without a location.
- A grep of the extracted text for "osf", "github", "request" and "available from" found no other location.

## Locations named and what was checked
1. Harvard Dataverse doi:10.7910/DVN/DX5T9G (the audited deposit). Checked. DOI resolves (HTTP 200) to the Dataverse citation page. API (`data_statement_raw/dataverse_DX5T9G.json`): version 1.0, RELEASED 2023-02-21, 23 files, 847,156,282 bytes, none restricted, all downloaded without sign-in; per-file sha256 in `data_statement_raw/files_sha256.json`. The four ingested tabular files were also fetched in original format (`?format=original`); their MD5 matches the Dataverse record.
2. "The replication materials" (footnote 19): taken to mean the same deposit. Checked: `code/06_Estimate Open.R` contains the footnote 19/20 probit models (comment "Probit results for Footnote 20; verisimilitude"). This is about a secondary result, not a target.
3. "Available from the authors" (footnote 19): not checked (no author contact, per protocol). Not needed for any target.
4. BES 2017 and CCES 2018 (footnote 13, no location given in the article): the deposit itself contains both files the code reads (`data/BES/bes_f2f_2017_v1.5.dta`, `data/CCES/cces18_common_vv.dta`); the ReadMe cites their original sources (UK Data Service SN 8418, DOI 10.5255/UKDA-SN-8418-1; CCES Common Content 2018, https://doi.org/10.7910/DVN/ZSBZ7K, V6). Those external sources were not checked because the deposit already holds the files.

## Files the code reads vs files present
Read calls found by grep over all deposited R scripts (excluding files the code itself writes under `output/`):

| script, line | file read | in deposit? |
|---|---|---|
| 00, 52 and 69 to 76 | `code/X_Auxiliary functions.R`, `code/01` to `code/08` | yes, all 9 scripts |
| 01, 13 | `data/ViralBorders - US.csv` | yes (datafile 6911553; ingested as .tab, original .csv via ?format=original, 1,169,429 bytes, 1,628 data rows) |
| 01, 14 | `data/ViralBorders - UK.csv` | yes (6911559; original .csv 1,168,013 bytes, 1,605 data rows) |
| 01, 120 | `data/CCES/cces18_common_vv.dta` | yes (6911546; 839,424,284 bytes, Stata 14 format, served as-is) |
| 01, 134 | `data/BES/bes_f2f_2017_v1.5.dta` | yes (6911551; ingested as .tab, original .dta 1,845,588 bytes, Stata format 115, readable by foreign::read.dta) |
| 08, 13 | `data/News Queries/News.csv` | yes (6911556; original .csv 2,570 bytes) |
| 00, file.copy | `data/cascara_geo_trimmed.png` | yes (6911548) |

All other reads (`output/Prepped_survey_data.csv`, `output/Target_data.csv`, `output/Estimates-Main.Rdata`) are files written earlier in the same pipeline.

Only discrepancy: file extensions. With Dataverse's default download the four ingested files arrive as `.tab` (tab-separated, different bytes); the code needs the original `.csv`/`.dta` uploads, which Dataverse serves with `?format=original`. No file is missing, so no absence search was needed.

## Finding
Complete: the statement points only to the audited Dataverse deposit, and every file the deposited code reads is present there (original formats available from Dataverse). Under CHANGELOG #4 the materials rule is met by the deposit alone.
