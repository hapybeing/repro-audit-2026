# Agent A, 17_T1NXVQ. Driver: one Table 1 model per R process (PREREG section 2, F1-F3, step 6; section 3 R_a, R_b, R_c).
# Usage: Rscript run_model.R <MODEL_NAME: pool_xsec|pool_ldv> <VARIANT: main|rb|rc|ra> <SEEDS: auto|K|none>
#   main + auto : fit, then step 6 with seed 1 timed, K = min(10, floor(25/t)) (at least 3, else stop), seeds 1..K
#   main + K    : fit, then step 6 with seeds 1..K (K read from outputs/boot_K.json)
#   ra   + K    : fit (identical to main), then R_a draws with seeds 1001..1000+K
#   rb / rc + none : refit with the pre-registered change, no bootstrap
args <- commandArgs(trailingOnly = TRUE)
MODEL_NAME <- args[1]; VARIANT <- args[2]; SEEDS <- args[3]
A_DIR <- "/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/17_T1NXVQ/A"
OUT_DIR <- file.path(A_DIR, "outputs")
setwd("/workspace/audit_runs/17_T1NXVQ/A/replication")
stopifnot(!file.exists("data/models/pool_model.ls.rds"), !file.exists("data/models/pool_se.ls.rds"))
t_start <- Sys.time()
cat("START", MODEL_NAME, VARIANT, SEEDS, format(t_start, tz = "UTC"), "UTC\n")

source("scripts/analysis/analysis_globals.R")   # with env fixes E1, E2 (see diffs/)
load_data(reload = F)

if (VARIANT == "rb") {
  # R_b: |z| > 3 on length.norm or elevmean.norm (static lattice graph, z over non-missing edges, sample SD) -> NA
  z_of <- function(v) (v - mean(v, na.rm = TRUE)) / sd(v, na.rm = TRUE)
  zl <- z_of(E(graph)$length.norm); ze <- z_of(E(graph)$elevmean.norm)
  fl <- !is.na(zl) & abs(zl) > 3; fe <- !is.na(ze) & abs(ze) > 3; fu <- fl | fe
  cat("R_b flagged edges: length.norm", sum(fl), "elevmean.norm", sum(fe), "union", sum(fu), "of", length(fu), "\n")
  write.csv(data.frame(n_edges_graph = length(fu), flag_length = sum(fl), flag_elev = sum(fe), flag_union = sum(fu)),
            file.path(OUT_DIR, paste0("rb_flags_", MODEL_NAME, ".csv")), row.names = FALSE)
  E(graph)$length.norm[fu] <- NA
  E(graph)$elevmean.norm[fu] <- NA
}

code <- readLines(file.path(A_DIR, "scripts/analysis_pool_A.R"))
if (VARIANT == "rc") {
  i <- grep("sigma2 = 10, ", code, fixed = TRUE); stopifnot(length(i) == 1)
  code[i] <- sub("sigma2 = 10, ", "sigma2 = 1000, ", code[i], fixed = TRUE)   # R_c: weaker penalty (diffs/R_c_sigma2.diff)
  cat("R_c line now:", code[i], "\n")
}
if (VARIANT != "main") {
  # robustness / R_a fits must not overwrite the main fitted model files
  i <- grep("saveRDS(model.ls, file = file.path(OUT_DIR", code, fixed = TRUE); stopifnot(length(i) == 1)
  code[i] <- sub('paste0("pool_", MODEL_NAME, "_model.rds")', 'paste0("pool_", MODEL_NAME, "_", VARIANT, "_model.rds")', code[i], fixed = TRUE)
}
eval(parse(text = code), envir = globalenv())
t_fit <- Sys.time()
fit_min <- as.numeric(difftime(t_fit, t_start, units = "mins"))
cat("FIT DONE minutes:", round(fit_min, 2), "\n")
m <- model.ls[[1]]
est <- data.frame(model = MODEL_NAME, variant = VARIANT, term = names(m$estimate), estimate = unname(m$estimate),
                  maxlik_se = unname(miscTools::stdEr(m)))
