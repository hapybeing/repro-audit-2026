## Robustness R_b (outlier exclusion) and R_c (year as factor), as pre-registered in PREREG.md section 3.
## Also a sanity refit of the identical formula on the saved estimation sample (must equal T1 exactly).
.libPaths(c("/workspace/audit_runs/24_U9CKK6/A/rlib", .libPaths()))
suppressMessages(library(lme4))
S <- "/workspace/audit_runs/24_U9CKK6/A"
OUT <- "/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/24_U9CKK6/A/outputs"
ctl <- lmerControl(optimizer = "Nelder_Mead")
row_of <- function(check, target, term, m, extra = list()) {
  fe <- fixef(m); se <- sqrt(diag(as.matrix(vcov(m)))); names(se) <- names(fe)
  z <- fe[[term]] / se[[term]]
  data.frame(check = check, target = target, term = term, estimate = fe[[term]], se = se[[term]], t_value = z,
             p_naive = 2 * pnorm(-abs(z)), nobs = nobs(m),
             conv_messages = paste(m@optinfo$conv$lme4$messages, collapse = " | "),
             dropped_cols = paste(attr(getME(m, "X"), "col.dropped"), collapse = ";"), extra, stringsAsFactors = FALSE)
}
res <- list()
fileout <- file.path(OUT, "robustness_bc.csv")
save_res <- function() write.csv(do.call(rbind, res), fileout, row.names = FALSE)

## ---- Table 1 Model 2 (T1) ----
s <- readRDS(file.path(S, "models", "sample_cycle_AE_fit2.rds")); d <- s$data; f <- s$formula
m0 <- lmer(f, data = d, control = ctl)
res[["sanity_T1"]] <- row_of("sanity_refit_on_saved_sample", "T1", "challenge:days_to_nat", m0, list(rows_dropped = 0)); save_res(); rm(m0); invisible(gc())
y <- as.numeric(d$embed_dict_scale); z <- (y - mean(y)) / sd(y); keep <- abs(z) <= 3
mb <- lmer(f, data = d[keep, ], control = ctl)
res[["R_b_T1"]] <- row_of("R_b_outliers_absz_gt3", "T1", "challenge:days_to_nat", mb, list(rows_dropped = sum(!keep))); save_res(); rm(mb); invisible(gc())
fc <- update(f, . ~ . - year + as.factor(year))
cat("R_c formula:", deparse(fc, width.cutoff = 500L), "\n")
mc <- lmer(fc, data = d, control = ctl)
res[["R_c_T1"]] <- row_of("R_c_year_as_factor", "T1", "challenge:days_to_nat", mc, list(rows_dropped = 0)); save_res(); rm(mc, d); invisible(gc())

## ---- Table 2 secondary R_b (T5, T6) ----
for (spec in list(c("AUT_sal_model", "aut_dict_scale", "T5", "challenge:aut_sal"),
                  c("EU_sal_model", "int_dict_scale", "T6", "challenge:EU_sal"))) {
  s <- readRDS(file.path(S, "models", paste0("sample_", spec[1], ".rds"))); d <- s$data; f <- s$formula
  m0 <- lmer(f, data = d, control = ctl)
  res[[paste0("sanity_", spec[3])]] <- row_of("sanity_refit_on_saved_sample", spec[3], spec[4], m0, list(rows_dropped = 0)); save_res(); rm(m0); invisible(gc())
  y <- as.numeric(d[[spec[2]]]); z <- (y - mean(y)) / sd(y); keep <- abs(z) <= 3
  mb <- lmer(f, data = d[keep, ], control = ctl)
  res[[paste0("R_b_", spec[3])]] <- row_of("R_b_outliers_absz_gt3_secondary", spec[3], spec[4], mb, list(rows_dropped = sum(!keep))); save_res(); rm(mb, d); invisible(gc())
}
cat("done\n"); print(do.call(rbind, res)[, c("check", "target", "estimate", "se", "p_naive", "nobs", "rows_dropped")])
