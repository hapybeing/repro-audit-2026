# Pre-registered robustness checks R_a, R_b, R_c on model2B (Table B Model 2). Writes outputs/robustness.csv and outputs/R_a_bootstrap_draws.csv
.libPaths(c(Sys.getenv("FIXLIB", "/workspace/audit_runs/07_JH9DBC/A/rlib"), "/workspace/audit_runs/07_JH9DBC/A/rlib", .libPaths()))
suppressMessages({library(haven); library(dplyr); library(fixest)})
P <- "/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/07_JH9DBC/A"
dataall <- read_dta("/workspace/audit_runs/07_JH9DBC/A/run/data.dta")
data <- dataall |> filter(year_2012 == 0)
term <- "year_2018:juicio"  # fixest name for juicio*year_2018 when juicio main effect is absorbed
f2 <- voto_pro_gober ~ year_2018 + juicio*year_2018 + log_pobtot + log_pib + econ_growth + hom_per100 | unique_id + partido_gober
base <- feols(f2, data = data)
res <- list()
# R_a cluster bootstrap
set.seed(20261010)
ids <- unique(data$unique_id); B <- 1000
fb <- voto_pro_gober ~ year_2018 + juicio*year_2018 + log_pobtot + log_pib + econ_growth + hom_per100 | new_id + partido_gober
draws <- rep(NA_real_, B)
spl <- split(seq_len(nrow(data)), data$unique_id)
for (b in 1:B) {
  s <- sample(ids, length(ids), replace = TRUE)
  idx <- unlist(lapply(seq_along(s), function(k) spl[[as.character(s[k])]]))
  nid <- unlist(lapply(seq_along(s), function(k) rep(k, length(spl[[as.character(s[k])]]))))
  d <- data[idx, ]; d$new_id <- nid
  m <- tryCatch(feols(fb, data = d, notes = FALSE, warn = FALSE), error = function(e) NULL)
  if (!is.null(m) && term %in% names(coef(m))) draws[b] <- coef(m)[term]
}
write.csv(data.frame(rep = 1:B, estimate = draws), file.path(P, paste0("outputs/R_a_bootstrap_draws", Sys.getenv("OUTSUF"), ".csv")), row.names = FALSE)
ok <- draws[!is.na(draws)]
ci <- quantile(ok, c(.025, .975), type = 7)
pa <- min(1, 2*min(mean(ok >= 0), mean(ok <= 0)))
res$R_a <- data.frame(id="R_a", estimate=coef(base)[term], se=sd(ok), ci_low=ci[1], ci_high=ci[2], p_value=pa,
  n_used=length(ok), n_failed=sum(is.na(draws)), rows_dropped=NA, nobs=nobs(base), n_clusters=length(ids), extra="")
# R_b outliers
z <- (data$voto_pro_gober - mean(data$voto_pro_gober)) / sd(data$voto_pro_gober)
db <- data[abs(z) <= 3, ]
mb <- feols(f2, data = db); ctb <- coeftable(mb)
q <- quantile(data$voto_pro_gober, c(.01, .99), type = 7)
dt <- data[data$voto_pro_gober >= q[1] & data$voto_pro_gober <= q[2], ]
mt <- feols(f2, data = dt); ctt <- coeftable(mt)
res$R_b <- data.frame(id="R_b", estimate=ctb[term,1], se=ctb[term,2], ci_low=NA, ci_high=NA, p_value=ctb[term,4],
  n_used=nobs(mb), n_failed=NA, rows_dropped=sum(abs(z) > 3), nobs=nobs(mb), n_clusters=NA,
  extra=sprintf("secondary 1/99 pct trim: dropped=%d nobs=%d estimate=%.6f se=%.6f p=%.6g", nrow(data)-nrow(dt), nobs(mt), ctt[term,1], ctt[term,2], ctt[term,4]))
# R_c state-clustered SE
sc <- summary(base, vcov = ~id_estado); ctc <- coeftable(sc)
res$R_c <- data.frame(id="R_c", estimate=ctc[term,1], se=ctc[term,2], ci_low=NA, ci_high=NA, p_value=ctc[term,4],
  n_used=nobs(base), n_failed=NA, rows_dropped=0, nobs=nobs(base), n_clusters=length(unique(data$id_estado)),
  extra=paste("vcov:", trimws(grep("Standard-errors", capture.output(print(sc)), value=TRUE)), "; multilevel model2 secondary: not applicable"))
out <- do.call(rbind, res)
write.csv(out, file.path(P, paste0("outputs/robustness", Sys.getenv("OUTSUF"), ".csv")), row.names = FALSE)
print(out)
cat("fixest version used:", as.character(packageVersion("fixest")), "\n")
