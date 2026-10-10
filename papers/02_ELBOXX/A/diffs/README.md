# Environment fixes, 02_ELBOXX, Agent A

No author file was changed, so there is no .diff file. The authors' replication.R, analysis_data_creation.R
and visualization.R were run byte-identical to the Dataverse copies (sha256 in ../checksums.sha256).

Environment-level actions (no code edits):

1. Original CSVs. The three ingested tables were downloaded with `?format=original` (atop5_1a.csv,
   atop5_1sy.csv, dyadic_mid_4.02.csv), because analysis_data_creation.R reads `.csv` with read.csv. md5 of all three
   equals the Dataverse md5 (905d804c..., ed909cfc..., 741ae2ea...). Working directory set to a scratch folder holding
   all files (replaces opening AJPS_rep_secretally.Rproj).

2. System clock (faketime). `peacesciencer::create_stateyears()` (v1.1.0, default `mry = TRUE`) extends the state-year
   frame to `as.numeric(format(Sys.Date(), "%Y")) - 1`. Run on 2026-10-09 it adds the year 2025 (195 extra country-years,
   N = 17706 instead of the authors' 17511), which changes test 1 (T4, T5) and leaves test 2 unchanged
   (outputs/targets_pathA_clock2026.csv, outputs/code_review_facts.csv). To reproduce the authors' environment the
   run of record sets the process clock to the authors' log date with
   `faketime '2025-05-06 13:14:00' Rscript scripts/run_pathA.R ...` (Debian package faketime 0.9.10, installed with
   apt-get). This is an environment fix only: no line of code changed. With it the rebuilt `d` is identical to the
   shipped `d` in AJPS_analysis_data.RData (outputs/compare_d_rebuilt_vs_shipped.csv).

3. Package versions: logr 1.3.8, common 1.1.3, peacesciencer 1.1.0 installed with remotes::install_version into a fresh
   R_LIBS_USER (peacesciencer pulled stevemisc 1.9.0, the current CRAN version; the authors' stevemisc version is not
   recorded). tidyverse 2.0.0 / dplyr 1.1.4 from the system library (minor drift: lubridate 1.9.4, ggplot2 3.5.1,
   purrr 1.0.4, foreign 0.8-90 versus the authors' 1.9.3, 3.5.0, 1.0.2, 0.8-86). R 4.5.0 versus authors' 4.3.3.

`log_open()` with no file name worked under Rscript (wrote log/replication.log); no change needed.
