# DATA_STATEMENT: 14_CJISMY (Intra-ethnic divisions and disagreement over self-determination demands in ethnic movements, PSRM 2025, doi 10.1017/psrm.2024.33)

Written 2026-10-10 (IST). Checks run 2026-10-10 between 15:28 and 15:35 UTC (about 21:00 IST). No sign-in, no author contact, no analysis code run.

## Source read
- Cambridge Core publisher PDF (open access, CC BY-NC 4.0): https://www.cambridge.org/core/services/aop-cambridge-core/content/view/A01DEE38CA7EDB4CB3A63735B6033E60/S2049847024000335a.pdf/div-class-title-intra-ethnic-divisions-and-disagreement-over-self-determination-demands-in-ethnic-movements-div.pdf , HTTP 200, 278,790 bytes, sha256 dd635403b6d4affbee10f8148fc5f236c5e56843c39feb84a31cd5ff219e3b78 (same file as in PREREG.md). Short excerpt: `data_statement_raw/statement_excerpt.txt`.

## Verbatim statement (journal p. 829, PDF p. 15, after the Conclusion)
"To obtain replication material for this article, see https://doi.org/10.7910/DVN/CJISMY. The updated EPR-O data can be found at https://doi.org/10.7802/2767."

Related lines elsewhere in the article: p. 821 (Section 3.1), on the expanded EPR-O dataset: "It is available at https://doi.org/10.7802/2767."; p. 815, footnote 1: "All hypotheses and variables were pre-registered at the Open Science Foundation at https://osf.io/8z6ng."; p. 829: "The supplementary material for this article can be found at https://doi.org/10.1017/psrm.2024.33."

## Locations the statement points to
1. Harvard Dataverse doi:10.7910/DVN/CJISMY (the audited deposit), "replication material".
2. GESIS Data Archive doi:10.7802/2767, "the updated EPR-O data".
(The OSF link is a pre-registration, not named as a data or code location; the supplementary-material DOI is the article page with the appendix. Both are listed below for completeness but are not counted as data locations.)

## Checks per location
1. Dataverse CJISMY (`data_statement_raw/dataverse_CJISMY.json`): checked. Version 1, released 2024-07-03, 44 files (25 R scripts, readme.txt, codebook PDF, 5 ingested `.tab` data files with CSV originals, 12 `.csv.gz` data files), 265,536,687 bytes, none restricted, all public, CC0 1.0. Files are flat (no folders); scripts read `data/<name>.csv`, which is a path and format matter (originals available via `?format=original`), not a missing file.
2. GESIS doi:10.7802/2767: partly checked. DataCite resolves it (HTTP 200) to "Ethnic Power Relations - Organizations (EPR-O) Dataset", GESIS Data Archive, 2024, version 1.0.0, landing URL https://search.gesis.org/research_data/SDN-10.7802-2767 . The landing page returned HTTP 403 to scripted requests (curl, 2026-10-10 about 15:33 UTC), so its file list was not read. No deposited script reads a file from GESIS by name; the deposit itself carries `epro_t.tab` (original `epro_t.csv`), which readme.txt calls the updated EPR-O data in raw format.
3. (Not a data location) OSF node 8z6ng: public project "Heterogeneity in Autonomy and Secession Demands project", one file `prereg_osf_upload.pdf`, no child components.

## Script read calls compared with files present
Read calls found by `grep` for read_csv, read.csv, rast, st_read, source, load in all 25 scripts.

| script | file read (line) | present in deposit? |
|---|---|---|
| crosssection_linear.R (headline, Table 1), and the other main-results scripts in the readme (panel_linear_probability.R, panel_logistic.R, panel_linear_probability_only_variation.R) | `funs_and_constants.R`; `data/epro_data_h1.csv`, `data/epro_data_h2.csv`, `data/epro_geo_data_h3.csv` (lines 13-18 in crosssection_linear.R) | yes (`funs_and_constants.R`; data as `epro_data_h1.tab`, `epro_data_h2.tab`, `epro_geo_data_h3.tab` with CSV originals) |
| crosssection_linear_gov_inclusion.R, crosssection_weighted_share.R, analysis_fragmentation_orgs.R, multilevel_models.R, descriptives_summary_tables.R, h1_robustness_*.R, robustness_agri_thresholds.R, robustness_centrifugal_centripetal.R, robustness_h2_*.R | same three CSVs and `funs_and_constants.R` (h1 or h2 only for some) | yes |
| robustness_no_low_confidence.R, robustness_no_multiethnic.R, robustness_no_temp_links.R, robustness_only_viol_elec.R | `data/epro_*_<variant>.csv.gz` (12 files) | yes, all 12 |
| all_models_crossectional.R (line 13), crosssection_max_disagreement.R (line 13) | `source("C:/Users/Frederik Gremler/Documents/paper_content_lea/analysis/helper_functions_eo2_extraction_analysis.R")` | no |
| agricultural_variables_epr_desc.R (line 5) | `C:/Users/Frederik Gremler/Documents/paper_secession/data_raw/data.csv` | no |
| spatial_hhi_h3.R (lines 14, 17, 85) | `data_raw/gpw-v4-population-count-rev11_2000_30_min_tif/gpw_v4_population_count_rev11_2000_30_min.tif`; `C:/Users/Frederik Gremler/Documents/paper_adoption/data/GeoEPR-2019.csv`; `data_raw/EPR_merged.csv` | no (its output `hhi.csv` is deposited as `hhi.tab`) |

