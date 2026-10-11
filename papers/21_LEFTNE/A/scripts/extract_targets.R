# Re-executes, in a fresh session, only the authors' own data-loading and model lines for each target, copied verbatim
# from "01- Replication_Text.R" (lines 343-363, 366-387, 392-397) and "02- Replication_Appendix.R" (lines 27-30, 107, 109).
# Writes outputs/targets_extracted<suffix>.csv. Usage: Rscript extract_targets.R <suffix>   (run with wd = RUNDIR/data)
args <- commandArgs(trailingOnly = TRUE); suffix <- if (length(args)) args[1] else ""
OUT <- "/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/21_LEFTNE/A/outputs"
suppressPackageStartupMessages({library(car); library(dplyr)})
lavver <- as.character(packageVersion("lavaan")); cat("lavaan", lavver, "from", find.package("lavaan"), "\n")
rows <- list()
add <- function(id, est, se, stat, p, n, src, note = "") rows[[length(rows) + 1]] <<- data.frame(id = id, estimate = est, se = se, statistic = stat, p_value = p, nobs = n, model = src, lavaan_version = lavver, note = note)

## ---- T1: Text script lines 343-363 (verbatim) ----
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
cat("Study 1 TREATMENT levels:", levels(df$TREATMENT), "| class of TRUMP:", class(df$TRUMP), "| levels:", levels(df$TRUMP), "\n")
print(table(df$TREATMENT, useNA = "ifany"))
fit1 <- tryCatch(lavaan:::sem(mix_mod, data=df, std.lv=TRUE), error = function(e) e)
if (inherits(fit1, "error")) { cat("STUDY1 SEM ERROR:", conditionMessage(fit1), "\n"); add("T1", NA, NA, NA, NA, NA, "lavaan sem Study 1", paste("error:", conditionMessage(fit1))) } else {
  pe <- lavaan::parameterEstimates(fit1); n1 <- lavaan::lavInspect(fit1, "nobs")
  for (lab in c("indirTRUMPanger", "indirCLINTONanger", "indirTRUMPhope", "indirCLINTONhope")) { r <- pe[pe$label == lab, ]
    add(if (lab == "indirTRUMPanger") "T1" else paste0("S1_", lab), r$est, r$se, r$z, r$pvalue, n1, "lavaan sem Study 1 (Text 343-363)") }
  write.csv(pe, file.path(OUT, paste0("lavaan_study1_parameterEstimates", suffix, ".csv")), row.names = FALSE)
}

## ---- T2: Text script lines 366-387 (verbatim) ----
df_TESS <- readRDS("NORC.RDS")
df_TESS$CLINTON <- car::recode(df_TESS$TREATMENT, "'Alexa'= 0; 'Trump'=0; 'MeToo'=0; 'March'=0; 'Clinton'= 1")
df_TESS$TRUMP <- car::recode(df_TESS$TREATMENT, "'Alexa'= 0; 'Trump'=1; 'MeToo'=0; 'March'=0; 'Clinton'= 0")
df_TESS$METOO <- car::recode(df_TESS$TREATMENT, "'Alexa'= 0; 'Trump'=0; 'MeToo'=1; 'March'=0; 'Clinton'= 0")
df_TESS$MARCH <- car::recode(df_TESS$TREATMENT, "'Alexa'= 0; 'Trump'=0; 'MeToo'=0; 'March'=1; 'Clinton'= 0")
df_TESS$Engage <- df_TESS$futureengage
df_TESS$anxiety <- df_TESS$fear
cat("Study 2 TREATMENT levels:", levels(df_TESS$TREATMENT), "| class of TRUMP:", class(df_TESS$TRUMP), "\n")
print(table(df_TESS$TREATMENT, useNA = "ifany"))
fit2 <- tryCatch(lavaan:::sem(mix_mod, data=df_TESS, std.lv=TRUE), error = function(e) e)
if (inherits(fit2, "error")) { cat("STUDY2 SEM ERROR:", conditionMessage(fit2), "\n"); add("T2", NA, NA, NA, NA, NA, "lavaan sem Study 2", paste("error:", conditionMessage(fit2))) } else {
  pe <- lavaan::parameterEstimates(fit2); n2 <- lavaan::lavInspect(fit2, "nobs")
  for (lab in c("indirTRUMPanger", "indirCLINTONanger", "indirTRUMPhope", "indirCLINTONhope")) { r <- pe[pe$label == lab, ]
    add(if (lab == "indirTRUMPanger") "T2" else paste0("S2_", lab), r$est, r$se, r$z, r$pvalue, n2, "lavaan sem Study 2 (Text 366-387)") }
  write.csv(pe, file.path(OUT, paste0("lavaan_study2_parameterEstimates", suffix, ".csv")), row.names = FALSE)
}

## ---- T3, T4: Appendix lines 27-30, 107, 109 (verbatim) ----
df <- readRDS("Qualtrics_2019.RDS")
df$TREATMENT_sort <- factor(df$TREATMENT, levels = c("Alexa","Trump","Clinton"))
df %>%
  filter(TREATMENT == "Trump" | TREATMENT == "Clinton" | TREATMENT == "Alexa") -> df
anger1 <- lm(anger ~ TREATMENT, data = df)
anger3 <- lm(anger ~ TREATMENT * party_leanersinc, data = df)
s <- summary(anger1)$coefficients; r <- s["TREATMENTTrump", ]
add("T3", r[1], r[2], r[3], r[4], nobs(anger1), "lm(anger ~ TREATMENT) Appendix 107", paste("R2", summary(anger1)$r.squared))
s <- summary(anger3)$coefficients; r <- s["TREATMENTTrump:party_leanersinc", ]
add("T4", r[1], r[2], r[3], r[4], nobs(anger3), "lm(anger ~ TREATMENT * party_leanersinc) Appendix 109", paste("R2", summary(anger3)$r.squared))

## ---- T5, T6: Text lines 392-397 (verbatim) ----
df_cces <- readRDS("CES2020.RDS")
df_cces %>%
  filter(complier == 1) -> df_compliers
mod2 <- lm(futureengage_novote ~ TREATMENT, data = df_compliers)
s <- summary(mod2)$coefficients; print(s)
r <- s["TREATMENTTreatment of Women", ]
add("T5", r[1], r[2], r[3], r[4], nobs(mod2), "lm(futureengage_novote ~ TREATMENT) compliers, Text 397", paste("R2", summary(mod2)$r.squared))
add("T6", nobs(mod2), NA, NA, NA, nobs(mod2), "nobs(mod2)")
for (nm in setdiff(rownames(s), "TREATMENTTreatment of Women")) add(paste0("T3ctx_", nm), s[nm, 1], s[nm, 2], s[nm, 3], s[nm, 4], nobs(mod2), "Table 3 context")

res <- do.call(rbind, rows)
write.csv(res, file.path(OUT, paste0("targets_extracted", suffix, ".csv")), row.names = FALSE)
print(res, digits = 6)
