# Loads the authors' helper functions (fs_diag, run_ivglm, grab_by_name, fmt...) verbatim from
# wildfire_data_analysis.R lines 354-405 (SECTION 4), without running anything else.
src <- readLines("wildfire_data_analysis.R", warn = FALSE)[354:405]
eval(parse(text = src), envir = globalenv())
