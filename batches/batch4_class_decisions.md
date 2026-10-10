# Batch 4 classification decisions (fixed before any batch 4 reproduction run)

Written 2026-10-11 (IST) after the five pre-registrations and before any of the authors' analysis code was run. Frozen with the pre-registrations in batch4_prereg_hashes.txt. Applies PROTOCOL.md section 7 and CHANGELOG_METHOD.md #4, #5 and #6 exactly as in batches 1 to 3. Nothing here changes those rules; it records how they apply to cases the batch 4 pre-registrations raised. The batch 2 and batch 3 decisions carry over where relevant.

1. Renamed deposited files (16 timelines.tab, 17 HEG .tab files, 20 FY3G_PMR.HDF4, postvar.nc and swath file locations). Pointing the code at the deposited file with the same content, or using Dataverse `?format=original`, is a path-only environment fix, as for 11 in batch 3.

2. Session driver (19_KH0SQ2). Appendix_plus.R cannot run top to bottom as deposited (load() lines commented out). Running the pre-registered target lines (892 to 958) in a fresh session through a driver that only adds `load("all_merged.RData")` is an environment fix and sets the main class. The alternative class, if that driver is not accepted as an environment fix, is C and is reported beside it.

3. Reduced bootstrap (17_T1NXVQ). The targets are the point estimates and vertex counts. The printed 120-draw percentile intervals are out of scope on this machine (about 19 CPU-hours) and are not compared. Significance uses the pre-registered reduced bootstrap with the authors' seeds 1..K. If the point estimates and counts match and significance holds, the main class is A. The alternative class, if only the full bootstrap counts, is E. Pinned package versions are tried first.

4. Row order (18_YXC5K5). The main class uses Benchmarking_DataAnalysis.Rmd exactly as deposited, row by row. The docid-paired rerun (R_c) is a robustness check and never changes the class (PROTOCOL.md section 7), but its outcome is reported next to the class in the report and the summary. The first F1 candidate listed in PREREG.md (the script's own positive class) sets the class.

5. Missing code (20_SINIYU). No replacement code is written by agents for a module or a table that is not deposited. A target whose code is not deposited, or cannot run because a module it imports is missing from the deposit and every location the data statement names, counts as not produced, and the class follows CHANGELOG #4 (C). The claims that need CMA-MESO and its 3D-Var system are listed as out of scope.

6. Sample-size-only or p-only mismatches follow CHANGELOG #6 (C, not D), as in batch 2. Statistic ambiguity: the first candidate listed in PREREG.md sets the class.

7. Robustness checks never change the class (PROTOCOL.md section 7).
