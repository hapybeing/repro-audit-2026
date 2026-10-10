# DATA_STATEMENT: 06_VSV5DM (Leadership in a Pandemic, Political Research Quarterly 78(2) 2025, doi 10.1177/10659129241301785)

Written 2026-10-10 (IST, about 17:55), under rule CHANGELOG_METHOD #4 (materials = deposit plus every location the article's own statement points to) and #5. Checks run 2026-10-10 between about 11:49 and 12:25 UTC. No sign-in, no author contact, no posting. No analysis code was run.

## Sources read
- Main article PDF, 16 pages, sha256 ae02f4271a1cafefe627895cacb963763997fbba280ee2ae6408b3412e639081 (obtained through the browser from https://journals.sagepub.com/doi/pdf/10.1177/10659129241301785 ; direct curl returns HTTP 403). Statement excerpt: `data_statement_raw/article_statement_excerpt_p13.txt`.
- Online appendix PDF, 49 pages, sha256 9db99f76a93334cdd993edca78eb9a84d80255c899275893dc40f6efce788dd6 (via https://journals.sagepub.com/action/downloadSupplement?doi=10.1177%2F10659129241301785&file=sj-pdf-1-prq-10.1177_10659129241301785.pdf). `pdftotext` output searched for "dataverse", "replicat", "availab", "crowdtangle" (case-insensitive): 0 hits. The appendix has no data statement.
- Publisher HTML full text (https://journals.sagepub.com/doi/full/10.1177/10659129241301785): its "Supplementary Material" section lists two files, `sj-pdf-1-prq-10.1177_10659129241301785.pdf` (555.31 KB) and `sj-zip-2-prq-10.1177_10659129241301785.zip` (533.77 KB).
- Not in Europe PMC (REST search `DOI:10.1177/10659129241301785`, 0 hits, about 11:55 UTC). OpenAlex OA URL is the Sage PDF (`data_statement_raw/openalex_work.json`).

## Verbatim statement (article p. 449, PDF p. 13, heading "Supplemental Material")
"Supplemental material for this article is available online. The dataset used for this paper along with replication files is made available at: https://doi.org/10.7910/DVN/VSV5DM."

There is no separate "Data availability" section. Endnote 5 (p. 449) describes CrowdTangle as the collection tool and does not mention restrictions. The deposit README (not the article) says: "The original raw data contains the actual text from each Facebook, however, restrictions apply to the availability of these data, which were used under license for this study."

## Locations the statement points to
1. Harvard Dataverse doi:10.7910/DVN/VSV5DM (the audited deposit).
2. "Supplemental material ... available online": the Sage-hosted supplements of the article, namely (a) the appendix PDF `sj-pdf-1-...pdf` and (b) `sj-zip-2-prq-10.1177_10659129241301785.zip` (533.77 KB).

## Check of each location
1. Dataverse (checked). API `https://dataverse.harvard.edu/api/datasets/:persistentId/?persistentId=doi:10.7910/DVN/VSV5DM` (saved as `data_statement_raw/dataverse_VSV5DM.json`): version 1.0, released 2024-11-06, CC0 1.0, 5 files, none restricted: Multivariate Analysis.Rmd (68539 bytes), Time-Series Analysis.Rmd (40867), StateLeg_COVIDFacebookActivity.Rdata (158004), StateLeg_WeeklyCOVIDFacebookActivity.RData (459760), ReadMe File.txt (1460). All five downloaded with HTTP 200 and MD5s matching the metadata; sha256 in `data_statement_raw/prereg_downloads.sha256`.
   - Files the code reads vs files present. Every read call in both scripts (grep for `load(`, `read`, `import(`, `readRDS`, `fread`, `read.csv`):
     - `Multivariate Analysis.Rmd` line 27: `load("StateLeg_COVIDFacebookActivity.Rdata")`: present (object `by_leg`, 654 x 82, contains every model variable).
     - `Time-Series Analysis.Rmd` line 22: `load("StateLeg_WeeklyCOVIDFacebookActivity.RData")`: present (object `by_week`, 25451 x 78).
     - No other read call. All other file references are outputs (`ggexport`, `htmlreg(file=)`, `print(xtable, file=)`) into folders `Total Activity Analysis_RaceAndGender/` and `Total Activity Analysis_RaceAndGenderAndParty_v1/`, which are not in the deposit and must be created by the runner (README says so).
   - Not deposited, by the authors' own description: raw Facebook post text and the keyword-counting step (README: restricted, licensed). The code does not read them; the analysis starts from the deposited counts.
2a. Appendix PDF (checked, read). Contains the reported tables (A8, A10 used for targets); no data or code.
2b. Sage ZIP `sj-zip-2-...zip` (could NOT be checked). Attempts on 2026-10-10:
   - About 12:24 UTC, `curl -sL -A "Mozilla/5.0" "https://journals.sagepub.com/action/downloadSupplement?doi=10.1177%2F10659129241301785&file=sj-zip-2-prq-10.1177_10659129241301785.zip"`: HTTP 403, 5884-byte HTML (Cloudflare page), no archive.
   - About 12:18 to 12:22 UTC, Hark browser agent: the same downloadSupplement URL (3 navigations) and `https://journals.sagepub.com/doi/suppl/10.1177/10659129241301785/suppl_file/sj-zip-2-prq-10.1177_10659129241301785.zip` (1 navigation) timed out with no page change; clicking the ZIP link on the article page 3 times produced no download. Earlier the same day, routes via the Google Docs viewer, the DOI resolver and the r.jina.ai proxy returned a Cloudflare or Sage "cookieAbsent" interstitial.
   - Wayback Machine availability API for the Sage supplement and article PDF URLs: no snapshots (`archived_snapshots: {}`), about 12:00 UTC.
   - Its contents are therefore unknown. Its size (533.77 KB) is in the range of the compressed Dataverse files (728,630 bytes uncompressed in total), so it may be a copy of the replication package, but that is not established.

## Absence searches
None needed: the deposit contains every file the deposited code reads. This file makes no absence claim beyond "not deposited" items that the authors' own README describes as restricted, and "could not be checked" for the Sage ZIP.

## Finding
Deposit alone complete for the code as deposited: the article's statement names the Dataverse deposit (and the Sage online supplements), and the Dataverse deposit holds both data files that the two scripts read. The Sage ZIP named indirectly by "Supplemental material ... available online" could not be opened (Cloudflare), so whether it holds anything beyond the Dataverse files is unknown; this does not affect the materials rule because nothing the code reads is missing. Raw post text and keyword-coding code are not shared (restricted, per README), so the count variables themselves cannot be rebuilt.
