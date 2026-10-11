# Install pinned versions (README) first, then PREREG fallbacks, into the per-run library. Ncpus=1, one at a time.
lib <- "/workspace/audit_runs/25_914AN0/A/rlib"; .libPaths(c(lib, .libPaths()))
options(repos=c(CRAN="https://cloud.r-project.org"), Ncpus=1)
logf <- "/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/25_914AN0/A/outputs/install_log.tsv"
rec <- function(...) { cat(paste(format(Sys.time(), tz="Asia/Kolkata"), ..., sep="\t"), "\n", file=logf, append=TRUE) }
args <- commandArgs(TRUE)
try_pkg <- function(pkg, pin, fallbacks){
  for (v in c(pin, fallbacks)) {
    ok <- tryCatch({
      if (v == "current") install.packages(pkg, lib=lib, dependencies=NA) else remotes::install_version(pkg, version=v, lib=lib, upgrade="never", dependencies=NA, Ncpus=1)
      ip <- installed.packages(lib.loc=lib)
      pkg %in% rownames(ip) && (v=="current" || ip[pkg,"Version"]==v)
    }, error=function(e){ rec(pkg, v, "ERROR", conditionMessage(e)); FALSE })
    if (isTRUE(ok)) { rec(pkg, v, "OK", installed.packages(lib.loc=lib)[pkg,"Version"]); return(invisible(TRUE)) }
    rec(pkg, v, "FAILED", "")
  }
  rec(pkg, "ALL", "FAILED", ""); invisible(FALSE)
}
plan <- list(
  lfe=list("3.0-0", c("current")),
  fixest=list("0.12.0", c("0.12.1","current")),
  Matching=list("4.10-14", c("current")),
  optimx=list("2023-10.21", c("current")),
  data.table=list("1.15.4", c("current")),
  robustlmm=list("3.3-1", c("current")),
  SUNGEO=list("1.3.0", c("1.4.0")),
  lme4=list("1.1-35.3", character(0))
)
for (p in args) try_pkg(p, plan[[p]][[1]], plan[[p]][[2]])
