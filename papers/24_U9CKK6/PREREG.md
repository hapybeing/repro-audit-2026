# PREREG: 24_U9CKK6

Written 2026-10-11 (IST, about 02:30), before any analysis code was run. No analysis code (R or Python) was executed to write this file. Only downloads, sha256 hashing, text search of the scripts, and a read-only streaming scan of the .Rdata file headers (column names, types and lengths; `data_statement_raw/rdata_structure.py`) were done.

The main text was read (publisher HTML, open access). The two printed tables that carry the targets (Table 1 and Table 2) are images/pop-ups not present in the HTML text; they were transcribed by a browser session from the publisher's "Display Table" pop-up and checked against the publisher PDF in the Taylor & Francis reader (both identical, per that session). I could not download the PDF myself (Cloudflare 403 to curl), so the table values rest on that browser transcription; Agent A and B should each re-read the target cells from the PDF or "Display Table" before comparing.

- Paper: Kollberg, M. (2024). "The challenger advantage - how challenger parties disrupt mainstream party dominance in the European Parliament". Journal of European Public Policy, 32(9), 2252-2281 (online 2024). DOI https://doi.org/10.1080/13501763.2024.2391510 . Licence CC BY (OpenAlex: hybrid OA, publishedVersion).
- Text source read:
  - Publisher full-text HTML https://www.tandfonline.com/doi/full/10.1080/13501763.2024.2391510 (fetched 2026-10-11 IST as extracted text, 180,821 bytes, sha256 0195fcc14f1f7b35f55a8dab783a7c07b874019b66de08887e1bcdd2e9091134; scratch copy `/workspace/audit_runs/24_U9CKK6/prereg/tf_full.txt`).
  - Tables 1 and 2: "Display Table" pop-ups on https://www.tandfonline.com/doi/figure/10.1080/13501763.2024.2391510 and the PDF https://www.tandfonline.com/doi/pdf/10.1080/13501763.2024.2391510 (browser transcription, 2026-10-11 IST; notes file `/workspace/web/notes/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/tandf-24_u9ckk6-tu_upyudo62mdlv5hdypt74plbmso/tables_kollberg_2024.md`).
  - Online supplement (appendix) from figshare https://ndownloader.figshare.com/files/49076409 (`rjpp_a_2391510_sm1745.pdf`, 2,512,055 bytes, sha256 95f2d48026190954c4a61c211fb62e25b9a8d7cdd6d143c1a93e7cb4c7313afd). Not used for targets.
- Dataset: "Replication Data for: The Challenger Advantage - How Challenger Parties disrupt Mainstream Party Dominance in the European Parliament", Harvard Dataverse, https://doi.org/10.7910/DVN/U9CKK6 , version 1.0 (released 2024-08-28), CC0 1.0, 28 files, 832,680,633 bytes, none restricted. File list API: https://dataverse.harvard.edu/api/datasets/:persistentId/?persistentId=doi:10.7910/DVN/U9CKK6 . Per-file URL: https://dataverse.harvard.edu/api/access/datafile/<id> .

## Dataset files

