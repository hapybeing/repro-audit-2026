# Loads saved session objects, writes target coefficients and PCA loadings.
.libPaths(c("/workspace/audit_runs/08_SQRZR8/A/rlib", .libPaths()))
suppressMessages(library(estimatr))
OUT <- Sys.getenv("OUTDIR"); IN <- Sys.getenv("INFILE", file.path(OUT, "session_models.RData"))
TAG <- Sys.getenv("TAG", "")
load(IN)
outcomes <- c("positive_emo_rv","negative_emo","neutral_emo_rv","general_attitude_fic","general_attitude_real")
terms <- c("surveillance_facPersonalized","surveillance_facPublic","censorship_facPersonalized","censorship_facPublic")
rows <- list()
for (o in outcomes) { m <- all_models[[paste0(o, ".mod2")]]; s <- summary(m)$coefficients
  for (t in terms) rows[[length(rows)+1]] <- data.frame(outcome=o, term=t, estimate=s[t,"Estimate"],
     se=s[t,"Std. Error"], p_value=s[t,"Pr(>|t|)"], nobs=nobs(m), r2=m$r.squared, se_type=m$se_type) }
df <- do.call(rbind, rows)
write.csv(df, file.path(OUT, paste0("targets_extracted", TAG, ".csv")), row.names = FALSE)
print(df, digits = 6)
if (exists("pca_emotion")) { L <- unclass(pca_emotion$loadings)[, 1:5]
  write.csv(data.frame(item=rownames(L), L), file.path(OUT, paste0("pca_loadings", TAG, ".csv")), row.names = FALSE)
  print(round(L, 3)) }
