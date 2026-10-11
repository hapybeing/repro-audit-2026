# Installs pinned versions first, then PREREG fallbacks, into R_LIBS_USER. One package at a time, Ncpus=1.
lib <- Sys.getenv("R_LIBS_USER"); .libPaths(c(lib, .libPaths()))
options(repos=c(CRAN="https://cloud.r-project.org"), Ncpus=1)
logf <- file.path(Sys.getenv("PKGLOG")); lg <- function(...) cat(format(Sys.time()), ..., "\n", file=logf, append=TRUE)
plan <- list(
  list(p="lfe", pin="3.0-0", fb="current"),
  list(p="fixest", pin="0.12.0", fb=c("0.12.1","current")),
  list(p="lme4", pin="1.1-35.3", fb="debian"),
  list(p="robustlmm", pin="3.3-1", fb="current"),
  list(p="Matching", pin="4.10-14", fb="current"),
  list(p="optimx", pin="2023-10.21", fb="debian"),
  list(p="data.table", pin="1.15.4", fb="debian"),
  list(p="SUNGEO", pin="1.3.0", fb=c("1.4.0","current"))
)
only <- commandArgs(TRUE); if(length(only)) plan <- Filter(function(x) x$p %in% only, plan)
for (x in plan) {
  if (x$p %in% rownames(installed.packages(lib.loc=lib))) { lg(x$p, "already in rlib", as.character(packageVersion(x$p, lib.loc=lib))); next }
  ok <- FALSE
  for (v in c(x$pin, x$fb)) {
    if (v=="debian") { lg(x$p, "fallback: use Debian system version", as.character(packageVersion(x$p))); ok<-TRUE; break }
    lg(x$p, "trying", v)
    r <- try({ if (v=="current") install.packages(x$p, lib=lib, dependencies=c("Depends","Imports","LinkingTo")) else remotes::install_version(x$p, version=v, lib=lib, upgrade="never", dependencies=c("Depends","Imports","LinkingTo")) }, silent=TRUE)
    if (x$p %in% rownames(installed.packages(lib.loc=lib))) { lg(x$p, "INSTALLED", as.character(packageVersion(x$p, lib.loc=lib)), "(requested", v, ")"); ok<-TRUE; break }
    lg(x$p, "FAILED", v, if(inherits(r,"try-error")) as.character(r) else "")
  }
  if(!ok) lg(x$p, "NO VERSION INSTALLED")
}
