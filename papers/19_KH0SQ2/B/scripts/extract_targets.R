OUT <- "/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/19_KH0SQ2/B/outputs"
m <- readRDS(file.path(OUT, "S1_S10_models.rds"))
rows <- list()
for (nm in names(m)) { s <- summary(m[[nm]])$coefficients
  rows[[nm]] <- data.frame(model=nm, term=rownames(s), estimate=s[,1], se=s[,2], t=s[,3], p=s[,4],
    nobs=nobs(m[[nm]]), r2=summary(m[[nm]])$r.squared, row.names=NULL) }
d <- do.call(rbind, rows)
write.csv(d, file.path(OUT, "targets_extracted.csv"), row.names=FALSE)
print(d, digits=6)
