# DATA_STATEMENT: 21_LEFTNE (Gendered Political Contexts, Emotions, and Engagement, BJPolS 2025, doi 10.1017/S0007123425101166)

Written 2026-10-11 (IST, about 02:20). Checks run 2026-10-10 between about 20:38 and 20:42 UTC. No sign-in, no author contact. Rule: CHANGELOG_METHOD.md #4 (materials = deposit plus every location the article's own statement names) and #5 (absence claims need a repeatable log).

## Sources read
- Publisher PDF (open access, CC BY 4.0): https://www.cambridge.org/core/services/aop-cambridge-core/content/view/3665F10236319D5BAB8ED639242B29A2/S0007123425101166a.pdf/gendered-political-contexts-emotions-and-engagement-a-case-study-of-the-2016-us-presidential-election.pdf : HTTP 200, 489,045 bytes, sha256 9e11f10eb7e3a761aa2cae5d9354ab4b5e6a480bb682e5a3ee28226a0ae48d60. Excerpt: `data_statement_raw/statement_excerpt_article_p18.txt`.
- Cambridge Core article page (HTML), same statement under the heading "Data availability statement".
- Supplementary information: https://static.cambridge.org/content/id/urn%3Acambridge.org%3Aid%3Aarticle%3AS0007123425101166/resource/name/S0007123425101166sup001.doc : HTTP 200, 2,709,504 bytes, sha256 64165d965e1bb1072bd5caf7a43ceb501ac0008402400dc9c7d68c2988c42c3e. Excerpt: `data_statement_raw/statement_excerpt_SI.txt`.

## Verbatim statements
1. Article, p. 18, "Data availability statement": "Replication data for this article can be found in Harvard Dataverse at: https://doi.org/10.7910/DVN/LEFTNE"
2. SI, "Appendix D: Discussion of Ethics and Human Participants" (last paragraph of the SI): "The data and coding necessary to produce the findings in the main text and the S.I. are publicly available at: https://doi.org/10.7910/DVN/LEFTNE"

The article's reference list also cites the dataset (DeMora et al. 2025, Harvard Dataverse, V1). No other location (OSF, GitHub, "on request", author website) is named in the article or the SI text (searched the PDF text and the SI strings for dataverse, osf, github, request, available).

## Locations named
1. Harvard Dataverse doi:10.7910/DVN/LEFTNE (the audited deposit). Checked.

## Reachability and contents (2026-10-10, about 20:38 and 20:41 UTC)
- `https://dataverse.harvard.edu/api/datasets/:persistentId/?persistentId=doi:10.7910/DVN/LEFTNE` : status OK (`data_statement_raw/dataverse_LEFTNE.json`, sha256 f04846c2bdce15b0110256e711aa00539df714edf32bbf7401a771782b07b3c1). `.../versions` : HTTP 200, one version (1.0, RELEASED, deposited 2025-10-30), 3 files, none restricted, licence CC0 1.0 (`data_statement_raw/versions.json`).
- Files: `01- Replication_Text.R`, `02- Replication_Appendix.R`, `Data.zip` (ANES16.RDS, ANES18.RDS, CES2020.RDS, NORC.RDS, Qualtrics_2019.RDS). All three downloaded without authentication; sha256 values in PREREG.md.

## Read calls in the code versus files present

| script, line | read call | file in deposit |
|---|---|---|
| 01- Replication_Text.R, 42 and 343 | `readRDS("Qualtrics_2019.RDS")` | yes (Data.zip) |
| 01- Replication_Text.R, 47 and 366 | `readRDS("NORC.RDS")` | yes |
| 01- Replication_Text.R, 53 | `readRDS("ANES16.RDS")` | yes (loaded, never used later in the script) |
| 01- Replication_Text.R, 54 | `readRDS("ANES18.RDS")` | yes (loaded, never used later in the script) |
| 01- Replication_Text.R, 392 | `readRDS("CES2020.RDS")` | yes |
| 02- Replication_Appendix.R, 27 | `readRDS("Qualtrics_2019.RDS")` | yes |
| 02- Replication_Appendix.R, 32 | `readRDS("NORC.RDS")` | yes |
| 02- Replication_Appendix.R, 37 | `readRDS("CES2020.RDS")` | yes |

File names match the read calls exactly (files sit inside Data.zip; working directory must be the unzipped folder). No `source()` of helper files, no other inputs. A string scan of the compressed .RDS files (not loading them) found the variable names the code uses for the targets: Qualtrics_2019 (TREATMENT with levels including Alexa, Trump, Clinton, MeToo, Marches; anger, hope, fear, futureengage, party_leanersinc, GENDER, EDUCATION_r, Vote_Choice, party), NORC (TREATMENT, anger, hope, fear, futureengage, party), CES2020 (TREATMENT with levels Relaxed, Trump, Treatment of Women, Treatment of Minorities; complier, futureengage_novote, Gender_Party, word_count, teamweight). Agents confirm after loading.

Because the deposit contains every file the code reads, no absence search for a data file was needed and none was run.

## Results without code (noted, not data absences)
The SI statement says the deposit covers the findings in the main text and the SI. No deposited code produces SI Table C1 or Figures C1 to C3 (ANES time series 2000 to 2020; DIME candidate counts; the ANES time-series and DIME files are not in the deposit), the combined multiple-mediator indirect effects and Democratic-women subgroup values on pp. 14 to 15, or the Cohen's d values on p. 17; footnote 20's 2024 student experiment has neither data nor code. None of these is a pre-registered target. Their absence was established only by reading both deposited scripts in full and the Dataverse file list above; no external search was run for them.

## Finding
Deposit complete for the pre-registered targets: the article and SI name only the audited Dataverse deposit, it is public, and every file the two scripts read is in it. The SI's broader claim ("findings in the main text and the S.I.") is not fully met by the deposited code for the items listed above, which are outside the targets.
