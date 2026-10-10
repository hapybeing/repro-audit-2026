# DATA_STATEMENT: 22_W2TSVL (Framing Labor Action, Perspectives on Politics 24(3), doi 10.1017/S1537592725000660)

Written 2026-10-11 (IST). Checks run 2026-10-10 between 20:38 and 20:41 UTC (2026-10-11 02:08 to 02:11 IST). No sign-in, no author contact, no analysis code run.

## Source read
- Publisher PDF, https://www.cambridge.org/core/services/aop-cambridge-core/content/view/6FA86B96F76F1A17BD7DF6E7B28910FD/S1537592725000660a.pdf/div-class-title-framing-labor-action-experimental-evidence-from-teachers-in-mexico-div.pdf : HTTP 200, 473,342 bytes, sha256 f92d18a5a84b22551a1ffd3b6e1b76ae39cb6f4ff9092ba50529f28b4db50d96 (same file as in PREREG.md). Short excerpt: `data_statement_raw/statement_excerpt.txt`.
- Publisher supplementary material S1537592725000660sup001.pdf (Appendix A and B), sha256 b72cfccc1bd5e0ca829a03f1ff0fc6548aa36e8394fe4f3815feb716087d2456. It names no data location.

## Verbatim statement (p. 1267, section "Data replication")
"Data replication sets are available in Harvard Dataverse at: https://doi.org/10.7910/DVN/W2TSVL"

The reference list (p. 1267) also cites the deposit: Chambers-Ju, Christopher, and Mart Trasberg. 2025. "Replication Data for: Framing Labor Action: Experimental Evidence from Teachers in Mexico." Harvard Dataverse. DOI: 10.7910/DVN/W2TSVL.

## Locations the statement points to
1. Harvard Dataverse doi:10.7910/DVN/W2TSVL (the audited deposit). This is the only data location the statement names.

Other links in the article that are not data locations (listed for completeness, not counted under CHANGELOG #4):
- OSF preregistration https://osf.io/azut2 ("The Moral Economy of Education Reform in Mexico", registered 2023-10-25), cited in the Acknowledgments. Checked via https://api.osf.io/v2/registrations/azut2/ (HTTP 200): its OSF storage holds one file, `UT-TEC VP_ Oct 18 2023_FINAL.docx` (99,018 bytes), no data or code (`data_statement_raw/osf_azut2.json`, `osf_files2.json`). Not downloaded.
- Supplementary material at http://doi.org/10.1017/S1537592725000660 (Appendix A tables and Appendix B on the treatments); no data files.

## Reachability and completeness check
- Dataverse API (`data_statement_raw/dataverse_W2TSVL.json`): HTTP 200, version 1, released 2025-04-23, 5 files, none restricted, licence CC0 1.0. Each file downloaded with HTTP 200 after the API's 303 redirect (sizes and sha256 in PREREG.md and `prereg_download_checksums.sha256`).
- Read calls in the code compared to files present:

| script | line | read call | file in deposit? |
|---|---|---|---|
| Framing Labor Action_R script.R | 14 | `read_dta(".../Analysis/OA23 Base UT-TEC.dta")` (absolute Windows path) | yes: datafile 10903648, original upload `OA23 Base UT-TEC.dta` (Dataverse shows it as `.tab`; stored md5 matches the .dta original) |
| Framing Labor Action_R script.R | 15 | `#dta <- read_dta("OA23 Base UT-TEC.dta")` (commented) | same file |
| Framing Labor Action_Appendix A1.R | 14 | `read_dta(".../Analysis/OA23 Base UT-TEC.dta")` (absolute Windows path) | same file |

  No other file is read (`grep -n "read_\|load(\|source(\|readRDS\|read\.\|fread"` over both scripts gives only these lines). Every variable the code uses is a column of the file.
- Not reproducible from the deposit alone, but not read by code: the census column of Table A5 comes from an external Data OPM / INEGI document (Appendix A1.R comment lines 301-302). This is not a file the code reads and is not a target.

## Finding
Deposit alone complete for the code: the statement points only to the audited Dataverse deposit, which holds the data file both scripts read, both scripts, a README and the appendix. The only gap between code and deposit is the absolute file path (a path-only fix). No absence search was needed, because no file the code reads is missing.
