# Code-observation check (not pre-registered): Table A4 typed constants (Appendix A1.R lines 234, 264)
# against means computed from the data frame the authors' appendix script built. Agent B.
OUT <- Sys.getenv("OUTDIR")
dta <- readRDS(file.path(OUT, "dta_after_appendix_script.rds"))
u <- as.numeric(as.character(dta$unions)); s <- as.numeric(dta$Support_teachers)
lv <- c("Control", "Strike", "Pro_strike", "Anti_strike", "Double_frame")
typed_u <- c(3.25, 3.08, 3.41, 2.96, 3.17); typed_s <- c(4.36, 4.18, 4.91, 4.40, 4.43)
mu <- sapply(lv, function(l) mean(u[dta$Treatment == l], na.rm = TRUE)); ms <- sapply(lv, function(l) mean(s[dta$Treatment == l], na.rm = TRUE))
r <- data.frame(treatment = lv, unions_mean_computed = mu, unions_typed = typed_u, unions_match_2dp = round(mu, 2) == typed_u,
                support_mean_computed = ms, support_typed = typed_s, support_match_2dp = round(ms, 2) == typed_s, row.names = NULL)
write.csv(r, file.path(OUT, "check_tableA4_means.csv"), row.names = FALSE)
ov <- data.frame(var = c("unions", "Support_teachers"), n = c(sum(!is.na(u)), sum(!is.na(s))), mean = c(mean(u, na.rm = TRUE), mean(s, na.rm = TRUE)),
                 sd = c(sd(u, na.rm = TRUE), sd(s, na.rm = TRUE)), n_rows_data = nrow(dta))
write.csv(ov, file.path(OUT, "check_overall_means.csv"), row.names = FALSE)
# What the appendix script's own line 224-226 gives (mean of an ordered factor)
cat("appendix line 226 equivalent, mean(ordered factor):", suppressWarnings(mean(dta$unions, na.rm = TRUE)), "\n")
print(r, digits = 5); print(ov, digits = 5)
