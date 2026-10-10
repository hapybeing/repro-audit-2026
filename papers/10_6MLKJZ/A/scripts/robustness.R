# Pre-registered robustness checks R_a, R_b, R_c (PREREG.md section 3). Usage: Rscript robustness.R RUNDIR OUTDIR [a|b|c|all]
suppressMessages({library(cregg); library(jsonlite); library(data.table)})
args <- commandArgs(trailingOnly = TRUE); rundir <- args[1]; outdir <- args[2]; which <- ifelse(length(args) > 2, args[3], "all")
d <- readRDS(file.path(rundir, "pooled_df2.rds"))
feats <- c("Gender","Age","Citizenship","Composition","Unemployment","Supportive","Since","Education")
fc1v <- c("Gender","Age","Citizenship","Composition","Unemployment","Supportive")
lvmap <- do.call(rbind, lapply(feats, function(f) data.frame(var = f, level = levels(d[[f]]))))
ds <- d[d$sector %in% c("Private Sector", "Public Sector"), ]
ds$sector <- droplevels(ds$sector)
E1lev <- "2 Adults, 3 Childr."
f_fig1 <- selected ~ Gender + Age + Citizenship + Composition + Unemployment + Supportive + Citizenship + Since + Education
f_fig2 <- selected ~ Gender + Age + Citizenship + Composition + Unemployment + Supportive + Since + Education

## ---------- R_a cluster bootstrap ----------
if (which %in% c("a", "all")) {
  orig <- cj(data = d, formula = f_fig1, estimate = "mm", by = ~ sector, id = ~ respondentIndex)
  e1row <- orig[orig$level == E1lev & orig$sector == "Private Sector", ]
  cc <- ds[complete.cases(ds[, c("selected", feats)]), ]
  # respondent x level sums and counts
  levs <- lvmap$level
  S <- N <- matrix(0, nrow = 0, ncol = length(levs))
  ids <- sort(unique(cc$respondentIndex)); idx <- match(cc$respondentIndex, ids)
  S <- matrix(0, length(ids), length(levs), dimnames = list(ids, levs)); N <- S
  for (k in seq_along(levs)) { v <- lvmap$var[k]; m <- cc[[v]] == levs[k]
    S[, k] <- tapply(cc$selected * m, idx, sum); N[, k] <- tapply(as.numeric(m), idx, sum) }
  sec <- cc$sector[match(ids, cc$respondentIndex)]
  ip <- which(sec == "Private Sector"); iu <- which(sec == "Public Sector")
  mmfun <- function(w, ii) colSums(S[ii, , drop = FALSE] * w) / colSums(N[ii, , drop = FALSE] * w)
  # check: unweighted means equal cregg MMs
  chk <- mmfun(rep(1, length(ip)), ip)[E1lev]
  set.seed(20261009); B <- 1000
  bp <- bu <- matrix(NA, B, length(levs), dimnames = list(NULL, levs))
  for (b in 1:B) {
    wp <- tabulate(sample.int(length(ip), length(ip), replace = TRUE), length(ip))
    wu <- tabulate(sample.int(length(iu), length(iu), replace = TRUE), length(iu))
    bp[b, ] <- mmfun(wp, ip); bu[b, ] <- mmfun(wu, iu)
  }
  e1s <- bp[, E1lev]
  pval <- min(1, 2 * min(mean(e1s <= 0.5), mean(e1s >= 0.5)))
  dif <- bu - bp
  ci_d <- t(apply(dif, 2, quantile, c(0.025, 0.975)))
  excl <- ci_d[, 1] > 0 | ci_d[, 2] < 0
  fc1_lv <- levs[lvmap$var %in% fc1v]
  ra <- list(E1_cregg = e1row$estimate, E1_cregg_se = e1row$std.error, E1_unweighted_check = unname(chk),
    n_resp_private = length(ip), n_resp_public = length(iu), B = B, seed = 20261009,
    boot_ci_lower = unname(quantile(e1s, 0.025)), boot_ci_upper = unname(quantile(e1s, 0.975)), boot_se = sd(e1s),
    p_value = pval, same_dir_sig = (e1row$estimate > 0.5) && quantile(e1s, 0.025) > 0.5,
    FC1_count = sum(excl[fc1_lv]), FC1_levels = fc1_lv[excl[fc1_lv]],
    Since_Education_levels_excl0 = levs[excl & lvmap$var %in% c("Since", "Education")])
  write(toJSON(ra, auto_unbox = TRUE, pretty = TRUE, digits = NA), file.path(outdir, "robustness_R_a.json"))
  write.csv(data.frame(level = levs, var = lvmap$var, diff_lower = ci_d[, 1], diff_upper = ci_d[, 2]), file.path(outdir, "robustness_R_a_mmdiff_ci.csv"), row.names = FALSE)
  print(ra)
}

