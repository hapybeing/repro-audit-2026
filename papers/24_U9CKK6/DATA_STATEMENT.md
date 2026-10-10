# DATA_STATEMENT: 24_U9CKK6 (The challenger advantage, Journal of European Public Policy 2024, doi 10.1080/13501763.2024.2391510)

Written 2026-10-11 (IST, about 02:30), before any analysis code was run. Checks run 2026-10-10 between about 20:38 and 20:49 UTC (2026-10-11 02:08 to 02:19 IST). No sign-in, no author contact.

## Source read
- Publisher full-text HTML (open access, CC BY): https://www.tandfonline.com/doi/full/10.1080/13501763.2024.2391510 , extracted text 180,821 bytes, sha256 0195fcc14f1f7b35f55a8dab783a7c07b874019b66de08887e1bcdd2e9091134. The PDF could not be fetched by curl (HTTP 403, Cloudflare); a browser session opened it in the publisher reader to transcribe Tables 1 and 2.
- Online supplement (figshare, https://ndownloader.figshare.com/files/49076409 , sha256 95f2d48026190954c4a61c211fb62e25b9a8d7cdd6d143c1a93e7cb4c7313afd): searched its text for "dataverse", "replication", "github", "osf", "parlgov", "Wratil", "available": no data or code location named.

## Verbatim statement (article, section "Data availability statement", after the Disclosure statement)
"Data and replication files are available at: https://doi.org/10.7910/DVN/U9CKK6"

## Locations the statement points to
1. Harvard Dataverse doi:10.7910/DVN/U9CKK6 (the audited deposit). No other location is named in the statement, the article text, or the supplement.

## Reachability and contents check
- Dataverse API https://dataverse.harvard.edu/api/datasets/:persistentId/?persistentId=doi:10.7910/DVN/U9CKK6 : HTTP 200, version 1.0, released 2024-08-28, 28 files, 832,680,633 bytes, none restricted, CC0 1.0. Folders: Scripts (11 R scripts), Data (11 files), NLP_Model (5 files), readme.txt. Downloaded and hashed: all scripts, readme, `Data/EP_debates_07062023.Rdata`, `Data/RdW_salience.Rdata` (sha256 in PREREG.md; md5 of each matched Dataverse).

## Files the code reads vs files present (every read call in the 11 scripts)

| script, line | read call | in deposit? |
|---|---|---|
| 1_QTA_Embeddings.R 13 | `load("Data/EP_prepped_110323.Rdata")` | yes |
| 1_QTA_Embeddings.R 26-29 | `load("NLP_Model/...28102021.Rdata")` (commented out) | yes (4 files) |
| 2_QTA_Debatetopics.R 13 | `load("Data/EP_complete_dict_110323.Rdata")` | yes |
| 2_QTA_Debatetopics.R 35 | `load("NLP_Model/out50_05112021.Rdata")` (commented out) | yes |
| 3_OppositionControl.R 20, 28, 33 | `read_xlsx("Data/EP6_RCVs.xlsx")`, EP7, EP8 | yes |
| 3_OppositionControl.R 57 | `read.csv2("Data/Members.csv")` | yes |
| 3_OppositionControl.R 209 | `load("Data/EP_debates_11032023.Rdata")` | yes |
| 4_OppositionControlNat.R 23 | `read.csv("parlgov/view_party.csv")` | **no** |
| 4_OppositionControlNat.R 34 | `read.csv("parlgov/view_cabinet.csv")` | **no** |
| 4_OppositionControlNat.R 131 | `load("Data/EP_debates_11032023.Rdata")` | yes |
| 5, 6, 7, 8, 9, 10, 11 | `load("Data/EP_debates_07062023.Rdata")` | yes |
| 8_analysis3.R 47 | `read_xlsx("Data/eurostat_asylum.xlsx", sheet = 3)` | yes |
| 8_analysis3.R 98 | `read.csv("Data/eurostat_unemployment.csv")` | yes, served as `eurostat_unemployment.tab`; original .csv via `?format=original` (path-only mapping) |
| 9_analysis4.R 16 | `load("Data/RdW_salience.Rdata")` | yes |
| 10_analysis_5.R 16 | `read_dta("Data/eurobarmeter_challengers_2023.dta")` with comment "Wratil (forthcoming) - dataset will be added upon publication by Wratil" | **no** |

No `source()` of helper files exists in any script. Script 6 lines 132 and 246 use variables `right` and `left` that no script creates and that are not columns of `EP_debates` (a variable, not a file; listed in PREREG.md risks).

## Absence searches (repeatable)
Script: `data_statement_raw/absence_searches_24.py`; output: `data_statement_raw/absence_searches.json` (exact URL, time, HTTP status, total result count, hits per query). Run at 2026-10-10 about 20:48 UTC (the JSON `utc` field was rendered by the sandbox as "Sun 2026-10-11 2:18 AM IST (UTC+05:30)", which is the same moment). Hit rule: a file with the exact name the script reads inside doi:10.7910/DVN/U9CKK6.

| query | where | HTTP | results |
|---|---|---|---|
| view_party.csv | deposit file list, all versions (`/api/datasets/:persistentId/versions?persistentId=doi:10.7910/DVN/U9CKK6`) | 200 | 0 |
| view_cabinet.csv | same | 200 | 0 |
| eurobarmeter_challengers_2023.dta | same | 200 | 0 |
| .dta | same | 200 | 0 |
| parlgov | same | 200 | 0 |
| eurobar | same | 200 | 0 |
| "eurobarmeter_challengers_2023" | Harvard Dataverse search API, type=file (`/api/search?q=%22eurobarmeter_challengers_2023%22&type=file&per_page=100`) | 200 | 0 |
| name:"view_party.csv" | Harvard Dataverse search API, type=file | 200 | 0 |
| name:"view_cabinet.csv" | Harvard Dataverse search API, type=file | 200 | 0 |
| eurobarmeter_challengers_2023.dta (unquoted) | Harvard Dataverse search API, type=file | 200 | 14791 (token match on unrelated files; none in U9CKK6; no exact name match) |
| Wratil challengers eurobarometer; eurobarometer challengers Wratil 2023 | Harvard Dataverse search API, type=dataset | 200 | 7593; 25601 (unquoted token matches). Among the first 50 items of the first query: the audited deposit itself, 'Eurobarometer 91.5', and other unrelated 'challenger' replication datasets; no dataset by Wratil with a Eurobarometer challengers file. Outside the named location; does not count for rule #4 |

ParlGov data are public elsewhere (parlgov.org, cited in the article as Doring and Manow 2020), but the article's statement does not point there, so under CHANGELOG #4 they do not count toward the materials.

## Finding
Statement found; it names only the audited Dataverse deposit, which is reachable and public. Deposit incomplete for the full pipeline: three files the code reads are absent (`parlgov/view_party.csv`, `parlgov/view_cabinet.csv` for script 4; `Data/eurobarmeter_challengers_2023.dta` for script 10). For the pre-registered targets (Table 1 from script 6, Table 2 from script 9) every file read is present: both scripts start from the deposited intermediate `Data/EP_debates_07062023.Rdata` (and `Data/RdW_salience.Rdata` for script 9). Whether the missing upstream files matter for the class is for the lead under rule #4; they do not block T1 to T6.
