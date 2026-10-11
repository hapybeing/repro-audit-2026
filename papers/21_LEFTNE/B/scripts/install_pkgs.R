# Installs missing CRAN packages into the per-run library, one at a time, Ncpus=1, with a memory guard.
lib <- "/workspace/audit_runs/21_LEFTNE/B/rlib"; .libPaths(c(lib, .libPaths()))
options(repos = c(CRAN = "https://cloud.r-project.org"), Ncpus = 1)
memavail <- function() as.numeric(sub("kB","",strsplit(grep("MemAvailable", readLines("/proc/meminfo"), value=TRUE), ":\\s+")[[1]][2]))/1024
need <- c("lavaan","aod","Rmisc","janitor","huxtable","jtools","margins","interplot","dotwhisker","qualtRics","mediation","hrbrthemes","effectsize")
for (p in need) {
  if (p != "lavaan" && requireNamespace(p, quietly = TRUE)) { cat("have", p, "\n"); next }
  if (p == "lavaan" && p %in% rownames(installed.packages(lib.loc = lib))) { cat("have lavaan in rlib\n"); next }
  while (memavail() < 1500) { cat("waiting for memory, MemAvailable MB =", round(memavail()), "\n"); Sys.sleep(30) }
  cat("installing", p, "at", format(Sys.time()), "\n")
  install.packages(p, lib = lib, dependencies = c("Depends","Imports","LinkingTo"))
}
cat("DONE\n")
