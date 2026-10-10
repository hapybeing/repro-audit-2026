# Environment fixes (Agent B, 02_ELBOXX)

No file written by the authors was edited. replication.R and analysis_data_creation.R were run byte-identical to the Dataverse copies (sha256 in ../checksums.sha256).

1. `run_pathA_faketime_date.diff` (invocation only, not a code change).
   Why: `analysis_data_creation.R` line 61 calls `peacesciencer::create_stateyears()` with its default `mry = TRUE`.
   In peacesciencer 1.1.0 this sets the last year of the state-year frame to `as.numeric(format(Sys.Date(), "%Y")) - 1`
   (printed source of `create_stateyears`, see ../LOG.md). Run in 2026, the frame ends in 2025 and `d` has 17706 rows;
   the authors' run (LOG.pdf, 2025-05-06) ended in 2024 with 17511 rows. The extra 195 country-years (year 2025) all have
   disputes = 0 and secret_alliances = 0, which changes M1 (T4, T5) but not M2 (all 2025 rows have pub_def = 0).
   Fix: run the unchanged code under libfaketime with the clock set to 2025-05-06 13:14:00 (the authors' LOG.pdf start time),
   so `Sys.Date()` returns 2025-05-06. Both the as-is run and the fixed run are reported.
2. `driver_pathA.R` (../scripts/) sources the unchanged replication.R and then saves test1, test2 and d to scratch for extraction.
   It adds nothing before the authors' code except printing Sys.Date().
3. Working directory: each run was started inside a folder holding the authors' files (replaces opening the .Rproj).
   `logr::log_open()` with no file name worked under Rscript (log written to log/replication.log); no change needed.
