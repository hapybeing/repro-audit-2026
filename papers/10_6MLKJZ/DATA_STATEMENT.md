# DATA_STATEMENT: 10_6MLKJZ (Prioritizing exceptional social needs, Public Policy and Administration 41(1): 32-54, doi 10.1177/09520767231210025)

Written 2026-10-10 (IST, about 17:50), before any analysis code was run. Checks run 2026-10-10 between about 11:50 and 12:20 UTC. No sign-in, no author contact. Rule: CHANGELOG_METHOD.md #4 (materials = the deposit plus every location the article's own data/code statement points to) and #5a (absence claims backed by a repeatable search log).

## Finding

**No data availability statement found.** The article has no "Data availability", replication, or code statement, and names no data or code location (no Dataverse, OSF, GitHub, Zenodo or other repository, and no "available on request"). The online appendix has none either. So the statement points to no location, and the materials for rule #4 are the audited deposit only: Harvard Dataverse doi:10.7910/DVN/6MLKJZ. The link between article and deposit exists only on the Dataverse side (the dataset's publication field cites the article as "forthcoming", without a DOI).

**Deposit alone: every file the code reads is present.** Two of the four raw conjoint files differ from the code's paths in letter case only (`data_UHH.csv` and `data_HSVN.csv` in the deposit vs `data_uhh.csv` and `data_hsvn.csv` in the code). One upstream step is not in the deposit (a Stata do-file that made `survey_data.csv`, per a cached 2020 script header). The deposited code does not call it. See the table below.

## Where I looked for a statement

| source | how read | result |
|---|---|---|
| Sage HTML full text, https://journals.sagepub.com/doi/full/10.1177/09520767231210025 | Hark web fetch service, 2026-10-10 about 12:00 UTC. Whole page read: abstract, all body sections, end matter, footnotes 1-5, references, Supplementary Material box. Section list and end matter transcribed verbatim in `data_statement_raw/sage_html_structure_and_end_matter.md` | End matter: Declaration of conflicting interests, Funding, ORCID iD, Footnotes, References, Supplementary Material. No data/code statement |
| Sage PDF, https://journals.sagepub.com/doi/pdf/10.1177/09520767231210025 (23 pages) | Hark browser agent through the Google Docs viewer, 2026-10-10. Notes: `data_statement_raw/article_pdf_read_notes_2026-10-10.md` | No "Data availability", "Data availability statement" or "Replication" heading or text. The only nearby statement is "Supplemental material for this article is available online." (Supplemental Material, journal p. 50 per the notes; one line of the notes says PDF page 19, the summary says PDF page 20 / journal p. 50) |
| Online appendix, Sage supplementary file sj-pdf-1-ppa-10.1177_09520767231210025.pdf (5 pages) | Hark browser agent, Chrome PDF viewer via https://journals.sagepub.com/action/downloadSupplement?doi=10.1177%2F09520767231210025&file=sj-pdf-1-ppa-10.1177_09520767231210025.pdf , 2026-10-10. Transcript: `data_statement_raw/supplement_pdf_transcript_2026-10-10.md` | No statement and no repository named. External names are only DALIA Research, the ESOMAR Code and the German micro census |
| Crossref work metadata | `data_statement_raw/crossref_work.json` | `relation` field empty |
| Harvard Dataverse dataset metadata | `data_statement_raw/dataverse_6MLKJZ.json` | publication citation "Dietrich, B., Jankowski, M., Schnapp, K. & Tepe, M. (2023). Prioritizing Exceptional Social Needs. ... Public Policy and Administration, forthcoming." No DOI or URL |

Limits: no byte copy of the article PDF or HTML could be saved. Direct scripted requests to journals.sagepub.com get a Cloudflare 403 interstitial (`data_statement_raw/access_attempts.json`, made by `data_statement_raw/access_attempts.py`, about 11:54 UTC). So the term search below runs on our transcripts and reading notes, not on the publisher file. The "no statement" finding rests on two complete readings (HTML and PDF), one by me and one by the browser agent.

## Search log (repeatable)

Script: `data_statement_raw/statement_searches.py` (run from repo/). Output: `data_statement_raw/statement_searches.json` (exact URLs, UTC times, HTTP status, totals, hits). Last run 2026-10-10T12:17Z. Hit rule: a transcript line containing the term (case-insensitive); in the repository searches, an item whose title contains "prioriti" and "social needs".

