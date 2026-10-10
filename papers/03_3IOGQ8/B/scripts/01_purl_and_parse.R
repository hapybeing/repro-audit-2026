# Agent B: extract R code from the authors' Rmd and check it parses. No analysis is run here.
args <- commandArgs(trailingOnly = TRUE)
rmd <- args[1]; out_r <- args[2]; out_json <- args[3]
knitr::purl(rmd, output = out_r, documentation = 0, quiet = TRUE)
ok <- tryCatch({ex <- parse(out_r); TRUE}, error = function(e) {message(conditionMessage(e)); FALSE})
src <- readLines(rmd, warn = FALSE)
n_chunks <- sum(grepl("^```\\{r", src))
code <- readLines(out_r, warn = FALSE)
inputs <- grep("read\\.csv\\(|openMSfile\\(|read_excel\\(|load\\(|readRDS\\(|fread\\(", src, value = FALSE)
res <- list(rmd_lines = length(src), n_r_chunks = n_chunks, purled_lines = length(code),
            parses = ok, n_top_level_expressions = if (ok) length(ex) else NA,
            input_calls = lapply(inputs, function(i) list(line = i, code = trimws(src[i]))))
jsonlite::write_json(res, out_json, auto_unbox = TRUE, pretty = TRUE)
