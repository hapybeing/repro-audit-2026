# DATA_STATEMENT: 19_KH0SQ2 (Quotas or parity?, Journal of European Public Policy, doi 10.1080/13501763.2024.2402864)

Written 2026-10-10 (IST), before any analysis code was run. Checks run 2026-10-10 between about 17:20 and 17:35 UTC (22:50 to 23:05 IST). No sign-in, no author contact.

## Finding
No data availability statement found. The article names no location for data or code. Under CHANGELOG #4(a) the materials for classification are the Harvard Dataverse deposit alone (doi:10.7910/DVN/KH0SQ2), which the article does not cite but which cites the article. That deposit contains every file the deposited code reads (see below), so the materials question for the targets is "deposit complete for the targets; article cites no data location".

## Where I looked
1. Publisher full-text HTML, https://www.tandfonline.com/doi/full/10.1080/13501763.2024.2402864 (direct curl: HTTP 403 from Cloudflare; read through the web_fetch tool, 169,418-byte text copy, sha256 22b24847e43104b2a8425d20294279d6435ed1bc8e364fff5efda2d53a2e016e, kept in scratch `/workspace/audit_runs/19_KH0SQ2/prereg/tandf_page.txt`). Its sections are Abstract, Introduction, two theory sections, Experimental design, Experimental results, Conclusion, Supplemental material, Acknowledgements, Disclosure statement, Additional information (Funding, Notes on contributors), Footnotes, References. There is no "Data availability statement" section. A pattern search (`data availability|availability of data|data and code|replication (data|materials|files)|dataverse|10.7910/DVN/KH0SQ2`, case-insensitive) gives 0 hits.
2. Publisher PDF (31 pages incl. cover, journal pp. 2409-2438), viewed in a browser without sign-in on 2026-10-10 (direct curl to https://www.tandfonline.com/doi/pdf/10.1080/13501763.2024.2402864 gives HTTP 403). Result: no section or sentence on data availability, replication, Dataverse or where data/code can be found. The space between the endnotes and the References (journal p. 2433) holds only Acknowledgements, Disclosure statement and Funding. Not downloaded, so no hash.
3. Crossref metadata, https://api.crossref.org/works/10.1080/13501763.2024.2402864 : HTTP 200, 0 pattern hits (no relation to a dataset).
4. Online Appendix PDF (figshare copy of the T&F supplement, https://ndownloader.figshare.com/files/49219486 , sha256 4f00b351cb593c5bd90d85a88df93b66c9c7f607414cbd03d2c9e7bab28040f2): HTTP 200, text layer 0 pattern hits. Its tables are images, so the image content was read visually for Tables S1 and S10 only; no data location appears in the prose.
5. Dataverse record (reverse link only, not an article statement): https://dataverse.harvard.edu/api/datasets/:persistentId/?persistentId=doi:10.7910/DVN/KH0SQ2 , HTTP 200, version 2 released 2024-07-11, 7 files, none restricted.

Exact queries, URLs, HTTP status and byte counts: `data_statement_raw/statement_searches.json`, produced by `data_statement_raw/statement_searches_19.py` (re-runnable). Note: in this sandbox `time.strftime(... gmtime())` returns an IST-formatted string, so the `utc` field reads "Sat 2026-10-10 11:03 PM IST (UTC+05:30)", which is 17:33 UTC. Short excerpts: `data_statement_raw/statement_excerpt.txt`.

## Verbatim statement
None. The only related sentences (not data statements):
- "Supplemental data for this article can be accessed online at https://doi.org/10.1080/13501763.2024.2402864 ." (Supplemental Material section of the HTML; front matter of the PDF.)
- Footnote 5: "We registered hypotheses related to this manuscript in the following pre-analysis plan: https://osf.io/6hfnt/?view_only=30a3981430324807a3eeddf5eb5686ce ."

## Locations the article names, and what they hold
| location | named where | checked | data or code there? |
|---|---|---|---|
| T&F supplemental material (doi landing page; file rjpp_a_2402864_sm5162.pdf, figshare 10.6084/m9.figshare.27036622) | "Supplemental data ..." line | yes, 2026-10-10 | one PDF (Online Appendix). No data, no code. |
| OSF pre-analysis plan, node 6hfnt (view-only link) | footnote 5 | yes, OSF API file listing, HTTP 200 | one file, `OSF_blind_2022.pdf` (pre-analysis plan). No data, no code. |

Neither is a data/code location, so rule #4 adds nothing to the materials beyond the deposit.

## Do the files the code reads exist in the deposit?
Every read call in the deposited scripts, against the files present (`grep -n "load(" *.R`):

| script | line | call | in deposit? |
|---|---|---|---|
| main_text_figs_JEPP_FINAL.R | 41 | `load("all_merged.RData")` | yes |
| main_text_figs_JEPP_FINAL.R | 634 | `load("yougov_uk_conjoint.RData")` | yes |
| main_text_figs_JEPP_FINAL.R | 666 | `load("FRCONJdataset.RData")` | yes |
| Appendix_plus.R | 6 (commented) | `#load("dataset.RData")` | yes |
| Appendix_plus.R | 18 (commented) | `#load("all_merged.RData")` | yes |
| Appendix_plus.R | 183 (commented) | `#load("FRdataset.RData")` | yes |
| Appendix_plus.R | 363, 391 (comments) | "load yougov_uk_conjoint.RData", "load FRCONJdataset.RData" | yes |
| Appendix_plus.R | 1248 | `load("all_merged.RData")` | yes |

No `read.*`, `readRDS` or `haven::read_*` calls. Name references that are not data reads: `Appendix_plus.R` l. 2 points to `main_text_figs_JEPP_R1` (deposited as `main_text_figs_JEPP_FINAL.R`, which has the Fig S12 code); l. 636 says "use appendix.r code", no file of that name is deposited, and the objects it refers to (`uksd`, `frsd`) are built later in `Appendix_plus.R` (l. 1059, 1100). Neither affects a target.

Because no file the code reads is missing, no absence search for a missing data file was needed. The only absence claim here is "no data availability statement", backed by the searches above.
