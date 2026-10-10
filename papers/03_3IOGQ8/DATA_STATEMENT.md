# DATA_STATEMENT: 03_3IOGQ8 (Circular Engineered Sortase, JACS 2024, doi 10.1021/jacs.4c12585)

Written 2026-10-10 (IST). Checks run 2026-10-10 between 06:30 and 06:50 UTC (12:00 to 12:20 IST). No sign-in, no author contact, nothing downloaded except API metadata. No classification or result file was changed.

## Source read
- Europe PMC full text XML, PMC11638967 (CC BY 4.0): https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11638967/fullTextXML (saved: `data_statement_raw/europepmc_fulltext_PMC11638967.xml`).
- Publisher page https://pubs.acs.org/doi/10.1021/jacs.4c12585 read via web_fetch fallback (curl returns HTTP 403): same two Dataverse mentions, no "Data Availability" section, no PXD, MSV, PRIDE, MassIVE or ProteomeXchange text.
- The article has no separate Data Availability section. The only data pointers are two sentences in Experimental Methods, "Middle-Down Proteomics".

## Verbatim statements
- "Raw data (10.7910/DVN/3IOGQ8) was analyzed using Byonic MS/MS search engine (Protein Metrics) using the following settings: [...]"
- "Peptide spectrum matches (PSMs) from Byonic were exported and subsequently processed in R (4.3.2) using RStudio, custom scripts (available at 10.7910/DVN/3IOGQ8), and packages parallel (4.3.2), [...]"
- "Bottom-Up Proteomics" section: "Raw data was analyzed in Skyline and further processed with in-house software EpiProfile." (no location given for bottom-up data).
- Supporting Information: "Peptides identified and quantified in middle-down mass spectrometry (XLSX)" and an SI PDF, at https://pubs.acs.org/doi/10.1021/jacs.4c12585 .
- Dataset description on Dataverse (not the paper): "Raw and processed bottom-up and middle-down mass spectrometry data, and scripts used in said processing."

## Locations the statement points to
1. Harvard Dataverse doi:10.7910/DVN/3IOGQ8 (the audited deposit itself). Nothing else.
2. No ProteomeXchange/PRIDE/MassIVE accession, no GitHub, no "on request".

## Accession search (2026-10-10)
- Europe PMC text-mined accession annotations for PMC11638967 (`europepmc_annotations_accessions.json`): only 1UBQ (a PDB structure ID) and 10.7910/DVN/3IOGQ8. No PXD/MSV.
- Europe PMC database cross-links for PMID 39585806 (`europepmc_databaseLinks.json`): none.
- PRIDE Archive API v2 keyword search (`pride_v2_keyword_search.json`): 39585806, jacs.4c12585, 10.1021/jacs.4c12585, "circular engineered sortase", cW11, "sortase histone", Whedon, "middle-down TMT histone H3", "Corin MS275", EBZ_Cole, "histone H3 sortase chromatin", cut-and-paste. No relevant project (cW11 returns two unrelated projects, PXD010124 and PXD000008). PRIDE v3 search for Whedon: empty; for sortase: the same 6 unrelated projects listed by Agent B.
- PXD accessions surfaced by a web search, checked via https://www.ebi.ac.uk/pride/ws/archive/v2/projects/<ID> (`pride_v2_websearch_hit_check.json`): PXD049969 (Tholey, top-down sample prep), PXD046444 and PXD046357 (Guzman/Olsen, nDIA), PXD071607 (VVD-065), PXD058823 (Aurora kinase A), PXD048719 (Cole lab, mTORC2/Akt). None is this paper.
- Agent B's earlier searches (B/outputs/inputs_and_open_routes.json, 2026-10-09): ProteomeXchange PROXI and the full MassIVE listing (20,351 datasets) gave no dataset for this paper.
- Because no accession exists, the PRIDE /projects/<ID> and /files check for the missing input could not be run on a relevant project.

## Reachability of the pointed-to location (2026-10-10)
- DVN/3IOGQ8 (`dataverse_3IOGQ8.json`, `dataverse_3IOGQ8_versions.json`): status OK, version 1 only (released 2024-09-11), 3 files, 499,041,687 bytes, none restricted: two Thermo RAW files (253,010,642 and 245,887,307 bytes) and Byonic_Middle-Down_Processing_Notebook.Rmd (143,738 bytes).
- Missing input the deposited code needs (A/outputs/input_inventory.txt, B/outputs/inputs_and_open_routes.json): `Byonic_results.csv` (Byonic PSM export, read at Rmd line 498), the mzML.gz conversions (line 671 onward; could be regenerated from RAW with open tools), the real MS.Alias.name values, and the search FASTA. Also absent despite the dataset description: any processed table and all bottom-up data.
- The Byonic PSM export is not at the pointed-to location and not in any public proteomics repository found. Its size is unknown (never deposited anywhere, so nothing to measure).

## Finding
Needs external location that does not exist: the paper points only to the audited Dataverse deposit, which lacks the Byonic PSM export the code reads; no PRIDE/ProteomeXchange/MassIVE accession exists, so the missing input is not available at any pointed-to or discoverable location.

## Exact searches behind the absence claim (repeatable)
Every query, URL, time (UTC), HTTP status and result count, with the rule for what would count as a hit: `ABSENCE_SEARCHES.md`, generated from `data_statement_raw/absence_searches.json` by `scripts/absence_searches.py 03` and `scripts/make_absence_md.py` (run 2026-10-10). The searches listed above from the first pass are kept as written; the re-run reaches the same finding. The re-run covers ProteomeXchange PROXI (central index of PRIDE, MassIVE, jPOST, iProX, PeptideAtlas, Panorama), PRIDE Archive API v2 and v3, the full MassIVE dataset listing, the jPOST PROXI listing, the article's Supporting Information (PDF and XLSX, sha256 equal to PREREG.md) and the article full text, with 11 search terms including the raw-file prefix EBZ_Cole. The live SI zip from Europe PMC took longer than 110 s to stream, so the SI step read the members Agent A downloaded from the same URL on 2026-10-09 (sha256 recorded in the JSON).
