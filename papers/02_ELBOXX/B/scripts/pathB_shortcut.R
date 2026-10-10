# Path B (shortcut): load the shipped analysis data and run the two cor.test lines
# exactly as in replication.R lines 13 and 22-23. outdir must be scratch (rds holds data).
args <- commandArgs(trailingOnly = TRUE)
datadir <- args[1]; outdir <- args[2]
e <- new.env(); load(file.path(datadir, "AJPS_analysis_data.RData"), envir = e)
cat("objects in RData:", ls(e, all.names = TRUE), "\n")
d <- e$d
str(d)
test1 <- cor.test(d$secret_alliances, d$disputes)
print(test1)
pubdef <- d[d$pub_def == 1,]
test2 <- cor.test(pubdef$secret_alliances, pubdef$disputes)
print(test2)
cat("range(year):", range(d$year), " nrow:", nrow(d), " n pub_def==1:", nrow(pubdef),
    " n pub_def>=1:", sum(d$pub_def >= 1), " max pub_def:", max(d$pub_def), "\n")
saveRDS(list(test1 = test1, test2 = test2, d = d), file.path(outdir, "pathB_objects.rds"))
