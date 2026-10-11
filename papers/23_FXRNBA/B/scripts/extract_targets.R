# Reads saved Table 1 objects and writes targets_extracted.csv (all numbers from the authors' objects).
args <- commandArgs(TRUE)
OUT <- "/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/23_FXRNBA/B/outputs"
inf <- if (length(args) >= 1) args[1] else "table1_objects.rds"
outf <- if (length(args) >= 2) args[2] else "targets_extracted.csv"
o <- readRDS(file.path(OUT, inf))
b3 <- o$r3$pm25_mean$beta; se3 <- o$r3$pm25_mean$se; p3 <- o$r3$pm25_mean$p
p3_summary <- NA_real_
sc <- o$iv3_summary_coef
if (is.matrix(sc) && "pm25_mean" %in% rownames(sc)) p3_summary <- sc["pm25_mean", ncol(sc)]
fs <- unname(o$fs3_coef["z_smoke"]); fs_se <- sqrt(o$fs3_vcov["z_smoke", "z_smoke"])
fs_p <- 2 * pnorm(-abs(fs / fs_se))
fs_glm <- unname(o$fs3_glm_coef["z_smoke"])
rows <- list(
  c("T1_beta_model3", b3), c("T1_se_model3", se3),
  c("T2_p_model3_grab_by_name", p3), c("T2_p_model3_summary_ivglm", p3_summary),
  c("T3_N_main", o$N_main), c("T4_F_model3", o$d3_F), c("partialR2_model3", o$d3_pr2),
  c("T5_fs_coef_model3_feols", fs), c("T5_fs_se_model3_clustered", fs_se), c("T5_fs_p_model3_normal", fs_p),
  c("T5_fs_coef_model3_glm_in_ivglm", fs_glm), c("fs3_nobs", o$fs3_nobs),
  c("T6_cand1_pct_exp_unrounded", 100 * (exp(b3 * fs) - 1)),
  c("T6_cand2_pct_linear", 100 * b3 * fs),
  c("T6_cand3_pct_exp_rounded7", 100 * (exp(b3 * 7.0) - 1)),
  c("M1_beta", o$r1$pm25_mean$beta), c("M1_se", o$r1$pm25_mean$se), c("M1_p", o$r1$pm25_mean$p), c("M1_F", o$d1F), c("M1_pr2", o$d1pr2),
  c("M2_beta", o$r2$pm25_mean$beta), c("M2_se", o$r2$pm25_mean$se), c("M2_p", o$r2$pm25_mean$p), c("M2_F", o$d2F), c("M2_pr2", o$d2pr2),
  c("M4_beta", o$r4$pm25_mean$beta), c("M4_se", o$r4$pm25_mean$se), c("M4_p", o$r4$pm25_mean$p), c("M4_F", o$d4F), c("M4_pr2", o$d4pr2),
  c("N_copoll", o$N_copoll))
df <- data.frame(quantity = sapply(rows, `[`, 1), value = as.numeric(sapply(rows, `[`, 2)))
df$fixest_version <- o$fixest_version; df$ivtools_version <- o$ivtools_version
write.csv(df, file.path(OUT, outf), row.names = FALSE)
print(format(df, digits = 10))
