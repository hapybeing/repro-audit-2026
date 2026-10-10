# DATA_STATEMENT: 09_4U8CTG (Blinded by out-group hatred, European Political Science Review 2026, doi 10.1017/S1755773926100575)

Written 2026-10-10 (IST, about 17:35). Checks run 2026-10-10 between about 11:50 and 11:58 UTC (17:20 to 17:28 IST). No sign-in, no registration, no author contact. Rule: CHANGELOG_METHOD.md #4 (materials = deposit plus every location the article's own statement names) and #5 (absence claims backed by a repeatable search log).

## Source read
- Article PDF, Cambridge Core (gold OA, CC BY 4.0): https://www.cambridge.org/core/services/aop-cambridge-core/content/view/F3C7D48398A9094C5F890832A7A876BF/S1755773926100575a.pdf/div-class-title-blinded-by-out-group-hatred-why-does-radical-party-entry-fail-to-boost-its-voters-satisfaction-with-democracy-div.pdf : HTTP 200, 589,781 bytes, sha256 27dbe332769586d1979272ef0b94c5ee6aed0b23403d39bd4d6939732d70fcaa (per-download stamp on each page, so the hash is download-specific). Text: `data_statement_raw/paper_pdftotext.txt`; excerpt: `data_statement_raw/statement_excerpt.txt`.
- OpenAlex record: `data_statement_raw/openalex_work.json`.

## Verbatim statement (p. 21, "Data availability statement", after "Supplementary material")
"Data for Study 1 are drawn from the 2022 French Election Study (FES), available upon registration at the Sciences Po ELIPSS repository: https://data.sciencespo.fr/dataverse/elipss.
The quantitative data and replication files for Study 2 are publicly available at the Harvard Dataverse: https://doi.org/10.7910/DVN/4U8CTG. The replication files include a preprocessing script for waves 3 and 4 of the 2022 FES, required to replicate the analyses for Study 1.
The qualitative data for Study 2 are not publicly available in order to protect respondents' privacy and anonymity, but may be obtained from the corresponding author upon reasonable request."

Other text that bears on it: footnote 6 (p. 10) names the experiment's pre-analysis plan at https://osf.io/b4tjr (a plan, not data or code). Text p. 8 calls the FES "a publicly available representative panel survey".

## Locations the statement names
1. Harvard Dataverse doi:10.7910/DVN/4U8CTG (the audited deposit): Study 2 data and all scripts.
2. Sciences Po ELIPSS repository, https://data.sciencespo.fr/dataverse/elipss : Study 1 FES 2022 data, "upon registration".
3. Corresponding author, on request: Study 2 qualitative (open-ended) answers. Not contacted (audit rule).

## Check of each location

### 1. Harvard Dataverse 4U8CTG
Checked. Metadata API: status OK, version 1.0, published 2026-06-12, 66 files, none restricted (`data_statement_raw/dataverse_4U8CTG.json`). Every non-image file downloaded; sha256 in PREREG.md.

Script read calls versus files present:

| script, line | reads | in deposit? |
|---|---|---|
| 00, line 51 | `raw_data/elipss_fes2022_v3.csv` | no (README: download from ELIPSS) |
| 00, line 64 | `raw_data/elipss_fes2022_cses_v4.csv` | no (README: download from ELIPSS) |
| 01, line 108; 02, line 146 | `data/study1_fes_panel.csv` | no (written by 00, line 198) |
| 02, line 148 | `data/study1_fes_panel_long.csv` | no (written by 00, line 229) |
| 01, line 111; 02, line 143 | `data/study2_experiment_data.csv` | yes (ingested as .tab; original CSV served with `?format=original`, 62,782 bytes) |
| 01, line 115; 02, line 144 | `data/study2_experiment_data_long.csv` | yes (original CSV, 120,509 bytes) |
| 02, line 145 | `data/pilot_study_data.csv` | yes (original CSV, 24,373 bytes) |
| 02, lines 152 to 153 | `data/study2_qualitative_answers_proportions.csv` | yes |
| 02, lines 154 to 155 | `data/study2_qualitative_answers_icr.rds` | yes |

The columns used by the target models (`block`, `treatment`, `swd_ch`, `affect_LREM_ch`, `swd_w1`, `swd_w2`, `affect_LREM_w1`, `affect_LREM_w2`, `age`, `gender`, `educ`, `income`, `zemmour_winner2ndr`, `opened_quest`) are in the header of `study2_experiment_data.csv`. The file also has an `opened_quest` column (open-ended text); README says the coded responses underlying Appendix C are not included. Not examined further; no target uses it.

Finding for the deposit: complete for Study 2; the four Study 1 inputs are absent, as the README and statement say.

