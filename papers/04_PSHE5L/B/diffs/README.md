# Environment fixes, 04_PSHE5L, Agent B

Original file: `Rural Populism - Socius - Public Code.R` (Dataverse file 10695152, sha256 955871dc...). Only the two PREREG-allowed fixes below were applied for the primary run. `combined_primary.diff` is both together (the script actually run, saved as scripts/patched_primary.R).

1. `01_data_path.diff` (line 9): the script reads `Downloads/320-942_Rural_West_COVID-19_Survey_4.5.21.csv`, which is not in the Dataverse deposit. Changed to the local path of the public OSF file `Rural_Populism_Dataset.csv` (https://osf.io/download/wr3ve/, sha256 f839986a...). Note: the public file is a 30-column extract with a different name from the 117-column file the script was written for (PREREG fix 1).
2. `02_comment_out_RAW_Q24_mutate.diff` (lines 19-20): `mutate(across(all_of(cols_to_convert), ~ as.numeric(.)))` errors on the public CSV ("Can't subset elements that don't exist. Elements `RAW_Q24A` ... don't exist"). The created variables are not used anywhere later. Commented out (PREREG fix 2). Line 17 (assigns a character vector) and line 22 (`class(rural$RAW_Q24C)`, returns "NULL" with a warning, no error) do not error, so per PREREG ("If the line does not error, leave it") they were left unchanged.
3. PREREG fix 3 (commenting out `library(semPlot)`, `library(xtable)`, `library(gt)`) was NOT needed: all three were installed in the fresh library within the 20-minute cap (gt needed V8, which installed with DOWNLOAD_STATIC_LIBV8=1, an install-time environment variable, no code change).

Diagnostic only (does not define the class): `DIAGNOSTIC_only_q15_line188_uncommented.diff` re-enables the authors' own commented line 188 `rural$Q15[rural$Q15 == 8] <- NA`, applied on top of the primary patch, exactly as pre-registered.
