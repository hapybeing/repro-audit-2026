# Diagnostics (not targets): (1) how lavaan handles the car::recode factor dummies in Study 2 (compare with numeric 0/1
# copies and with OLS); (2) the Table 3 sample (T6) composition. Writes outputs/diagnostics.json. wd = RUNDIR/data.
suppressPackageStartupMessages({library(car); library(dplyr); library(lavaan); library(jsonlite)})
OUT <- "/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/21_LEFTNE/A/outputs"
mix_mod <- '
Engage ~ b1 * anxiety + b2 * anger + b3 * hope + c1 * TRUMP + c2 * CLINTON + c3 * MARCH + c4 * METOO
anxiety ~ a1 * TRUMP + a99 * CLINTON + a98 * MARCH + a97 * METOO
anger ~ a2 * TRUMP + a299 * CLINTON + a298 * MARCH + a297 * METOO
hope ~ a3 * TRUMP + a399 * CLINTON + a398 * MARCH + a397 * METOO
indirTRUMPanger := a2 * b2
'
res <- list(lavaan_version = as.character(packageVersion("lavaan")))
q <- readRDS("Qualtrics_2019.RDS"); res$study1_TREATMENT_class <- class(q$TREATMENT)
d <- readRDS("NORC.RDS"); res$study2_TREATMENT_class <- class(d$TREATMENT)
d$CLINTON <- car::recode(d$TREATMENT, "'Alexa'= 0; 'Trump'=0; 'MeToo'=0; 'March'=0; 'Clinton'= 1")
d$TRUMP <- car::recode(d$TREATMENT, "'Alexa'= 0; 'Trump'=1; 'MeToo'=0; 'March'=0; 'Clinton'= 0")
d$METOO <- car::recode(d$TREATMENT, "'Alexa'= 0; 'Trump'=0; 'MeToo'=1; 'March'=0; 'Clinton'= 0")
d$MARCH <- car::recode(d$TREATMENT, "'Alexa'= 0; 'Trump'=0; 'MeToo'=0; 'March'=1; 'Clinton'= 0")
d$Engage <- d$futureengage; d$anxiety <- d$fear
res$study2_TRUMP_class <- class(d$TRUMP); res$study2_TRUMP_levels <- levels(d$TRUMP)
f_fac <- sem(mix_mod, data = d, std.lv = TRUE)
dn <- d; for (v in c("TRUMP","CLINTON","METOO","MARCH")) dn[[v]] <- as.numeric(as.character(dn[[v]]))
f_num <- sem(mix_mod, data = dn, std.lv = TRUE)
pf <- parameterEstimates(f_fac); pn <- parameterEstimates(f_num)
res$study2_max_abs_diff_est_factor_vs_numeric <- max(abs(pf$est - pn$est), na.rm = TRUE)
res$study2_indirTRUMPanger_factor <- pf$est[pf$label == "indirTRUMPanger"]; res$study2_indirTRUMPanger_numeric <- pn$est[pn$label == "indirTRUMPanger"]
res$study2_nobs_factor <- lavInspect(f_fac, "nobs"); res$study2_nobs_numeric <- lavInspect(f_num, "nobs")
cc <- dn[complete.cases(dn[, c("Engage","anxiety","anger","hope","TRUMP","CLINTON","MARCH","METOO")]), ]
res$study2_a2_lavaan <- pf$est[pf$label == "a2"]; res$study2_a2_ols_same_rows <- unname(coef(lm(anger ~ TRUMP + CLINTON + MARCH + METOO, data = cc))["TRUMP"])
# T6 sample
ces <- readRDS("CES2020.RDS")
res$ces_rows <- nrow(ces); res$ces_complier_table <- as.list(table(ces$complier, useNA = "ifany"))
comp <- ces %>% filter(complier == 1)
res$compliers_rows <- nrow(comp); res$compliers_NA_outcome <- sum(is.na(comp$futureengage_novote)); res$compliers_NA_treatment <- sum(is.na(comp$TREATMENT))
res$compliers_by_treatment <- as.list(table(as.character(comp$TREATMENT), useNA = "ifany"))
res$nobs_mod2 <- nobs(lm(futureengage_novote ~ TREATMENT, data = comp))
write_json(res, file.path(OUT, "diagnostics.json"), auto_unbox = TRUE, pretty = TRUE, digits = NA); print(toJSON(res, auto_unbox = TRUE, pretty = TRUE, digits = 8))
