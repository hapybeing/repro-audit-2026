# Agent B driver: fit one Table 1 model (AUDIT_MODEL = pool_xsec | pool_ldv) with the authors' code
# (analysis_pool_B.R = analysis_pool.R with pre-registered changes F1-F3), then extract numbers.
# Optional AUDIT_CHECK: "" (main), "Rb" (outlier edges set to NA), "Rc" (sigma2 = 1000).
P <- "/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/17_T1NXVQ/B"
S <- "/workspace/audit_runs/17_T1NXVQ/B"
setwd(file.path(S, "replication"))
model <- Sys.getenv("AUDIT_MODEL"); chk <- Sys.getenv("AUDIT_CHECK")
tag <- if (chk == "") model else paste0(chk, "_", model)
t0 <- Sys.time()
source("scripts/analysis/analysis_globals.R")
load_data(reload = F)
code <- readLines("scripts/analysis/pspm/analysis_pool_B.R")
if (chk == "Rb") {
  # Pre-registered R_b: on the static lattice, z of length.norm and elevmean.norm (sample SD, non-missing),
  # set to NA every edge with |z| > 3 on either variable.
  z <- function(x) (x - mean(x, na.rm = TRUE)) / sd(x, na.rm = TRUE)
  zl <- z(E(graph)$length.norm); ze <- z(E(graph)$elevmean.norm)
  fl <- !is.na(zl) & abs(zl) > 3; fe <- !is.na(ze) & abs(ze) > 3; fu <- fl | fe
  write.csv(data.frame(n_edges_total = ecount(graph), n_flag_length = sum(fl), n_flag_elev = sum(fe), n_flag_union = sum(fu)),
            file.path(P, "outputs", paste0("Rb_flagged_edges_", model, ".csv")), row.names = FALSE)
  E(graph)$length.norm[fu] <- NA; E(graph)$elevmean.norm[fu] <- NA
}
if (chk == "Rc") {
  i <- grep("sigma2 = 10,", code, fixed = TRUE); stopifnot(length(i) == 1)
  code[i] <- sub("sigma2 = 10,", "sigma2 = 1000,", code[i], fixed = TRUE)  # pre-registered R_c
}
Sys.setenv(AUDIT_OUT = file.path(S, "models", if (chk == "") "main" else chk)); dir.create(Sys.getenv("AUDIT_OUT"), showWarnings = FALSE, recursive = TRUE)
eval(parse(text = code), envir = globalenv())
m <- model.ls[[1]]
se <- tryCatch(miscTools::stdEr(m), error = function(e) tryCatch(sqrt(diag(vcov(m))), error = function(e2) rep(NA, length(m$estimate))))  # maxLik::stdEr gave NA in the two main fits (not exported there)
out <- data.frame(model = model, check = ifelse(chk == "", "main", chk), term = names(m$estimate), estimate = unname(m$estimate),
                  stdEr_maxLik = unname(se), sum_N = sum(m$N), sum_N_edges = sum(m$N_edges), sum_N_groups = sum(m$N_groups),
                  N_instances = m$N_instances, maxLik_code = m$code, maxLik_message = m$message)
write.csv(out, file.path(P, "outputs", paste0("targets_", tag, ".csv")), row.names = FALSE)
hwm <- grep("VmHWM", readLines("/proc/self/status"), value = TRUE)
cat("RESULT", tag, "minutes", round(as.numeric(difftime(Sys.time(), t0, units = "mins")), 2), hwm, "\n")
print(out[, 3:5]); print(sessionInfo())
