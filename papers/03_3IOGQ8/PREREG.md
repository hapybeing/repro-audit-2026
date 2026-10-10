# PRE-REGISTRATION: 03_3IOGQ8

Written 2026-10-09 (IST), before any analysis code was run. No analysis code was run to write this document.

- Paper: Whedon S. D., Lee K., Wang Z. A., et al. "Circular Engineered Sortase for Interrogating Histone H3 in Chromatin". J. Am. Chem. Soc. 2024, 146(49), 33914-33927. DOI https://doi.org/10.1021/jacs.4c12585 (PMID 39585806, PMCID PMC11638967, open access CC BY 4.0).
- Paper text read from: Europe PMC full text XML https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11638967/fullTextXML (sha256 b1a47451aec28d80c701135a9a70d759cbc82e11846b926beaba82e10c3ba846).
- Supporting information read from: Europe PMC supplementary files bundle https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11638967/supplementaryFiles (zip sha256 be4ff554b3afe6112076426d2e81241d03b4696624ace24149d7fd49224ed97b), containing `ja4c12585_si_001.xlsx` (Tables S2 to S5; sha256 f5d47bb73aa02d04a6153e16ba6acb02206580b213e35b722092d2bd509386c8) and `ja4c12585_si_002.pdf` (SI PDF; sha256 bf87a894e403945d3510c24f24b0538a09904098330b4a7c2a0f5c26bfb2f4e1). The same files are listed on https://pubs.acs.org/doi/10.1021/jacs.4c12585 .
- Dataset: Whedon S. "A circular engineered sortase for interrogating histone H3 in chromatin - Source Data", Harvard Dataverse, version 1, DOI https://doi.org/10.7910/DVN/3IOGQ8 , licence CC0 1.0.
- Note for the record: REPO/PROTOCOL.md was not present in the repository when this pre-registration was written (only AGENT_RUNBOOK.md, CHANGELOG_METHOD.md and META.md were read). The runbook's classification summary (A to E) was used as the reference.

## 0. What the dataset contains (from the Dataverse API file list, 2026-10-09)

| file id | file | size (bytes) | type |
|---|---|---|---|
| 10407991 | 20240215_EBZ_Cole_20ng_293_MS275vDMSO_1to1_6plex_2-15grad.raw | 253,010,642 | Thermo RAW (middle-down, DMSO vs MS275 6plex) |
| 10407990 | 20240216_EBZ_Cole_20ng_293_1to1_6plex_DMSO_Corin_g2-15.raw | 245,887,307 | Thermo RAW (middle-down, DMSO vs Corin 6plex) |
| 10408478 | Byonic_Middle-Down_Processing_Notebook.Rmd | 143,738 | R notebook (3351 lines; sha256 5f364768836c382b7b68ba93207e450d7b42dee13bc554d222a55676e976a538) |

There is no README, no processed/intermediate table, no Byonic PSM export, no mzML file and no bottom-up data, although the dataset description says "Raw and processed bottom-up and middle-down mass spectrometry data, and scripts". File list API: https://dataverse.harvard.edu/api/datasets/:persistentId/?persistentId=doi:10.7910/DVN/3IOGQ8

