# DATA_STATEMENT: 04_PSHE5L (Rural Populism and Tolerance for Political Violence, Socius 2025, doi 10.1177/23780231251317227)

Written 2026-10-10 (IST). Checks run 2026-10-10 between 06:35 and 06:50 UTC (12:05 to 12:20 IST). No sign-in, no author contact. No classification or result file was changed.

## Source read
- Sage HTML full text, https://journals.sagepub.com/doi/10.1177/23780231251317227 , read via web_fetch fallback (direct curl returns HTTP 403; a browser session hit a Cloudflare interstitial). Saved: `data_statement_raw/sage_fulltext_webfetch.md` (143,672 bytes, sha256 18dfba5fada919c95cc1115308c2b930e1349305022972965df50ce2337704ea). The copy is complete: it contains all sections listed in the article's contents (Abstract through Supplementary Material), Tables 2 to 4 and the reference list.
- Not in Europe PMC or PMC (Europe PMC search by DOI: 0 hits, `europepmc_search.json`). OpenAlex lists only the publisher landing page (`openalex_work.json`).
- Supplementary file sj-docx-1-srd-10.1177_23780231251317227.docx: first pass (2026-10-10, about 06:40 UTC) could not read it. Second pass (2026-10-10, 10:10 to 10:25 UTC): READ IN FULL (26 pages) through the Google Docs viewer, https://docs.google.com/viewer?url=<the supplementary URL>, after every direct route was blocked. Routes and results:
  - Scripted (`scripts/p04_supplement_attempts.py`, output `data_statement_raw/supplement_access_attempts.json`): the supplementary file URL https://journals.sagepub.com/doi/suppl/10.1177/23780231251317227/suppl_file/sj-docx-1-srd-10.1177_23780231251317227.docx , the supplementary listing, the article landing page, https://doi.org/10.1177/23780231251317227 , and the Crossref text-mining links (full-xml, pdf) all return HTTP 403 with a Cloudflare "Just a moment..." page. Crossref, Unpaywall, OpenAlex and Semantic Scholar return HTTP 200 but list only the publisher landing page or PDF, no supplement copy. Wayback: no snapshot of the supplementary path (CDX search: HTTP 200, empty list; the availability API returned HTTP 404 "not found" to the script, and an earlier manual curl call to it returned an empty snapshot list).
  - Not scripted: the Hark fetch service returned "page extraction failed" for the file and the listing; figshare API search by article DOI and by title returned 0 results; a headless browser saw the Cloudflare interstitial on the direct URL (Ray IDs a484d823fd8af4e3, a484d8617b28f4e3), and the Office Online viewer returned an error.
  - What the supplement contains (notes: `data_statement_raw/supplement_read_2026-10-10.md`): section headings "Notes on Appendix Material", "Hypotheses for Each SEM Pathway", "Table Comparing Operationalization of Populism", "Extended Discussion on Data Collection", measurement, structural and robustness model sections with inline R code and output, "Overall Model Summary". Search inside the viewer for ICPSR, repository, doi, http, request, shared, OSF, github, deposit and dataverse: no match. It describes the survey (USPS Delivery Sequence File sample, rural counties in 11 western states, 2021) and the IRB approval (Yale Human Research Protection Program), but names no repository, URL, DOI or "on request" route for data or code.
  - Limit of this evidence: the docx itself could not be downloaded, so no sha256 of it is recorded; the reading is from the rendered viewer and is documented by the agent notes only.

## Verbatim statements
- The article has no Data Availability, Data and Code, or Replication statement. Its sections are: Abstract, Conceptualizing Populism, Operationalizing Grievance and Populism, Operationalizing Populism and Violence, Data and Methods, Results, Discussion and Conclusion, Acknowledgments, Funding, ORCID iDs, References, Biographies, Supplementary Material.
- Text search of the full HTML for osf, 10.7910, dataverse, github, zenodo, icpsr, "replication data/code/material", "on request", "upon request", "data availability": no hit in the article text (the only "request" is Sage's boilerplate about permission requests for supplemental material).
- Closest data-related sentence (Data and Methods): "Poststratification rake weights adjusted for demographics [...] (see the Supplemental Material for further data and institutional review board details)."
- Funding statement names NSF grant 2029990 ("RAPID: Impacts of COVID-19 Pandemic on Rural Attitudes about Federal Aid and Recovery"), with no data link.

## Locations the statement points to
None in the article text and none in the supplementary file. In particular, neither points to OSF, and neither cites the Harvard Dataverse deposit.

Links that exist but are not made by the article:
1. Harvard Dataverse doi:10.7910/DVN/PSHE5L (`dataverse_PSHE5L.json`): version 1, released 2024-11-07, 1 file ("Rural Populism - Socius - Public Code.R", 14,238 bytes), description "R code for replication.", no related-publication field, no OSF link in metadata.
2. OSF component "Rural Populism", https://osf.io/mtd4z/ (`osf_node_mtd4z.json`, `osf_node_mtd4z_files.json`): public, created 2024-11-13, modified 2025-01-11, empty description; child of OSF project 64ezg "Impact of Covid-19 in Rural America" (`osf_node_64ezg.json`, whose description refers to a different paper, "Impacts of Covid-19 in Rural America"). Files: the identical R script (14,238 bytes, sha256 955871dc...e7a5) and Rural_Populism_Dataset.csv (79,755 bytes, sha256 f839986a...b2ec). As PREREG.md section 0 already records, this component was found by browsing the team's other OSF project, not from the paper.

## Reachability check (2026-10-10)
- OSF API and both OSF download URLs reachable without sign-in: HEAD https://osf.io/download/wr3ve/ HTTP 200, content-length 79755; https://osf.io/download/6zsmv/ HTTP 200, content-length 14238.
- Dataverse PSHE5L API: status OK.

## Finding
Not confirmed: the article contains no data availability statement and does not point to OSF (or to Dataverse); the deposit alone is code only, and the data are complete only at an external location (OSF mtd4z) that the audit found by its own search, not by following the paper. The supplementary docx was read on 2026-10-10 and contains no data location either, so rule 4 (CHANGELOG_METHOD.md #4) still gives C; class and counts unchanged.

## Exact searches behind the absence claim (repeatable)
Every query, URL, time, HTTP status and result count: `ABSENCE_SEARCHES.md` (generated from `data_statement_raw/absence_searches.json` by `scripts/absence_searches.py 04` and `scripts/make_absence_md.py`, run 2026-10-10). Supplement routes: `data_statement_raw/supplement_access_attempts.json`.
