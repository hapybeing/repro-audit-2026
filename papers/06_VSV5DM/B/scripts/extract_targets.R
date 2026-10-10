# Sources the purled authors' code up to and including the line that exports rg_me
# (marginaleffects_table_white_men_gop.doc), i.e. the end of the chunk
# "##Count Models -Republican White Men as a reference", then writes the targets.
RUN <- "/workspace/audit_runs/06_VSV5DM/B/run"
OUT <- "/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/06_VSV5DM/B/outputs"
setwd(RUN)
code <- readLines("multivariate.R")
cut <- grep("marginaleffects_table_white_men_gop.doc", code, fixed = TRUE)
stopifnot(length(cut) == 1)
writeLines(code[1:cut], "multivariate_upto_A8.R")
source("multivariate_upto_A8.R", echo = FALSE)
s <- summary(res2)
cf <- summary(covid)$coefficients
lev <- c("Democratic White Men","Republican White Women","Democratic White Women","Democratic Men of Color","Democratic Women of Color")
rows <- list()
for (l in lev) {
  m <- s[s$factor == paste0("rpg", l), ]
  k <- paste0("rpg", l)
  rows[[l]] <- data.frame(level = l, AME = m$AME, AME_SE = m$SE, AME_z = m$z, AME_p = m$p,
                          AME_lower = m$lower, AME_upper = m$upper,
                          coef = cf[k, 1], coef_SE = cf[k, 2], coef_t = cf[k, 3], coef_p = cf[k, 4])
}
df <- do.call(rbind, rows)
df$nobs <- nobs(covid); df$deviance <- deviance(covid); df$dispersion <- summary(covid)$dispersion
df$cut_line_in_purled_R <- cut
write.csv(df, file.path(OUT, "targets_extracted.csv"), row.names = FALSE)
saveRDS(list(covid = covid, by_leg2 = by_leg2), file.path(RUN, "covid_model.rds"))
print(df, digits = 10)