What the R notebook does (read in full at the level of its section structure, and in detail for the input, normalisation, test and output sections):
1. Reads `Byonic_results.csv` (line 498), a PSM export from the commercial Byonic search engine (Protein Metrics). Filters PEP.2D <= 0.05 and Delta Mod Score >= 10, keeps H3.1/H3.3 tail sequences, parses modifications.
2. Splits the PSMs into experiments by `MS.Alias.name`, with placeholder names `"your_ms_experiment_1"` for all three experiments (lines ~600-608).
3. Opens spectra with `mzR::openMSfile()` from `.mzML.gz` files at placeholder paths `C:/path_to_your_data/file1.mzML.gz` etc. (lines 671-679). The deposited files are Thermo `.raw`, so a RAW to mzML conversion is needed first.
4. Matches EThcD fragment ions (15 ppm), resolves multi-PSM spectra, extracts TMT reporter ions with isotope correction, computes proteoform fractional intensity.
5. TMT channel normalisation three ways (cumulative, mean, median; from line 2693), log2 transform, then per proteoform (`all_mods`) a two-sided Welch `t.test()` of all log2 reporter values from DMSO channels (126, 127, 128) vs drug channels (129, 130, 131) pooled over all single-PSM scans of that proteoform (lines ~2950-3130). log2 fold change `fc_cum` = mean(log2 drug) minus mean(log2 DMSO). Volcano classification: |log2FC| > 0.6 and p < 0.05.
6. Writes `experiment1_proteoform_df_<suffix>.csv`, whose 15 columns (all_mods, proteoform_intensity, percent_abundance, cumulative/mean/median p value, log2-fold change, ctrl_percent, var_percent) are exactly the columns of SI Tables S2 to S5. Only "experiment1" is processed downstream; the notebook must be run once per 6plex sample with experiment1 pointed at that sample.
7. Contains no random number generation (no `set.seed`, no sampling). `parallel::makeCluster(detectCores()/2)` is used for speed only.

## 1. Headline result and target numbers

Abstract claim this code+data could reproduce: "cW11 sortase ... facilitating multiplex 'cut-and-paste' middle-down proteomics with tandem mass tags. This cut-and-paste proteomics approach permits the quantitative analysis of histone H3 modification crosstalk after treatment with different histone deacetylase inhibitors."

Main quantitative statement in the text (Results, section "'Cut-and-Paste' Middle-Down Proteomics of Histone H3 Modifications"): "Relative to the DMSO vehicle, both HDAC inhibitors significantly decreased H3 tail proteoforms with one or two modifications while increasing those with three or four modifications (Figure 1h,i). The most significant increase was seen in H3K9acK14acK23acK27me2; however, a greater increase was seen with MS275 than with Corin (155% vs 110% increase)." and "By LC-MS/MS, we identified ~150 uniquely modified peptides (proteoforms) in a combined DMSO vehicle/Corin sample and ~180 in a combined DMSO vehicle/MS275 sample (Figure 1f and Tables S2 and S3)."

The R notebook writes the per-proteoform table that is published as SI Tables S2 to S5, so the targets are taken from that table and from the text values derived from it.

| id | description | paper value | decimals | location |
|---|---|---|---|---|
| T1 | Percent increase of H3K9acK14acK23acK27me2 after MS275 vs DMSO | 155 | 0 | Main text, Results, "Cut-and-Paste" Middle-Down Proteomics section ("155% vs 110% increase") |
| T2 | Percent increase of H3K9acK14acK23acK27me2 after Corin vs DMSO | 110 | 0 | Same sentence as T1 |
| T3 | Cumulative-normalisation log2 fold change, proteoform "K9ac K14ac K23ac K27me2", DMSO vs MS275 | 1.35671135138228 | 14 | SI xlsx ja4c12585_si_001.xlsx, sheet TableS5_DMSO_MS275_quantifiabl (also TableS3), column `cumulative_log2-fold_change` |
| T4 | Cumulative-normalisation log2 fold change, proteoform "K9ac K14ac K23ac K27me2", DMSO vs Corin | 1.07715354602644 | 14 | SI xlsx, sheet TableS4_DMSO_Corin_quantifiable (also TableS2), column `cumulative_log2-fold_change` |
| T5 | Number of proteoforms (rows) identified in the DMSO/MS275 6plex sample | 179 | 0 | SI xlsx, sheet TableS3_DMSO_MS275_proteoforms, count of data rows (text says "~180") |

Supporting values from the same rows, for context only (not targets): MS275 cumulative p = 6.05188382826008e-53; Corin cumulative p = 4.29831138583007e-38. Number of rows: Table S2 (Corin, all) 157, Table S4 (Corin, quantifiable) 73, Table S5 (MS275, quantifiable) 98.

