# Reads saved Table 1 objects (rds from run_part.R or run_full.R) and writes a targets CSV.
# Usage: Rscript extract_targets.R <OUTDIR> <infile.rds> <outfile.csv>
args <- commandArgs(trailingOnly = TRUE)
OUT <- args[1]; infile <- args[2]; outfile <- args[3]
suppressPackageStartupMessages({library(ivtools); library(fixest)})
o <- readRDS(file.path(OUT, infile))
b3 <- o$r3$pm25_mean$beta; se3 <- o$r3$pm25_mean$se; p3 <- o$r3$pm25_mean$p
sc <- o$iv3_summary_coef
p3_summary <- if ("pm25_mean" %in% rownames(sc)) sc["pm25_mean", ncol(sc)] else NA
fs <- unname(o$fs3_coef["z_smoke"]); fs_se <- unname(o$fs3_se["z_smoke"]); fs_p <- unname(o$fs3_p["z_smoke"])
rows <- data.frame(
  quantity = c("T1_beta_model3", "T1_se_model3", "T2_p_model3_grab_by_name", "T2_p_model3_summary_ivglm",
               "T3_N_main", "T4_F_model3", "partialR2_model3",
               "T5_fs_coef_model3", "T5_fs_se_clustered", "T5_fs_p_clustered", "T5_fs_nobs",
               "T6_cand1_exp", "T6_cand2_linear", "T6_cand3_exp_rounded7",
               "M1_beta", "M1_se", "M1_p", "M1_F", "M1_pr2",
               "M2_beta", "M2_se", "M2_p", "M2_F", "M2_pr2",
               "M4_beta", "M4_se", "M4_p", "M4_F", "M4_pr2", "N_copoll"),
  value = c(b3, se3, p3, p3_summary, o$N_main, o$d3_F, o$d3_pr2,
            fs, fs_se, fs_p, o$fs3_nobs,
            100 * (exp(b3 * fs) - 1), 100 * b3 * fs, 100 * (exp(b3 * 7.0) - 1),
            o$r1$pm25_mean$beta, o$r1$pm25_mean$se, o$r1$pm25_mean$p, o$d1F, o$d1pr2,
            o$r2$pm25_mean$beta, o$r2$pm25_mean$se, o$r2$pm25_mean$p, o$d2F, o$d2pr2,
            o$r4$pm25_mean$beta, o$r4$pm25_mean$se, o$r4$pm25_mean$p, o$d4F, o$d4pr2, o$N_copoll))
rows$fixest_version <- o$fixest_version
write.csv(rows, file.path(OUT, outfile), row.names = FALSE)
print(rows, digits = 10)
