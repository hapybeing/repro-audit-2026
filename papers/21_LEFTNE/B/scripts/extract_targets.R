# Re-executes, in a fresh session, only the authors' data-loading and model lines for T1-T6 (copied verbatim)
# and writes outputs/targets_extracted.csv. Usage: Rscript extract_targets.R <outfile_suffix>
if (Sys.getenv("NO_RLIB") != "1") .libPaths(c("/workspace/audit_runs/21_LEFTNE/B/rlib", .libPaths()))  # NO_RLIB=1: system library only (lavaan 0.6.19 version check)
suppressMessages({library(dplyr); library(car)})
args <- commandArgs(TRUE); suf <- if (length(args)) args[1] else ""
OUT <- "/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/21_LEFTNE/B/outputs"
setwd("/workspace/audit_runs/21_LEFTNE/B/data")
cat("lavaan version:", as.character(packageVersion("lavaan")), "from", find.package("lavaan"), "\n")
rows <- list()
add <- function(id, est, se, stat, p, n, note="") rows[[length(rows)+1]] <<- data.frame(id=id, estimate=est, se=se, statistic=stat, p_value=p, nobs=n, note=note)

# ---- T1: Text script lines 343-363 (verbatim)
df <- readRDS("Qualtrics_2019.RDS")
df$CLINTON <- car::recode(df$TREATMENT, "'Alexa'= 0; 'Trump'=0; 'MeToo'=0; 'Marches'=0; 'Clinton'= 1")
df$TRUMP <- car::recode(df$TREATMENT, "'Alexa'= 0; 'Trump'=1; 'MeToo'=0; 'Marches'=0; 'Clinton'= 0")
df$METOO <- car::recode(df$TREATMENT, "'Alexa'= 0; 'Trump'=0; 'MeToo'=1; 'Marches'=0; 'Clinton'= 0")
df$MARCH <- car::recode(df$TREATMENT, "'Alexa'= 0; 'Trump'=0; 'MeToo'=0; 'Marches'=1; 'Clinton'= 0")
df$Engage <- df$futureengage
df$anxiety <- df$fear
mix_mod <- '
Engage ~ b1 * anxiety + b2 * anger + b3 * hope + c1 * TRUMP + c2 * CLINTON + c3 * MARCH + c4 * METOO
anxiety ~ a1 * TRUMP + a99 * CLINTON + a98 * MARCH + a97 * METOO
anger ~ a2 * TRUMP + a299 * CLINTON + a298 * MARCH + a297 * METOO
hope ~ a3 * TRUMP + a399 * CLINTON + a398 * MARCH + a397 * METOO
indirTRUMPanxiety := a1 * b1
indirTRUMPanger := a2 * b2
indirTRUMPhope := a3 * b3
indirCLINTONanxiety := a99 * b1
indirCLINTONanger := a299 * b2
indirCLINTONhope := a399 * b3
'
cat("Study 1 TREATMENT levels/table:\n"); print(table(df$TREATMENT, useNA="ifany")); cat("class TRUMP:", class(df$TRUMP), "\n")
fit1 <- tryCatch(lavaan:::sem(mix_mod, data=df, std.lv=TRUE), error=function(e) e)
if (inherits(fit1, "error")) { cat("T1 ERROR:", conditionMessage(fit1), "\n"); add("T1",NA,NA,NA,NA,NA,paste("error:",conditionMessage(fit1)))
} else { pe <- lavaan::parameterEstimates(fit1); print(pe[pe$op==":=",]); r <- pe[pe$label=="indirTRUMPanger",]
  add("T1", r$est, r$se, r$z, r$pvalue, lavaan::lavInspect(fit1,"nobs"))
  r2 <- pe[pe$label=="indirCLINTONanger",]; add("T1_context_Clinton", r2$est, r2$se, r2$z, r2$pvalue, lavaan::lavInspect(fit1,"nobs"))
  write.csv(pe, file.path(OUT, paste0("lavaan_study1_pe", suf, ".csv")), row.names=FALSE) }