The headline script and every script the readme lists for the main results read only files that are in the deposit. The missing files are read only by scripts outside that list: a descriptive check written for the pre-registration (`agricultural_variables_epr_desc.R`, a single `table()` call), the construction of the deposited `hhi.csv`, and two cross-sectional scripts that source a local helper file. Whether those two scripts feed an appendix table was not established (the appendix was not opened). The construction of the analysis files `epro_data_h*.csv` from raw EPR-O is not in the deposit.

## Searches for the missing files (repeatable)
Script: `data_statement_raw/absence_searches_14.py`; full output with per-query UTC timestamps, HTTP status, totals and returned names: `data_statement_raw/absence_searches.json`. All run 2026-10-10 at 15:34 UTC. Hit rule: a file with exactly the missing name, in a dataset or repository linked to these authors or this article.

| source | query | URL | HTTP | results | hits |
|---|---|---|---|---|---|
| Harvard Dataverse Search API | fileName:"helper_functions_eo2_extraction_analysis.R", type=file | https://dataverse.harvard.edu/api/search?q=fileName%3A%22helper_functions_eo2_extraction_analysis.R%22&type=file&per_page=100 | 200 | 0 | 0 |
| Harvard Dataverse Search API | fileName:"GeoEPR-2019.csv", type=file | https://dataverse.harvard.edu/api/search?q=fileName%3A%22GeoEPR-2019.csv%22&type=file&per_page=100 | 200 | 0 | 0 |
| Harvard Dataverse Search API | fileName:"EPR_merged.csv", type=file | https://dataverse.harvard.edu/api/search?q=fileName%3A%22EPR_merged.csv%22&type=file&per_page=100 | 200 | 0 | 0 |
| Harvard Dataverse Search API | fileName:"gpw_v4_population_count_rev11_2000_30_min.tif", type=file | https://dataverse.harvard.edu/api/search?q=fileName%3A%22gpw_v4_population_count_rev11_2000_30_min.tif%22&type=file&per_page=100 | 200 | 0 | 0 |
| Harvard Dataverse Search API | fileName:"data.csv", type=file | https://dataverse.harvard.edu/api/search?q=fileName%3A%22data.csv%22&type=file&per_page=100 | 200 | 623 | 0 (none in a dataset whose title matches the article or EPR-O; only the first 100 were screened) |
| Harvard Dataverse Search API | authorName:"Gremler", type=dataset | https://dataverse.harvard.edu/api/search?q=authorName%3A%22Gremler%22&type=dataset&per_page=100 | 200 | 2 | 0 (CJISMY itself and doi:10.7910/DVN/PGEGXZ, a different article) |
| OSF API | osfstorage listing of node 8z6ng | https://api.osf.io/v2/nodes/8z6ng/files/osfstorage/ | 200 | 1 | 0 (only `prereg_osf_upload.pdf`) |
| OSF API | child components of node 8z6ng | https://api.osf.io/v2/nodes/8z6ng/children/ | 200 | 0 | 0 |
| GitHub repository search API (unauthenticated; code search needs sign-in) | helper_functions_eo2_extraction_analysis | https://api.github.com/search/repositories?q=helper_functions_eo2_extraction_analysis | 200 | 0 | 0 |
| GitHub repository search API | EPR-O disagreement self-determination | https://api.github.com/search/repositories?q=EPR-O+disagreement+self-determination | 200 | 0 | 0 |
| GitHub repository search API | Gremler EPR | https://api.github.com/search/repositories?q=Gremler+EPR | 200 | 0 | 0 |
| DataCite API | doi 10.7802/2767 | https://api.datacite.org/dois/10.7802/2767 | 200 | 1 | n/a (resolves to the EPR-O dataset; file list not readable, landing page HTTP 403) |

Limits: the `data.csv` search screened only the first 100 of 623 results; GitHub code search and the GESIS file list were not reachable without sign-in or past a 403. GeoEPR-2019 and GPW v4 are public third-party datasets that may be obtainable from their producers, but the article's statement does not point to them; under rule #4 they would not count.

## Finding
Headline: complete. The statement's main location (Dataverse CJISMY) holds every file read by `crosssection_linear.R` (Table 1) and by all scripts the readme lists for the main results.
Not complete for the whole deposit: five files read by four non-headline scripts are not in the deposit or in any searched location (the helper script `helper_functions_eo2_extraction_analysis.R`, `data_raw/data.csv`, `GeoEPR-2019.csv`, `EPR_merged.csv`, the GPW v4 2000 raster). The second named location (GESIS EPR-O) resolves but its files could not be listed by script.
