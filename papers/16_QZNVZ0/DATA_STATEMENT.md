# DATA_STATEMENT: 16_QZNVZ0 (Multidimensional Diversity and Research Impact in Political Science, Perspectives on Politics, doi 10.1017/S1537592724000641)

Written 2026-10-10 (IST), during pre-registration, before any analysis code was run. Downloads and checks made 2026-10-10 between about 17:21 and 17:25 UTC (22:51 to 22:55 IST). No sign-in, no author contact.

## Sources read
- Publisher PDF (open access, CC BY 4.0), https://www.cambridge.org/core/services/aop-cambridge-core/content/view/5D73412ABAA95A29464A350713C01FCE/S1537592724000641a.pdf/div-class-title-multidimensional-diversity-and-research-impact-in-political-science-what-50-years-of-bibliometric-data-tell-us-div.pdf : HTTP 200, 2,880,081 bytes, sha256 0266d0bb4881ba4834989aff0622f55f4c26ed17ad8c6f8636347a45021094ba (per-download watermark). Short excerpt: `data_statement_raw/statement_excerpt.txt`.
- Online appendix (Word), https://static.cambridge.org/content/id/urn%3Acambridge.org%3Aid%3Aarticle%3AS1537592724000641/resource/name/S1537592724000641sup001.docx : HTTP 200, 510,618 bytes, sha256 0a718395350446356976fd6e04b71026001d4dd16972afe2a7ae144c53414ed7. Text search for "dataverse", "replicat", "github", "osf", "download": no hit naming a data or code location. (The same path with `.pdf` returned HTTP 500; no PDF appendix exists at that address.)
- OpenAlex record (`data_statement_raw/openalex_work.json`); Dataverse dataset and versions API responses (`data_statement_raw/dataverse_QZNVZ0.json`, `data_statement_raw/versions.json`).

## Verbatim statement (p. 700, section "Data Replication")
"Data replication sets are available in Harvard Dataverse at: https://doi.org/10.7910/DVN/QZNVZ0."

The "Supplementary Material" section on the same page points to https://doi.org/10.1017/S1537592724000641 (the online appendix, checked above; it is not a data location). No other data or code location is named in the article.

## Locations the statement points to
1. Harvard Dataverse doi:10.7910/DVN/QZNVZ0 (the audited deposit). No other location.

## Check of location 1 (2026-10-10)
- Dataverse API: latest version 2.0, released 2024-10-03 22:12 UTC, CC0 1.0, 6 files, none restricted: readme.txt, Regression.ipynb, Visualizations.ipynb, regression_table_anonymous_final.csv, journal_scatter.csv, timelines.tab (ingested from original timelines.csv, retrievable with `?format=original`). All downloaded without sign-in; each md5 matches the Dataverse md5; sha256 in PREREG.md. Version 1.0 (2024-04-29) had earlier copies of four files; version 2.0 is audited.
- The deposit readme lists exactly these data files ("regression_table_anonymous_final.csv, journal_scatter.csv, and timelines.csv") and the two notebooks.
- Read calls in the code vs files present:
  - Regression.ipynb cell 1: `pd.read_csv('regression_table_anonymous_final.csv', index_col=0)`: present (datafile 10577540).
  - Visualizations.ipynb cell 2: `pd.read_csv('timelines.csv', index_col=0)`: present as the original-format download of datafile 10577539 (shown in the deposit as `timelines.tab`; the name differs only because of Dataverse ingest).
  - Visualizations.ipynb cell 13: `pd.read_csv('journal_scatter.csv')`: present (datafile 8940073).
  - No other read, open, load or import of a data file in either notebook (imports only pandas, numpy, statsmodels, plotly, math).
- Not deposited and not claimed by the readme: code that builds `regression_table_anonymous_final.csv` from the raw Web of Science records (author name ethnicity and gender coding, topic model, affiliation weights). No deposited script reads or references such a file, so no absence search was needed under CHANGELOG #5(a); this is a statement about the deposit's file list only.

## Searches for missing files
None needed: no file read by the deposited code is missing.

## Finding
Complete for the analysis: the statement points only to the audited Dataverse deposit, and every file the two notebooks read is there (timelines.csv via the original-format download). The upstream construction of the regression table from raw WoS data is not part of the deposit, so the analysis data cannot be rebuilt from source records; the targets do not depend on that step.
