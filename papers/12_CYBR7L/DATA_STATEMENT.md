# DATA_STATEMENT: 12_CYBR7L (Dominating the Narrative, PS: Political Science & Politics 2026, doi 10.1017/S1049096526102029)

Written 2026-10-10 (IST), before any analysis code was run. Checks run 2026-10-10 between about 15:25 and 15:35 UTC (20:55 to 21:05 IST). No sign-in, no author contact.

## Source read
- Publisher open-access PDF (CC BY 4.0), https://www.cambridge.org/core/services/aop-cambridge-core/content/view/85A7AE39961CEEB5C533F9C735533086/S1049096526102029a.pdf/div-class-title-dominating-the-narrative-how-scholars-outside-of-africa-define-african-politics-in-the-top-political-science-journals-div.pdf : HTTP 200, 5,098,593 bytes, 11 pages, sha256 a89bc3aaf813b209ead80f53d834d8df70eb4c3deb7ec9d314b2b43e5a1cdf90 (same file as in PREREG.md). Excerpt: `data_statement_raw/statement_excerpt.txt`.
- Online appendix PDF, https://static.cambridge.org/content/id/urn%3Acambridge.org%3Aid%3Aarticle%3AS1049096526102029/resource/name/S1049096526102029sup001.pdf : HTTP 200, 352,178 bytes, sha256 a90b30399c0a5b79c6e81dd028d9757e7b2745f2ef900413c4efd3c67971c0b1. Searched for "dataverse", "osf", "github", "figshare", "zenodo", "request", "available": no data or code location named (its only "available" mentions are the journal-ranking source and a remark that no public dataset of author nationality exists).
- Metadata: Crossref (`data_statement_raw/crossref_work.json`), OpenAlex (`data_statement_raw/openalex_work.json`), Dataverse (`data_statement_raw/dataverse_CYBR7L.json`).

## Verbatim statement (p. 712, "DATA AVAILABILITY STATEMENT")
"Research documentation and data that support the findings of this study are openly available at the PS: Political Science & Politics Harvard Dataverse at https://doi.org/10.7910/DVN/CYBR7L."

The same deposit is cited in Data and Methods (p. 704, "(Zimbalist and Omodei 2026)") and in the reference list (p. 713). The article names no other data or code location. It describes the data as drawn from SciSciNet (Lin et al. 2023), cited as a source, not as a location of the replication materials.

## Locations the statement points to
1. Harvard Dataverse doi:10.7910/DVN/CYBR7L (the audited deposit). Checked: yes.

## Reachability and completeness check (2026-10-10)
- Dataverse API: status OK, version 1, released 2026-02-06, 4 files, none restricted: README.txt, replication_code.ipynb, SciSciNet_AfricanPolitics_Data (original .csv), SciSciNet_AfricanPolitics_CitingCited (original .csv). All four downloaded with HTTP 200; sizes and sha256 in PREREG.md.
- Files the code reads compared with files present (from reading the notebook, not running it):

| read call in `replication_code.ipynb` | file in deposit | present |
|---|---|---|
| cell 2: `pd.read_csv('SciSciNet_AfricanPolitics_Data.csv')` | SciSciNet_AfricanPolitics_Data.csv (datafile 13378108, original format) | yes |
| cell 5: `pd.read_csv('SciSciNet_AfricanPolitics_CitingCited.csv')` | SciSciNet_AfricanPolitics_CitingCited.csv (datafile 13378106, original format) | yes |

  The notebook has no other read call (no `open(...)` in read mode, no other `read_*`). Its two `open(..., 'w')` calls and `savefig` calls write outputs.
- Upstream source named in README.txt (not in the article's statement, not read by the code): SciSciNet, https://doi.org/10.6084/m9.figshare.c.6076908 . Checked only that it resolves: doi.org returned HTTP 302 to springernature.figshare.com collection 6076908. Not needed to run the notebook.

## Not covered by the deposit (described, no absence search needed)
The notebook produces Figures 1 to 6 and Tables 1 and 2 of the article. The appendix Tables A.1 to A.6 and Figures A.1 to A.5 are not produced by it. Appendix Table A.4 is based on a different sample (165 of 3297 authors in 1956-2021, African studies outlets) that the README does not describe as part of the deposit, and Tables A.5 and A.6 add an author (Kimuli Kasara) whose name does not appear in either deposited CSV (grep, 0 hits). No appendix number is a target, and no file the code reads is missing, so no external absence search was run.

## Finding
Deposit alone complete for the targets: the statement points only to the audited Dataverse deposit, which holds the notebook and both files it reads.
