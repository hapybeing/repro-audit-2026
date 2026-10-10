# PREREG: 15_1BBC4E

Written 2026-10-10 (IST, about 21:10), before any analysis code was run. None of the authors' scripts was executed to write this file. The deposit was downloaded and its files were read as text; the one data file the targets use (`Measures_merged.rds`) was opened only to list its dimensions and column names (Python `pyreadr`), no statistic was computed from it.

- Paper: Schmid, J. W. (2025). "Electoral autocracies, hybrid regimes, and multiparty autocracies: same, same but different?" Democratization, 32(6), 1565-1588. DOI https://doi.org/10.1080/13510347.2025.2476183 . Open access (CC BY, per OpenAlex).
- Text source read: the publisher PDF https://www.tandfonline.com/doi/pdf/10.1080/13510347.2025.2476183 , read as extracted text through the web_fetch tool on 2026-10-10 (about 15:33 UTC). A direct curl download of the PDF returned HTTP 403 (Cloudflare), so no PDF bytes were saved and no sha256 of the PDF exists. The HTML full text (https://www.tandfonline.com/doi/full/10.1080/13510347.2025.2476183) was also read; its extracted text is kept in scratch (`/workspace/audit_runs/15_1BBC4E/prereg/tf_full.txt`, sha256 bcf3c791c59d7f6e117bfc5b387b0b644328fd333e5e47916140f0ba55ee76e7). In the HTML version Table 3 is not rendered inline (only a CSV link, which returned 403); the Table 3 values below come from the PDF text. Page numbers are the journal page numbers (1565 to 1588).
- Main text: read in full. Supplemental appendix (fdem_a_2476183_sm8178.pdf, 214.4 KB): NOT read (HTTP 403 by curl, web_fetch extraction failed). No target is taken from the appendix.
- Dataset: "Replication Data for: Electoral Autocracies, Hybrid Regimes, and Multiparty Autocracies: Same, same but different?", Harvard Dataverse, https://doi.org/10.7910/DVN/1BBC4E , version 1.0, released 2025-09-19, licence CC0 1.0. 49 files, none restricted.
  - File list API: https://dataverse.harvard.edu/api/datasets/:persistentId/?persistentId=doi:10.7910/DVN/1BBC4E (saved: `data_statement_raw/dataverse_1BBC4E.json`)
  - Each file downloaded with `curl -A "repro-audit-2026" https://dataverse.harvard.edu/api/access/datafile/<id>` (all HTTP 200, 2026-10-10 about 15:29 UTC). The md5 of every file (originals for the four ingested tabular files) matches the Dataverse metadata. sha256 below; full list also in `/workspace/audit_runs/15_1BBC4E/prereg/deposit_sha256.txt`.
  - ROOT = `Replication Data/Replication Files. Electoral Autocracy. Hybrid Regimes. Multiparty Autocracy. Same. same but different` (the R project folder; it contains spaces and full stops).