| source | query | URL | HTTP | total | relevant |
|---|---|---|---|---|---|
| transcript of Sage HTML end matter | "data availab", "availability", "replication", "dataverse", "osf", "github", "zenodo", "repository", "code", "syntax", "request" | local file | n/a | 0 for every term except "request" (1: Sage's generic licence sentence on re-use permission requests) | 0 |
| PDF reading notes and appendix transcript | same terms | local files | n/a | the only lines that match are the browser agent's own statements that no such statement exists (listed in the JSON) | 0 |
| Harvard Dataverse search API | "10.1177/09520767231210025" | https://dataverse.harvard.edu/api/search?q=%2210.1177%2F09520767231210025%22&type=dataset&per_page=100 | 200 | 0 | 0 |
| Harvard Dataverse search API | "Prioritizing Exceptional Social Needs" | https://dataverse.harvard.edu/api/search?q=%22Prioritizing+Exceptional+Social+Needs%22&type=dataset&per_page=100 | 200 | 1 | 1 (doi:10.7910/DVN/6MLKJZ, the audited deposit) |
| OSF API v2 public nodes | title filter "Prioritizing exceptional social needs" | https://api.osf.io/v2/nodes/?filter%5Btitle%5D=Prioritizing+exceptional+social+needs | 200 | 0 | 0 |
| GitHub repository search API | Prioritizing exceptional social needs | https://api.github.com/search/repositories?q=Prioritizing+exceptional+social+needs | 200 | 0 | 0 |
| Zenodo records API | both queries above | https://zenodo.org/api/records?q=... | 400 (request rejected; no result) | n/a | not established |
| Crossref relation field | 10.1177/09520767231210025 | https://api.crossref.org/works/10.1177/09520767231210025 | 200 | 0 | 0 |

The repository searches are context only. Under rule #4 a location we find ourselves would not count anyway, and none was found apart from the audited deposit. The Zenodo query failed (HTTP 400), so absence on Zenodo is not established.

## Locations named by the statement

None (no statement). The deposit checked: Harvard Dataverse doi:10.7910/DVN/6MLKJZ, version 1.0, released 2023-10-08, 71 files, none restricted, CC0 1.0. All 71 files were downloaded on 2026-10-10 (sha256 in `prereg_download_checksums.sha256`).

## Files the code reads vs files in the deposit

| script, line | read call | path the code uses | in deposit? |
|---|---|---|---|
| 01_preparation_function.R 33-36, 47 | `fread(x)` over `four_surveys` | `../data/conjoint_data/raw_data/data_rh.csv` | yes, `data/conjoint_data/raw_data/data_rh.csv` (id 7451193, stored as .tab; original CSV via `?format=original`) |
| same | same | `../data/conjoint_data/raw_data/data_uhh.csv` | present as `data_UHH.csv` (id 7451201): **case differs**; resolves on Windows/macOS, not on case-sensitive Linux |
| same | same | `../data/conjoint_data/raw_data/data_hsvn.csv` | present as `data_HSVN.csv` (id 7451141): **case differs**, as above |
| same | same | `../data/conjoint_data/raw_data/data_civic.csv` | yes (id 7451176, .tab; original CSV) |
| 01_preparation_function.R 69-78 | `write.table` then `cjoint::read.qualtrics` | `../data/conjoint_data/prep_data/prep_csv_<rh,uhh,hsvn,civic>.csv` | written by the code before it is read; deposited copies also present (ids 7451179, 7451177, 7451165, 7451192) |
| 03_data_prep_and_merge.R 21 | `data.table::fread` | `../data/survey_data/survey_data.csv` | yes (id 7451197, stored as `survey_data.tab`; original CSV via `?format=original`) |
| 04_analysis.R | no read calls; uses objects from 01-03; `ggsave` to `../figures/*.png` | n/a | the 7 output PNGs are deposited |

Not read by the code: `survey_data.dta` (id 7451152; Dataverse label `survey_data-1.tab`), the 7 figure PNGs, `analysis.Rproj` and 49 RStudio state files.

Upstream step not deposited (observation, not a missing read): the cached 2020 header of `03_data_prep_and_merge.R` (`.Rproj.user/6797E066/sources/session-e08d5f22/4E5BB0CC-contents`) gives its input as "C2_2.csv (erzeugt ?ber C2_1_Conjoint.do)". No `.do` file, and no file named C2_1_Conjoint or C2_2, is in the deposit file list (`data_statement_raw/dataverse_6MLKJZ.json`). The deposited 03 script reads `survey_data.csv` instead, which is present. The paper's cleaning steps that the R code does not perform (speeder control, inconsistent-pattern checks, German-nationality restriction; see PREREG.md section 1) may have been done in that step or before export. Whether the deposited raw files already reflect them will only be known from the runs.

## Note for classification (judgment call, flagged)

The article cites no data location, as in batch 1 paper 04. The difference is that here the deposit itself holds all the data and code the scripts read. Whether rule #4 gives a C for "no statement" alone, or only when the deposit is incomplete, should be checked against the wording applied in batch 1 (`batches/batch1_class_rules.json`). I did not open that file (I kept to the files the brief lists).
