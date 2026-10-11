# diffs: 23_FXRNBA agent A

No file of the deposit was changed, so there is no .diff file.
- wildfire_data_analysis.R ran unchanged (sha256 69407b41..., same as the deposit) via scripts/run_part.R (lines 1-668 copied verbatim to part_1_668.R and sourced) and scripts/run_full.R (whole script sourced).
- Folder layout: the deposited files were placed under 'Data Analysis/', 'Beats/', 'Crime Data/' (the Dataverse directory labels), which are the relative paths the code already uses. No path edit was needed.
- Locale: run with LC_ALL=C.UTF-8 (environment variable, not a code change).