### 2. Sciences Po ELIPSS (Study 1)
Checked, without an account.
- The FES 2022 datasets exist: wave 3 doi:10.21410/7E4/DST7ZY ("French Election Study 2022, Vague 3 (ELIPSS 2022)") and wave 4 doi:10.21410/7E4/W76IMT ("French Election Study 2022, Vague 4 (ELIPSS 2022)"), both licence CC BY-SA 4.0, `fileAccessRequest` true (`data_statement_raw/elipss_DST7ZY.json`, `elipss_W76IMT.json`).
- Wave 3: the CSV zip (id 5296) and the .tab files (5298, 5301) are flagged restricted; an anonymous request to 5296 returned HTTP 403 "Not authorized". One SAS file (id 5297, `fr.cdsp.ddi.elipss.fes3_2022_V3.sas.zip`) is flagged unrestricted and downloaded with HTTP 200 (312,170 bytes, sha256 aba2ca63...ccd56); its listing shows a SAS program and a `.sas7bdat` data file. It was listed only, then deleted, and not used: it is not the CSV the code reads, and wave 4 is needed anyway.
- Wave 4: all data files (5346, 5348, 5349, 5350) are flagged restricted; an anonymous request to 5346 returned HTTP 403.
- Public DDI codebooks (ids 11115, 11116) list the variable names that 00 selects (`UID_fes3`, `fes3_QA04_C`, `UID_fes4`, `POIDS_fes4`, `fes4_Q22`, `fes4_Q04a`, `fes4_Q07a`...`fes4_Q07g`, `fes4_Q10p1`, `fes4_Q10p2`, `fes4_Q16b/c/g/h`). The `.a` / `.b` suffixed names read at 00 lines 79 to 82 could not be checked without the data.
- File names differ: the code expects `elipss_fes2022_v3.csv` and `elipss_fes2022_cses_v4.csv`; ELIPSS serves `fr.cdsp.ddi.elipss.fes3_2022_V3.csv.zip` and `fr_cdsp_ddi_elipss_202204fes4_cses.zip` (and others). A user must download, unzip and rename.
- All probes: `data_statement_raw/elipss_access_checks.json`.

Finding for ELIPSS: the location exists and appears to hold the needed data, but the data files require registration (as the statement says). Not obtainable under the audit's no-sign-in rule, so Study 1 (targets T5, T6) cannot be run.

### 3. Corresponding author (qualitative data)
Not checked (author contact is not allowed). No target depends on it.

## Searches for the missing Study 1 files (rule #5)
Rule for a hit: a publicly downloadable copy of `study1_fes_panel.csv`, `study1_fes_panel_long.csv`, `elipss_fes2022_v3.csv` or `elipss_fes2022_cses_v4.csv`, or an unrestricted FES 2022 wave 3 and wave 4 data file in a format the 00 script can read after renaming. Script: `data_statement_raw/search_elipss.py`; raw responses: `data_statement_raw/elipss_searches.json`. All via the Dataverse Search API, unauthenticated, User-Agent "repro-audit-2026".

| UTC time | query URL | HTTP | result count |
|---|---|---|---|
| 2026-10-10T11:55Z | https://data.sciencespo.fr/api/search?q=elipss_fes2022_v3&type=file&per_page=50 | 200 | 0 |
| 2026-10-10T11:55Z | https://data.sciencespo.fr/api/search?q=elipss_fes2022_cses_v4&type=file&per_page=50 | 200 | 0 |
| 2026-10-10T11:55Z | https://data.sciencespo.fr/api/search?q=French+Election+Study+2022&type=dataset&per_page=50 | 200 | 559 (top hits: FES 2022 waves 1 to 5, incl. DST7ZY and W76IMT) |
| 2026-10-10T11:55Z | https://data.sciencespo.fr/api/search?q=FES+2022+ELIPSS&type=dataset&per_page=50 | 200 | 203 (FES 2022 waves and ENEF 2022 waves) |
| 2026-10-10T11:55Z | https://data.sciencespo.fr/api/search?q=Persico&type=dataset&per_page=50 | 200 | 8 (FES 2022 waves 1 to 5 among them) |
| 2026-10-10T11:55Z | https://dataverse.harvard.edu/api/search?q=%22study1_fes_panel%22&type=file&per_page=50 | 200 | 0 |
| 2026-10-10T11:55Z | https://dataverse.harvard.edu/api/search?q=elipss_fes2022&type=file&per_page=50 | 200 | 0 |

(Exact second-level timestamps are in `elipss_searches.json`.) Then the wave 3 and wave 4 file lists and access probes above (11:56 to 11:58 UTC). Result: no public copy of the four files found; the ELIPSS data files the code needs are restricted. This absence holds only within what was searched (the two Dataverse installations); general web search engines and OSF were not searched, and per rule #4 a copy found elsewhere would not count toward the class anyway.

## Finding
Partly complete. Study 2 (experiment; targets T1 to T4): complete in the deposit. Study 1 (FES panel; targets T5, T6): missing from the deposit by design; the statement points to ELIPSS, where the data exist but are registration-only, so they are not obtainable under audit rules. Qualitative raw answers: on request only (no target uses them).
