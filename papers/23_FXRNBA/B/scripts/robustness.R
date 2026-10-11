# Pre-registered robustness checks R_a, R_b, R_c and the exploratory sample check for 23_FXRNBA.
# Builds seattle_main and the helper functions by sourcing the authors' lines 1-405 unchanged (data load, samples, helpers; no models).
# Usage: Rscript robustness.R Ra | Rbc
mode <- commandArgs(TRUE)[1]
RUN <- "/workspace/audit_runs/23_FXRNBA/B/run"; setwd(RUN)
src <- readLines("wildfire_data_analysis.R", warn = FALSE)
writeLines(src[1:405], "/workspace/audit_runs/23_FXRNBA/B/part_1_405.R")
source("/workspace/audit_runs/23_FXRNBA/B/part_1_405.R")
mode <- commandArgs(TRUE)[1]
OUT <- "/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/23_FXRNBA/B/outputs"
W <- "holiday + awnd + tmax + tmin + prcp"; FE3 <- "station + year + month + dow"
f_fs <- as.formula(paste("pm25_mean ~ z_smoke +", W, "+", FE3))
f_ss <- as.formula(paste("assault ~ pm25_mean +", W, "+", FE3))
stopifnot(nrow(seattle_main) == 7163)

if (mode == "Ra") {
  set.seed(20261011)
  B <- 999
  dates <- sort(unique(seattle_main$date))
  rows_by_date <- split(seq_len(nrow(seattle_main)), as.character(seattle_main$date))
  idxf <- "/workspace/audit_runs/23_FXRNBA/B/Ra_boot_indices.rds"  # moved out of repo (12 MB); written to outputs/ in the run, sha256 in LOG.md
  if (file.exists(idxf)) idx <- readRDS(idxf) else {
    idx <- lapply(seq_len(B), function(b) {
      d <- sample(as.character(dates), length(dates), replace = TRUE)
      unlist(rows_by_date[d], use.names = FALSE)
    })
    saveRDS(idx, idxf)
  }
  cat("Ra_boot_indices sha256-able file written; B generated =", length(idx), "\n")
  fit1 <- function(dd) {
    dd <- droplevels(dd)
    fs_glm <- glm(f_fs, data = dd)
    ss_glm <- glm(f_ss, family = poisson(link = "log"), data = dd)
    iv <- ivtools::ivglm(estmethod = "ts", fitX.LZ = fs_glm, fitY.LX = ss_glm, data = dd,
                         ctrl = TRUE, vcov.fit = FALSE)
    conv <- isTRUE(ss_glm$converged) && isTRUE(fs_glm$converged)
    c(unname(iv$est["pm25_mean"]), conv)
  }
  csvf <- file.path(OUT, "Ra_boot.csv")
  done <- if (file.exists(csvf)) read.csv(csvf) else data.frame(rep = integer(), est = numeric(), converged = integer(), error = character())
  Buse <- as.integer(Sys.getenv("RA_B", "999"))
  todo <- setdiff(seq_len(Buse), done$rep)
  buf <- list(); t0 <- Sys.time()
  for (b in todo) {
    r <- tryCatch(fit1(seattle_main[idx[[b]], ]), error = function(e) structure(c(NA, 0), msg = conditionMessage(e)))
    buf[[length(buf) + 1]] <- data.frame(rep = b, est = r[1], converged = as.integer(r[2]),
                                          error = ifelse(is.null(attr(r, "msg")), "", attr(r, "msg")))
    if (length(buf) == 50 || b == tail(todo, 1) || (nrow(done) == 0 && length(buf) == 20 && b == 20)) {
      done <- rbind(done, do.call(rbind, buf)); buf <- list()
      write.csv(done, csvf, row.names = FALSE)
      cat(format(Sys.time()), "saved", nrow(done), "replicates; elapsed this session", round(as.numeric(difftime(Sys.time(), t0, units = "secs"))), "s\n")
    }
  }
  cat("RA DONE\n")
}

