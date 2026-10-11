# Pre-registered robustness checks R_a, R_b, R_c (PREREG.md section 3). Run with wd = RUNDIR/data.
# Usage: Rscript robustness.R <step>   step in: Ra_study1 | Ra_study2 | Rb | Rc
# Authors' data-loading lines and model string copied verbatim from "01- Replication_Text.R" 343-362 / 366-385 and
# "02- Replication_Appendix.R" 27-30, 107. Authors' files are never edited.
step <- commandArgs(trailingOnly = TRUE)[1]
OUT <- "/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/21_LEFTNE/A/outputs"
suppressPackageStartupMessages({library(car); library(dplyr); library(lavaan)})
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
vars <- c("Engage", "anxiety", "anger", "hope", "TRUMP", "CLINTON", "MARCH", "METOO")
get_ind <- function(fit, lab = "indirTRUMPanger") { pe <- parameterEstimates(fit); pe[pe$label == lab, c("est", "se", "z", "pvalue")] }

if (grepl("^Ra_", step)) {
  study <- sub("Ra_", "", step); df <- if (study == "study1") load_s1() else load_s2()
  fit0 <- lavaan:::sem(mix_mod, data=df, std.lv=TRUE)
  cc <- df[complete.cases(df[, vars]), ]
  n <- nrow(cc); nl <- lavInspect(fit0, "nobs")
  cat(study, "complete rows", n, "lavaan nobs", nl, "\n")
  K <- 1000
  set.seed(20261011)
  idx <- lapply(seq_len(K), function(k) sample(n, n, replace = TRUE))  # same RNG stream as drawing inside the loop; lavaan ML fits draw no random numbers
  f <- file.path(OUT, paste0("Ra_draws_", study, ".csv"))
  done <- if (file.exists(f)) read.csv(f) else data.frame(k = integer(), est = numeric(), status = character())
  t0 <- Sys.time()
  for (k in setdiff(seq_len(K), done$k)) {
    r <- tryCatch({ fb <- lavaan:::sem(mix_mod, data = cc[idx[[k]], ], std.lv = TRUE)
      if (!lavInspect(fb, "converged")) data.frame(k = k, est = NA, status = "not_converged") else data.frame(k = k, est = get_ind(fb)$est, status = "ok") },
      error = function(e) data.frame(k = k, est = NA, status = paste("error:", conditionMessage(e))))
    done <- rbind(done, r)
    if (k %% 100 == 0) write.csv(done, f, row.names = FALSE)
    if (as.numeric(difftime(Sys.time(), t0, units = "secs")) > 540) { write.csv(done, f, row.names = FALSE); cat("time slice ended at k =", k, "\n"); quit(save = "no") }
  }
  write.csv(done, f, row.names = FALSE)
  ok <- done$est[done$status == "ok"]; o <- get_ind(fit0)
  ci <- quantile(ok, c(.025, .975), names = FALSE); pb <- min(2 * mean(ok <= 0), 1)
  s <- data.frame(id = "R_a", study = study, K = K, n_rows = n, lavaan_nobs = nl, n_ok = length(ok), n_failed = K - length(ok),
                  estimate = o$est, boot_ci_low = ci[1], boot_ci_high = ci[2], boot_sd = sd(ok), p_value = pb, seed = 20261011)
  write.csv(s, file.path(OUT, paste0("Ra_summary_", study, ".csv")), row.names = FALSE); print(s)
}

if (step == "Rb") {
  # T3 primary
  df <- readRDS("Qualtrics_2019.RDS")
  df$TREATMENT_sort <- factor(df$TREATMENT, levels = c("Alexa","Trump","Clinton"))
  df %>%
    filter(TREATMENT == "Trump" | TREATMENT == "Clinton" | TREATMENT == "Alexa") -> df
  m0 <- lm(anger ~ TREATMENT, data = df)
  used <- df[rownames(df) %in% rownames(model.frame(m0)), ]
  z <- (used$anger - mean(used$anger)) / sd(used$anger)
  kept <- used[abs(z) <= 3, ]
  m1 <- lm(anger ~ TREATMENT, data = kept); r <- summary(m1)$coefficients["TREATMENTTrump", ]
  out <- data.frame(id = "R_b", part = "T3", n_before = nrow(used), n_dropped = sum(abs(z) > 3), max_abs_z = max(abs(z)),
                    estimate = r[1], se = r[2], p_value = r[4], nobs = nobs(m1))
  # T1 secondary
  d1 <- load_s1(); cc <- d1[complete.cases(d1[, vars]), ]
  z2 <- (cc$Engage - mean(cc$Engage)) / sd(cc$Engage)
  fit <- lavaan:::sem(mix_mod, data = cc[abs(z2) <= 3, ], std.lv = TRUE); g <- get_ind(fit)
  out <- rbind(out, data.frame(id = "R_b", part = "T1", n_before = nrow(cc), n_dropped = sum(abs(z2) > 3), max_abs_z = max(abs(z2)),
                    estimate = g$est, se = g$se, p_value = g$pvalue, nobs = lavInspect(fit, "nobs")))
  write.csv(out, file.path(OUT, "Rb_summary.csv"), row.names = FALSE); print(out)
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
  out <- NULL
  for (study in c("study1", "study2")) {
    d <- if (study == "study1") load_s1() else load_s2()
    d <- d[d$TREATMENT %in% c("Alexa", "Trump", "Clinton"), ]
    fit <- lavaan:::sem(mod3, data = d, std.lv = TRUE); g <- get_ind(fit)
    out <- rbind(out, data.frame(id = "R_c", study = study, estimate = g$est, se = g$se, z = g$z, p_value = g$pvalue, nobs = lavInspect(fit, "nobs")))
  }
  write.csv(out, file.path(OUT, "Rc_summary.csv"), row.names = FALSE); print(out)
}
