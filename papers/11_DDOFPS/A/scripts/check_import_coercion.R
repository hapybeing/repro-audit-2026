# Check: rio::import (readxl) warned "Expecting logical in DL.../R...C116". Which columns lose values
# because readxl guessed their type from the first 1000 rows? Compare the import as the script does it
# with readxl::read_excel(guess_max = Inf). Writes OUTDIR/import_coercion_check_<label>.csv
args <- commandArgs(trailingOnly = TRUE)
f <- args[1]; outdir <- args[2]; label <- args[3]
suppressPackageStartupMessages({library(rio); library(readxl)})
a <- suppressWarnings(rio::import(f))
b <- suppressWarnings(readxl::read_excel(f, guess_max = Inf))
stopifnot(identical(names(a), names(b)), nrow(a) == nrow(b))
res <- data.frame(col_index = seq_along(a), column = names(a),
                  class_script = sapply(a, function(x) class(x)[1]),
                  class_guessmax_inf = sapply(b, function(x) class(x)[1]),
                  nonNA_script = sapply(a, function(x) sum(!is.na(x))),
                  nonNA_guessmax_inf = sapply(b, function(x) sum(!is.na(x))))
res$values_lost <- res$nonNA_guessmax_inf - res$nonNA_script
res$used_by_targets <- res$column %in% c("ano", "APE4", "APE3", "numpartido")
write.csv(res, file.path(outdir, paste0("import_coercion_check_", label, ".csv")), row.names = FALSE)
print(res[res$values_lost != 0 | res$used_by_targets, ])
