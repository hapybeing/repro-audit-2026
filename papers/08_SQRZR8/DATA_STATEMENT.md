# DATA_STATEMENT: 08_SQRZR8 (Knowing Is Disturbing, Perspectives on Politics, doi 10.1017/S1537592725103551)

Written 2026-10-10 (IST), during pre-registration, before any analysis code was run. Checks run 2026-10-10 between about 11:49 and 11:55 UTC (17:19 to 17:25 IST). No sign-in, no author contact.

## Sources read
- Publisher PDF (Open Access, CC BY 4.0), https://www.cambridge.org/core/services/aop-cambridge-core/content/view/42AEE2A628849EC66A948C140CBB93F6/S1537592725103551a.pdf/div-class-title-knowing-is-disturbing-emotions-and-public-attitudes-toward-digital-control-under-autocracy-div.pdf : HTTP 200, 1,919,132 bytes, sha256 f221f4cabeb620dab030a6a6504c01a69181edcb5650947e56f93f777d81cd08 (per-download watermark, so re-downloads hash differently). Excerpt: `data_statement_raw/statement_excerpt.txt`.
- Online appendix PDF, https://static.cambridge.org/content/id/urn%3Acambridge.org%3Aid%3Aarticle%3AS1537592725103551/resource/name/S1537592725103551sup001.pdf : HTTP 200, 2,185,952 bytes, sha256 0ed5f4a6898c4f9b48842b73986e6c3c6ac1912d7e250903afcc16e72a10ae56. Text search for "dataverse", "replication", "data avail": no hit (no further data location named).
- OpenAlex record (`data_statement_raw/openalex_work.json`).

## Verbatim statement (p. 982, section "Data replication")
"Data replication sets are available in Harvard Dataverse at: https://doi.org/10.7910/DVN/SQRZR8."

The same deposit is cited in the reference list (p. 984): "Guo, Danqi and Genia Kostka. 2025. "Replication Data for: Knowing Is Disturbing: Emotions and Public Attitudes toward Digital Control under Autocracy." Harvard Dataverse, https://doi.org/10.7910/DVN/SQRZR8." The methods text (p. 972) cites it for the final sample: "Our final sample consisted of 4,507 participants (Guo & Kostka 2025)." The article's "Supplementary material" section (p. 982) points to the online appendix at http://doi.org/10.1017/S1537592725103551, which is an appendix, not a data location.

## Locations the statement points to
1. Harvard Dataverse doi:10.7910/DVN/SQRZR8 (the audited deposit). No other location is named.

Not counted (found by us, not cited in the statement): OpenAlex lists a repository copy of the article at Refubium (https://refubium.fu-berlin.de/handle/fub188/50459). Not checked for data; under CHANGELOG #4(a) it would not count toward the class.

## Check of location 1 (2026-10-10)
- Dataverse API (`data_statement_raw/dataverse_SQRZR8.json`): version 1.0 (the only version), released 2025-10-28, CC0 1.0, 5 files, none restricted: ReadMe.txt, main_rep.R, append_rep.R, data_raw_rep.csv, data_cleaned_rep.tab (ingested from original data_cleaned_rep.csv, original retrievable with `?format=original`, md5 matches the listed md5). All downloaded without sign-in; sha256 in PREREG.md.
- Read calls in the code vs files present:
  - main_rep.R line 22: `read.csv("data_cleaned_rep.csv", sep=",")`: present (as original-format download of datafile 12134916).
  - append_rep.R line 27: `read.csv("data_cleaned_rep.csv", sep=",")`: present (same file).
  - No other read, load, readRDS or source call in either script.
- File named in ReadMe.txt but not deposited: `data_preparation_rep.R`, described as "code that replicates the preparation of raw data for analysis, which generates a new dataset "data_cleaned_rep.csv"". It is not read by any deposited script. `data_raw_rep.csv`, its input, is deposited.

## Searches for the undeposited file (repeatable)
Script: `data_statement_raw/absence_08.py` (run from that folder, `python3 absence_08.py`); raw output `data_statement_raw/absence_searches.json`. Times are UTC as recorded by the script. A hit = any file named data_preparation_rep.R, or any other Dataverse dataset or dataset version for this article.

| # | Site | Query | URL | Time (UTC) | HTTP | Results | Hits |
|---|---|---|---|---|---|---|---|
| 1 | Harvard Dataverse Search API | `fileName:"data_preparation_rep.R"`, type=file | https://dataverse.harvard.edu/api/search?q=fileName%3A%22data_preparation_rep.R%22&per_page=100&type=file | 2026-10-10T11:54:22Z | 200 | 0 | none |
| 2 | Harvard Dataverse Search API | `data_preparation_rep`, type=file | https://dataverse.harvard.edu/api/search?q=data_preparation_rep&per_page=100&type=file | 2026-10-10T11:54:22Z | 200 | 0 | none |
| 3 | Harvard Dataverse Search API | `"Knowing is Disturbing"`, type=dataset | https://dataverse.harvard.edu/api/search?q=%22Knowing+is+Disturbing%22&per_page=100&type=dataset | 2026-10-10T11:54:22Z | 200 | 1 | none (the only result is the audited deposit SQRZR8) |
| 4 | Harvard Dataverse Search API | `Guo Kostka digital control`, type=dataset (first 100 of results inspected) | https://dataverse.harvard.edu/api/search?q=Guo+Kostka+digital+control&per_page=100&type=dataset | 2026-10-10T11:54:22Z | 200 | 55112 (OR match) | none other than SQRZR8 in the first 100 |
| 5 | Harvard Dataverse versions API | all versions of doi:10.7910/DVN/SQRZR8 | https://dataverse.harvard.edu/api/datasets/:persistentId/versions?persistentId=doi:10.7910/DVN/SQRZR8 | 2026-10-10T11:54:22Z | 200 | 1 version | none (v1.0 lists only the 5 files above) |

Exact per-row times are in absence_searches.json. Searches cover Harvard Dataverse only; GitHub and other sites were not searched (GitHub code search needs sign-in). A search can show absence only within what it searched.

## Finding
Deposit alone complete for the analysis: the statement points only to the audited Dataverse deposit, and every file the analysis scripts read (`data_cleaned_rep.csv`) is there. One file named in the deposit's own ReadMe, `data_preparation_rep.R` (raw-to-cleaned preparation), is not deposited and was not found by the searches above; it is not read by the analysis code, so the targets do not depend on it, but the data-preparation step cannot be reproduced from the deposit.