## ---------- R_b duration trimming ----------
if (which %in% c("b", "all")) {
  raw <- c(rh = "data_rh.csv", uhh = "data_UHH.csv", hsvn = "data_HSVN.csv", civic = "data_civic.csv")
  d$sam <- sub("\n.*", "", as.character(d$Sample))
  drop_ids <- character(0); info <- list()
  for (s in names(raw)) {
    r <- fread(file.path(rundir, "data/conjoint_data/raw_data", raw[[s]]), data.table = FALSE, select = c("ResponseId", "Duration (in seconds)"))
    r$dur <- suppressWarnings(as.numeric(r[["Duration (in seconds)"]])); r <- r[!is.na(r$dur), ]
    ids <- unique(d$respondentIndex[d$sam == s])
    rr <- r[r$ResponseId %in% ids, ]
    q <- quantile(rr$dur, c(0.01, 0.99), type = 7)
    dr <- rr$ResponseId[rr$dur < q[1] | rr$dur > q[2]]
    drop_ids <- c(drop_ids, dr)
    info[[s]] <- list(n_resp_in_pooled = length(ids), n_matched_duration = nrow(rr), dup_ids = sum(duplicated(rr$ResponseId)),
                      p01 = unname(q[1]), p99 = unname(q[2]), dropped = length(dr))
  }
  dred <- d[!(d$respondentIndex %in% drop_ids), ]
  m1 <- cj(data = dred, formula = f_fig1, estimate = "mm", by = ~ sector, id = ~ respondentIndex)
  m2 <- cj(data = dred, formula = f_fig2, estimate = "mm_diff", by = ~ sector, id = ~ respondentIndex)
  write.csv(as.data.frame(m1), file.path(outdir, "robustness_R_b_fig1_mm.csv"), row.names = FALSE)
  write.csv(as.data.frame(m2), file.path(outdir, "robustness_R_b_fig2_mmdiff.csv"), row.names = FALSE)
  e <- m1[m1$level == E1lev & m1$sector == "Private Sector", ]
  z <- (e$estimate - 0.5) / e$std.error
  m2$var <- lvmap$var[match(m2$level, lvmap$level)]
  ex <- (m2$lower > 0 | m2$upper < 0)
  rb <- list(per_sample = info, total_dropped = length(unique(drop_ids)),
    n_resp_private = length(unique(dred$respondentIndex[dred$sector %in% "Private Sector"])),
    n_resp_public = length(unique(dred$respondentIndex[dred$sector %in% "Public Sector"])),
    E1 = e$estimate, se = e$std.error, lower = e$lower, upper = e$upper, z_vs_0.5 = z, p_value = 2 * pnorm(-abs(z)),
    same_dir_sig = e$estimate > 0.5 && e$lower > 0.5,
    FC1_count = sum(ex & m2$var %in% fc1v), FC1_levels = m2$level[ex & m2$var %in% fc1v],
    Since_Education_levels_excl0 = m2$level[ex & m2$var %in% c("Since", "Education")])
  write(toJSON(rb, auto_unbox = TRUE, pretty = TRUE, digits = NA), file.path(outdir, "robustness_R_b.json"))
  print(rb)
}

## ---------- R_c AMCE + omnibus ----------
if (which %in% c("c", "all")) {
  am <- cj(ds, selected ~ Gender + Age + Citizenship + Composition + Unemployment + Supportive + Since + Education,
           estimate = "amce", by = ~ sector, id = ~ respondentIndex)
  write.csv(as.data.frame(am), file.path(outdir, "robustness_R_c_amce.csv"), row.names = FALSE)
  e <- am[am$level == E1lev & am$sector == "Private Sector", ]
  an <- cregg::cj_anova(ds, selected ~ Gender + Age + Citizenship + Composition + Unemployment + Supportive + Since + Education, by = ~ sector)
  capture.output(print(an), file = file.path(outdir, "robustness_R_c_anova.txt"))
  rc <- list(baseline_Composition = levels(ds$Composition)[1], AMCE = e$estimate, se = e$std.error, lower = e$lower, upper = e$upper,
    p_value = e$p, same_dir_sig = e$estimate > 0 && e$p < 0.05,
    anova_F = an$F[2], anova_df = c(an$Df[2]), anova_p = an[["Pr(>F)"]][2], anova_same_conclusion = an[["Pr(>F)"]][2] >= 0.05)
  write(toJSON(rc, auto_unbox = TRUE, pretty = TRUE, digits = NA), file.path(outdir, "robustness_R_c.json"))
  print(rc)
}
