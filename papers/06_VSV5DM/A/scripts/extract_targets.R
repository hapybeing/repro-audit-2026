# Source purled authors' code up to and including the line exporting marginaleffects_table_white_men_gop.doc,
# then write unrounded target quantities. Usage: Rscript extract_targets.R <purled.R> <outdir>
args <- commandArgs(TRUE); f <- args[1]; outdir <- args[2]
L <- readLines(f)
cut <- grep("marginaleffects_table_white_men_gop.doc", L, fixed = TRUE)[1]
cat("cut line in purled file:", cut, "\n")
exprs <- parse(text = L[1:cut], keep.source = TRUE)
srcs <- attr(exprs, "srcref")
for (i in seq_along(exprs)) {
  tryCatch(eval(exprs[[i]], envir = globalenv()),
           error = function(e) cat("ERROR at purled line", srcs[[i]][1], ":", conditionMessage(e), "\n"))
}
s <- as.data.frame(summary(res2))
cf <- summary(covid)$coefficients
rows <- list()
for (k in seq_len(nrow(s))) {
  lev <- s$factor[k]
  rows[[length(rows)+1]] <- data.frame(quantity="AME", term=lev, estimate=s$AME[k], se=s$SE[k], stat=s$z[k], p=s$p[k], lower=s$lower[k], upper=s$upper[k])
  rows[[length(rows)+1]] <- data.frame(quantity="coef", term=lev, estimate=cf[lev,1], se=cf[lev,2], stat=cf[lev,3], p=cf[lev,4], lower=NA, upper=NA)
}
rows[[length(rows)+1]] <- data.frame(quantity="nobs", term="covid", estimate=nobs(covid), se=NA, stat=NA, p=NA, lower=NA, upper=NA)
rows[[length(rows)+1]] <- data.frame(quantity="deviance", term="covid", estimate=deviance(covid), se=NA, stat=NA, p=NA, lower=NA, upper=NA)
rows[[length(rows)+1]] <- data.frame(quantity="dispersion", term="covid", estimate=summary(covid)$dispersion, se=NA, stat=NA, p=NA, lower=NA, upper=NA)
out <- do.call(rbind, rows)
write.csv(out, file.path(outdir, "targets_extracted.csv"), row.names = FALSE)
print(out, digits = 10)
saveRDS(list(covid=covid, mf=model.frame(covid), by_leg2=by_leg2), "covid_model.rds")
