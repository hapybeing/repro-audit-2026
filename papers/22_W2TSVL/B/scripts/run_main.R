# Wrapper for the authors' main (figure) script, cross-check only (agent B).
# broom::tidy is wrapped to record the coefficients of each polr fit passed to it; the call itself is unchanged.
OUT <- Sys.getenv("OUTDIR")
.cap <- list()
tidy <- function(x, ...) {
  if (inherits(x, "polr")) {
    s <- summary(x)$coefficients
    .cap[[length(.cap) + 1]] <<- data.frame(fit = length(.cap) + 1, term = rownames(s), estimate = s[, 1], se = s[, 2], nobs = nobs(x), row.names = NULL)
    write.csv(do.call(rbind, .cap), file.path(OUT, "main_script_polr_coefs.csv"), row.names = FALSE)
  }
  broom::tidy(x, ...)
}
pdf(file.path(OUT, "main_script_figures.pdf"))
source("Framing Labor Action_R script.R", echo = TRUE, max.deparse.length = Inf)
dev.off()
cat("MAIN_SCRIPT_DONE\n")