# ---- T2: Text script lines 366-387 (verbatim)
df_TESS <- readRDS("NORC.RDS")
df_TESS$CLINTON <- car::recode(df_TESS$TREATMENT, "'Alexa'= 0; 'Trump'=0; 'MeToo'=0; 'March'=0; 'Clinton'= 1")
df_TESS$TRUMP <- car::recode(df_TESS$TREATMENT, "'Alexa'= 0; 'Trump'=1; 'MeToo'=0; 'March'=0; 'Clinton'= 0")
df_TESS$METOO <- car::recode(df_TESS$TREATMENT, "'Alexa'= 0; 'Trump'=0; 'MeToo'=1; 'March'=0; 'Clinton'= 0")
df_TESS$MARCH <- car::recode(df_TESS$TREATMENT, "'Alexa'= 0; 'Trump'=0; 'MeToo'=0; 'March'=1; 'Clinton'= 0")
df_TESS$Engage <- df_TESS$futureengage
df_TESS$anxiety <- df_TESS$fear
cat("Study 2 TREATMENT table:\n"); print(table(df_TESS$TREATMENT, useNA="ifany"))
fit2 <- tryCatch(lavaan:::sem(mix_mod, data=df_TESS, std.lv=TRUE), error=function(e) e)
if (inherits(fit2, "error")) { cat("T2 ERROR:", conditionMessage(fit2), "\n"); add("T2",NA,NA,NA,NA,NA,paste("error:",conditionMessage(fit2)))
} else { pe <- lavaan::parameterEstimates(fit2); print(pe[pe$op==":=",]); r <- pe[pe$label=="indirTRUMPanger",]
  add("T2", r$est, r$se, r$z, r$pvalue, lavaan::lavInspect(fit2,"nobs"))
  r2 <- pe[pe$label=="indirCLINTONanger",]; add("T2_context_Clinton", r2$est, r2$se, r2$z, r2$pvalue, lavaan::lavInspect(fit2,"nobs"))
  write.csv(pe, file.path(OUT, paste0("lavaan_study2_pe", suf, ".csv")), row.names=FALSE) }

# ---- T3, T4: Appendix lines 27-30, 107, 109 (verbatim)
df <- readRDS("Qualtrics_2019.RDS")
df$TREATMENT_sort <- factor(df$TREATMENT, levels = c("Alexa","Trump","Clinton"))
df %>%
  filter(TREATMENT == "Trump" | TREATMENT == "Clinton" | TREATMENT == "Alexa") -> df
anger1 <- lm(anger ~ TREATMENT, data = df)
anger3 <- lm(anger ~ TREATMENT * party_leanersinc, data = df)
s <- summary(anger1)$coefficients["TREATMENTTrump",]; add("T3", s[1], s[2], s[3], s[4], nobs(anger1), paste("R2", summary(anger1)$r.squared))
s <- summary(anger3)$coefficients["TREATMENTTrump:party_leanersinc",]; add("T4", s[1], s[2], s[3], s[4], nobs(anger3))
cat("3-arm Study 1 rows:", nrow(df), "\n")

# ---- T5, T6: Text script lines 392-398 (verbatim)
df_cces <- readRDS("CES2020.RDS")
df_cces %>%
  filter(complier == 1) -> df_compliers
mod2 <- lm(futureengage_novote ~ TREATMENT, data = df_compliers)
print(summary(mod2))
s <- summary(mod2)$coefficients["TREATMENTTreatment of Women",]; add("T5", s[1], s[2], s[3], s[4], nobs(mod2))
add("T6", nobs(mod2), NA, NA, NA, nobs(mod2))
res <- do.call(rbind, rows)
write.csv(res, file.path(OUT, paste0("targets_extracted", suf, ".csv")), row.names=FALSE)
print(res, digits=6)