Pre-registered conversion and comparison rules:
- T1 and T2 are computed from the reproduced cumulative log2 fold change as 100 * (2^fc_cum - 1). Cumulative normalisation is the primary method stated in the Methods ("channel normalized to the maximum average channel"; mean and median "produced broadly similar results").
- Observation recorded before any run: applying that formula to the published SI values gives 156.10 for MS275 and 110.99 for Corin, so the text values 155 and 110 do not equal the SI values rounded to 0 decimals (they are consistent with truncation, or with a slightly different calculation). Therefore even an exact reproduction of Table S5 will give match_to_rounding = false for T1 while being within 5%. For T1 and T2 the agent should report match_to_rounding as specified in the runbook, and add in `note` whether floor(reproduced) equals the paper value. The primary judgement for T1 and T2 is within_5pct and same conclusion (MS275 increase > Corin increase, both p < 0.05 and log2FC > 0.6).
- T3 and T4 are copied with all 14 decimals stored in the xlsx; match_to_rounding at 14 decimals is expected only if the identical Byonic export, mzML conversion and package versions are used. within_5pct is the practical criterion.
- T5 is a count of rows in the reproduced Corin/MS275 `proteoform_df` csv for the MS275 sample.
- "Same conclusion" for the headline: in both drug comparisons, K9ac K14ac K23ac K27me2 is classified UP (fc_cum > 0.6, p < 0.05) and the MS275 fold change exceeds the Corin fold change.

## 2. Exact reproduction plan

Script: `Byonic_Middle-Down_Processing_Notebook.Rmd` (Dataverse file id 10408478), run chunk by chunk with `Rscript -e "rmarkdown::render()"` or by extracting chunks with `knitr::purl()`, once per 6plex sample.