if (mode == "Rbc") {
  res <- list()
  # Original Model 3 point estimate, refit here for the bootstrap reference
  iv0 <- run_ivglm(f_fs, f_ss, seattle_main); r0 <- grab_by_name(iv0, "pm25_mean")
  res$orig_beta <- r0$pm25_mean$beta; res$orig_se <- r0$pm25_mean$se; res$orig_p <- r0$pm25_mean$p
  # T5 candidate 3: glm first stage inside run_ivglm for Model 3
  res$T5_cand3_glm_fs_coef <- unname(coef(glm(f_fs, data = droplevels(seattle_main)))["z_smoke"])
  # R_b: pooled |z| > 3 on assault
  z <- (seattle_main$assault - mean(seattle_main$assault)) / sd(seattle_main$assault)
  keep <- abs(z) <= 3
  drop_by_station <- table(seattle_main$station[!keep])
  dat_b <- seattle_main[keep, ]
  ivb <- run_ivglm(f_fs, f_ss, dat_b); rb <- grab_by_name(ivb, "pm25_mean")
  db <- fs_diag(as.formula(paste("pm25_mean ~ z_smoke +", W, "|", FE3)), as.formula(paste("pm25_mean ~", W, "|", FE3)), dat_b)
  res$Rb_beta <- rb$pm25_mean$beta; res$Rb_se <- rb$pm25_mean$se; res$Rb_p <- rb$pm25_mean$p
  res$Rb_F <- db$F; res$Rb_N <- nrow(dat_b); res$Rb_dropped <- sum(!keep)
  for (s in names(drop_by_station)) res[[paste0("Rb_dropped_", gsub(" ", "_", s))]] <- as.integer(drop_by_station[[s]])
  res$Rb_z_cutoff_assault_low <- mean(seattle_main$assault) - 3 * sd(seattle_main$assault)
  res$Rb_z_cutoff_assault_high <- mean(seattle_main$assault) + 3 * sd(seattle_main$assault)
  # R_c: 2SLS on log(1+assault)
  rc <- fixest::feols(log(1 + assault) ~ holiday + awnd + tmax + tmin + prcp | station + year + month + dow | pm25_mean ~ z_smoke,
                      data = seattle_main, cluster = ~date)
  ct <- fixest::coeftable(rc)
  res$Rc_beta <- ct["fit_pm25_mean", 1]; res$Rc_se <- ct["fit_pm25_mean", 2]; res$Rc_p <- ct["fit_pm25_mean", 4]
  res$Rc_F_ivwald <- unname(fixest::fitstat(rc, "ivwald")[[1]]$stat); res$Rc_N <- nobs(rc)
  # Exploratory (not pre-registered): listwise deletion over the Model 3 variables only
  ex <- seattle13 %>% filter(year(date) >= 2013 & year(date) <= 2023) %>%
    dplyr::select(assault, pm25_mean, smokepm_dummy, awnd, tmax, tmin, prcp, station, date, year, month, dow, holiday) %>%
    na.omit() %>%
    mutate(z_smoke = as.numeric(as.character(smokepm_dummy)), station = factor(station), year = factor(year),
           month = factor(month), dow = factor(dow, ordered = FALSE), holiday = factor(holiday), date = as.Date(date), awnd = as.numeric(awnd))
  ive <- run_ivglm(f_fs, f_ss, ex); re <- grab_by_name(ive, "pm25_mean")
  res$EXPL_N_model3_vars_only <- nrow(ex); res$EXPL_rows_dropped_by_extra_naomit_cols <- nrow(ex) - nrow(seattle_main)
  res$EXPL_beta <- re$pm25_mean$beta; res$EXPL_se <- re$pm25_mean$se; res$EXPL_p <- re$pm25_mean$p
  out <- data.frame(quantity = names(res), value = as.numeric(unlist(res)))
  write.csv(out, file.path(OUT, "robustness_Rb_Rc.csv"), row.names = FALSE)
  print(format(out, digits = 10))
}
