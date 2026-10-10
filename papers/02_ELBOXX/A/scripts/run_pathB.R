# Path B (shortcut): load the shipped AJPS_analysis_data.RData and run the two cor.test lines
# exactly as in replication.R lines 15 and 24-25. Usage: Rscript run_pathB.R <RData> <outdir>
args <- commandArgs(trailingOnly = TRUE)
load(args[1])
test1 <- cor.test(d$secret_alliances, d$disputes)
pubdef <- d[d$pub_def == 1,]
test2 <- cor.test(pubdef$secret_alliances, pubdef$disputes)
row <- function(name, tt, n) data.frame(route = "pathB_shipped_RData", test = name, n = n,
  r = unname(tt$estimate), ci_low = tt$conf.int[1], ci_high = tt$conf.int[2],
  t = unname(tt$statistic), df = unname(tt$parameter), p = tt$p.value)
res <- rbind(row("M1_test1_all", test1, sum(complete.cases(d$secret_alliances, d$disputes))),
             row("M2_test2_pubdef1", test2, sum(complete.cases(pubdef$secret_alliances, pubdef$disputes))))
write.csv(res, file.path(args[2], "targets_pathB.csv"), row.names = FALSE)
saveRDS(d, file.path(args[2], "d_shipped.rds"))
options(digits = 15); print(res); print(dim(d)); print(range(d$year))