sha256 given for files downloaded for this pre-registration (all downloaded files' md5 matched the Dataverse md5). For files not downloaded, the Dataverse md5 is given. Folder = Dataverse directoryLabel.

| datafile id | folder/file | bytes | sha256 (downloaded) or md5 (Dataverse) | needed for targets |
|---|---|---|---|---|
| 10431957 | readme.txt | 1863 | sha256 b8a4b8bd2d0a3b22219832789dbd1cefb2788a3b7c57384eef554a3c825a5042 | doc |
| 10431971 | Scripts/1_QTA_Embeddings.R | 14435 | sha256 e457ecff42fb437541d59f9eb6c1bcf939934206cd8069f5cf3fd5c67a89b159 | no |
| 10431979 | Scripts/2_QTA_Debatetopics.R | 5618 | sha256 287ac61fbdc2613c92b761119d02ffddbc0cd5db48d1d8d4cfbb21c9d36adaeb | no |
| 10431970 | Scripts/3_OppositionControl.R | 8479 | sha256 fcb38344c137302f1fcf85f0945f2850f23859832fd55a8bb274edfeace0c250 | no |
| 10431972 | Scripts/4_OppositionControlNat.R | 5063 | sha256 3ed078447e76d8aa7f323a6878aa00b9d7afcd2c8ce3d0ea4c4f20fd09f92e45 | no |
| 10431973 | Scripts/5_Descriptives.R | 14316 | sha256 8f26903642d8c52e9a63c197fed700e2d85e5e2c5fa0af6a9cff7e3749a81f83 | no |
| 10431975 | Scripts/6_analysis1.R | 36862 | sha256 fd9d4d746528fd70865eaa159b0f246ca5f7fb256d032a8034b4c758e98a393e | yes (Table 1) |
| 10431978 | Scripts/7_analysis2.R | 29312 | sha256 08138dc06aaa4036c6f33eb7fc8752baf850274fd3421662d0304149ff5daf24 | no |
| 10431969 | Scripts/8_analysis3.R | 26630 | sha256 ed76c78ee9d1ca1157ef3f0409538c5b9da7fa5a5f82a5dd06cc53de147ed893 | no |
| 10431976 | Scripts/9_analysis4.R | 22890 | sha256 4a6c15513c5a91c3c1f44eeaeb33b026f657cf62d65128d6f87c93933990428d | yes (Table 2) |
| 10431974 | Scripts/10_analysis_5.R | 27633 | sha256 2889526af6be0f4674c9e0a511572ae93caf654836268a9eaf2a255ca6d7cd32 | no |
| 10431977 | Scripts/11_analysis6.R | 9845 | sha256 93c479fd0ee9e0857237e4e8888f5b28c3b614c7bac961ba38049100a13a6988 | no |
| 10431963 | Data/EP_debates_07062023.Rdata | 176144411 | sha256 ae12ce2cc5b89209b2def160d6c7d7049493ba4cccfb704f5da8c6c88a146149 | yes (Tables 1, 2) |
| 10431967 | Data/RdW_salience.Rdata | 418958 | sha256 a35bc511f62cf002b9ff5fcb41e0af6910c914f858ca3c24a7d0661540bdb15e | yes (Table 2, EU model) |
| 10431966 | Data/EP_complete_dict_110323.Rdata | 160440130 | md5 2491ee1d1cc0ecf3ef11cdc11d912e52 | no |
| 10431958 | Data/EP_debates_11032023.Rdata | 176079798 | md5 53957229c88c55b5da6e69c5fc6501ce | no |
| 10431961 | Data/EP_prepped_110323.Rdata | 157160854 | md5 01095d3f46ff2aaedbc09fad8ec2f1db | no |
| 10431968 | Data/EP6_RCVs.xlsx | 20711891 | md5 25b8ef0198606cfdf023fc6a2b0ace63 | no |
| 10431962 | Data/EP7_RCVs.xlsx | 19281699 | md5 b9c791b724976a6e31fc164093de4baf | no |
| 10431965 | Data/EP8_RCVs.xlsx | 28133116 | md5 d6f7098719dcfae5ca05ae6ce696766f | no |
| 10431964 | Data/eurostat_asylum.xlsx | 61366 | md5 94179269f12445dc18fc7fe567c6c030 | no |
| 10431959 | Data/eurostat_unemployment.tab (original format: eurostat_unemployment.csv via `?format=original`) | 22681735 (.tab) | md5 28f5edb5253b5ff41eba954802f79f0e (.tab) | no |
| 10431960 | Data/Members.csv | 10348622 | md5 f501bde1328ee14e1bcc495d85dca872 | no |
| 10431983 | NLP_Model/context_28102021.Rdata | 14478229 | md5 845fb4c77a6eb803abc39b05a7587401 | no |
| 10431980 | NLP_Model/main_28102021.Rdata | 14477748 | md5 9c7cbc8810bbe181c4de22a5d4784c49 | no |
| 10431984 | NLP_Model/out50_05112021.Rdata | 3106061 | md5 82300927982c8ec7e4aeb6ad0a44ecf7 | no |
| 10431981 | NLP_Model/w2v_28102021.Rdata | 14478181 | md5 e65b806d3b27e5508bed3f8be48a314d | no |
| 10431982 | NLP_Model/word_vectors_28102021.Rdata | 14474888 | md5 3379b6763b3f49173b7d3404e313edde | no |

Structure of the two input files (streaming header scan, `data_statement_raw/ep_structure.json`, `rdw_structure.json`): `EP_debates_07062023.Rdata` holds one object `EP_debates`, a data.frame of 299,660 rows and 117 columns (uncompressed serialized size 750,823,713 bytes; columns 4 `text` and 6 `ori_text` are speech texts). Column 19 `year` is stored as double (numeric), `challenge` (col 72) is double, `party_id` (col 17) integer, `mep_ids` (col 2) and `country` (col 18) character, `EU_party` (col 16) factor. `RdW_salience.Rdata` holds `padpanel`, a data.frame of 5,235 rows and 62 columns including `country`, `month`, `eu.w`.

## 1. Headline results and targets

Main claim (abstract): "Challenger parliamentarians engage in anti-establishment rhetoric in the run-up to elections and issue-entrepreneurship during crises." The Results section reports this with Table 1 (multilevel linear models of a speech's standardised anti-establishment rhetoric score on challenger status interacted with proximity to the next EP and national election; random intercepts for MEPs and parties) and Table 2 (issue emphasis on challenger status interacted with issue salience). Text: challenger MEPs "engage significantly more in anti-establishment rhetoric in the run-up to national elections" (Challenger * Proximity to next Nat. Election); proximity to EP elections raises it for both party types with no interaction; for Table 2 "the coefficients of the interaction effects Challenger * Austerity Salience and Challenger * EU Salience in Table 2 are significant and positive". Figure 3 is "based on Model 2, Table 1", so Model 2 is the pre-registered Table 1 column.

Targets (copied exactly from the printed tables; coefficients are lmer fixed effects in standard-deviation units of the outcome, printed to 2 decimals):

| id | quantity | code object | paper value | decimals | location |
|---|---|---|---|---|---|
| T1 | Challenger * Proximity to next National Election, Model 2 | `fixef(cycle_AE_fit2)["challenge:days_to_nat"]` (6_analysis1.R line 365) | 0.02 (SE 0.00, ***) | 2 | Table 1, column Model 2, row "Challenger * Proximity to next National Election" |
| T2 | Proximity to next EP-Election, Model 2 | `fixef(cycle_AE_fit2)["days_to_EP"]` | 0.01 (SE 0.00, ***) | 2 | Table 1, Model 2, row "Proximity to next EP-Election" |
| T3 | Challenger, Model 2 | `fixef(cycle_AE_fit2)["challenge"]` | 0.05 (SE 0.01, ***) | 2 | Table 1, Model 2, row "Challenger" |
| T4 | Num. obs., Model 2 | `nobs(cycle_AE_fit2)` | 266854 (printed "266,854") | 0 | Table 1, Model 2, row "Num. obs." (Models 1, 3, 4 print the same number) |
| T5 | Challenger * Austerity Salience, Austerity model | `fixef(AUT_sal_model)["challenge:aut_sal"]` (9_analysis4.R line 65) | 0.04 (SE 0.01, **) | 2 | Table 2, column "Austerity", row "Challenger * Austerity Salience" |
| T6 | Challenger * EU Salience, European Integration model | `fixef(EU_sal_model)["challenge:EU_sal"]` (9_analysis4.R line 89) | 0.02 (SE 0.01, *) | 2 | Table 2, column "European Integration", row "Challenger * EU Salience" |

Which p-value: the tables print stars only; no star legend is printed under either table in the article. The code writes the tables with `texreg(..., include.ci = FALSE, custom.note = "%stars ...")`, i.e. texreg's default thresholds (*** p < 0.001, ** p < 0.01, * p < 0.05). For `lmerMod` objects texreg's default `method = "naive"` computes p = 2 * pnorm(-|estimate / SE|) (texreg extract.R, extract.lme4, checked in texreg 1.40 source). Candidates, first is pre-registered: (1) naive normal p from the Wald t, as texreg computes it; (2) Satterthwaite p from lmerTest (exploratory only, not used for any criterion). `lmerTest` is not loaded by scripts 6 or 9.

Conclusion criterion for `same_conclusion` (rounding in R with `round(x, 2)`):
- T1, T2, T3: estimate > 0 and pre-registered p < 0.001 (paper: ***).
- T5: estimate > 0 and 0.001 <= p < 0.01 (paper: **). A p below 0.001 is recorded as a different star bucket (stronger), `same_conclusion = false`, with a note.
- T6: estimate > 0 and 0.01 <= p < 0.05 (paper: *). Same rule for a stronger bucket.
- T4: `same_conclusion = true` if |N - 266854| <= 5. An N-only mismatch with matching estimates is read under CHANGELOG #6(a).
- Note for comparison: the printed values have one or two significant digits, so `within_5pct` computed against the printed value (as the runbook defines it) is not informative for T1 to T3, T5, T6 (for example a true 0.016 is 20% from 0.02 yet prints as 0.02). Agents compute it as defined and also report `match_to_rounding`, which is the meaningful test here.

Secondary numbers (context only, not targets): Table 1 Model 2 LR-Position 0.02 (0.01) *, EP-Opposition 0.06 (0.01) ***, Challenger * Proximity to next EP-Election 0.00 (0.01), Num. groups MEP IDs 1466, Party IDs 204, AIC 738,747.50, Log Likelihood -369,309.75. Table 2 Num. obs. 101077 (Austerity), 233056 (Immigration), 77276 (European Integration); Austerity Salience 0.01 (0.01); EU Salience -0.01 (0.00) **; Challenger * Immigration Salience -0.00 (0.01).

Inconsistencies noticed while reading (described, not judged):
1. Table 1 prints "Year Fixed Effects: Yes" for all four models. In 6_analysis1.R the four Table 1 models (lines 356, 365, 374, 384) enter `year` without `as.factor()`, and `year` is stored as a numeric (double) column in `EP_debates_07062023.Rdata`, so as written the term is a single linear year slope. Other models in the same script (lines 84, 93, 103, 136) and all Table 2 models (9_analysis4.R lines 69, 82, 93) use `as.factor(year)`.
2. Row and column labels in the printed tables differ from the labels in the deposited `texreg` calls: Table 1 prints "EP-Opposition" and "National Opposition" where 6_analysis1.R lines 397-406 (custom.coef.map) map to "EP Opposition" and "Nat. Opposition"; Table 2 prints column "European Integration" and row "National Opposition" where 9_analysis4.R maps "EU-Integration" and "Nat. Opposition". The printed tables also show mixed number formatting (Table 1 Num. obs. "266,854" in Models 1-2, "266854" in Models 3-4; Table 2 Num. obs. without commas). The printed tables were therefore edited after export or come from a different run of the code.
3. The deposited code writes Table 1 to `Tables/AE_cycle_240124.tex` and Table 2 to `Tables/issues_sal_08062023.tex`; neither output file is deposited (the readme says the Figures and Tables folders were left empty).
4. Proximity variables are built as `days_to_EP <- scale(days_from_EP)` (6_analysis1.R line 353, comment "Make them more intuitive as of reviewer request"); the printed label is "Proximity to next EP-Election". Whether larger values mean closer or further from the election is not stated in the code; the sign reading is the authors' and is not part of any criterion here.

## 2. Reproduction plan

Layout: create RUNDIR with subfolders `Data/`, `Tables/`, `tables/`, `Figures/`, `Figures_new/`; put `EP_debates_07062023.Rdata` and `RdW_salience.Rdata` in `RUNDIR/Data/` (deposit folder `Data`, file names unchanged, so no path mapping is needed); working directory = RUNDIR. Scripts are read from the deposit's `Scripts/` folder but run with working directory RUNDIR (path-only setting, no edit).

Only scripts 6 and 9 feed the targets, and both start from the deposited intermediate `Data/EP_debates_07062023.Rdata` (the output of scripts 1 to 4). Scripts 1 to 5, 7, 8, 10, 11 are not run.

Pre-registered primary run (target blocks only, authors' lines verbatim, run with `Rscript` via `source(textConnection(lines[...]), echo = TRUE)` or by copying the line ranges unchanged into `scripts/run_table1.R` and `scripts/run_table2.R` with a diff showing they are byte-identical to the ranges):
- Table 1 (T1 to T4): 6_analysis1.R lines 1 to 53 (load, EU_party relabel, centering of columns 22:24, 27:71, 73:75, 77:107, 117:118, scaling), then lines 346 to 416 (chall_fact, `days_to_EP`/`days_to_nat`, models `cycle_AE`, `cycle_AE_fit2`, `cycle_AE_fit3`, `cycle_AE_fit_group`, texreg to `Tables/AE_cycle_240124.tex`). Lines 54 to 345 fit other models and do not change any variable used by lines 346 to 416 (checked by text search: the only assignment in that range is `chall_fact` at line 130, which line 349 recreates). Reason for not sourcing the whole script: lines 132 and 246 use variables `right` and `left` that are not created in any deposited script and are not columns of `EP_debates` (see Known risks), so a top-to-bottom run stops at line 132 before reaching Table 1; and the script keeps about 25 fitted models in memory.
- Table 2 (T5, T6): 9_analysis4.R lines 1 to 123 (load, RdW merge, centering, scaling, `AUT_sal_model`, `Immi_sal_model`, `EU_sal_model`, texreg to `Tables/issues_sal_08062023.tex`).
- After each model is fitted, `saveRDS(model, "outputs/<name>.rds")` (added after the authors' line, recorded as an env fix diff) so a sandbox restart costs one model, not the run.
- Extraction: `scripts/extract_targets.R` reads the saved models and writes `outputs/targets_extracted.csv` with, for each target term: estimate, SE (`sqrt(diag(vcov(m)))`), t, naive p (`2*pnorm(-abs(t))`), nobs, number of groups, and the lme4 convergence messages (`m@optinfo$conv$lme4$messages`). Also save the two .tex files texreg writes to `outputs/`. `scripts/build_results.py` builds `results.json` from that CSV.

Allowed environment fixes (each as a diff): package versions; setting the working directory; creating output folders; the `saveRDS` lines above; if `sjPlot`, `sjstats`, `fixest`, `ggeffects` or `skimr` cannot be installed on this machine, commenting out only those `library()` lines, since no function from them is called in the line ranges above (checked by text search: the ranges call `lmer`, `lmerControl`, `texreg`, base R, and in script 9 `group_by`, `summarise`, `mutate`, `case_when`, `left_join` from tidyverse and `as.yearmon` from zoo).

Packages: lme4, texreg, zoo, tidyverse (dplyr), Matrix; plus the library() lines listed. No versions are pinned anywhere in the deposit (no renv.lock, no sessionInfo, readme silent). Use current CRAN versions; record them. Fallback if current lme4 fails to build on Debian R 4.5: the Debian binary `r-cran-lme4`.

Memory: estimated peak 2.5 to 3.5 GB for the Table 1 block (the data.frame is about 0.75 GB serialized, mostly two text columns, about 1 to 1.3 GB in memory; the centering `apply` and `cbind` add about 0.5 GB; each lmer on 266,854 rows with about 65 fixed effects holds a dense X of about 0.13 GB plus copies, and the block keeps four fitted models). Pre-registered memory fallback, used if peak RSS (`/usr/bin/time -v`) passes about 3 GB or R is killed: (F1) insert right after the `load()` line `EP_debates$text <- NA_character_; EP_debates$ori_text <- NA_character_` (columns 4 and 6 keep their positions, so the index-based centering is unchanged; neither column is used in scripts 6 or 9); (F2) after each model's `saveRDS`, `rm()` it and `gc()`, and build the texreg table at the end from the saved RDS files. Estimation lines, data and order are unchanged under F1 and F2. No randomness is involved in these models (no seed is set or needed).

Wall time: unknown until run; my estimate is 1 to 5 minutes per lmer fit (Nelder_Mead, 267k rows, two random intercepts), seven target models, under 45 minutes in total.

## 3. Robustness checks (pre-registered)

Primary quantity for all three checks: T1, the Challenger * Proximity to next National Election coefficient in Table 1 Model 2 (`cycle_AE_fit2`), estimated with the authors' formula, data and `lmerControl(optimizer = "Nelder_Mead")`, REML as in the original. Inference: naive normal p as texreg computes it. "Same direction and significance as paper" = estimate > 0 and p < 0.001, unless a check states otherwise. The estimation sample is `model.frame(cycle_AE_fit2)` rows (complete cases on the formula variables) taken from `EP_eurobar_cent` as built by lines 1 to 53 and 349 to 354.

R_a. Party-cluster bootstrap (different resample). Clusters = `party_id` (204 parties). `set.seed(20261011)`; pre-generate all K draws up front (each draw: sample the 204 party ids with replacement) and save them to `outputs/R_a_draws.rds`, so a restart resumes deterministically. For each draw build the resample by stacking all rows of each drawn party; relabel `party_id` and `mep_ids` as `paste(id, copy_index)` so repeated copies are separate groups; refit the identical `cycle_AE_fit2` formula; record the T1 coefficient, convergence messages and any dropped rank-deficient columns. Save results every 5 draws (`outputs/R_a_partial.csv`). K rule: time the first refit (t seconds); K = min(200, floor(3600 / t)); if that is below 30, run K = 30 provided 30 * t <= 7200, otherwise R_a is reported as not run with t. Report the original estimate, the bootstrap SE, the 2.5 and 97.5 percentiles, K and failed refits (counted, not replaced). Same direction and significance = original estimate > 0, the 95% percentile interval excludes 0, and the normal p from estimate / bootstrap SE is < 0.001 (with K <= 200 the percentile interval alone cannot resolve p < 0.001, so both conditions are required and reported separately).

R_b. Outlier exclusion on the outcome. Within the `cycle_AE_fit2` estimation sample, compute z = (y - mean(y)) / sd(y) for y = `embed_dict_scale`; drop rows with |z| > 3; refit the identical formula; report the T1 coefficient, SE, naive p and the number of rows dropped. Secondary (reported, not primary): the same rule on the outcome within the estimation sample of `AUT_sal_model` (y = `aut_dict_scale`, report T5) and of `EU_sal_model` (y = `int_dict_scale`, report T6); for these, same direction and significance = estimate > 0 and p in the paper's star bucket (T5: 0.001 <= p < 0.01; T6: 0.01 <= p < 0.05), with p < 0.05 also reported.

R_c. Alternative analysis choice: year as fixed effects. Refit `cycle_AE_fit2` with `year` replaced by `as.factor(year)` and nothing else changed (same data, controls, random intercepts, optimizer). This matches the "Year Fixed Effects: Yes" row printed in Table 1 and the specification used in Table 2 and other models of the same script (inconsistency 1). Report the T1 coefficient, SE, naive p, nobs.

## 4. Known risks

- Missing inputs, not needed for the targets: `4_OppositionControlNat.R` lines 23 and 34 read `parlgov/view_party.csv` and `parlgov/view_cabinet.csv`, and `10_analysis_5.R` line 16 reads `Data/eurobarmeter_challengers_2023.dta` (code comment: "Wratil (forthcoming) - dataset will be added upon publication by Wratil"). None is in the deposit (searches in DATA_STATEMENT.md). Script 4's output `EP_debates_07062023.Rdata` is deposited, and script 10 feeds appendix leads-and-lags results only, so neither blocks T1 to T6. They make scripts 4 and 10 unrunnable from the deposit.
- Undefined variables in script 6: `AE_fit_int_plot` (line 132) and `AE_fixed_YFCF_int_group` (line 246) use `right` and `left`, which no deposited script creates and which are not columns of `EP_debates` (117 column names read from the file). A full top-to-bottom run of 6_analysis1.R would stop at line 132. These models feed appendix results, not the targets; the pre-registered line ranges avoid them.
- File-name mapping: `8_analysis3.R` line 98 reads `Data/eurostat_unemployment.csv`; Dataverse serves it as `eurostat_unemployment.tab` by default, and the original `.csv` via `https://dataverse.harvard.edu/api/access/datafile/10431959?format=original` (verified the redirect names `eurostat_unemployment.csv`). Script 8 is not needed for the targets. Script 8 also writes to lower-case `tables/` (lines 156, 386).
- Year term (inconsistency 1): if the printed Table 1 came from a run with `as.factor(year)`, the deposited code (linear year) may not reproduce Table 1 exactly; R_c gives the factor-year version for comparison, but under PROTOCOL the deposited code as written is what is reproduced.
- No package versions pinned; lme4 optimiser results can shift in later decimals across versions; with values printed to 2 decimals this is unlikely to matter except near a rounding boundary (for example a true 0.015).
- Memory and time: see section 2 (shared 7 GB machine; F1 and F2 fallbacks; R_a K rule). No Stata or proprietary dependency.
- Paper numbers: taken from a browser transcription of the publisher pop-up and PDF; I could not fetch the PDF with curl (HTTP 403). Agents should confirm the six target cells against the PDF before scoring.
