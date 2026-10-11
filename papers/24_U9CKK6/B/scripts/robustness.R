## Pre-registered robustness checks R_a, R_b, R_c (PREREG.md section 3), built on the saved original models.
## Estimation sample = model.frame(cycle_AE_fit2) (complete cases on the formula variables, as PREREG defines it).
## Usage: Rscript robustness.R <mode: rc|rb|rbsec|ra> <models_dir> <outputs_dir> [deadline_epoch_seconds for ra]
suppressMessages(library(lme4))
a <- commandArgs(TRUE); mode <- a[1]; md <- a[2]; od <- a[3]
ctrl <- lmerControl(optimizer = "Nelder_Mead")
frame_of <- function(m) {          # model frame with factor-wrapped columns restored to plain names
  mf <- model.frame(m); nm <- names(mf)
  if ("as.factor(country)" %in% nm) { mf$country <- as.character(mf[["as.factor(country)"]]); mf[["as.factor(country)"]] <- NULL }
  if ("as.factor(year)" %in% nm) { mf$year <- as.numeric(as.character(mf[["as.factor(year)"]])); mf[["as.factor(year)"]] <- NULL }
  attr(mf, "terms") <- NULL; mf$mep_ids <- as.character(mf$mep_ids); mf$party_id <- as.character(mf$party_id)
  as.data.frame(mf) }
summ <- function(m, term) { fe <- fixef(m); se <- sqrt(diag(as.matrix(vcov(m)))); names(se) <- names(fe)
  cm <- m@optinfo$conv$lme4$messages
  data.frame(term = term, estimate = unname(fe[term]), se = unname(se[term]), p_naive = 2 * pnorm(-abs(fe[term] / se[term])),
             nobs = nobs(m), conv = if (is.null(cm)) "none" else paste(cm, collapse = " | "),
             dropped = paste(attr(m@pp$X, "col.dropped"), collapse = ";"), row.names = NULL) }
if (mode %in% c("rc", "rb", "ra")) { m0 <- readRDS(file.path(md, "cycle_AE_fit2.rds")); f0 <- formula(m0); d0 <- frame_of(m0)
  est0 <- unname(fixef(m0)["challenge:days_to_nat"]); rm(m0); invisible(gc()) }
if (mode == "rc") {
  f <- update(f0, . ~ . - year + as.factor(year)); t0 <- Sys.time()
  m <- lmer(f, data = d0, control = ctrl); s <- summ(m, "challenge:days_to_nat"); s$secs <- as.numeric(difftime(Sys.time(), t0, units = "secs"))
  s$formula <- paste(deparse(f, width.cutoff = 500), collapse = " "); write.csv(s, file.path(od, "R_c_factor_year.csv"), row.names = FALSE); print(s) }
if (mode == "rb") {
  y <- as.numeric(d0$embed_dict_scale); z <- (y - mean(y)) / sd(y); keep <- abs(z) <= 3
  t0 <- Sys.time(); m <- lmer(f0, data = d0[keep, ], control = ctrl); s <- summ(m, "challenge:days_to_nat")
  s$rows_dropped <- sum(!keep); s$secs <- as.numeric(difftime(Sys.time(), t0, units = "secs"))
  write.csv(s, file.path(od, "R_b_outliers_T1.csv"), row.names = FALSE); print(s) }
if (mode == "rbsec") {
  res <- list()
  for (x in list(c("AUT_sal_model", "aut_dict_scale", "challenge:aut_sal", "T5"), c("EU_sal_model", "int_dict_scale", "challenge:EU_sal", "T6"))) {
    m0 <- readRDS(file.path(md, paste0(x[1], ".rds"))); f <- formula(m0); d <- frame_of(m0); rm(m0); invisible(gc())
    f <- update(f, . ~ . - as.factor(year) + as.factor(year))  # same terms; year column restored to numeric, wrapped by as.factor() as in the original
    y <- as.numeric(d[[x[2]]]); z <- (y - mean(y)) / sd(y); keep <- abs(z) <= 3
    m <- lmer(f, data = d[keep, ], control = ctrl); s <- summ(m, x[3]); s$target <- x[4]; s$rows_dropped <- sum(!keep)
    res[[x[4]]] <- s; rm(m, d); invisible(gc()) }
  out <- do.call(rbind, res); write.csv(out, file.path(od, "R_b_outliers_T5_T6.csv"), row.names = FALSE); print(out) }
if (mode == "ra") {
  deadline <- if (length(a) >= 4) as.numeric(a[4]) else Inf
  dfile <- file.path(od, "R_a_draws.rds"); pfile <- file.path(od, "R_a_partial.csv"); kfile <- file.path(od, "R_a_K.txt")
  parties <- sort(unique(d0$party_id))
  if (!file.exists(dfile)) { set.seed(20261011); draws <- lapply(1:200, function(k) sample(parties, length(parties), replace = TRUE)); saveRDS(draws, dfile) }
  draws <- readRDS(dfile)
  done <- if (file.exists(pfile)) read.csv(pfile) else NULL
  rows_by_party <- split(seq_len(nrow(d0)), d0$party_id)
  K <- if (file.exists(kfile)) as.integer(readLines(kfile)[1]) else NA
  k <- if (is.null(done)) 1 else max(done$draw) + 1
  while (k <= 200 && (is.na(K) || k <= K)) {
    if (as.numeric(Sys.time()) > deadline) { cat("DEADLINE reached before draw", k, "\n"); break }
    dr <- draws[[k]]; idx <- unlist(rows_by_party[dr], use.names = FALSE)
    copy <- rep(seq_along(dr), times = lengths(rows_by_party[dr]))
    d <- d0[idx, ]; d$party_id <- paste(d$party_id, copy); d$mep_ids <- paste(d$mep_ids, copy)
    t0 <- Sys.time()
    r <- tryCatch({ m <- lmer(f0, data = d, control = ctrl); s <- summ(m, "challenge:days_to_nat"); rm(m); s },
                  error = function(e) data.frame(term = "challenge:days_to_nat", estimate = NA, se = NA, p_naive = NA, nobs = nrow(d), conv = paste("ERROR:", conditionMessage(e)), dropped = ""))
    secs <- as.numeric(difftime(Sys.time(), t0, units = "secs"))
    r$draw <- k; r$secs <- secs; done <- rbind(done, r); write.csv(done, pfile, row.names = FALSE)
    if (is.na(K)) { Kr <- min(200, floor(3600 / secs)); if (Kr < 30) Kr <- if (30 * secs <= 7200) 30 else 0
      K <- Kr; writeLines(c(as.character(K), paste("first_refit_secs", secs)), kfile) }
    cat("draw", k, "est", r$estimate, "secs", round(secs), "\n"); rm(d); invisible(gc()); k <- k + 1 }
  est <- done$estimate[!is.na(done$estimate)]
  s <- data.frame(original_estimate = est0, K_rule = K, K_done = length(est), failed = sum(is.na(done$estimate)),
                  boot_se = if (length(est) > 1) sd(est) else NA, q025 = if (length(est) > 1) quantile(est, 0.025) else NA,
                  q975 = if (length(est) > 1) quantile(est, 0.975) else NA, row.names = NULL)
  s$p_normal <- 2 * pnorm(-abs(s$original_estimate / s$boot_se))
  write.csv(s, file.path(od, "R_a_summary.csv"), row.names = FALSE); print(s) }
