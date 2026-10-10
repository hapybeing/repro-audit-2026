# Pre-registered robustness checks R_a, R_b, R_c (PREREG.md section 3) for 15_1BBC4E, agent B.
suppressMessages(library(jsonlite))
o <- "/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/15_1BBC4E/B/outputs"
ead <- readRDS("/workspace/audit_runs/15_1BBC4E/B/work/Data/Regimedata/Measures_merged.rds")
vars <- c(LIED="RegType_lied_EA", RoW="RegType_RoW_EA", Polity="Politytype_Anocracy", FH="status_fh_PF",
          ARD="HTW_RegType_MP_Autocracy", AoW="RegType_magaloni_EA", CPR="AnckarRegtype_MP_Autocracy")
X <- as.data.frame(ead)[, vars]; names(X) <- names(vars)
X[] <- lapply(X, as.numeric)
cc <- as.character(ead$Final_Code)
cat("rows", nrow(X), "countries", length(unique(cc)), "NA Final_Code", sum(is.na(cc)), "\n")
cat("value sets:\n"); print(lapply(X, function(v) sort(unique(v))))
cm <- function(d) suppressWarnings(cor(d, use = "pairwise.complete.obs"))
summ <- function(m) { ut <- m[upper.tri(m)]; w <- which(m == max(ut, na.rm=TRUE), arr.ind=TRUE)[1,]
  list(T1 = m["ARD","AoW"], T2 = m["Polity","CPR"], T3 = m["LIED","RoW"], max21 = max(ut, na.rm=TRUE),
       max_pair = paste0(rownames(m)[w[1]], "-", colnames(m)[w[2]]), median21 = median(ut, na.rm=TRUE)) }
full <- summ(cm(X)); t1 <- full$T1
# R_a country-cluster bootstrap
set.seed(20261010)
idx_by <- split(seq_len(nrow(X)), cc)
ctry <- names(idx_by); B <- 1000
boot <- matrix(NA_real_, B, 4, dimnames=list(NULL, c("T1","T2","T3","max21")))
for (b in 1:B) {
  dr <- sample(ctry, length(ctry), replace = TRUE)
  s <- summ(cm(X[unlist(idx_by[dr], use.names=FALSE), ]))
  boot[b,] <- c(s$T1, s$T2, s$T3, s$max21)
}
write.csv(boot, file.path(o, "R_a_bootstrap_draws.csv"), row.names = FALSE)
bt <- boot[, "T1"]; ok <- !is.na(bt)
ci <- quantile(bt[ok], c(.025,.975), names=FALSE)
R_a <- list(estimate = t1, ci_low = ci[1], ci_high = ci[2], boot_se = sd(bt[ok]), n_resamples = B,
  n_undefined = sum(!ok), share_ge_073 = mean(bt[ok] >= 0.73),
  p_value = min(2*mean(bt[ok] <= 0), 1),
  secondary_ci = lapply(c(T2="T2",T3="T3",max21="max21"), function(k) quantile(boot[,k], c(.025,.975), na.rm=TRUE, names=FALSE)),
  seed = 20261010, n_countries = length(ctry))
# R_b leave-one-country-out influence on T1, drop top 1% (ceiling, at least 1)
pair_ok <- !is.na(X$ARD) & !is.na(X$AoW)
elig <- sort(unique(cc[pair_ok]))
loo <- sapply(elig, function(k) { keep <- cc != k; suppressWarnings(cor(X$ARD[keep], X$AoW[keep], use="pairwise.complete.obs")) })
infl <- data.frame(country = elig, T1_without = loo, abs_change = abs(loo - t1))
infl <- infl[order(-infl$abs_change), ]
write.csv(infl, file.path(o, "R_b_loco_influence.csv"), row.names = FALSE)
k <- max(1, ceiling(0.01 * length(elig)))
drop <- infl$country[1:k]
Xb <- X[!(cc %in% drop), ]
sb <- summ(cm(Xb)); ctb <- cor.test(Xb$ARD, Xb$AoW)
R_b <- list(n_eligible_countries = length(elig), n_dropped = k, dropped = drop,
  dropped_country_years = sum(cc %in% drop), estimate = unname(ctb$estimate), ci_low = ctb$conf.int[1], ci_high = ctb$conf.int[2],
  p_value = ctb$p.value, n_pairs = sum(!is.na(Xb$ARD) & !is.na(Xb$AoW)), secondary = sb)
# R_c listwise common sample
Xc <- na.omit(X); sc <- summ(cor(Xc)); ctc <- cor.test(Xc$ARD, Xc$AoW)
write.csv(as.data.frame(cor(Xc)), file.path(o, "R_c_listwise_matrix.csv"))
R_c <- list(N = nrow(Xc), estimate = unname(ctc$estimate), ci_low = ctc$conf.int[1], ci_high = ctc$conf.int[2],
  p_value = ctc$p.value, secondary = sc)
out <- list(full_sample = full, R_a = R_a, R_b = R_b, R_c = R_c, R_version = R.version.string)
write_json(out, file.path(o, "robustness.json"), auto_unbox = TRUE, digits = NA, pretty = TRUE)
cat(toJSON(out, auto_unbox=TRUE, digits=6, pretty=TRUE), "\n")
