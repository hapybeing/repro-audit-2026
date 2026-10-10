# Path A wrapper (Agent A). Runs the authors' replication.R UNCHANGED in the current
# working directory (a scratch copy of the Dataverse files with the original CSVs),
# then saves the analysis data frame and the two htest objects so numbers can be
# extracted by script. Usage: Rscript run_pathA.R <outdir> <label>
args <- commandArgs(trailingOnly = TRUE)
outdir <- args[1]; label <- args[2]
dir.create(outdir, showWarnings = FALSE, recursive = TRUE)
source("replication.R")   # authors' file; it rm()s everything, so re-read args after
args <- commandArgs(trailingOnly = TRUE); outdir <- args[1]; label <- args[2]
saveRDS(d, file.path(outdir, paste0("d_", label, ".rds")))
row <- function(name, tt, n) data.frame(route = label, test = name, n = n,
  r = unname(tt$estimate), ci_low = tt$conf.int[1], ci_high = tt$conf.int[2],
  t = unname(tt$statistic), df = unname(tt$parameter), p = tt$p.value)
res <- rbind(row("M1_test1_all", test1, sum(complete.cases(d$secret_alliances, d$disputes))),
             row("M2_test2_pubdef1", test2, sum(complete.cases(pubdef$secret_alliances, pubdef$disputes))))
write.csv(res, file.path(outdir, paste0("targets_", label, ".csv")), row.names = FALSE)
write.csv(data.frame(route = label, sys_date = as.character(Sys.Date()), nrow_d = nrow(d),
  min_year = min(d$year), max_year = max(d$year)), file.path(outdir, paste0("meta_", label, ".csv")), row.names = FALSE)
options(digits = 15); print(res)
