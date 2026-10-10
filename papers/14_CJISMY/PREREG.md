# PREREG: 14_CJISMY

Written 2026-10-10 (IST, about 21:10), before any analysis code was run. No analysis code from the deposit was executed to write this file. Only the paper, the deposit metadata, the R scripts, the readme and the header and value sets of one data file (`epro_data_h1.csv`, read with Python's csv module) were read.

The main text was readable: the full publisher PDF (open access, CC BY-NC 4.0) was downloaded and all numbers below are copied from it. The online supplementary appendix (Appendices A to W) was not opened; no target comes from it.

- Paper: Gremler, F., Vogt, M. and Weidmann, N. B. (2025). "Intra-ethnic divisions and disagreement over self-determination demands in ethnic movements". Political Science Research and Methods 13(4), 815-831 (first published online 2024). DOI https://doi.org/10.1017/psrm.2024.33
- Text source read: Cambridge Core PDF https://www.cambridge.org/core/services/aop-cambridge-core/content/view/A01DEE38CA7EDB4CB3A63735B6033E60/S2049847024000335a.pdf/div-class-title-intra-ethnic-divisions-and-disagreement-over-self-determination-demands-in-ethnic-movements-div.pdf (downloaded 2026-10-10 15:30 UTC, HTTP 200, 278,790 bytes, 17 pages, sha256 dd635403b6d4affbee10f8148fc5f236c5e56843c39feb84a31cd5ff219e3b78). Journal page = PDF page + 814.
- Dataset: "Replication Data for: Intra-Ethnic Divisions and Disagreement over Self-Determination Demands in Ethnic Movements", Harvard Dataverse, https://doi.org/10.7910/DVN/CJISMY , version 1, released 2024-07-03, licence CC0 1.0, 44 files, none restricted.
  - File list API: https://dataverse.harvard.edu/api/datasets/:persistentId/?persistentId=doi:10.7910/DVN/CJISMY (saved as `data_statement_raw/dataverse_CJISMY.json`, sha256 4d4143031972dcb8159a3245898b8008e7c1b8000abfadf20e332595cc25abe8).
  - Per-file download: `https://dataverse.harvard.edu/api/access/datafile/<id>` (follow redirects, `curl -L`; without `-L` the response body is empty). For ingested `.tab` files add `?format=original` to get the authors' CSV.
  - Downloaded for this pre-registration: all 25 `.R` files, `readme.txt`, and the original CSV of `epro_data_h1.tab`. The MD5 of every downloaded .R file and readme.txt matched the Dataverse checksum (the Dataverse MD5 of an ingested .tab file refers to the .tab version, so it cannot be compared with the original CSV). Scratch copies and `checksums.sha256` are in /workspace/audit_runs/14_CJISMY/prereg/.
  - Deposit layout is flat (no folders), although the scripts read `data/<file>.csv`.

## Dataset files

| datafile id | file (as deposited) | original format | bytes (Dataverse filesize) | sha256 (if downloaded) | Dataverse MD5 |
|---|---|---|---|---|---|
| 10360785 | `01_make_directories.R` |  | 96 | 1e8380c32b5ad669c12bd560944437851b204f9ab1717209f7b9ae3be9b1f0d8 | 318973dff22cd766b1bdda969f1bcf9b |
| 10360818 | `agricultural_variables_epr_desc.R` |  | 243 | 5431b20a6167b241b0a869a972bebba222ec041237442fd24070453c11717063 | 9b879de596811c9b7da650321a00ff47 |
| 10360783 | `all_models_crossectional.R` |  | 6141 | 0d6b8185d6a71918f822e1b2c689a5b5b85567a3e09ae1d71817691e48276b16 | 4f5315bdbab40e79d5c0bfdc92b3d197 |
| 10360806 | `analysis_fragmentation_orgs.R` |  | 3446 | ec21c61ad3f3982298fe47943b4264704ab33216d9f98c86f2b3cadf99f0ecc2 | 10e9c34c0e2b7ed5628a1e9897b61135 |
| 10360798 | `crosssection_linear.R` |  | 11740 | 04db812908bf7a75f95046ea94bd2953d8770b8db54923470d3b9c36e3c24d0f | 0127ced86315df80821cd9943aaed9ad |
| 10360810 | `crosssection_linear_gov_inclusion.R` |  | 8933 | a19d89bbc2829a79114f0ea562447852e5c023d8e8388a6351eacf9a0685eadc | 71ca0249450145e5155940f0c304013d |
| 10360803 | `crosssection_max_disagreement.R` |  | 7489 | 1c13d00dd5926f21b6a7305449b831ac95b10761f323f40784180b4fbd522d79 | e6ca2321c5f48112d4dd7f5461ad5214 |
| 10360790 | `crosssection_weighted_share.R` |  | 5142 | f758c45e671176647bccd854d3555d56a9ba9ce0580d3c66ff46ca10ca5d58bb | c5501aa432f6764f93b7bdab35a7fabe |
| 10360808 | `descriptives_summary_tables.R` |  | 3522 | 0cec4886b280e069c11dc882147d65aa95a34024afb5c0823add6c28ffadf3ab | 2269a050a1214d46ef73820726e313f0 |
| 10360797 | `EPR Org_codebook.pdf` |  | 1015677 | not downloaded | 276333f2f7950a3a39c1f6e950afa5be |
| 10360796 | `epro_data_h1.tab` | `epro_data_h1.csv` 1839633 bytes | 1775671 | original csv (?format=original, 1839633 bytes): cc27339c09263ba5633c4170ad00556b8bab4a402a5c918f6da2192ed6cc1139 | 7d44157562ce2822050f95a9d0a2d904 |
| 10360794 | `epro_data_h1_no_low_confidence.csv.gz` |  | 611749 | not downloaded | 36bb8c961e43dd7a5ab01d365229661b |
| 10360780 | `epro_data_h1_no_multiethnic.csv.gz` |  | 535658 | not downloaded | f7e310142d0d5d6c735727315924afcd |
| 10360821 | `epro_data_h1_no_temp.csv.gz` |  | 601036 | not downloaded | 444794b42e8aa4073f061401e86dfb1d |
| 10360809 | `epro_data_h1_only_viol_elec.csv.gz` |  | 397693 | not downloaded | 09b2e50a6f3705570272e1c3fe9a393f |
| 10360801 | `epro_data_h2.tab` | `epro_data_h2.csv` 25185448 bytes | 20938086 | not downloaded | b5eacb8e6f6283025ee2aaa66fb7d3e6 |
| 10360811 | `epro_data_h2_no_low_confidence.csv.gz` |  | 3129477 | not downloaded | d90b2c24b333278fdf504728ef3a30bb |
| 10360805 | `epro_data_h2_no_multiethnic.csv.gz` |  | 2716825 | not downloaded | 86d3832e7a3c7769000bbe6f745bb4a7 |
| 10360793 | `epro_data_h2_no_temp.csv.gz` |  | 3078325 | not downloaded | 3f9c797d30bca8878c216527a61489e5 |
| 10360781 | `epro_data_h2_only_viol_elec.csv.gz` |  | 2015682 | not downloaded | 2ef0d536a40726fd067c5a4809d09d5e |
| 10360802 | `epro_geo_data_h3.tab` | `epro_geo_data_h3.csv` 82037766 bytes | 80408984 | not downloaded | 6362fdad47c61ea6d67788abf6d65d0a |
| 10360789 | `epro_geo_data_h3_no_low_confidence.csv.gz` |  | 17980257 | not downloaded | 7c776e81b989f10aab8768822ad61848 |
| 10360782 | `epro_geo_data_h3_no_multiethnic.csv.gz` |  | 17650623 | not downloaded | 639533dcdc12b590ae2d3c5730e61ae5 |
| 10360795 | `epro_geo_data_h3_no_temp.csv.gz` |  | 17922343 | not downloaded | 204b7dc77d51ff6cb815f594ea6833f4 |
| 10360817 | `epro_geo_data_h3_only_viol_elec.csv.gz` |  | 5659767 | not downloaded | 847b7179586cd405d07e1093d06eb73f |
| 10360815 | `epro_t.tab` | `epro_t.csv` 77530080 bytes | 78919635 | not downloaded | 4b0440f6d1a3e2545c1c441ccd8e1513 |
| 10360800 | `funs_and_constants.R` |  | 3893 | 9f2511f6167f07e02de0f86052c3b717a9038b374c1c2638c5afc5f87d2d5688 | a05a858f9ec7005506a9e70ff4ef6de7 |
| 10360804 | `h1_robustness_fourfold_comparison.R` |  | 4074 | 2bf23a0e865a1eca99d5756c26a444b15cd542ab867c22b2af69188b353880d9 | 6f36030fbe51f764cd5811d6ad35ead5 |
| 10360814 | `h1_robustness_pasture_land_livestock.R` |  | 2734 | 6ef5d897eb216c11d47beb7979353d3317e8aa3b92502d3e750e676f6253a84c | 0069dfe87ef9a8d46d2c0d1280c245fa |
| 10360799 | `hhi.tab` | `hhi.csv` 10017274 bytes | 10036680 | not downloaded | 8b040e1c692db953e34945b3c97a176f |
| 10360820 | `multilevel_models.R` |  | 11963 | 08386883be6001696c2593d67cfae2289cc6900b04498b8fd7ae225d6acc2384 | 70f46f13de76e3536102fceb365a4fdd |
| 10360819 | `panel_linear_probability.R` |  | 7963 | aba29a6c69656b183b14d50ad3a7ac8554daf7d4e74ced5595843e18846621b0 | c7bb71e3d9606eadc7435bc2d6f4a524 |
| 10360822 | `panel_linear_probability_only_variation.R` |  | 11443 | 699a03ca5d9fa5c77bbcb5f26950c5f2c1bd3825cc9041f95661316c9c53c12c | 0863b2801b7efc87753c24f1ab1c0c4e |
| 10360787 | `panel_logistic.R` |  | 4774 | bfb8e814d96122c5fa2b4e902b2c916e9fa21fa647c749888b63f176971ac5cd | b38028cda58ffd2caba4b21a9bc6c189 |
| 10360788 | `readme.txt` |  | 2927 | 5582e4a12b8c7735211136daeb50dcf28ed49339c10cb0206a5d580314f65318 | cbf6c795fac2c77d0369f33848e903e4 |
| 10360813 | `robustness_agri_thresholds.R` |  | 2881 | 1fbda9c747264c266b7a02e35e59dab3147acc22c49cd18998da204ec36ea9ea | b1ce43eee554efb667eed6d864e76dd8 |
| 10360816 | `robustness_centrifugal_centripetal.R` |  | 5244 | f716b7a8cc0783e387ac5f28cca2a15e5824189b122adce1dc291baa41a6491e | 03528dc7a3d59f88ff5330e258e9e5ff |
| 10360812 | `robustness_h2_linguistic_segments.R` |  | 5504 | ca0bb697efb6b135cda9957969609f8414c837f00a3cc8bcdc0a0939c8d3f403 | 4125b2cf0f05b70d9f1d2bd002a9525b |
| 10360786 | `robustness_h2_religious_alignment_cross_sectional.R` |  | 8120 | d8c1fa8ee48494f2f963af46e0818324ca75416c794ced6176161b20f039077a | 47c2ee2111df218913f1738d0bc11ead |
| 10360791 | `robustness_no_low_confidence.R` |  | 5232 | 3da7e21f835a7b58e2f1982bffe6477ea38f0c446c2ca3dc4ac8d9199663bce2 | 7730122d61fba854dd32d0153801a68e |
| 10360807 | `robustness_no_multiethnic.R` |  | 5219 | 905fd3722bce9d87ffbca492cc1c6e7e3af366c3472c00e1c392a5dd0514ad46 | 6113138387e2861dffddd45b6b8f8852 |
| 10360784 | `robustness_no_temp_links.R` |  | 5191 | 25acac29c7d18a53261d3cc1f65c7622f4225c64fa9899375451a802e4bf6135 | d5e9bcab7cbe1f296b1ed9fadc14c843 |
| 10360792 | `robustness_only_viol_elec.R` |  | 5216 | b1e67514accfa2b5db8ec591513f1fd92d0d1c9d6a7c1d84ae2676698d972f42 | 26966b00e00aa5f9a3ccfb61a0e5263d |
| 10360779 | `spatial_hhi_h3.R` |  | 3389 | 02c9cf5b526af8903e4df2bd63ec761abea8440af4cb7d379292e71adda34691 | ffcc49b6d2cf4deabbf9cac1d4178199 |

## 1. Headline result and targets

Main claim (abstract, p. 815): "Our pre-registered study finds support for one of our hypotheses: heterogeneity in groups' income sources increases disagreement over self-determination demands." The table that reports it is Table 1 ("Cross-sectional models testing H1", p. 824): linear models with country fixed effects and standard errors clustered by country, on group-level means over 2000-2019 (p. 823). Models 1 and 2 use the binary disagreement measure (mean over years), Models 3 and 4 the share of dissenting organizations. Table note: "***p < 0.001; **p < 0.01; *p < 0.05; ⋅p < 0.1."

| id | quantity | paper value | decimals | code object (crosssection_linear.R) | location |
|---|---|---|---|---|---|
| T1 | Natural resources and agriculture, Model 1 (binary disagreement) | 0.51 (SE 0.12, ***) | 2 | `coef(full_model_h1)["resource_and_agriculture"]` (line 51) | Table 1, p. 824, Model 1 |
| T2 | Natural resources and agriculture, Model 3 (prop. disagreement) | 0.19 (SE 0.06, **) | 2 | `coef(full_model_h1_max)["resource_and_agriculture"]` (line 54) | Table 1, p. 824, Model 3 |
| T3 | Neither resources nor agri (baseline: both), Model 2 | -0.48 (SE 0.16, **) | 2 | `coef(full_model_h1_n_resources)["none_one_or_both_nats_agri_charNone"]` (line 57) | Table 1, p. 824, Model 2 |
| T4 | Resources or agri (baseline: both), Model 2 | -0.50 (SE 0.11, ***) | 2 | `coef(full_model_h1_n_resources)["none_one_or_both_nats_agri_charSingle"]` (line 57) | Table 1, p. 824, Model 2 |
| T5 | Num. obs., Model 1 | 138 | 0 | `nobs(full_model_h1)` | Table 1, p. 824, row "Num. obs." |

The printed table maps to texreg's `list(full_model_h1, full_model_h1_n_resources, full_model_h1_max, full_model_h1_n_resources_max)` (lines 77-83), written to `tables/h1_crosssection_lin.tex`; the same four models are printed to the console by `screenreg` (lines 65-66). The labels come from `coef_map` in `funs_and_constants.R`.

Sample sizes printed: Table 1 prints "Num. obs." 138 and "Num. groups: Country" 62 for each of Models 1 to 4. No other N is printed for these models in the main text.

Statistic behind the stars (ambiguity). The table shows stars, not p-values. Candidates, in order; the first is pre-registered:
1. p-value from `fixest::coeftable()` of each model as estimated (country-clustered SE, t distribution with fixest's default degrees of freedom), which is what texreg reads for fixest objects.
2. Two-sided normal p-value from coefficient / clustered SE.

Conclusion criterion for `same_conclusion`:
- T1: estimate > 0 and p < 0.001 (paper ***).
- T2: estimate > 0 and p < 0.01 (paper **).
- T3: estimate < 0 and p < 0.01 (paper **).
- T4: estimate < 0 and p < 0.001 (paper ***).
- A p-value in a stricter band than printed still counts as the same conclusion; the band reached is reported in the note.
- T5: same conclusion if N is within 5 of 138; `match_to_rounding` only if exactly 138.
- T3 and T4 are defined with "Both" as the reference level, as the table states. If the run's reference level is not "Both", see Section 2 (step 5).

Secondary numbers (context only, not targets): Model 2 R2 0.72, Model 1 R2 0.70 and adj. R2 0.39; Model 4 coefficients -0.17* (0.08) and -0.21*** (0.05); Figure 2 (predictions from Models 1 and 2) has no numeric values beyond the prose.

Inconsistencies noticed while reading (described, not judged):
- p. 824: the text says a min-to-max change of the income-streams variable "predicts a 0.2 point increase in the value of disagreement", referring to the left panel of Figure 2 (Model 1). Table 1 prints 0.51 for that coefficient in Model 1; 0.19 is the Model 3 coefficient.
- p. 825: "diverse income streams are associated with higher levels of agreement"; the hypothesis and Table 1 concern disagreement.
- The paper calls the H1 variable dichotomous (p. 823). The H1 data file is decadal (years 1950, 1960, ..., 2010; 238 group-years in 2000 and 2010 for 139 groups in 62 countries, from reading the file), and the code takes the mean of `resource_and_agriculture` and of `disagreement` over the years >= 2000. In the cross-section both can therefore be 0, 0.5 or 1. The paper (p. 823) says continuous variables are aggregated by mean and nominal ones by mode.
- The categorical H1 variable is built with `Mode(as.factor(...))` inside `summarize` (line 26). With two years per group, ties are broken by first occurrence (the 2000 value), per the `Mode` function in `funs_and_constants.R`.
- Table labels differ slightly from `coef_map` (paper "Number of kin groups" and "Any multiethnic organization"; code "N kin groups" and "Any multiethnic organizations"), so the printed table text was edited after export or produced from a different label map. Cosmetic.
- readme.txt says the datasets are "in the data folder" and names `epro_t.csv`; the deposit is flat and holds Dataverse-ingested `.tab` versions (CSV originals available via `?format=original`).
- One row in the 2000-2010 H1 data has a missing `nightlight_total_pc_log` (from reading the file); 139 groups against the printed 138 observations is consistent with one group being dropped for missing values, but this was not checked by running anything.

## 2. Reproduction plan

Scripts the readme lists for the main results: `01_make_directories.R`, `crosssection_linear.R`, `panel_linear_probability.R`, `panel_logistic.R`, `panel_linear_probability_only_variation.R`. All targets come from `crosssection_linear.R` (H1 section, lines 20-115). The panel scripts are not needed for the targets and are not part of this reproduction.

Steps (RUNDIR = /workspace/audit_runs/14_CJISMY/<AGENT>/run):
1. Download `funs_and_constants.R`, `01_make_directories.R`, `crosssection_linear.R` (datafile ids 10360800, 10360785, 10360798) and the original CSVs of `epro_data_h1.tab` (10360796), `epro_data_h2.tab` (10360801) and `epro_geo_data_h3.tab` (10360802) with `?format=original`. Save them as `RUNDIR/data/epro_data_h1.csv`, `RUNDIR/data/epro_data_h2.csv`, `RUNDIR/data/epro_geo_data_h3.csv`. Record sha256. (The script reads all three at lines 16-18 even though only h1 is needed for the targets. Expected original sizes: 1,839,633; 25,185,448; 82,037,766 bytes.) The h1 original CSV fetched for this pre-registration has sha256 cc27339c09263ba5633c4170ad00556b8bab4a402a5c918f6da2192ed6cc1139.
2. Working directory RUNDIR. Run `Rscript 01_make_directories.R` (creates `plots/`, `tables/`), then `Rscript -e 'source("crosssection_linear.R", echo=TRUE, max.deparse.length=Inf); save(list=ls(), file="outputs/session.RData")'`, logging stdout/stderr to `outputs/`. The script has no random number calls.
3. Package versions: readme records R 4.2.1 (Windows) with fixest 0.11.1, texreg 1.38.6, dplyr 1.0.9, readr 2.1.2, ggplot2 3.3.6, patchwork 1.1.2, specr 1.0.0, broom.mixed 0.2.9.4, marginaleffects 0.11.1, vctrs 0.5.1. Following the runbook and CHANGELOG #6(b), try fixest 0.11.1 first (`remotes::install_version`), and if it builds, also dplyr 1.0.9 and vctrs 0.5.1 where they install on R 4.5. Record what was installed. If fixest 0.11.1 cannot be built, use current CRAN fixest and say so.
4. Allowed environment fixes (each as a diff): file paths; `library(specr)` and `library(broom.mixed)` may be removed if they cannot be installed, because no function from either is called in `crosssection_linear.R` (checked by reading); plotting/ggsave lines (95-115, 200-221) may be made non-fatal if `marginaleffects` or a graphics device fails, since they do not touch estimates.
5. Extraction: `scripts/extract_targets.R` loads `outputs/session.RData` and writes `outputs/targets_extracted.csv` with, for each of the four H1 models: every coefficient, clustered SE, t, p (`fixest::coeftable`), `nobs()`, the number of fixed-effect groups, the factor levels of `none_one_or_both_nats_agri_char` in `mean_h1` in order, and the fixest version. If the reference level of `none_one_or_both_nats_agri_char` is not "Both", T3 and T4 as-is are reported as not produced (null, with the levels found), and as a labelled deviation the extraction script also refits Model 2 with `relevel(factor(none_one_or_both_nats_agri_char), ref = "Both")` on the same data (`outputs/targets_releveled.csv`); the class is judged on the as-is run and the deviation is reported alongside (CHANGELOG #4(c) style). `scripts/build_results.py` builds `results.json` from those CSVs. The `.tex` table is copied to `outputs/` as a cross-check.
6. Expected small differences: none in estimates if the data and model match (OLS, no randomness). Possible differences: (a) newer fixest versions drop singleton fixed-effect groups by default, which changes `nobs()` (and possibly clustered SEs through the small-sample correction) without changing coefficients; this is why fixest 0.11.1 is tried first, and if current fixest is also run, both are reported; (b) the factor reference level (step 5).

## 3. Robustness checks (pre-registered)

All three target the main H1 estimate, T1 (`resource_and_agriculture` in `full_model_h1`). Each also reports the same quantity for Model 3 (T2) as secondary, but the primary estimate written to `results.json` is the T1 quantity. Estimation sample for all checks: the rows of `mean_h1` that `full_model_h1` used (`mean_h1[obs(full_model_h1), ]`, 138 rows if the run matches). Formula throughout (F1): `disagreement ~ resource_and_agriculture + n_orgs + regaut + groupsize + incidence_flag + status_pwrrank + any_multiethnic + nightlight_total_pc_log + n_tek_groups`. "Same direction and significance" for every check = coefficient > 0 and p < 0.05 two-sided (the paper's own lowest star threshold); whether p also stays below 0.001 (the band printed for T1) is reported in the note.

R_a. Country-cluster bootstrap. `set.seed(20261010)` once; 1000 resamples of the 62 countries with replacement; each drawn country contributes all its rows and gets a new unique id per draw (so duplicated countries are separate fixed effects and clusters); refit `feols(F1 | boot_id, cluster = ~boot_id)` and record the `resource_and_agriculture` coefficient. Report the original-sample estimate as `estimate`; `se_or_ci` = bootstrap SD and percentile 95% CI (2.5th and 97.5th percentiles); `p_value` = min(1, 2 x min(share of draws <= 0, share of draws >= 0)). Draws where the coefficient is not estimated (dropped for collinearity, or fit error) are counted and reported, not replaced; quantiles use the successful draws. Same direction and significance here = estimate > 0 and percentile CI excludes 0.

R_b. Outlier exclusion. The default |z| > 3 rule on the outcome is not informative here: in the cross-section the outcome `disagreement` is the mean of a 0/1 variable over the years 2000 and 2010, so it can only be 0, 0.5 or 1, and the main predictor has the same three values (from the data structure and value sets read for this file; no model run). Top/bottom 1% trimming of a three-valued variable is equally meaningless. Rule used instead (stated in advance): fit `lm(F1 + factor(countries_gwid))` on the estimation sample (check that its `resource_and_agriculture` coefficient equals `full_model_h1`'s to 1e-8 and record that); compute `cooks.distance()`; drop every case with Cook's distance > 4/N (N = rows of the estimation sample); cases with non-finite Cook's distance (leverage 1, e.g. the only group of a country) are kept and counted. Refit `feols(F1 | countries_gwid, cluster = ~countries_gwid)` on the remaining rows; report estimate, clustered SE, p (`fixest::coeftable`), and the number dropped. For completeness, also report (note only) how many cases the default |z| > 3 rule on `disagreement` would have removed, computed with the sample SD on the estimation sample. For the Model 3 secondary, apply the same Cook's rule using the Model 3 outcome `share_disagreement`.

R_c. Alternative analysis choice: no country fixed effects. Refit F1 by OLS on the same estimation sample without country fixed effects, SEs still clustered by country: `feols(F1, cluster = ~countries_gwid, data = est_sample)`. Reason: with 62 country effects for 138 groups, countries with a single group contribute nothing to the within-country estimate; the pooled model also uses between-country variation. Report estimate, clustered SE, p. Same rule for Model 3 as secondary.

## 4. Known risks

- fixest version: N (T5) and clustered SEs may differ under current fixest if singleton fixed effects are dropped; coefficients should not change. Under CHANGELOG #6(a), an N-only mismatch with matching estimates is class C, not D.
- Factor reference level for T3 and T4: `Mode(as.factor(x))` returns a factor whose levels are those present in each group; `summarize` combines them, and the resulting level order (and therefore the fixest reference) depends on dplyr/vctrs behaviour and group order. The paper's baseline is "Both". A different reference changes the T3/T4 coefficients without any change in the data.
- Data format: the deposit holds ingested `.tab` files; the code expects `data/*.csv`. Using `.tab` downloads instead of `?format=original` would break `read_csv` parsing. The fix (download originals into `data/`) is an environment fix.
- Packages: fixest 0.11.1, specr 1.0.0 and marginaleffects 0.11.1 may not build on R 4.5 / aarch64. Only fixest, readr, dplyr and texreg are needed for the targets.
- Missing files: some non-headline scripts read files that are not deposited (see DATA_STATEMENT.md): a sourced helper script in `all_models_crossectional.R` and `crosssection_max_disagreement.R`, raw inputs in `spatial_hhi_h3.R` (builds `hhi.csv`, which is deposited) and `agricultural_variables_epr_desc.R`. None is read by `crosssection_linear.R`, so the headline targets are not affected. The data-construction pipeline from raw EPR-O to `epro_data_h1.csv` is not in the deposit; the reproduction starts from the deposited analysis files.
- Compute: trivial (OLS on 138 rows). The h3 file is 82 MB and is read by the script but unused for the targets; memory is fine.
- No Stata or proprietary dependency. No sign-in needed.
