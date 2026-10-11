# Pre-registered R_a: date-cluster bootstrap of the Model 3 2SRI point estimate.
# Resumable: indices generated once (seed 20261011) and saved; results appended every 50 replicates.
suppressPackageStartupMessages({library(tidyverse); library(ivtools)})
OUT <- Sys.getenv("OUTDIR")
B_total <- as.integer(Sys.getenv("BOOT_B", "999"))
max_new <- as.integer(Sys.getenv("MAX_NEW", "100000"))
seattle_main <- readRDS(Sys.getenv("MAIN_RDS"))
W <- "holiday + awnd + tmax + tmin + prcp"; FE3 <- "station + year + month + dow"
f_fs <- as.formula(paste("pm25_mean ~ z_smoke +", W, "+", FE3))
f_ss <- as.formula(paste("assault ~ pm25_mean +", W, "+", FE3))
idx_file <- file.path(OUT, "Ra_boot_indices.rds"); res_file <- file.path(OUT, "Ra_boot.csv")
if (!file.exists(idx_file)) {
  set.seed(20261011)
  ud <- sort(unique(seattle_main$date))
  rows_by_date <- split(seq_len(nrow(seattle_main)), as.character(seattle_main$date))
  idx <- lapply(seq_len(999), function(b) {
    d <- sample(ud, length(ud), replace = TRUE)
    unlist(rows_by_date[as.character(d)], use.names = FALSE)
  })
  saveRDS(idx, idx_file)
}
idx <- readRDS(idx_file)
done <- if (file.exists(res_file)) read.csv(res_file) else data.frame()
todo <- setdiff(seq_len(B_total), done$rep)
todo <- head(todo, max_new)
fit1 <- function(ii) {
  d <- droplevels(seattle_main[ii, ])
  out <- tryCatch({
    fs <- glm(f_fs, data = d); ss <- glm(f_ss, family = poisson(link = "log"), data = d)
    fit <- ivtools::ivglm(estmethod = "ts", fitX.LZ = fs, fitY.LX = ss, data = d, ctrl = TRUE, vcov.fit = FALSE)
    c(est = unname(fit$est["pm25_mean"]), conv = as.numeric(fs$converged && ss$converged && fit$fitY.LX$converged), err = 0)
  }, error = function(e) c(est = NA, conv = 0, err = 1))
  out
}
buf <- list(); t0 <- Sys.time()
for (b in todo) {
  r <- fit1(idx[[b]])
  buf[[length(buf) + 1]] <- data.frame(rep = b, est = r[["est"]], converged = r[["conv"]], error = r[["err"]])
  if (length(buf) == 50 || b == tail(todo, 1)) {
    chunk <- do.call(rbind, buf)
    write.table(chunk, res_file, sep = ",", row.names = FALSE, col.names = !file.exists(res_file), append = file.exists(res_file))
    buf <- list(); cat("saved through rep", b, "elapsed", round(as.numeric(difftime(Sys.time(), t0, units = "secs")), 1), "s\n")
  }
}
cat("done; secs this session:", round(as.numeric(difftime(Sys.time(), t0, units = "secs")), 1), "\n")
