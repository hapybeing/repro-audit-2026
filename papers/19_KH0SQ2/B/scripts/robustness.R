# Pre-registered robustness checks R_a, R_b, R_c (PREREG section 3)
OUT <- "/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/19_KH0SQ2/B/outputs"
m <- readRDS(file.path(OUT, "S1_S10_models.rds"))
spec <- list(
  res4  = list(model="res4",  f=Support ~ Treatment,               term="TreatmentQuota",  target="T1"),
  res1  = list(model="res1",  f=Support ~ Treatment,               term="TreatmentQuota",  target="T2"),
  resg1 = list(model="resg1", f=Support ~ Treatment + resp_gender, term="resp_genderMale", target="T3"),
  resg2 = list(model="resg2", f=Support ~ Treatment + resp_gender, term="resp_genderMale", target="T4"))
# estimation samples = model.frame of the fitted models (includes (weights))
est <- lapply(spec, function(s) { mf <- model.frame(m[[s$model]]); d <- mf[, setdiff(names(mf), "(weights)"), drop=FALSE]; d$Weight <- mf[["(weights)"]]; d })
fit <- function(f, d, w=TRUE) if (w) lm(f, data=d, weights=Weight) else lm(f, data=d)
getc <- function(mod, term) { s <- summary(mod)$coefficients; if (term %in% rownames(s)) s[term, c(1,2,4)] else c(NA,NA,NA) }
# R_a bootstrap
set.seed(20261010)
ra <- list(); draws_all <- list()
for (k in c("res4","res1","resg1","resg2")) { s <- spec[[k]]; d <- est[[k]]; n <- nrow(d)
  orig <- coef(fit(s$f, d))[s$term]
  b <- replicate(2000, { i <- sample(n, n, replace=TRUE); coef(fit(s$f, d[i,]))[s$term] })
  nna <- sum(is.na(b)); bb <- b[!is.na(b)]
  q <- quantile(bb, c(.005,.025,.05,.95,.975,.995), names=FALSE)
  p <- min(1, 2*min(mean(bb<=0), mean(bb>=0)))
  ra[[k]] <- data.frame(check="R_a", model=k, target=s$target, term=s$term, n=n, n_dropped=NA, estimate=orig, se=sd(bb), p=p,
    ci90_lo=q[3], ci90_hi=q[4], ci95_lo=q[2], ci95_hi=q[5], ci99_lo=q[1], ci99_hi=q[6], n_na_draws=nna)
  draws_all[[k]] <- b }
write.csv(do.call(cbind, draws_all), file.path(OUT, "R_a_bootstrap_draws.csv"), row.names=FALSE)
# R_b weight outliers, and confirmation on Support
rb <- list(); sup <- list()
for (k in names(spec)) { s <- spec[[k]]; d <- est[[k]]
  z <- (d$Weight - mean(d$Weight))/sd(d$Weight); keep <- abs(z) <= 3
  zs <- (d$Support - mean(d$Support))/sd(d$Support)
  sup[[k]] <- data.frame(model=k, n_dropped_support_absz_gt3=sum(abs(zs)>3), zmin=min(zs), zmax=max(zs))
  cc <- getc(fit(s$f, d[keep,]), s$term)
  rb[[k]] <- data.frame(check="R_b", model=k, target=s$target, term=s$term, n=sum(keep), n_dropped=sum(!keep), estimate=cc[1], se=cc[2], p=cc[3],
    ci90_lo=NA, ci90_hi=NA, ci95_lo=NA, ci95_hi=NA, ci99_lo=NA, ci99_hi=NA, n_na_draws=NA) }
# R_c unweighted
rc <- list()
for (k in names(spec)) { s <- spec[[k]]; d <- est[[k]]; cc <- getc(fit(s$f, d, w=FALSE), s$term)
  rc[[k]] <- data.frame(check="R_c", model=k, target=s$target, term=s$term, n=nrow(d), n_dropped=0, estimate=cc[1], se=cc[2], p=cc[3],
    ci90_lo=NA, ci90_hi=NA, ci95_lo=NA, ci95_hi=NA, ci99_lo=NA, ci99_hi=NA, n_na_draws=NA) }
res <- rbind(do.call(rbind, ra), do.call(rbind, rb), do.call(rbind, rc))
write.csv(res, file.path(OUT, "robustness.csv"), row.names=FALSE)
write.csv(do.call(rbind, sup), file.path(OUT, "R_b_support_z_check.csv"), row.names=FALSE)
print(res, digits=5); print(do.call(rbind, sup))
