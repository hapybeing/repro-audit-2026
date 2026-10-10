# DATA_STATEMENT: 15_1BBC4E (Electoral autocracies, hybrid regimes, and multiparty autocracies: same, same but different?, Democratization 2025, doi 10.1080/13510347.2025.2476183)

Written 2026-10-10 (IST, about 21:15). Checks run 2026-10-10 between about 15:28 and 15:36 UTC. No sign-in, no author contact. Written before any analysis code was run.

## Source read
- Publisher PDF, https://www.tandfonline.com/doi/pdf/10.1080/13510347.2025.2476183 , read as extracted text via the web_fetch tool (direct curl download: HTTP 403, Cloudflare; no PDF bytes saved, no sha256).
- Publisher HTML full text, https://www.tandfonline.com/doi/full/10.1080/13510347.2025.2476183 (extracted text in scratch, sha256 bcf3c791c59d7f6e117bfc5b387b0b644328fd333e5e47916140f0ba55ee76e7).
- Not in Europe PMC (REST search `DOI:10.1080/13510347.2025.2476183`, 0 hits). OpenAlex (`data_statement_raw/openalex_work.json`): hybrid OA, CC BY, OA URL is the publisher PDF, no repository copy.
- Short excerpt saved: `data_statement_raw/statement_excerpt.txt`.

## Verbatim statement
The article has no section titled "Data availability". The data/code pointer is on the first page (p. 1565), in the footer block under the CONTACT line:

"Replication data: https://doi.org/10.7910/DVN/1BBC4E"

Directly above it, same location: "Supplemental data for this article can be accessed online at https://doi.org/10.1080/13510347.2025.2476183" (repeated in the HTML "Supplemental Material" section, which links "Download PDF (214.4 KB)", file fdem_a_2476183_sm8178.pdf).

## Locations the statement points to
1. Harvard Dataverse doi:10.7910/DVN/1BBC4E (the audited deposit). Checked: yes.
2. Taylor & Francis supplemental material (online appendix PDF) at the article DOI. Checked: the link exists, but the file could not be read (curl HTTP 403 at about 15:35 UTC; web_fetch extraction failed). It is described as "Supplemental data"; from the main text it holds the appendices (A to K). No script reads any file from it. Whether it names a further data location could not be determined.
No other location (OSF, GitHub, "on request") is named in the main text (searched the extracted PDF and HTML text for "osf", "github", "request", "dataverse", "replication": only the Dataverse DOI above).

## Reachability and completeness check (Dataverse, 2026-10-10)
- API `https://dataverse.harvard.edu/api/datasets/:persistentId/?persistentId=doi:10.7910/DVN/1BBC4E` (`data_statement_raw/dataverse_1BBC4E.json`): HTTP 200, version 1.0, released 2025-09-19, 49 files, none restricted; publication field "IsSupplementTo" cites this article. All 49 files downloaded (HTTP 200); md5 of every file matches the metadata.
- Read calls in the scripts compared with files present (paths relative to the R project folder):

| script | file read | present in deposit? |
|---|---|---|
| Comparing Indices/Comparison.R, Share_Common_Sample.R, Agreement across all.R, Pairwise agreement.R (target path) | Data/Regimedata/Measures_merged.rds | yes (10992326) |
| Covariates/*.R (4 scripts) | Data/Regimedata/Measures_merged_covariates.rds | yes (10992279) |
| Data Preparation/Merging_measures.R | Data/Regimedata/lied6_4.rds, vdem13.rds, fh_23.rds, magaloni_awd1_0.rds, polity_v.rds, AF_1.rds, htw_ARD_6.rds, Miller_Strategic_Origins_Data.RData | yes (all 8) |
| Data Preparation/Merging_measures.R | Data/Regimedata/BMR_demcoding.csv | yes as original of ingested BMR_demcoding.tab (10992283, `?format=original`) |
| Data Preparation/add_covariates.R | Data/Covariates/ucdp-intrastate-count-onset.csv | yes as original of ingested .tab (10992285) |
| Data Preparation/add_covariates.R | Data/Regimedata/vdem13.rds; Data/Covariates/estimates_gdppc_model_combined_normal_noslope_gamma_lambda_additive_test_20220215.rds | yes (10992315; 10992324) |
| Replications/Kim/Kim_Replication_Data_Preparation.R | Data/Replication/Kim/nam_data.dta | yes as original of ingested nam_data.tab (10992292) |
| Replications/Kim/Kim_Replication_Analysis.R | Data/Replication/Kim/Kim_Replication_Ready.rda | yes (10992316) |
| Replications/Miller/Miller_Replication_Data_Preparation.R | Data//Replication/Miller/EAHumanDev_CPS_Replication.dta | yes as original of ingested .tab (10992311) |
| Replications/Miller/Replication Analysis.R | Data/Replication/Miller/Miller_Replication_Ready.rda | yes (10992304) |

Non-file dependencies (not data files): `Merging_measures.R` and `add_covariates.R` install the `democracyData` package from GitHub; `Kim_Replication_Data_Preparation.R` loads cshapes, maptools, rgeos. These affect only optional data preparation.

## Finding
Deposit alone complete for the files the code reads: every file read by any deposited script is in the Dataverse deposit (four of them under Dataverse's ingested .tab name, with the original format available via `?format=original`). No absence claim is made, so no absence search log is needed. One named location (the T&F supplemental appendix) could not be read; no script depends on it.
