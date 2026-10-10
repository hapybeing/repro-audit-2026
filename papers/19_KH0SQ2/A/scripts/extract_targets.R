OUT <- "/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/19_KH0SQ2/A/outputs"
m <- readRDS(file.path(OUT, "S1_S10_models.rds"))
rows <- list()
for (nm in names(m)) { s <- summary(m[[nm]]); cf <- s$coefficients
  rows[[nm]] <- data.frame(model = nm, term = rownames(cf), estimate = cf[,1], se = cf[,2], t = cf[,3], p = cf[,4],
                           nobs = nobs(m[[nm]]), r2 = s$r.squared, row.names = NULL) }
d <- do.call(rbind, rows)
write.csv(d, file.path(OUT, "targets_extracted.csv"), row.names = FALSE)
load("/workspace/audit_runs/19_KH0SQ2/A/deposit/all_merged.RData")
write.csv(as.data.frame(table(country = all$country)), file.path(OUT, "descriptive_country_counts.csv"), row.names = FALSE)
print(d, digits = 6)
