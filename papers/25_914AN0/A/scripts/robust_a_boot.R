# R_a case bootstrap, resumable. Usage: Rscript robust_a_boot.R <K> <kmax_this_call> <outcomes comma list>
source("/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/25_914AN0/A/scripts/robust_common.R")
a <- commandArgs(TRUE); K <- as.integer(a[1]); kmax <- as.integer(a[2]); use <- strsplit(a[3], ",")[[1]]
D1 <- est_sample(outs[["MIA"]]); n <- nrow(D1)
# Estimation sample with all four outcome columns (fix 2026-10-11: run 1 kept only MIA_100, so the other three refits errored; kept as outputs/ra_boot_failed_run1.csv)
D <- as.data.table(X_s)[, c(unname(outs), needed), with=FALSE]; D <- D[complete.cases(D)]; D[, y := MIA_100]
if (nrow(D) != n || !isTRUE(all.equal(D[, c("MIA_100", needed), with=FALSE], D1[, c("MIA_100", needed), with=FALSE]))) stop("estimation samples differ across outcomes")
set.seed(20261011); idx <- lapply(1:K, function(k) sample(n, n, replace=TRUE))
f <- file.path(PDIR,"outputs","ra_boot.csv")
done <- if (file.exists(f)) fread(f) else data.table(k=integer(), outcome=character(), b=numeric(), ok=logical(), secs=numeric())
buf <- list()
for (k in setdiff(1:min(K,kmax), unique(done$k))) {
  Db <- D[idx[[k]]]
  for (nm in use) {
    t0 <- Sys.time()
    b <- tryCatch({ Db[, y := get(outs[[nm]])]; nkvd_row(fit_fe(Db))[1] }, error=function(e) NA_real_)
    buf[[length(buf)+1]] <- data.table(k=k, outcome=nm, b=b, ok=!is.na(b), secs=as.numeric(difftime(Sys.time(),t0,units="secs")))
  }
  if (k %% 10 == 0 || k == min(K,kmax)) { done <- rbind(done, rbindlist(buf)); buf <- list(); fwrite(done, f); message("saved through k=", k) }
}
if (length(buf)) { done <- rbind(done, rbindlist(buf)); fwrite(done, f) }
