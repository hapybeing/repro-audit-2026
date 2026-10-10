# DATA_STATEMENT: 18_YXC5K5 (Benchmarking AI and human text classifications..., Research & Politics 2025, doi 10.1177/20531680251332353)

Written 2026-10-10 (IST, about 23:10), before any analysis code was run. Rule 4 (CHANGELOG #4) and absence-search rule (CHANGELOG #5a). No sign-in, no author contact.

## Sources read
- Main text, Sage HTML: https://journals.sagepub.com/doi/full/10.1177/20531680251332353 , read 2026-10-10 about 22:53 IST via the web_fetch tool (sandbox curl: HTTP 403 Cloudflare). Not downloaded, no sha256. Excerpt: `data_statement_raw/statement_excerpt.txt`.
- Online supplement (36 pp.), read 2026-10-10 about 22:56 IST via the Google Docs viewer (direct URL HTTP 403 Cloudflare). Searched for "dataverse", "github", "osf", "avail", "request", "replication": no data or code availability statement and no repository named; the only related phrase is "the replication code" in Appendix C prose (p. 3), with no location.
- Europe PMC: 0 hits for the DOI. OpenAlex (`data_statement_raw/openalex_work.json`): gold OA, no repository copy listed.

## Verbatim statement (main text, section "Data availability statement", after the footnotes)
"My data will be made available on the Research & Politics Harvard Dataverse repository. *"

(The asterisk has no visible target in the HTML read. The article information panel on the same page says "Data availability statement / Data is available for this article.") The statement names no DOI and does not mention code.

## Locations the statement points to
1. Research & Politics Harvard Dataverse. Checked 2026-10-10: the audited deposit doi:10.7910/DVN/YXC5K5 sits in the collection "Research & Politics Dataverse" (alias `researchandpolitics`, Dataverse search API), version 1.0 (the only version), released 2025-04-04 18:38 UTC, 94 files, none restricted, licence CC0 1.0. A Dataverse dataset search for the article title returns only this dataset (1 result), and a search for author "Tripp, Alexander" returns 3 datasets, the other two being unrelated papers (LJSEY1, BWMJRW). So the statement's location is the audited deposit.

No other location is named in the article or the supplement. The deposit's own memo (`Benchmarking_ExplanatoryMemo.docx`) says the raw newspaper article texts are not included "as that may violate copyrights" and offers them by email; that is a deposit note, not an article location, and email was not used (no author contact).

## Files read by the code vs files present
Read calls were listed from the three Rmd files (literal file names in read_csv / readLines calls, plus the file lists passed to `read_and_process`).

- `Benchmarking_DataAnalysis.Rmd` (produces every target): reads 22 CSV files (`pi_codings_2ndhalf.csv`, `human10_agree.csv`, `human4_agree.csv`, 12 GPT output files, 6 Claude output files, `6-12-24gpt10lab_fewshot_spanish.csv`). All 22 are in the deposit under exactly those names. Complete.
- `Benchmarking_Supplementary.Rmd` (appendix analyses, not a target): reads `Undergrad_codings_coder1/2/3 - Sheet1.csv` and `Group_ROCCA_codings - Sheet1.csv`; Dataverse ingested these and serves them as `.tab` by default, but the original `.csv` files with exactly these names are available via `?format=original` (md5 matches the Dataverse metadata). All other files it reads are present (`human*_agree.csv`, `AI_goldstandard_*_v2.csv`, `prompt*_output.jsonl`, `prompt*_expl_output.jsonl`, `pi_codings_2ndhalf.csv`, `*_notext.csv`, prompt `.txt` files). The four `prompt1.jsonl`, `prompt1_expl.jsonl`, `prompt7.jsonl`, `prompt7_expl.jsonl` names (lines 382-385) are commented-out writes, not reads. Appendix H (Tables A7 to A10) also needs article text: line 1004 computes `word_count = str_count(text, ...)` and line 1102 takes `texts = human_10lab$text` for the readability scores, where `human_10lab` is read from `AI_goldstandard_ten_v2.csv` (line 1001), whose deposited columns are only docid and the 8 label codes (no `text`). So, from reading the code and the file header (not run), the Appendix H covariates cannot be rebuilt from deposited files. Not a target.
- `Benchmarking_DataGeneration.Rmd` (sends articles to the OpenAI and Anthropic APIs; produces the LLM output CSVs, which are deposited): reads files that are NOT in the deposit:
  - `full_df_for_classification_ten.csv` (line 1482; code comment: "I do not include this file because it contains the raw text data");
  - `batch_part1_output_v2.jsonl`, `batch_part2_output_v2.jsonl` (lines 1545-1546, a "Colombia" batch run of about 9,009 requests that the paper's tables do not use);
  - `rnums.csv`, `all_news.csv` (lines 82, 85, on commented-out lines in an `eval = F` chunk; comment says they contain raw text);
  - a `text` column (`select(docid, text)`, line 265) that `AI_goldstandard_ten_v2.csv` does not contain (its columns are docid and the 8 label codes); the same column is needed by `Benchmarking_Supplementary.Rmd` lines 1004 and 1102.
  It also needs paid API keys. The memo states all of this openly.

## Absence searches for the missing files (scripted)
Script: `data_statement_raw/absence_searches_18.py` (run from repo/; public APIs only). Output: `data_statement_raw/absence_searches.json`. Hit rule: a file whose name equals the missing name exactly (Dataverse, Zenodo, dataset versions), or a repository/dataset clearly for this article (GitHub, OSF, Dataverse dataset searches).

| source | query | URL | UTC time | HTTP | results | hits |
|---|---|---|---|---|---|---|
| Harvard Dataverse Search API (files, all collections) | `fileName:"full_df_for_classification_ten.csv"` | https://dataverse.harvard.edu/api/search?q=fileName%3A%22full_df_for_classification_ten.csv%22&type=file&per_page=100 | 2026-10-10T17:32:08Z | 200 | 0 | 0 |
| Zenodo records API | `filename:full_df_for_classification_ten.csv` | https://zenodo.org/api/records?q=filename%3Afull_df_for_classification_ten.csv&size=25 | 2026-10-10T17:32:09Z | 200 | 0 | 0 |
| Harvard Dataverse Search API (files, all collections) | `fileName:"batch_part1_output_v2.jsonl"` | https://dataverse.harvard.edu/api/search?q=fileName%3A%22batch_part1_output_v2.jsonl%22&type=file&per_page=100 | 2026-10-10T17:32:10Z | 200 | 0 | 0 |
| Zenodo records API | `filename:batch_part1_output_v2.jsonl` | https://zenodo.org/api/records?q=filename%3Abatch_part1_output_v2.jsonl&size=25 | 2026-10-10T17:32:10Z | 200 | 0 | 0 |
| Harvard Dataverse Search API (files, all collections) | `fileName:"batch_part2_output_v2.jsonl"` | https://dataverse.harvard.edu/api/search?q=fileName%3A%22batch_part2_output_v2.jsonl%22&type=file&per_page=100 | 2026-10-10T17:32:11Z | 200 | 0 | 0 |
| Zenodo records API | `filename:batch_part2_output_v2.jsonl` | https://zenodo.org/api/records?q=filename%3Abatch_part2_output_v2.jsonl&size=25 | 2026-10-10T17:32:12Z | 200 | 0 | 0 |
| Harvard Dataverse dataset versions (YXC5K5) | `all versions, file lists` | https://dataverse.harvard.edu/api/datasets/:persistentId/versions?persistentId=doi:10.7910/DVN/YXC5K5 | 2026-10-10T17:32:12Z | 200 | 1 | 0 |
| Harvard Dataverse Search API (datasets) | `"Benchmarking AI and Human Text Classifications"` | https://dataverse.harvard.edu/api/search?q=%22Benchmarking+AI+and+Human+Text+Classifications%22&type=dataset&per_page=100 | 2026-10-10T17:32:13Z | 200 | 1 | 0 |
| Harvard Dataverse Search API (datasets) | `authorName:"Tripp, Alexander"` | https://dataverse.harvard.edu/api/search?q=authorName%3A%22Tripp%2C+Alexander%22&type=dataset&per_page=100 | 2026-10-10T17:32:13Z | 200 | 3 | 0 |
| GitHub repository search API | `Benchmarking AI human text classifications newspaper frames` | https://api.github.com/search/repositories?q=Benchmarking+AI+human+text+classifications+newspaper+frames | 2026-10-10T17:32:14Z | 200 | 0 | 0 |
| GitHub repository search API | `Tripp LLM newspaper frames Spanish immigration` | https://api.github.com/search/repositories?q=Tripp+LLM+newspaper+frames+Spanish+immigration | 2026-10-10T17:32:14Z | 200 | 0 | 0 |
| OSF nodes API | `filter[title]="Benchmarking AI"` | https://api.osf.io/v2/nodes/?filter%5Btitle%5D=Benchmarking+AI | 2026-10-10T17:32:14Z | 200 | 2 | 0 |

Result: no copy of the missing raw-text or batch-output files was found in any searched location. The searches cover only these services; they cannot show that no copy exists elsewhere.

## Finding
Materials named by the statement (rule 4): the Research & Politics Dataverse deposit, which is the audited deposit.
- For the targets: complete. Every file read by `Benchmarking_DataAnalysis.Rmd` is deposited under the name the code uses.
- For the full pipeline: incomplete by the author's stated design. The raw newspaper texts (and the files derived from them) and the Colombia batch outputs are not deposited; the data-generation step also needs paid API access. This affects regenerating the LLM outputs and the Appendix H text covariates (Tables A7 to A10), not the Table A1 targets.
