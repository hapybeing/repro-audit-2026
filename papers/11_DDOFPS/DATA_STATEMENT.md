# DATA_STATEMENT: 11_DDOFPS (Banco de Dados de Propaganda Eleitoral (HGPE) ... 1998-2018, DADOS 68(1) 2025, e20230099, doi 10.1590/dados.2025.68.1.001)

Written 2026-10-10 (IST), about 21:15 IST. Checks run 2026-10-10 between 15:28 and 15:42 UTC. No sign-in, no author contact. Rule 4 (CHANGELOG_METHOD.md #4) and #5(a) applied.

## Source read
- SciELO HTML (pt), https://www.scielo.br/j/dados/a/5KCvrPtYzZNWj4MFNZBRPLB/?lang=pt , read through the web_fetch tool on 2026-10-10 (scripted curl gets HTTP 403, bot challenge; no copy or hash saved).
- SciELO PDF (pt), https://www.scielo.br/j/dados/a/5KCvrPtYzZNWj4MFNZBRPLB/?format=pdf&lang=pt , saved by a browser print (17 pages, sha256 45558bbbc82081530534de93efed0678013c40b0d93b67ecaf1f00c9bf3935b1, `/workspace/audit_runs/11_DDOFPS/prereg/paper_pt_browserprint.pdf`). Text extracted with pdftotext; grep for "disponibilidade", "dataverse", "osf", "github", "solicita" in the PDF text: no hit.
- Excerpt file: `data_statement_raw/statement_and_target_excerpts.txt`.

## Verbatim statement (SciELO HTML, section "Declaração de disponibilidade de dados", after the Notas)
"Banco de dados: <https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/DDOFPS>"

The section is not printed in the PDF (the PDF ends with Notas on pp. 14 to 15 and Referencias on pp. 16 to 17). The text also names the two databases and their formats: "Foi nomeado bd_doxa_programas_HGPE, nos formatos do R (RData) e Excel (.xlsx)" and "bd_doxa_candidatos_HGPE (tambem nos formatos do R (RData) e Excel (.xlsx)" (PDF p. 7). The statement names a data location only; it does not mention code.

## Locations the statement points to
1. Harvard Dataverse doi:10.7910/DVN/DDOFPS (the audited deposit). No other location is named.

## Check of that location (2026-10-10, 15:28 UTC)
- Dataverse API (`/workspace/audit_runs/11_DDOFPS/prereg/dataverse_DDOFPS.json`): version 1 (only version), released 2024-01-03, CC0 1.0, 9 files, none restricted. All 9 downloaded; md5 of each matches Dataverse.
- Both databases named in the paper are there in both stated formats: `bd_doxa_programas_HGPE.RData` and `.xlsx` (plus `bd_doxa_programas_HGPE_v2.xlsx`), `bd_doxa_candidatos_HGPE.RData` and `.xlsx`. Also the R script, `HGPE_lei.xlsx`, and two codebook PDFs.

## Script read calls versus files present

| line | read call in `Análise dos Dados Nota Técnica.R` | file present in deposit? |
|---|---|---|
| 10 | `import("HGPE_lei.xlsx")` | yes, same name |
| 67 | `import("bd_doxa_programas.xlsx")` | not under this name; same-structure files `bd_doxa_programas_HGPE.xlsx` (sheet `banco de dados`, 9439 rows, 123 columns) and `bd_doxa_programas_HGPE_v2.xlsx` (same sheet, rows and column names) are present |
| 94 | `read.xlsx("bd_doxa_candidatos.xlsx", sheet = "2002_2018")` | not under this name; `bd_doxa_candidatos_HGPE.xlsx` is present and contains a sheet named `2002_2018` (4563 rows, 52 columns) |

No other file reads. The RData files are not read by the script.

## Searches for the two file names the script reads (CHANGELOG #5a)
Script: `data_statement_raw/absence_11.py`; raw records: `data_statement_raw/absence_searches.json`. Hit rule: a file named exactly `bd_doxa_programas.xlsx` or `bd_doxa_candidatos.xlsx` in any version of the deposit or in any Harvard Dataverse dataset. Public APIs, no sign-in.

| source | query | URL | UTC | HTTP | results | hits |
|---|---|---|---|---|---|---|
| DDOFPS file list, all versions | exact name bd_doxa_programas.xlsx | https://dataverse.harvard.edu/api/datasets/:persistentId/versions?persistentId=doi:10.7910/DVN/DDOFPS | 2026-10-10 15:42:00 | 200 | 9 files in 1 version | 0 (near names: bd_doxa_programas_HGPE.RData, bd_doxa_programas_HGPE.xlsx, bd_doxa_programas_HGPE_v2.xlsx) |
| DDOFPS file list, all versions | exact name bd_doxa_candidatos.xlsx | same | 2026-10-10 15:42:00 | 200 | 9 files | 0 (near names: bd_doxa_candidatos_HGPE.RData, bd_doxa_candidatos_HGPE.xlsx) |
| Harvard Dataverse Search API, type=file | "bd_doxa_programas.xlsx" | https://dataverse.harvard.edu/api/search?q=%22bd_doxa_programas.xlsx%22&type=file&per_page=100 | 2026-10-10 15:42:00 | 200 | 0 | 0 |
| Harvard Dataverse Search API, type=file | "bd_doxa_candidatos.xlsx" | https://dataverse.harvard.edu/api/search?q=%22bd_doxa_candidatos.xlsx%22&type=file&per_page=100 | 2026-10-10 15:42:00 | 200 | 0 | 0 |
| Harvard Dataverse Search API, type=file | bd_doxa_programas | https://dataverse.harvard.edu/api/search?q=bd_doxa_programas&type=file&per_page=100 | 2026-10-10 15:42:01 | 200 | 0 | 0 |
| Harvard Dataverse Search API, type=file | bd_doxa_candidatos | https://dataverse.harvard.edu/api/search?q=bd_doxa_candidatos&type=file&per_page=100 | 2026-10-10 15:42:01 | 200 | 0 | 0 |
| Harvard Dataverse Search API, type=file (positive control) | bd_doxa_programas_HGPE.xlsx | https://dataverse.harvard.edu/api/search?q=bd_doxa_programas_HGPE.xlsx&type=file&per_page=100 | 2026-10-10 15:42:01 | 200 | 1 | DDOFPS file 7337779 (the deposited file, as expected) |
| Harvard Dataverse Search API, type=file (positive control) | HGPE_lei.xlsx | https://dataverse.harvard.edu/api/search?q=HGPE_lei.xlsx&type=file&per_page=100 | 2026-10-10 15:42:02 | 200 | 1 | DDOFPS file 7337787 |

Limit of the search: the Search API tokenises file names, so the partial queries `bd_doxa_programas` and `bd_doxa_candidatos` return 0 even though files whose names start with those strings exist in DDOFPS; the positive controls show full file names are found. The searches cover Harvard Dataverse only, which is the only location the statement names.

## Finding
Data present, file names differ. The statement points only to the audited Dataverse deposit, which is reachable and holds both databases the paper names, in both formats, and the script. Two of the three files the script reads are not deposited under the names the script uses: `bd_doxa_programas.xlsx` and `bd_doxa_candidatos.xlsx`. Same-structure files are deposited as `bd_doxa_programas_HGPE.xlsx` (and a second version, `bd_doxa_programas_HGPE_v2.xlsx`) and `bd_doxa_candidatos_HGPE.xlsx` (with the sheet `2002_2018` the script requests). Nothing in the deposit says which programs file the script used. Whether the path mapping is an environment fix (class A/B possible) or makes the materials unclear (C) is a classification reading for the lead; this file only records what is there.
