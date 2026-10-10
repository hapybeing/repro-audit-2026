# DATA_STATEMENT: 07_JH9DBC (Guilty by association, Party Politics 2025, doi 10.1177/13540688251366827)

Written 2026-10-10 (IST). Checks run 2026-10-10 between 11:50 and 12:20 UTC. No sign-in, no author contact. No analysis code was run.

## Sources read
- Publisher abstract page, https://journals.sagepub.com/doi/10.1177/13540688251366827 (public part; article itself is "Restricted access"). Read by public web fetch (about 11:51 UTC) and by a public browser session without sign-in (about 11:55 UTC); notes in `prereg_raw/browser_access_check_findings.md`.
- Publisher Supplementary Material PDF, `sj-pdf-1-ppq-10.1177_13540688251366827.pdf`, 15 pages, read page by page in a public browser session (about 12:00 to 12:10 UTC); `prereg_raw/browser_supplement_transcription.md`. Not downloadable to disk (Cloudflare 403), so no sha256.
- Not read: the main article body (paywalled; routes tried are listed in PREREG.md). The statement's footnote marker "*" points to a note whose text is not shown on the public page.

## Verbatim statement
Location: publisher article page, section "Data availability statement" (public abstract page):

"All data and materials used in this study will be made available in public repositories upon publication. *"

The page's "Information, rights and permissions" panel adds: "Data availability statement: Data is available for this article. View more information" (the link is behind the access wall).

## Locations the statement points to
1. "public repositories" (unnamed). The statement names no repository, URL or DOI. The supplement (all 15 pages) names no repository either: its "Dataset and codebook" section (p. iv) lists only original sources (INE, INEGI, "Own", eluniversal.com.mx).
2. The footnote behind "*" could not be read. If it names a location, that location is unchecked.

The audited deposit, Harvard Dataverse doi:10.7910/DVN/JH9DBC, is linked to the article from the Dataverse side: its metadata cite the article (relation "IsCitedBy", DOI 10.1177/13540688251366827) and its description reads "This is the replication material for: Ang, M. (2025). Guilty by association ..." (`prereg_raw/dataverse_JH9DBC.json`).

## Check of the deposit against what the code reads
- Dataverse API (`prereg_raw/dataverse_JH9DBC.json`, 11:50 UTC): version 2, released 2025-08-18, 3 files, none restricted: `codebook.pdf` (78418 B), `data.tab` (124613 B, ingested from an uploaded `data.dta`, 257682 B as original), `replication.R` (19675 B). MD5s of the downloads match the metadata.
- Read calls in `replication.R`: one, line 18 `read_dta("data.dta")`. No `source()`, `load()`, `read.csv` or other file reads. Present: yes, as the original-format download of datafile 11944075 (`?format=original`). The listed file name is `data.tab`, so the default download does not carry the name the code expects.
- Variables the code uses (unique_id, id_estado, estado, elec_year, voto_pro_gober, juicio, partido_gober, prev_exp_fleg, econ_growth, hom_per100, mentions_prop, log_pobtot, log_pib, st_elections_15_18, year_2012, year_2015, year_2018): all 17 present in the file header (19 columns, 900 rows).
- No file the code reads is missing, so no absence search was needed.

## Finding
Deposit alone complete: every file the code reads is in the audited Dataverse deposit. The article's statement points to no named location (only "public repositories"), so under CHANGELOG #4 the materials are the deposit, and they are complete. Caveat: the footnote to the statement is paywalled and unread; since the deposit is already complete, an extra location there could not change the materials verdict.