| datafile id | path | bytes | sha256 | note |
|---|---|---|---|---|
| 10992320 | `Replication Data/Readme.txt` | 2272 | 2661b5f7724cd41eaf7737a5c001ddbc1812d26e91196085f9af540c86c63bff |  |
| 10992307 | `ROOT/.RData` | 49 | 98d9344d7b42bf3f491eea59c146e20f75dd84f899274a71b4a16f87069f5271 |  |
| 10992301 | `ROOT/.Rhistory` | 26324 | 0dcec94342c8237ad7b5dae5e13f84b1f4b2636296ab9111a8210d37d9080110 |  |
| 10992306 | `ROOT/MTM R 3.0.Rproj` | 267 | 7ea129dd121b1588dc675da38fd6251ed91d2467e951923910683f7a1fb4b8ec |  |
| 10992305 | `ROOT/.Rproj.user/8409F39C/rmd-outputs` | 5 | 7c370d9536d7d0d6a0f7cd7f9826692acd93e4fb05ba46f7b630b879740343d3 |  |
| 10992323 | `ROOT/.Rproj.user/8409F39C/saved_source_markers` | 27 | 943cf5311c54c71f50cdf4d28d072c70ec8785a4b2b73bcc2000e6f1cf1dfc31 |  |
| 10992289 | `ROOT/.Rproj.user/8409F39C/pcs/files-pane.pper` | 323 | fd2e32e4fe132ad27fa3b0fffd805260f263238fd9be1cb284e6efb7411c06b8 |  |
| 10992282 | `ROOT/.Rproj.user/8409F39C/pcs/source-pane.pper` | 22 | fd4604a39edb54918b82c77db934a588e084305c43a827c948aa93ab2679c579 |  |
| 10992281 | `ROOT/.Rproj.user/8409F39C/pcs/windowlayoutstate.pper` | 289 | 3fa2bb1a36ae899546f0e0eae96f030561df278432ea5d80f53212263cb0f81d |  |
| 10992295 | `ROOT/.Rproj.user/8409F39C/pcs/workbench-pane.pper` | 57 | d55de6dc13788983c7c1dd94a52d450fe01364dd756488b76c0b1f61a125b409 |  |
| 10992294 | `ROOT/.Rproj.user/8409F39C/sources/per/t/2532172A` | 892 | 8c991e82e8c37eb6ebf8755991b9b1a3483a7cc30dd35623bc77250a729066fd |  |
| 10992308 | `ROOT/.Rproj.user/8409F39C/sources/per/t/2532172A-contents` | 7981 | 19fae4551aca3da29ccf41935087b42fea81c777e3e16fff845e17223dde423f |  |
| 10992321 | `ROOT/.Rproj.user/8409F39C/sources/per/t/C79C5DB5` | 846 | 6b3ceedf862870ae389f345e434318788b9106241782ad6d80681091492a82df |  |
| 10992296 | `ROOT/.Rproj.user/8409F39C/sources/per/t/C79C5DB5-contents` | 8448 | 7de8c1eff4dc2fd841fd791d830468aecbbb686ad708195e9f7236a74acc3e05 |  |
| 10992302 | `ROOT/.Rproj.user/8409F39C/sources/prop/445DF45A` | 54 | 9198e55dc22131a6a0920c04113e609afcccb491fe7a465df8f8bbff4f07d3bc |  |
| 10992287 | `ROOT/.Rproj.user/8409F39C/sources/prop/BCA53DCA` | 108 | 63b5f793cf483b7e86b4b949c94a27fd71e6dd282d3c0f3b825ebe392db82d75 |  |
| 10992313 | `ROOT/.Rproj.user/8409F39C/sources/prop/INDEX` | 604 | 684e5525aef409bfa29eafb63c8afa16211fe584b1cea59103d8c9b0c5d12331 |  |
| 10992286 | `ROOT/.Rproj.user/shared/notebooks/patch-chunk-names` | 0 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |  |
| 10992324 | `ROOT/Data/Covariates/estimates_gdppc_model_combined_normal_noslope_gamma_lambda_additive_test_20220215.rds` | 19867044 | 93f5021fc1438abb71447b39ef528adcba2c0235462c018e4e6ae01fbf84d7c5 |  |
| 10992285 | `ROOT/Data/Covariates/ucdp-intrastate-count-onset.tab` | 502483 | 5427a4d44a1814164c84b0df0a1c8c85b660739e21259100d2c98a24bad3f92a | ingested by Dataverse; original `ucdp-intrastate-count-onset.csv` (431990 bytes, sha256 7101eb7eb6734a28c0a37012a509035c5be68e0b33b6b1896e2aef86a50336b6) via `?format=original` |
| 10992317 | `ROOT/Data/Regimedata/AF_1.rds` | 24029 | 05d72f17849ac0312a2e9954495934eb6d4da015b8d3467b779839e6946dc8bf |  |
| 10992283 | `ROOT/Data/Regimedata/BMR_demcoding.tab` | 679039 | 35468bc65dfd7f928888e6af82b75e7fad16a47144b7d2c3fca1c4cd89d28bdd | ingested by Dataverse; original `BMR_demcoding.csv` (634176 bytes, sha256 b6d73eeb33111e22387163a51fa3316ba0ee666d5d0fff91954c97dcc43704a3) via `?format=original` |
| 10992326 | `ROOT/Data/Regimedata/Measures_merged.rds` | 137875 | d84b902215918d49b2f045e5c92de42fff5465d9caf8c914952871091d14f203 |  |
| 10992279 | `ROOT/Data/Regimedata/Measures_merged_covariates.rds` | 688152 | b40a6f0f56a6d61f06f1b49cc7fe1d6b41fa062108936e5741838c718083d734 |  |
| 10992284 | `ROOT/Data/Regimedata/Miller_Strategic_Origins_Data.RData` | 2451412 | 6868c20780d64bfc30a83d0325d8e13aef6ad93cb0f6d1b347dea638405e88be |  |
| 10992327 | `ROOT/Data/Regimedata/fh_23.rds` | 21836 | 2bc4921075a7dcf10174a8e0b7a667fd42814e0c7929a86f7f699aa99cc35292 |  |
| 10992298 | `ROOT/Data/Regimedata/htw_ARD_6.rds` | 103841 | 0fab064841d0abf3d1988833c1b9ea25228378d0e853b4b3e8b88efa7053fb6f |  |
| 10992290 | `ROOT/Data/Regimedata/lied6_4.rds` | 54166 | 4fb9771cf710d635f75087c34dfe76018fd97128da13b167560388516a9b6ddb |  |
| 10992309 | `ROOT/Data/Regimedata/magaloni_awd1_0.rds` | 110740 | 289e3518eae1ad10b63452ff1c0634ef95b4a1a767c51b32db91ac467efcca51 |  |
| 10992314 | `ROOT/Data/Regimedata/polity_v.rds` | 151767 | c716a1c9888ce964ea6c29bfd6f2e3654c960e0758bfada297e96ec9e81c6e16 |  |
| 10992315 | `ROOT/Data/Regimedata/vdem13.rds` | 31556767 | 8324b6a6b3b3febc3025c090615ba16d95d2e5c56a67ecb4af998dba3d6ac60e |  |
| 10992316 | `ROOT/Data/Replication/Kim/Kim_Replication_Ready.rda` | 776734 | d1f681e1ac7f2745b5566021932dedccca14d4dbfb0cf9a60d000099e097e309 |  |
| 10992292 | `ROOT/Data/Replication/Kim/nam_data.tab` | 4374035 | bcde930e2ad5c40b4780b9a6e2245d3780432a7030d384528f2eb6117956f823 | ingested by Dataverse; original `nam_data.dta` (5382667 bytes, sha256 886dcbb42761e7ce1869b849b43dbc2e18d8754715ea4110c13b360f3759cd0d) via `?format=original` |
| 10992311 | `ROOT/Data/Replication/Miller/EAHumanDev_CPS_Replication.tab` | 6591834 | bdce7066a06120864b1a7cee9663c78ae24e91928e0c8ff3ce0a8a5029844f00 | ingested by Dataverse; original `EAHumanDev_CPS_Replication.dta` (5831226 bytes, sha256 9626a5b35e5e97a0831b17a4c5127654afa66cea822b7614ae3305f549ea71fa) via `?format=original` |
| 10992304 | `ROOT/Data/Replication/Miller/Miller_Replication_Ready.rda` | 1956680 | dc09629d17bdc8bf8ce3b828abc01275b760b781dcbd4d0dee623ae27310d7a8 |  |
| 10992293 | `ROOT/Scripts/Comparing Indices/Agreement across all.R` | 2468 | 4aa4fc9b6ea09f9ddd71e77e62ef0cf1dca93faa7efc2c7f890e67e7b850ee9c |  |
| 10992319 | `ROOT/Scripts/Comparing Indices/Comparison.R` | 15700 | ea2802451a965234765d97e7d3159f3a64a26eea1c6b8a035ea427d92c5c521c |  |
| 10992299 | `ROOT/Scripts/Comparing Indices/Pairwise agreement.R` | 3970 | 2161bbe3d4ec5648e6a64b9b0641c5cf2f816ef32cc170753e003660dd33b54c |  |
| 10992288 | `ROOT/Scripts/Comparing Indices/Share_Common_Sample.R` | 4328 | 8fa34621f021b4af9dfaa17ee0bcb9a733cd643de3719cabfead7b3374db249f |  |
| 10992291 | `ROOT/Scripts/Covariates/Covariates Identify drivers of variation intrareg analysis.R` | 7122 | 0bd6539b119cfb510450b14b051cab74b4623ad90fa4843beaf8b3ad2fd174a7 |  |
| 10992318 | `ROOT/Scripts/Covariates/Covariates Identify drivers of variation.R` | 7033 | d0ca2a5adcec60a31d320b3c2b77665b1315a5bb1236e98dab8473f8e8c548e0 |  |
| 10992297 | `ROOT/Scripts/Covariates/Intra-Regime_Analysis.R` | 17701 | d82970e671f48f5ec5099e9950348350901813e71a253cc87f780e2d9b754935 |  |
| 10992322 | `ROOT/Scripts/Covariates/Run covariate models.R` | 7898 | 2c53e791be91c709cdb48647795f32375d8af199fe6d6643ffd9eeedc506fd9f |  |
| 10992280 | `ROOT/Scripts/Data Preparation/Merging_measures.R` | 13583 | fd9275410778c436fbf29eeabb5a569db0bbba042b17fcda187e67452840bfb2 |  |
| 10992310 | `ROOT/Scripts/Data Preparation/add_covariates.R` | 6752 | e734504d43db8653a3aded854928744351a33f8b19dafc6be5ec00f1e930bdee |  |
| 10992312 | `ROOT/Scripts/Replications/Kim/Kim_Replication_Analysis.R` | 8175 | f997add4cd1db37dd88cc8876ef2e13a2f3a731da2daa09f5238e68cfc181ea2 |  |
| 10992300 | `ROOT/Scripts/Replications/Kim/Kim_Replication_Data_Preparation.R` | 8717 | 407054149f1752a311a6bcb4ab2688437260d03d8d28a648ad268ae120e4b5a2 |  |
| 10992303 | `ROOT/Scripts/Replications/Miller/Miller_Replication_Data_Preparation.R` | 4421 | ad397fbf3525452cb81d4e522e47fae63da006359c68e0b1efdd9bcf85f21372 |  |
| 10992325 | `ROOT/Scripts/Replications/Miller/Replication Analysis.R` | 8367 | d375961d06b13bc5d079e4068dc6c0198b8e6c4206d7d956564fc5ad58c22099 |  |

