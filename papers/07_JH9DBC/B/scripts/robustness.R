# Pre-registered robustness checks R_a, R_b, R_c on model2B (PREREG section 3). Writes outputs/robustness.json
.libPaths(c("/workspace/audit_runs/07_JH9DBC/B/rlib_fx0121", "/workspace/audit_runs/07_JH9DBC/B/rlib", .libPaths()))  # fixest 0.12.1, as in the primary run
suppressPackageStartupMessages({library(fixest); library(lme4); library(haven); library(dplyr); library(jsonlite)})
OUT <- "/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/07_JH9DBC/B/outputs"
dataall <- read_dta("/workspace/audit_runs/07_JH9DBC/B/dl/data.dta")
data <- dataall |> filter(year_2012 == 0)
term <- "juicio:year_2018"
cf <- function(v, nm) { k <- intersect(c("juicio:year_2018","year_2018:juicio"), nm)[1]; if (is.na(k)) NA_real_ else unname(v[k]) }
ct_row <- function(ct) { k <- intersect(c("juicio:year_2018","year_2018:juicio"), rownames(ct))[1]; ct[k, ] }
f2B <- voto_pro_gober ~ year_2018 + juicio*year_2018 + log_pobtot + log_pib + econ_growth + hom_per100 | unique_id + partido_gober
f2  <- voto_pro_gober ~ juicio + year_2018 + juicio*year_2018 + log_pobtot + log_pib + econ_growth + hom_per100 + (1|unique_id) + (1|partido_gober)
m0 <- feols(f2B, data=data); est0 <- cf(coef(m0), names(coef(m0)))
me_sec <- function(d) { m <- lmer(f2, data=d); b <- fixef(m)[term]; se <- sqrt(diag(vcov(m)))[term]
  list(estimate=unname(b), se=unname(se), p_wald=unname(2*pnorm(-abs(b/se))), nobs=nobs(m)) }
res <- list(fixest_version=as.character(packageVersion("fixest")), model2B_default_vcov=sub("^Standard-errors: *","",grep("^Standard-errors", capture.output(print(m0)), value=TRUE)[1]))
## R_a cluster bootstrap
byid <- split(as.data.frame(data), data$unique_id)
set.seed(20261010)
ids <- unique(data$unique_id); B <- 1000; bt <- rep(NA_real_, B); btm <- rep(NA_real_, B)
fm <- voto_pro_gober ~ juicio + year_2018 + juicio*year_2018 + log_pobtot + log_pib + econ_growth + hom_per100 + (1|new_id) + (1|partido_gober)
for (b in 1:B) {
  draw <- sample(ids, length(ids), replace=TRUE)
  d <- do.call(rbind, lapply(seq_along(draw), function(k) { x <- byid[[draw[k]]]; x$new_id <- k; x }))
  fb <- voto_pro_gober ~ year_2018 + juicio*year_2018 + log_pobtot + log_pib + econ_growth + hom_per100 | new_id + partido_gober
  m <- tryCatch(feols(fb, data=d, notes=FALSE, warn=FALSE), error=function(e) NULL)
  if (!is.null(m)) bt[b] <- cf(coef(m), names(coef(m)))
  mm <- tryCatch(suppressMessages(suppressWarnings(lmer(fm, data=d))), error=function(e) NULL)
  if (!is.null(mm) && term %in% names(fixef(mm))) btm[b] <- fixef(mm)[term]
}
ok <- bt[!is.na(bt)]
ci <- unname(quantile(ok, c(.025,.975)))
p_a <- min(1, 2*min(mean(ok >= 0), mean(ok <= 0)))
write.csv(data.frame(rep=1:B, coef_model2B=bt, coef_model2_multilevel=btm), file.path(OUT, "R_a_bootstrap_draws.csv"), row.names=FALSE)
res$R_a <- list(estimate=est0, ci_low=ci[1], ci_high=ci[2], boot_se=sd(ok), p_value=p_a, n_rep=B, n_not_estimable=sum(is.na(bt)),
  pass=(est0 < 0 && ci[2] < 0),
  secondary_model2_multilevel={okm <- btm[!is.na(btm)]; list(estimate=me_sec(data)$estimate, ci_low=unname(quantile(okm,.025)), ci_high=unname(quantile(okm,.975)), boot_se=sd(okm), p_value=min(1,2*min(mean(okm>=0),mean(okm<=0))), n_not_estimable=sum(is.na(btm)))})
## R_b outliers
z <- (data$voto_pro_gober - mean(data$voto_pro_gober)) / sd(data$voto_pro_gober)
db <- data[abs(z) <= 3, ]
mb <- feols(f2B, data=db); ctb <- ct_row(coeftable(mb))
q <- quantile(data$voto_pro_gober, c(.01,.99), type=7)
dt <- data[data$voto_pro_gober >= q[1] & data$voto_pro_gober <= q[2], ]
mt <- feols(f2B, data=dt); ctt <- ct_row(coeftable(mt))
res$R_b <- list(estimate=ctb[1], se=ctb[2], p_value=ctb[4], rows_dropped=nrow(data)-nrow(db), nobs=nobs(mb),
  pass=(ctb[1] < 0 && ctb[4] < 0.05),
  secondary_trim_1_99=list(rows_dropped=nrow(data)-nrow(dt), estimate=ctt[1], se=ctt[2], p_value=ctt[4], nobs=nobs(mt)),
  secondary_model2_multilevel=me_sec(db))
## R_c state clustering
ctc <- ct_row(coeftable(summary(m0, vcov = ~id_estado)))
res$R_c <- list(estimate=ctc[1], se=ctc[2], p_value=ctc[4], n_clusters=length(unique(data$id_estado)),
  pass=(ctc[1] < 0 && ctc[4] < 0.05), secondary_model2_multilevel="not applicable",
  indicted_states=sort(unique(data$estado[data$juicio==1])))
write(toJSON(res, auto_unbox=TRUE, digits=NA, pretty=TRUE), file.path(OUT, "robustness.json"))
print(res)
