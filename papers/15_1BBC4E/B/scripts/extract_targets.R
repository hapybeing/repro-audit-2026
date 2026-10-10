# Extract full-precision target values from the saved author outputs.
o <- "/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/15_1BBC4E/B/outputs"
ce <- as.data.frame(readRDS(file.path(o, "corr_ea.rds")))
rownames(ce) <- ce$term; m <- as.matrix(ce[, -1])
tally <- read.csv(file.path(o, "agreement_ead2_tally.csv"))
nshare <- as.integer(readLines(file.path(o, "share_nrow_ead.txt")))
ut <- m[upper.tri(m)]
wm <- which(m == max(ut, na.rm = TRUE), arr.ind = TRUE)[1, ]
res <- data.frame(
  id = c("T1","T2","T3","T4","T4_candidate2","T5","T6","median21","mean21","max21"),
  value = c(m["ARD","AoW"], m["Polity","CPR"], m["LIED","RoW"], nshare, sum(tally$n),
            tally$n[tally$coded_by == 7], sum(tally$n[tally$coded_by >= 1]),
            median(ut), mean(ut), max(ut)),
  source = c(rep("corr_ea.rds",3), "share_nrow_ead.txt", rep("agreement_ead2_tally.csv",3), rep("corr_ea.rds",3)),
  note = c("", "", "", "nrow(ead) Share_Common_Sample.R", "sum(n) of ead2 tally", "n at coded_by==7", "sum n coded_by>=1",
           "median of 21 distinct pairs", "mean of 21 distinct pairs",
           paste0("largest pair: ", rownames(m)[wm[1]], "-", colnames(m)[wm[2]])))
write.csv(res, file.path(o, "targets_extracted.csv"), row.names = FALSE)
# Secondary: full Table 3 comparison against printed values (copied from PREREG.md secondary context)
paper <- rbind(LIED=c(NA,0.539,0.383,0.202,0.607,0.626,0.315), RoW=c(0.539,NA,0.398,0.300,0.567,0.460,0.255),
  Polity=c(0.383,0.398,NA,0.310,0.524,0.484,0.177), FH=c(0.202,0.300,0.310,NA,0.434,0.253,0.232),
  ARD=c(0.607,0.567,0.524,0.434,NA,0.636,0.380), AoW=c(0.626,0.460,0.484,0.253,0.636,NA,0.427),
  CPR=c(0.315,0.255,0.177,0.232,0.380,0.427,NA))
colnames(paper) <- rownames(paper)
cmp <- data.frame(row = rownames(m)[row(m)[upper.tri(m)]], col = colnames(m)[col(m)[upper.tri(m)]],
  reproduced = ut, paper = paper[upper.tri(paper)])
cmp$match_3dp <- round(cmp$reproduced, 3) == cmp$paper
write.csv(cmp, file.path(o, "table3_full_comparison.csv"), row.names = FALSE)
cat("Table 3 cells matching to 3 dp:", sum(cmp$match_3dp), "of", nrow(cmp), "\n")
print(res)