write.csv(est, file.path(OUT_DIR, paste0("fit_", MODEL_NAME, "_", VARIANT, ".csv")), row.names = FALSE)
cnt <- data.frame(model = MODEL_NAME, variant = VARIANT, N_sum = sum(m$N), N_edges_sum = sum(m$N_edges),
                  N_groups_sum = sum(m$N_groups), N_instances = m$N_instances,
                  N_by_period = paste(m$N, collapse = ";"), N_edges_by_period = paste(m$N_edges, collapse = ";"),
                  fit_minutes = fit_min)
write.csv(cnt, file.path(OUT_DIR, paste0("counts_", MODEL_NAME, "_", VARIANT, ".csv")), row.names = FALSE)

# Step 6 / R_a: body of the authors' foreach worker, run serially
boot_one <- function(learn_obj, i) {
  set.seed(i)
  reticulate::py_set_seed(i, disable_hash_randomization = TRUE)
  bse <- learn_obj$bootstrap_composite_log_likelihood(n_boot_iter = 1, burnin = burnin,
                                                      ci_level = 0.95, return_sims = T,
                                                      report_every = 5, cache_samples = T)
  bse$beta_boot
}
learn_obj <- model.ls[[1]]$learn_obj
csv <- file.path(OUT_DIR, paste0(ifelse(VARIANT == "ra", "boot_ra_seeds_", "boot_authorseeds_"), MODEL_NAME, ".csv"))
run_draw <- function(i) {
  t0 <- Sys.time()
  b <- tryCatch(boot_one(learn_obj, i), error = function(e) { cat("DRAW FAILED seed", i, conditionMessage(e), "\n"); NULL })
  secs <- as.numeric(difftime(Sys.time(), t0, units = "secs"))
  if (is.null(b)) {
    row <- data.frame(seed = i, seconds = secs, failed = TRUE)
  } else {
    row <- data.frame(seed = i, seconds = secs, failed = FALSE, as.data.frame(as.list(setNames(as.numeric(b[1, ]), colnames(b))), check.names = FALSE), check.names = FALSE)
  }
  write.table(row, csv, sep = ",", row.names = FALSE, col.names = !file.exists(csv), append = file.exists(csv))
  cat("DRAW seed", i, "seconds", round(secs, 1), "failed", is.null(b), "\n"); flush.console()
  secs / 60
}
cap_min <- 35
if (SEEDS != "none") {
  if (file.exists(csv)) file.remove(csv)
  if (SEEDS == "auto") {
    t1 <- run_draw(1)
    Kraw <- floor(25 / t1)
    K <- if (Kraw < 3) NA else min(10, Kraw)
    jsonlite::write_json(list(first_draw_minutes = t1, K_raw = Kraw, K = K, rule = "K = min(10, floor(25/t)), at least 3; else step 6 not run"),
                         file.path(OUT_DIR, "boot_K.json"), auto_unbox = TRUE, digits = NA)
    cat("K =", K, "(first draw", round(t1, 2), "min)\n")
    used <- t1
    if (!is.na(K) && K >= 2) for (i in 2:K) { if (used > cap_min) { cat("35-minute cap reached\n"); break }; used <- used + run_draw(i) }
  } else {
    K <- jsonlite::read_json(file.path(OUT_DIR, "boot_K.json"))$K
    seeds <- if (VARIANT == "ra") 1000 + (1:K) else 1:K
    used <- 0
    for (i in seeds) { if (used > cap_min) { cat("35-minute cap reached\n"); break }; used <- used + run_draw(i) }
  }
}
st <- readLines("/proc/self/status"); cat(grep("VmHWM|VmRSS", st, value = TRUE), sep = "\n")
cat("END", format(Sys.time(), tz = "UTC"), "UTC\n")
