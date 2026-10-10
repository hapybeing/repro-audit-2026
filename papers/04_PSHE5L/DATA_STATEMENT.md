# DATA_STATEMENT: 04_PSHE5L (Rural Populism and Tolerance for Political Violence, Socius 2025, doi 10.1177/23780231251317227)

Written 2026-10-10 (IST). Checks run 2026-10-10 between 06:35 and 06:50 UTC (12:05 to 12:20 IST). No sign-in, no author contact. No classification or result file was changed.

## Source read
- Sage HTML full text, https://journals.sagepub.com/doi/10.1177/23780231251317227 , read via web_fetch fallback (direct curl returns HTTP 403; a browser session hit a Cloudflare interstitial). Saved: `data_statement_raw/sage_fulltext_webfetch.md` (143,672 bytes, sha256 18dfba5fada919c95cc1115308c2b930e1349305022972965df50ce2337704ea). The copy is complete: it contains all sections listed in the article's contents (Abstract through Supplementary Material), Tables 2 to 4 and the reference list.
- Not in Europe PMC or PMC (Europe PMC search by DOI: 0 hits, `europepmc_search.json`). OpenAlex lists only the publisher landing page (`openalex_work.json`).
- Supplementary file sj-docx-1-srd-10.1177_23780231251317227.docx: NOT READ. curl, web_fetch and the browser were all blocked (HTTP 403 / Cloudflare); no Wayback snapshot exists. Earlier agents' logs (A/LOG.md, B/LOG.md) do not record reading it either.

## Verbatim statements
- The article has no Data Availability, Data and Code, or Replication statement. Its sections are: Abstract, Conceptualizing Populism, Operationalizing Grievance and Populism, Operationalizing Populism and Violence, Data and Methods, Results, Discussion and Conclusion, Acknowledgments, Funding, ORCID iDs, References, Biographies, Supplementary Material.
- Text search of the full HTML for osf, 10.7910, dataverse, github, zenodo, icpsr, "replication data/code/material", "on request", "upon request", "data availability": no hit in the article text (the only "request" is Sage's boilerplate about permission requests for supplemental material).
- Closest data-related sentence (Data and Methods): "Poststratification rake weights adjusted for demographics [...] (see the Supplemental Material for further data and institutional review board details)."
- Funding statement names NSF grant 2029990 ("RAPID: Impacts of COVID-19 Pandemic on Rural Attitudes about Federal Aid and Recovery"), with no data link.

## Locations the statement points to
None in the article text. In particular, the article does NOT point to OSF, and it does not cite the Harvard Dataverse deposit either. Whether the unread supplementary docx names a location is unknown.

Links that exist but are not made by the article:
1. Harvard Dataverse doi:10.7910/DVN/PSHE5L (`dataverse_PSHE5L.json`): version 1, released 2024-11-07, 1 file ("Rural Populism - Socius - Public Code.R", 14,238 bytes), description "R code for replication.", no related-publication field, no OSF link in metadata.
2. OSF component "Rural Populism", https://osf.io/mtd4z/ (`osf_node_mtd4z.json`, `osf_node_mtd4z_files.json`): public, created 2024-11-13, modified 2025-01-11, empty description; child of OSF project 64ezg "Impact of Covid-19 in Rural America" (`osf_node_64ezg.json`, whose description refers to a different paper, "Impacts of Covid-19 in Rural America"). Files: the identical R script (14,238 bytes, sha256 955871dc...e7a5) and Rural_Populism_Dataset.csv (79,755 bytes, sha256 f839986a...b2ec). As PREREG.md section 0 already records, this component was found by browsing the team's other OSF project, not from the paper.

## Reachability check (2026-10-10)
- OSF API and both OSF download URLs reachable without sign-in: HEAD https://osf.io/download/wr3ve/ HTTP 200, content-length 79755; https://osf.io/download/6zsmv/ HTTP 200, content-length 14238.
- Dataverse PSHE5L API: status OK.

## Finding
Not confirmed: the article contains no data availability statement and does not point to OSF (or to Dataverse); the deposit alone is code only, and the data are complete only at an external location (OSF mtd4z) that the audit found by its own search, not by following the paper. The supplementary docx could not be read and is the one remaining place a pointer could be.