Inputs required:
1. `Byonic_results.csv`: Byonic PSM export for each RAW file. NOT DEPOSITED. Producing it requires the commercial Byonic search engine (Protein Metrics licence) with the settings in the paper's Methods ("Middle-Down Proteomics" paragraph: no cleavage, 500 ppm precursor, 15 ppm fragment, EThcD, up to 6 common PTMs, Propionyl rare, TMT6plex fixed on H, +76.1001 Da C-terminus, FASTA of histones + contaminants + the two H3 tail sequences). The FASTA of "histone protein sequences, common contaminants" is also not deposited. The audit rules allow public downloads only and do not provide a Byonic licence, so this input cannot be regenerated by the audit.
2. mzML.gz versions of the two RAW files (file ids 10407991 and 10407990, ~250 MB each). These could be produced with the open-source ThermoRawFileParser (https://github.com/compomics/ThermoRawFileParser, Apache 2.0, Linux build available) using `-f=1` (mzML) and gzip. Scan numbering must match Byonic's `Scan.Number.s...Posit.`.
3. Environment fixes allowed by the runbook: set `directory` and the `openMSfile()` paths; set `MS.Alias.name` filter for experiment1 to the alias of the sample being processed.

Mapping to targets (only if input 1 becomes available):
- Run with experiment1 = MS275 file (`20240215_..._MS275vDMSO_...`): output `experiment1_proteoform_df_Byonic_max_mods_7_PEP.2D_0.05_min_delta_mod_10_ppm_tolerance_15_H-tag.csv` gives T3 (row `all_mods == "K9ac K14ac K23ac K27me2"`, column `cumulative_log2-fold_change`), T1 (via the formula above) and T5 (row count).
- Run with experiment1 = Corin file (`20240216_..._DMSO_Corin_...`): same csv gives T4 and T2.

Decision rule fixed now: if `Byonic_results.csv` (or an equivalent PSM export) cannot be obtained from public sources, the run cannot reach the analysis stage. The agent should then still (a) download nothing beyond what is needed to verify file integrity (checksums of the two RAW files are optional given size; the Rmd must be checksummed), (b) record that the pipeline stops at line 498 for want of its input, and (c) propose class E (could not run), noting in class_reason that the missing input is an intermediate from proprietary software (which also bears on class C, materials incomplete). The agent must not reconstruct the PSM table by any other search engine, because that would change the authors' analysis.

## 3. Robustness checks (all on the headline proteoform K9ac K14ac K23ac K27me2, both drugs, cumulative normalisation, using the notebook's `assigned_fractional_intensity_hits` restricted to `scan_number %in% single_hit_scans$scan_number`, exactly as the notebook's t-test chunk does)

(a) Resampling, seed 20261009. The pipeline has no random component, so a different seed alone is not meaningful. Nearest meaningful version: scan-level bootstrap. Within the proteoform, resample scans (rows) with replacement, B = 2000, `set.seed(20261009)`, recompute fc_cum = mean(log2_cum_129..131) minus mean(log2_cum_126..128) with `na.rm = TRUE` each time; report the percentile 95% CI of fc_cum and the share of resamples with fc_cum > 0.6. Same direction and significance = CI lower bound > 0.6 (or at minimum > 0).

(b) Outlier exclusion. Replicate-based rule: for each condition (DMSO channels 126/127/128; drug channels 129/130/131), compute each channel's mean log2_cum value over the proteoform's scans, and drop the one channel per condition whose mean is furthest from the condition's mean of channel means. Re-run the notebook's two-sided Welch t-test and fc_cum on the remaining 2 vs 2 channels (values pooled over scans as in the original). Report fc_cum, p value.

(c) Alternative analysis choice. The original test treats every reporter value from every scan as an independent observation (pooling scans). Alternative: biological-replicate-level test. For each of the six channels, take the mean of log2_cum over the proteoform's scans (one value per biological replicate), then a two-sided Welch t-test with n = 3 vs n = 3 (`t.test(drug, dmso)`); report the difference in means (log2FC), 95% CI and p value. Same direction and significance = log2FC > 0 and p < 0.05.

If the pipeline cannot run (see section 2), none of (a) to (c) can be run, because they need scan-level reporter intensities that exist only inside the pipeline. The SI tables contain only per-proteoform summaries, so no substitute check is possible from published material; the agent should mark each check `ran: false` with that reason. (The paper's own mean- and median-normalised columns in Tables S2 to S5 are a published sensitivity analysis, not an audit check, and may be quoted descriptively in `note` only.)

## 4. Feasibility notes

- Blocking issue: the notebook's sole tabular input, `Byonic_results.csv`, is not in the dataset, and generating it requires Byonic (commercial, licence needed) plus an undeposited FASTA. Without it, no target can be computed. Expected class: E (could not run), with materials incompleteness (C) as the underlying reason.
- Code is a template: placeholder Windows paths (`C:/Users/your_file_path/`, `C:/path_to_your_data/file1.mzML.gz`), placeholder experiment aliases (`your_ms_experiment_1` used for all three experiments), and it references three experiments while two RAW files are deposited. These are environment-level fixes, but require knowing Byonic's MS alias names.
- Size: about 499 MB total (two RAW files of about 250 MB). Only needed if a PSM table becomes available. Do not download them otherwise.
- Dependencies: R 4.3.2 used by authors; packages mzR 2.36.0 (Bioconductor, needs NetCDF/HDF5 and compilers; heavy source build on aarch64), purrr 1.0.2, tidyr 1.3.1, stringr 1.5.1, dplyr 1.1.4, xml2 1.3.6, readr 2.1.5, readxl 1.4.3, writexl 1.5.0, tidyverse 2.0.0, RColorBrewer 1.1-3, ggrepel 0.9.5, parallel. RAW to mzML conversion needs ThermoRawFileParser (.NET runtime). Note: in the sandbox used to write this pre-registration, `/workspace/mamba/envs/r/bin/Rscript` did not exist and no `Rscript` was on PATH; the run agent should check its own environment.
- Compute: ion matching runs over every PSM with parallel clusters; on 2 CPUs and 7 GB RAM, likely tens of minutes to hours per sample (not measured). `detectCores()/2` = 1 worker on this machine.
- Licence: dataset CC0 1.0 (https://creativecommons.org/publicdomain/zero/1.0/), so the Rmd and RAW files can be redistributed. Paper and SI are CC BY 4.0 (attribution required).
