# Environment fixes, 10_6MLKJZ agent A

No line of the authors' R code was changed. All four scripts ran byte-identical to the deposit (sha256 in ../checksums.sha256).

1. `00_raw_data_lowercase_symlinks.diff` (file-system change, no code change). `01_preparation_function.R` lines 33-36 read
   `../data/conjoint_data/raw_data/data_uhh.csv` and `data_hsvn.csv`; the deposit has `data_UHH.csv` and `data_HSVN.csv`.
   On case-sensitive Linux the names do not resolve. In the run copy I added symlinks `data_uhh.csv -> data_UHH.csv` and
   `data_hsvn.csv -> data_HSVN.csv`. The paths the code uses are unchanged, so `sam` stays `uhh` / `hsvn`. Allowed by PREREG section 2.

2. Package version (no file diff): cjoint 2.1.0 instead of the current CRAN cjoint 2.1.3. With cjoint 2.1.3 (published on CRAN
   2026-05-19) `prep_data()` stops inside `cjoint::read.qualtrics()` with
   "Caused by error in `$<-.data.frame`: ! replacement has 0 rows, data has 2048"
   (outputs/run_authors_log_attempt1_cjoint2.1.3_failed.txt). cjoint 2.1.0 (CRAN archive, 2018-10-19) was the CRAN release current
   when the scripts were last revised (2023-07-03 / 2023-07-11; 2.1.1 came out 2023-08-22). With 2.1.0 the function returns the
   columns `Response.ID` and `respondent` that 01_preparation_function.R lines 151-154 expect. Installed from
   https://cloud.r-project.org/src/contrib/Archive/cjoint/cjoint_2.1.0.tar.gz (needs shinyBS, installed from CRAN, 0.65.0).
   Allowed under "package versions".

3. Package source (no file diff): cregg 0.4.0 from the CRAN archive tarball (archived on CRAN 2024-09-05), as PREREG section 2 says.

4. Run order (no file diff): 04_analysis.R has its three `source()` lines commented out. My wrapper `scripts/run_authors.R`
   sources 01, 02, 03 and 04 in that order from `analysis/`, which is what the script header asks the user to do. The wrapper only
   saves objects afterwards (write.csv of the seven cj() results, saveRDS of pooled_df2 and match_data).

5. Locale: all runs with LANG=C.UTF-8 LC_ALL=C.UTF-8. No encoding change was needed: rvest 1.0.4 `repair_encoding()` ran (with a
   deprecation warning) and all renames and relabels matched; outputs/attribute_levels_check.csv shows the expected level counts
   (2, 4, 6, 5, 4, 3, 4, 4) and 0 NA rows for every attribute.

The deposited prep_data/*.csv were moved aside before the run so 01 regenerates them; the regenerated files parse cell-for-cell
identical to the deposited ones (outputs/prep_csv_comparison.json).
