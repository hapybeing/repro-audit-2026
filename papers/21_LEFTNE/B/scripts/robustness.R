# Pre-registered robustness checks R_a, R_b, R_c (PREREG section 3). Authors' data lines copied verbatim; authors' files untouched.
# Usage: Rscript robustness.R <step>  where step in Ra1, Ra2, Rb, Rc. Ra steps resume from saved draws.
.libPaths(c("/workspace/audit_runs/21_LEFTNE/B/rlib", .libPaths()))
suppressMessages({library(dplyr); library(car)})
step <- commandArgs(TRUE)[1]
OUT <- "/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/21_LEFTNE/B/outputs"
setwd("/workspace/audit_runs/21_LEFTNE/B/data")
cat("lavaan", as.character(packageVersion("lavaan")), "\n")
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
load_s1 <- function() {
  df <- readRDS("Qualtrics_2019.RDS")
  df$CLINTON <- car::recode(df$TREATMENT, "'Alexa'= 0; 'Trump'=0; 'MeToo'=0; 'Marches'=0; 'Clinton'= 1")
  df$TRUMP <- car::recode(df$TREATMENT, "'Alexa'= 0; 'Trump'=1; 'MeToo'=0; 'Marches'=0; 'Clinton'= 0")
  df$METOO <- car::recode(df$TREATMENT, "'Alexa'= 0; 'Trump'=0; 'MeToo'=1; 'Marches'=0; 'Clinton'= 0")
  df$MARCH <- car::recode(df$TREATMENT, "'Alexa'= 0; 'Trump'=0; 'MeToo'=0; 'Marches'=1; 'Clinton'= 0")
  df$Engage <- df$futureengage
  df$anxiety <- df$fear
  df }
load_s2 <- function() {
  df_TESS <- readRDS("NORC.RDS")
  df_TESS$CLINTON <- car::recode(df_TESS$TREATMENT, "'Alexa'= 0; 'Trump'=0; 'MeToo'=0; 'March'=0; 'Clinton'= 1")
  df_TESS$TRUMP <- car::recode(df_TESS$TREATMENT, "'Alexa'= 0; 'Trump'=1; 'MeToo'=0; 'March'=0; 'Clinton'= 0")
  df_TESS$METOO <- car::recode(df_TESS$TREATMENT, "'Alexa'= 0; 'Trump'=0; 'MeToo'=1; 'March'=0; 'Clinton'= 0")
  df_TESS$MARCH <- car::recode(df_TESS$TREATMENT, "'Alexa'= 0; 'Trump'=0; 'MeToo'=0; 'March'=1; 'Clinton'= 0")
  df_TESS$Engage <- df_TESS$futureengage
  df_TESS$anxiety <- df_TESS$fear
  df_TESS }
vars <- c("Engage","anxiety","anger","hope","TRUMP","CLINTON","MARCH","METOO")
indir <- function(fit, lab="indirTRUMPanger") { pe <- lavaan::parameterEstimates(fit); pe[pe$label==lab,] }

if (step %in% c("Ra1","Ra2")) {
  study <- if (step=="Ra1") "study1" else "study2"
  d0 <- if (step=="Ra1") load_s1() else load_s2()
  d <- d0[complete.cases(d0[, vars]), ]
  fit0 <- lavaan:::sem(mix_mod, data=d0, std.lv=TRUE)
  n <- nrow(d); cat(study, "complete rows", n, "lavaan nobs", lavaan::lavInspect(fit0,"nobs"), "\n")
  K <- as.integer(Sys.getenv("RA_K", "1000"))
  f <- file.path(OUT, paste0("Ra_draws_", study, ".csv"))
  # Draw all K index vectors up front from one set.seed call, so resuming reproduces the identical sequence.
  set.seed(20261011); idx <- lapply(seq_len(K), function(k) sample(n, n, replace = TRUE))
  done <- if (file.exists(f)) read.csv(f) else data.frame(b=integer(), est=numeric(), status=character())
  t0 <- Sys.time(); buf <- list()
  for (b in setdiff(seq_len(K), done$b)) {
    r <- tryCatch({ fb <- lavaan:::sem(mix_mod, data=d[idx[[b]], ], std.lv=TRUE)
      if (!lavaan::lavInspect(fb, "converged")) data.frame(b=b, est=NA, status="nonconverged") else data.frame(b=b, est=indir(fb)$est, status="ok") },
      error=function(e) data.frame(b=b, est=NA, status=paste("error:", conditionMessage(e))))
    buf[[length(buf)+1]] <- r
    if (b %% 100 == 0 || b == K) { done <- rbind(done, do.call(rbind, buf)); buf <- list(); write.csv(done, f, row.names=FALSE); cat("saved through", b, format(Sys.time()), "\n") }
    if (as.numeric(difftime(Sys.time(), t0, units="secs")) > 520) { if (length(buf)) { done <- rbind(done, do.call(rbind, buf)); write.csv(done, f, row.names=FALSE) }; cat("time slice ended at", b, "\n"); quit(status=3) }
  }
  ok <- done$est[done$status=="ok"]
  o <- indir(fit0)
  res <- data.frame(study=study, K=K, n_rows=n, lavaan_nobs=lavaan::lavInspect(fit0,"nobs"), estimate=o$est, orig_se=o$se, orig_p=o$pvalue,
    n_ok=length(ok), n_failed=sum(done$status!="ok"), boot_sd=sd(ok), ci_lo=unname(quantile(ok,.025)), ci_hi=unname(quantile(ok,.975)),
    p_boot=min(2*mean(ok<=0), 1))
  write.csv(res, file.path(OUT, paste0("Ra_summary_", study, ".csv")), row.names=FALSE); print(res)
}

