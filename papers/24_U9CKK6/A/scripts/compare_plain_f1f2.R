## Compare cycle_AE and cycle_AE_fit2 fitted in the killed plain run (saved before the kill) with the F1/F2 run.
suppressMessages(library(lme4))
S <- "/workspace/audit_runs/24_U9CKK6/A"
OUT <- "/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/24_U9CKK6/A/outputs"
res <- list()
for (nm in c("cycle_AE", "cycle_AE_fit2")) {
  a <- readRDS(file.path(S, "models_plain", paste0(nm, ".rds"))); b <- readRDS(file.path(S, "models", paste0(nm, ".rds")))
  res[[nm]] <- data.frame(model = nm, max_abs_diff_fixef = max(abs(fixef(a) - fixef(b))),
     max_abs_diff_se = max(abs(sqrt(diag(as.matrix(vcov(a)))) - sqrt(diag(as.matrix(vcov(b)))))),
     loglik_plain = as.numeric(logLik(a)), loglik_f1f2 = as.numeric(logLik(b)), nobs_plain = nobs(a), nobs_f1f2 = nobs(b))
}
write.csv(do.call(rbind, res), file.path(OUT, "plain_vs_f1f2.csv"), row.names = FALSE); print(do.call(rbind, res))
