# Loads outputs/session.RData and writes outputs/targets_extracted.csv (PREREG section 2).
args <- commandArgs(TRUE); tag <- if (length(args)) args[1] else "fixest_current"
libs <- c("/workspace/audit_runs/07_JH9DBC/B/rlib"); if (length(args) > 1) libs <- c(args[2], libs)
.libPaths(c(libs, .libPaths()))
suppressPackageStartupMessages({library(fixest); library(lme4); library(lmerTest)})
OUT <- "/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/07_JH9DBC/B/outputs"
load(file.path(OUT, paste0("session_", tag, ".RData")))
term <- "juicio:year_2018"
`%||%` <- function(a,b) if (is.null(a) || length(a)==0) b else a
rows <- list()
fe_row <- function(id, name, m) {
  ct <- coeftable(m); s <- summary(m); tm <- intersect(c("juicio:year_2018","year_2018:juicio"), rownames(ct))[1]
  data.frame(id=id, model=name, estimate=ct[tm,1], se=ct[tm,2], p=ct[tm,4],
             p_type="fixest t, model default vcov", vcov=sub("^Standard-errors: *","",trimws(grep("^Standard-errors", capture.output(print(s)), value=TRUE)[1])), fixest_version=as.character(packageVersion("fixest")),
             nobs=nobs(m), note=paste0("term ", tm, "; vcov: ", attr(s$cov.scaled, "type") %||% "", "; fixef sizes: ", paste(names(m$fixef_sizes), m$fixef_sizes, collapse=" ")))
}
for (x in list(c("T1","model1B"),c("T2","model2B"),c("T3","model3B"),c("secB4","model4B"))) rows[[length(rows)+1]] <- fe_row(x[1], x[2], get(x[2]))
me_row <- function(id, name, m) {
  b <- fixef(m)[term]; se <- sqrt(diag(vcov(m)))[term]; z <- b/se; pz <- 2*pnorm(-abs(z))
  d <- if (grepl("G$", name)) dplyr::filter(dplyr::filter(data, year_2012 != 1), st_elections_15_18 == 1) else data
  # Satterthwaite p (secondary): refit the identical formula with lmerTest on the same data the authors' code used
  ps <- tryCatch(summary(lmerTest::lmer(formula(m), data=d))$coefficients[term, "Pr(>|t|)"], error=function(e) NA)
  data.frame(id=id, model=name, estimate=unname(b), se=unname(se), p=unname(pz), p_type="Wald z two-sided",
             vcov="lmer", fixest_version=as.character(packageVersion("fixest")), nobs=nobs(m),
             note=paste0("Satterthwaite p=", signif(ps,6), " | groups: ", paste(names(ngrps(m)), ngrps(m), collapse=" ")))
}
for (x in list(c("secG1","model1G"),c("T5","model2G"),c("secG3","model3G"),c("secG4","model4G"),
               c("tab2_1","model1"),c("tab2_2","model2"),c("tab2_3","model3"),c("tab2_4","model4")))
  rows[[length(rows)+1]] <- me_row(x[1], x[2], get(x[2]))
res <- do.call(rbind, rows)
write.csv(res, file.path(OUT, paste0("targets_extracted_", tag, ".csv")), row.names=FALSE)
sink(file.path(OUT, paste0("model_summaries_", tag, ".txt")))
for (n in c("model1B","model2B","model3B","model4B")) { cat("=====", n, "\n"); print(summary(get(n))) }
for (n in c("model1","model2","model3","model4","model1G","model2G","model3G","model4G")) { cat("=====", n, "\n"); print(summary(get(n))) }
sink()
print(res)