if (step == "Rb") {
  # T3 primary: Appendix lines 27-30 (verbatim) then outlier rule on anger
  df <- readRDS("Qualtrics_2019.RDS")
  df$TREATMENT_sort <- factor(df$TREATMENT, levels = c("Alexa","Trump","Clinton"))
  df %>%
    filter(TREATMENT == "Trump" | TREATMENT == "Clinton" | TREATMENT == "Alexa") -> df
  m0 <- lm(anger ~ TREATMENT, data = df); u <- model.frame(m0)
  z <- (u$anger - mean(u$anger)) / sd(u$anger); keep <- abs(z) <= 3
  m1 <- lm(anger ~ TREATMENT, data = u[keep, ])
  s <- summary(m1)$coefficients["TREATMENTTrump",]
  r1 <- data.frame(check="Rb_T3", n_before=nrow(u), dropped=sum(!keep), estimate=s[1], se=s[2], p_value=s[4], z_max=max(abs(z)))
  # T1 secondary: lavaan estimation sample, z on Engage
  d0 <- load_s1(); d <- d0[complete.cases(d0[, vars]), ]
  z2 <- (d$Engage - mean(d$Engage)) / sd(d$Engage); keep2 <- abs(z2) <= 3
  fb <- lavaan:::sem(mix_mod, data=d[keep2, ], std.lv=TRUE); o <- indir(fb)
  r2 <- data.frame(check="Rb_T1", n_before=nrow(d), dropped=sum(!keep2), estimate=o$est, se=o$se, p_value=o$pvalue, z_max=max(abs(z2)))
  res <- rbind(r1, r2); write.csv(res, file.path(OUT, "Rb_results.csv"), row.names=FALSE); print(res)
}

if (step == "Rc") {
  mod3 <- '
Engage ~ b1 * anxiety + b2 * anger + b3 * hope + c1 * TRUMP + c2 * CLINTON
anxiety ~ a1 * TRUMP + a99 * CLINTON
anger ~ a2 * TRUMP + a299 * CLINTON
hope ~ a3 * TRUMP + a399 * CLINTON
indirTRUMPanxiety := a1 * b1
indirTRUMPanger := a2 * b2
indirTRUMPhope := a3 * b3
indirCLINTONanxiety := a99 * b1
indirCLINTONanger := a299 * b2
indirCLINTONhope := a399 * b3
'
  out <- list()
  for (st in c("study1","study2")) {
    d <- if (st=="study1") load_s1() else load_s2()
    d <- d[d$TREATMENT %in% c("Alexa","Trump","Clinton"), ]
    fb <- lavaan:::sem(mod3, data=d, std.lv=TRUE); o <- indir(fb)
    out[[st]] <- data.frame(check=paste0("Rc_", st), estimate=o$est, se=o$se, p_value=o$pvalue, nobs=lavaan::lavInspect(fb,"nobs"))
  }
  res <- do.call(rbind, out); write.csv(res, file.path(OUT, "Rc_results.csv"), row.names=FALSE); print(res)
}
