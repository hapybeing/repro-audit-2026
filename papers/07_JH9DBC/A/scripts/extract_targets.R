# Loads outputs/session.RData from the authors' replication.R run and writes outputs/targets_extracted.csv
.libPaths(c(Sys.getenv("FIXLIB", "/workspace/audit_runs/07_JH9DBC/A/rlib"), "/workspace/audit_runs/07_JH9DBC/A/rlib", .libPaths()))
suppressMessages({library(fixest); library(lme4); library(lmerTest)})
P <- "/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/07_JH9DBC/A"
load(file.path(P, paste0("outputs/session", Sys.getenv("OUTSUF"), ".RData")))
term <- "juicio:year_2018"
# replication.R line 624 removes datasubset; lmerTest refits need it, so rebuild it exactly as lines 568 to 570
suppressMessages(library(dplyr)); datasubset <- data |> filter(year_2012 != 1) |> filter(st_elections_15_18 == 1)
rows <- list()
for (m in c("model1B","model2B","model3B","model4B")) {
  mod <- get(m); ct <- coeftable(mod); s <- summary(mod); fterm <- grep("juicio", rownames(ct), value=TRUE); stopifnot(length(fterm)==1)
  rows[[m]] <- data.frame(model=m, type="feols", term=fterm, estimate=ct[fterm,1], se=ct[fterm,2],
     p_value=ct[fterm,4], p_type="fixest default", vcov=trimws(grep("Standard-errors", capture.output(print(s)), value=TRUE)), nobs=nobs(mod),
     n_groups=paste(names(mod$fixef_sizes), mod$fixef_sizes, sep="=", collapse=";"), p_satterthwaite=NA)
}
for (m in c("model1","model2","model3","model4","model1G","model2G","model3G","model4G")) {
  mod <- get(m); est <- fixef(mod)[term]; se <- sqrt(diag(as.matrix(vcov(mod))))[term]
  pz <- 2*pnorm(-abs(est/se))
  st <- tryCatch(summary(lmerTest::as_lmerModLmerTest(mod))$coefficients[term,"Pr(>|t|)"], error=function(e) NA)
  rows[[m]] <- data.frame(model=m, type="lmer", term=term, estimate=unname(est), se=unname(se), p_value=unname(pz),
     p_type="Wald z two-sided", vcov="model-based", nobs=nobs(mod),
     n_groups=paste(names(ngrps(mod)), ngrps(mod), sep="=", collapse=";"), p_satterthwaite=st)
}
out <- do.call(rbind, rows)
write.csv(out, file.path(P, paste0("outputs/targets_extracted", Sys.getenv("OUTSUF"), ".csv")), row.names=FALSE)
sink(file.path(P, paste0("outputs/vcov_headers", Sys.getenv("OUTSUF"), ".txt"))); for (m in c("model1B","model2B","model3B","model4B")) { cat("=====", m, "\n"); print(summary(get(m))) }; sink()
print(out)
cat("fixest version used:", as.character(packageVersion("fixest")), "\n")
