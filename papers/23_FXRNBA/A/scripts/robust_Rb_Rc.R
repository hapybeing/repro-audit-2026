# Pre-registered robustness checks R_b (|z|>3 outcome exclusion) and R_c (linear 2SLS on log(1+assault)).
suppressPackageStartupMessages({library(tidyverse); library(fixest); library(ivtools)})
OUT <- Sys.getenv("OUTDIR"); SCR <- Sys.getenv("SCRIPTDIR")
source(file.path(SCR, "helpers_from_authors.R"))
seattle_main <- readRDS(Sys.getenv("MAIN_RDS"))
W <- "holiday + awnd + tmax + tmin + prcp"; FE3 <- "station + year + month + dow"
# R_b
z <- (seattle_main$assault - mean(seattle_main$assault)) / sd(seattle_main$assault)
keep <- abs(z) <= 3
dropped <- seattle_main[!keep, ]
dat_b <- seattle_main[keep, ]
ivb <- run_ivglm(as.formula(paste("pm25_mean ~ z_smoke +", W, "+", FE3)),
                 as.formula(paste("assault ~ pm25_mean +", W, "+", FE3)), dat_b)
db <- fs_diag(as.formula(paste("pm25_mean ~ z_smoke +", W, "|", FE3)),
              as.formula(paste("pm25_mean ~", W, "|", FE3)), dat_b)
rb <- grab_by_name(ivb, "pm25_mean")$pm25_mean
by_st <- table(droplevels(dropped$station))
Rb <- data.frame(check = "R_b", estimate = rb$beta, se = rb$se, p = rb$p,
                 ci_low = rb$beta - 1.959964 * rb$se, ci_high = rb$beta + 1.959964 * rb$se,
                 first_stage_F = db$F, n = nrow(dat_b), n_dropped = sum(!keep),
                 dropped_by_station = paste(names(by_st), as.integer(by_st), sep = ":", collapse = "; "),
                 assault_mean = mean(seattle_main$assault), assault_sd = sd(seattle_main$assault),
                 min_dropped_assault = if (nrow(dropped)) min(dropped$assault) else NA)
# R_c
fc <- feols(as.formula(paste("log(1 + assault) ~", W, "|", FE3, "| pm25_mean ~ z_smoke")),
            data = seattle_main, cluster = ~date)
ct <- coeftable(fc)["fit_pm25_mean", ]
ivw <- fitstat(fc, "ivwald")
ivwF <- tryCatch(unname(ivw[[1]]$stat), error = function(e) NA)
Rc <- data.frame(check = "R_c", estimate = ct[1], se = ct[2], p = ct[4],
                 ci_low = ct[1] - 1.959964 * ct[2], ci_high = ct[1] + 1.959964 * ct[2],
                 first_stage_F = ivwF, n = nobs(fc), n_dropped = NA, dropped_by_station = "",
                 assault_mean = NA, assault_sd = NA, min_dropped_assault = NA)
res <- rbind(Rb, Rc); rownames(res) <- NULL
write.csv(res, file.path(OUT, "robustness_Rb_Rc.csv"), row.names = FALSE)
print(res, digits = 8); print(fitstat(fc, ~ ivwald + ivf + n))
cat("fixest", as.character(packageVersion("fixest")), "\n")
