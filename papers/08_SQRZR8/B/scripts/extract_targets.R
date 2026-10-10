# Loads saved session objects and writes target coefficients, nobs, PCA loadings, tab_3 html.
R <- "/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/08_SQRZR8/B/outputs"
load(file.path(R, "session_models.RData"))
suppressMessages(library(estimatr))
outs <- c("positive_emo_rv","negative_emo","neutral_emo_rv","general_attitude_fic","general_attitude_real")
terms <- c("surveillance_facPersonalized","surveillance_facPublic","censorship_facPersonalized","censorship_facPublic")
rows <- list()
for (o in outs) { m <- all_models[[paste0(o, ".mod2")]]
  for (t in terms) rows[[length(rows)+1]] <- data.frame(outcome=o, term=t, estimate=unname(m$coefficients[t]),
     std_error=unname(m$std.error[t]), p_value=unname(m$p.value[t]), nobs=m$nobs, r2=m$r.squared, se_type=m$se_type) }
res <- do.call(rbind, rows)
write.csv(res, file.path(R, "targets_extracted.csv"), row.names=FALSE)
L <- unclass(pca_emotion$loadings)[, 1:5]
write.csv(data.frame(item=rownames(L), L), file.path(R, "pca_loadings.csv"), row.names=FALSE)
print(res, digits=6); print(round(L,3))
# tab_3 html via sjPlot (separate call, authors' file not edited)
suppressMessages(library(sjPlot))
covs <- strsplit(covariates_str, " \\+ ")[[1]]
tab <- tab_model(all_models$positive_emo_rv.mod2, all_models$negative_emo.mod2, all_models$neutral_emo_rv.mod2,
  all_models$general_attitude_fic.mod2, all_models$general_attitude_real.mod2, digits=3, p.style="stars",
  show.ci=FALSE, show.se=TRUE, collapse.se=TRUE, rm.terms=covs, file=file.path(R, "tab_3_mod2.html"))
cat("complete cases info: nrow(data) =", nrow(data), "\n")
