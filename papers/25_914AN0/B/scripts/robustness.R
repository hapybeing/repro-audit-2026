# Pre-registered robustness checks R_a (case bootstrap), R_b (|z|>3 outcome exclusion), R_c (SE clustered by DIV_ARMY).
# Usage: Rscript robustness.R rb_rc | ra   (ra is resumable; saves every 50 replicates)
args <- commandArgs(TRUE); mode <- args[1]
RUNDIR <- "/workspace/audit_runs/25_914AN0/B"; OUT <- "/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/25_914AN0/B/outputs"
suppressMessages({library(data.table); library(lfe); library(Formula)})
X_s <- readRDS(file.path(RUNDIR,"inter/s1a.rds"))$X_s
need <- c("NKVD_OO","AGE_1941","soldiers_dist","RUS_100","URBAN_PCT","POP_DENSITY","M_10km_ADM3","DIV_ARMY","TID","bxid","N_SOLDIERS")
outs <- c(MIA="MIA_100", KIA="KIA_100", WMED="WMED_100", POW="POW_100")
# authors' formula, run2_main.R line 64
model_fe <- Formula::Formula(y ~  log(NKVD_OO+1) + scale(AGE_1941) + scale(soldiers_dist) + scale(RUS_100) + scale(URBAN_PCT) + scale(POP_DENSITY) + scale(M_10km_ADM3) | DIV_ARMY + TID + bxid )
model_cl <- Formula::Formula(y ~  log(NKVD_OO+1) + scale(AGE_1941) + scale(soldiers_dist) + scale(RUS_100) + scale(URBAN_PCT) + scale(POP_DENSITY) + scale(M_10km_ADM3) | DIV_ARMY + TID + bxid | 0 | DIV_ARMY)
est_sample <- function(yv) { d <- X_s[complete.cases(X_s[, c(yv, need), with=FALSE])]; d <- copy(d); d[, y := get(yv)]; d }
fit <- function(d, f=model_fe) { m <- lfe::felm(f, data=d, weights=d$N_SOLDIERS, exactDOF=TRUE); ct <- summary(m)$coefficients; r <- grep("NKVD", rownames(ct)); list(m=m, b=ct[r,1], se=ct[r,2], p=ct[r,4], n=m$N) }
if (mode=="rb_rc") {
  res <- list()
  for (k in names(outs)) { yv <- outs[[k]]; d <- est_sample(yv)
    f0 <- fit(d)
    z <- (d$y - mean(d$y))/sd(d$y); dd <- d[abs(z) <= 3]
    f1 <- fit(dd)
    f2 <- fit(d, model_cl); ncl <- length(unique(d$DIV_ARMY))
    res[[k]] <- data.table(outcome=yv, n_est=nrow(d), b_orig=f0$b, se_orig=f0$se,
      rb_b=f1$b, rb_se=f1$se, rb_l=f1$b-1.96*f1$se, rb_u=f1$b+1.96*f1$se, rb_p=f1$p, rb_n=f1$n, rb_dropped=nrow(d)-nrow(dd),
      rc_b=f2$b, rc_se=f2$se, rc_l=f2$b-1.96*f2$se, rc_u=f2$b+1.96*f2$se, rc_p=f2$p, rc_nclust=ncl)
    print(res[[k]]) }
  fwrite(rbindlist(res), file.path(OUT,"rb_rc.csv"))
}
if (mode=="ra") {
  K <- as.integer(args[2]); outs_ra <- if (length(args)>2 && args[3]=="MIAonly") outs["MIA"] else outs
  d <- est_sample("MIA_100")
  # Bootstrap draws on the MIA estimation sample; check that all four outcomes share it
  for (k in names(outs)) cat(k, "est sample rows:", nrow(est_sample(outs[[k]])), "\n")
  n <- nrow(d); set.seed(20261011); idx <- lapply(1:K, function(k) sample(n, n, replace=TRUE))
  f <- file.path(OUT,"ra_boot.csv"); done <- if (file.exists(f)) fread(f) else data.table()
  todo <- setdiff(1:K, if (nrow(done)) done$k else integer(0)); buf <- list(); t0 <- Sys.time()
  for (k in todo) {
    db <- d[idx[[k]]]; row <- data.table(k=k)
    for (o in names(outs_ra)) { db[, y := get(outs_ra[[o]])]; r <- tryCatch(fit(db)$b, error=function(e) NA_real_); row[, (o) := r] }
    buf[[length(buf)+1]] <- row
    if (k %% 50 == 0 || k == max(todo) || (k <= 10 && k == 10)) { done <- rbind(done, rbindlist(buf), fill=TRUE); buf <- list(); fwrite(done, f); cat("saved through k =", k, format(Sys.time()-t0), "\n") }
  }
}