- Note: REPO/PROTOCOL.md sections 5 to 7 were present and read for this file.

## 1. Headline results and targets

Main claim (abstract): seven measures of "pseudo-democratic autocracy" (PDA) "are not interchangeable and differ considerably from each other". The quantitative support for this claim in the main text is the empirical agreement section: Table 3 (p. 1575, pairwise Pearson correlations between the seven typologies' PDA dummies, "based on all joint observations in pairing") and the common-sample counts (intro p. 1567: "Pairwise correlations ... never exceed .63", "when looking at the sample of 6067 country-years covered by all typologies, only 144 country-years are unanimously coded as PDAs (with 3093 country-years being coded as a PDA by at least one measure)"). The regression results (Figure 5) are reported only as a coefficient plot with no printed numbers, so they are not used as targets.

Targets (copied exactly from the paper):

| id | quantity | exact statistic and code object | paper value | decimals | location |
|---|---|---|---|---|---|
| T1 | Correlation ARD vs AoW PDA dummies (largest pair) | Pearson r, pairwise complete obs: `corr.ea` cell row ARD, column AoW (`corrr::correlate()` of `HTW_RegType_MP_Autocracy` and `RegType_magaloni_EA`), `Scripts/Comparing Indices/Comparison.R` lines 14-16 | 0.636 | 3 | Table 3, p. 1575, row "Authoritarian Regimes Data Set", column AoW |
| T2 | Correlation Polity vs CPR PDA dummies (smallest pair) | same object, row Polity (`Politytype_Anocracy`), column CPR (`AnckarRegtype_MP_Autocracy`) | 0.177 | 3 | Table 3, p. 1575, row "Polity", column CPR |
| T3 | Correlation LIED vs RoW PDA dummies (within-branch pair) | same object, row LIED (`RegType_lied_EA`), column RoW (`RegType_RoW_EA`) | 0.539 | 3 | Table 3, p. 1575, row "Lexical Index of El. Dem.", column RoW |
| T4 | N of country-years coded by all seven typologies | `nrow(ead)` after `select(7 *_n vars, year) %>% na.omit()`, `Scripts/Comparing Indices/Share_Common_Sample.R` lines 10-13 | 6067 | 0 | Figure 2 caption, p. 1574; text p. 1567, 1575, 1576 |
| T5 | Common-sample country-years coded PDA by all seven | `n` at `coded_by == 7` in the `ead2` tally, `Scripts/Comparing Indices/Agreement across all.R` lines 6-22 | 144 | 0 | Text p. 1567 and p. 1576 ("144 out of 6067 country-years") |
| T6 | Common-sample country-years coded PDA by at least one | `sum(n[coded_by >= 1])` in the same `ead2` tally | 3093 | 0 | Text p. 1567 |

Ambiguity in which object gives T4 (candidates in order; the first is pre-registered): (1) `Share_Common_Sample.R` listwise sample on the seven three-category variables `*_n` plus year (this is the Figure 2 sample, whose caption states 6067); (2) `sum(n)` of the `ead2` tally in `Agreement across all.R` (listwise on the seven PDA dummies; the Figure 3 sample, which the text also calls the 6067 country-years). If the two differ, both are reported. For T6 the paper prints no table; the value is derived in the extraction script from the `ead2` tally (equivalently, T4 candidate 2 minus `n` at `coded_by == 0`). T5 and T6 must come from the same `ead2` object.

Conclusion criterion for `same_conclusion`:
- T1, T2, T3: reproduced r is positive and below 0.73, the lowest democracy-category correlation that the text (p. 1575) uses as the benchmark ("even the lowest correlation between the democracy classifications (.73 ...) is stronger than the strongest correlation between two PDA classifications"). For T1 additionally: ARD vs AoW is still the largest of the 21 pairs, or, if not, the largest pair is still below 0.73.
- T4: within 5% relative of 6067.
- T5: below 5% of the reproduced common sample (paper: "Only in 2% of the observations").
- T6: within 5% relative of 3093.
No target has an inferential statistic in the paper (no SE, CI or p-value is printed for Table 3 or the counts), so no p-value is part of any criterion.

Secondary context only (not targets; agents may report): Table 3 full matrix (LIED row 0.539 0.383 0.202 0.607 0.626 0.315; RoW row 0.539 0.398 0.300 0.567 0.460 0.255; Polity row 0.383 0.398 0.310 0.524 0.484 0.177; FH row 0.202 0.300 0.310 0.434 0.253 0.232; ARD row 0.607 0.567 0.524 0.434 0.636 0.380; AoW row 0.626 0.460 0.484 0.253 0.636 0.427; CPR row 0.315 0.255 0.177 0.232 0.380 0.427); text p. 1575: median correlation ".39", mean ".4"; democracy correlations median ".85" (mean ".84"), lowest ".73" (Appendix C, Table C1, not read); 81% and 51% unanimous agreement (p. 1575 to 1576); 56%, 44%, 29%, 15%, 23%, 64% (Figure 4 discussion, p. 1576).

Inconsistencies noticed while reading (described, not judged):
- The text says the highest pairwise correlation is ".63" (p. 1567 and p. 1575); Table 3 prints 0.636, which rounds to .64.
- The text gives the median correlation as ".39" (p. 1575). The median of the 21 distinct values printed in Table 3 is 0.398 (computed from the printed Table 3 values, not from the data), which rounds to .40; mean of the printed values is 0.405 (text ".4"). Both prose values are consistent with truncation rather than rounding. This is why the median is not a target.
- The intro (p. 1567) says "the median pairwise agreement on whether a country is an intermediate autocracy or not is only 23%"; this refers to Appendix E (not read). A different "23%" appears on p. 1576 (share of CPR PDAs coded differently by other typologies).
- The text (p. 1580) refers to "Table H1 in Appendix J"; the deposit Readme lists the script for "Table 4, Table J1".
- The Readme names "Scripts/Comparing Indices/Pairwise Agreement.R"; the deposited file is "Pairwise agreement.R" (case differs; matters on a case-sensitive file system; not used for targets).
- `Comparison.R` line 104 comment: the factor level order for Figure 1 "sometimes switched for reasons I was not able to identify" (Figure 1 only, not a target).
- The data preparation scripts read `BMR_demcoding.csv`, `ucdp-intrastate-count-onset.csv`, `nam_data.dta` and `EAHumanDev_CPS_Replication.dta`, but Dataverse serves these as ingested `.tab` files by default; the originals (correct md5) are available with `?format=original`. `Merging_measures.R` line 17 and `add_covariates.R` line 4 run `remotes::install_github("xmarquez/democracyData")` uncommented. None of this is on the target path: the Readme states the merged data are included and preparation need not be re-run.
- Table 3's own table-export line (Comparison.R line 23) is commented out; the table is only printed to the console (`corr.ea`, line 22).

## 2. Reproduction plan

Working directory = ROOT (the R project folder; the scripts use paths relative to it, e.g. `Data/Regimedata/Measures_merged.rds`). All three target scripts read only `Data/Regimedata/Measures_merged.rds` (datafile 10992326, present). No random numbers are used on the target path (no `set.seed`, no sampling).

Script order (independent of each other; run each in a fresh R session, output to `outputs/`):
1. `Scripts/Comparing Indices/Comparison.R` (Table 3, plus Table C1, Figures 1, 4, C1, D1). Packages: pacman, tidyverse, corrr, knitr, kableExtra, RColorBrewer, psych. T1 to T3 come from `corr.ea` (lines 14-16); also the median/mean summary at lines 27-30.
2. `Scripts/Comparing Indices/Share_Common_Sample.R` (Figure 2). T4 candidate 1 = `nrow(ead)` after line 13.
3. `Scripts/Comparing Indices/Agreement across all.R` (Figure 3). T5, T6 and T4 candidate 2 from `ead2` after line 22 (tally of `coded_by`).

Recommended way to run: `Rscript -e 'source("Scripts/Comparing Indices/Comparison.R", echo=TRUE, max.deparse.length=Inf); saveRDS(corr.ea, "<outputs>/corr_ea.rds")'` (similar for the other two, saving `ead` dimensions and the `ead2` tally). An extraction script `scripts/extract_targets.R` writes `outputs/targets_extracted.csv` with full-precision values (do not parse the console tibble print, which shows only about 3 significant digits). `scripts/build_results.py` builds `results.json` from that CSV.

Allowed environment fixes (each saved as a diff): installing packages into the per-run library (corrr, kableExtra, pacman, psych are not in the base env); replacing `pacman::p_load` by `library()` calls if pacman cannot install; making plotting calls non-fatal if a graphics device or font is missing (figures only, no target). Do not re-run the data-preparation scripts for the main reproduction (the Readme says the prepared data are included); rebuilding `Measures_merged.rds` may be done only as a clearly labelled exploratory check (CHANGELOG #4e) and never changes the class.

Expected sources of small differences: none expected (deterministic correlations and counts on a deposited data file). `corrr::correlate()` defaults (`use = "pairwise.complete.obs"`, `method = "pearson"`) should be recorded with the corrr version.

## 3. Robustness checks (pre-registered)

Primary quantity for all three checks: T1 (ARD vs AoW correlation). Each check also reports, as secondary, T2, T3, the largest of the 21 pairwise correlations and the median of the 21 correlations. The paper reports no inferential statistic for these quantities, so "same direction and significance" is defined here as: the estimate is positive, its 95% interval (or, in R_b and R_c, the `cor.test` 95% CI) excludes 0, and the estimate is below 0.73 (the paper's benchmark, p. 1575). The `same_direction_and_significance_as_paper` field is true only if all three hold for T1.

R_a. Country-cluster bootstrap. Input: `Measures_merged.rds`, the seven PDA dummies exactly as in Comparison.R. `set.seed(20261010)` once; 1000 resamples drawing countries (`Final_Code`) with replacement (all country-years of a drawn country enter, duplicated if drawn more than once); in each resample recompute the 7 x 7 pairwise-complete Pearson matrix with `cor(..., use = "pairwise.complete.obs")`. Report the original-sample T1 as the estimate, the 2.5th and 97.5th percentiles of the 1000 bootstrap T1 values as `se_or_ci`, the bootstrap SE, the share of resamples with T1 >= 0.73, and as p-value the two-sided bootstrap proportion min(2 x share of T1 <= 0, 1). Resamples where T1 is undefined are counted and reported, not replaced. Countries are resampled because country-years within a country are not independent.

R_b. Influential-country exclusion. The variables are binary dummies, so |z| > 3 and top/bottom 1% rules on the values are meaningless, and there is no continuous predictor. Rule instead: for each country (`Final_Code`) with at least one non-missing pair of the ARD and AoW dummies, recompute T1 without that country (leave-one-country-out); rank countries by |T1 without country minus T1 full|; drop the top 1% of these countries, rounded up to a whole number (at least 1 country); recompute the full 7 x 7 matrix on the remaining data. Report T1 with `cor.test` 95% CI and p, the dropped countries and how many country-years they had.

R_c. Alternative sample definition: listwise common sample. Compute the 7 x 7 Pearson matrix on the common sample only (country-years with all seven PDA dummies non-missing, i.e. the Figure 3 sample of `Agreement across all.R`, expected about 6067 rows), instead of pairwise complete observations. Report T1 with `cor.test` 95% CI and p, N, the largest pair and the median of the 21 values. Reason: Table 3 mixes different coverage periods across pairs (e.g. AoW 1950-2012 vs LIED 1789-2022), while the text's other agreement numbers use the common sample; this tests whether the "weak correlation" conclusion depends on that choice.

## 4. Known risks

- Paper text: Table 3 and all targets were read from text extracted from the publisher PDF, not from the PDF bytes (download blocked); no sha256 for the PDF. The supplemental appendix (Appendix C, E and others) could not be read.
- Files: all files the three target scripts read are present (`Measures_merged.rds`). For the non-target preparation scripts, four inputs exist only under their ingested names (.tab) in the default download; originals must be fetched with `?format=original`. The Kim preparation script loads cshapes, maptools and rgeos (maptools and rgeos are archived on CRAN); not on the target path.
- Provenance: the merged file is the authors' output of `Merging_measures.R`; the reproduction uses it as deposited. Re-deriving it needs `democracyData` from GitHub and is not part of the reproduction.
- Dependencies: light (corrr, kableExtra, psych, tidyverse). No Stata or proprietary software. No version pins in the deposit (no renv.lock, no sessionInfo); `.Rhistory` and a 49-byte `.RData` are deposited but give no versions.
- Compute: trivial (32,353 rows x 56 columns). R_a: 1000 recomputations of a 7 x 7 matrix, about a minute.
- Paths: the project folder name contains spaces and full stops; quote paths.
