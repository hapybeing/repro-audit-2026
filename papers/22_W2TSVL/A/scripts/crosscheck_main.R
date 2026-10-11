# Cross-check: polr fits captured (via trace) while the authors' main script ran, compared with appendix m1, m4, m7, m10.
args <- commandArgs(TRUE); OUT <- args[1]
suppressMessages(library(MASS))
fits <- readRDS("outputs/main_polr_fits.rds")
mods <- readRDS(file.path(OUT, "models_appendix.rds"))
top <- Filter(function(f) is.null(f$call$offset) && grepl("Treatment", deparse(f$call$formula)[1]) && length(coef(f)) == 4, fits)
cat("captured fits:", length(fits), " top-level Treatment fits:", length(top), "\n")
out <- list()
for (i in seq_along(top)) {
  f <- top[[i]]; b <- coef(f)
  out[[i]] <- data.frame(fit = i, formula = deparse(f$call$formula), nobs = nobs(f), term = names(b), estimate = unname(b), se = sqrt(diag(vcov(f)))[names(b)])
}
res <- do.call(rbind, out)
# Mapping (script order): Fig1 unions ref Control = m1; Fig2 unions ref Pro_strike = m4; Fig3 support ref Control = m7; Fig4 support ref Pro_strike = m10
map <- list(m1 = mods$m1, m4 = mods$m4, m7 = mods$m7, m10 = mods$m10)
nm <- c("m1","m4","m7","m10")
fig_ids <- unique(res$fit)
res$appendix_model <- nm[match(res$fit, fig_ids)]
res$appendix_estimate <- mapply(function(m, t) { tt <- sub("^Treatment", "", t); key <- c(Control="control", Strike="strike", Pro_strike="pro_strike", Anti_strike="anti_strike", Double_frame="double")[tt]; coef(map[[m]])[key] }, res$appendix_model, res$term)
res$abs_diff <- abs(res$estimate - res$appendix_estimate)
write.csv(res, file.path(OUT, "crosscheck_main_vs_appendix.csv"), row.names = FALSE)
print(res, digits = 6); cat("max abs diff:", max(res$abs_diff), "\n")
