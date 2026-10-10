# Extract target values at full precision from saved author objects.
OUT <- "/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/15_1BBC4E/A/outputs"
ce <- readRDS(file.path(OUT, "corr_ea.rds")); m <- as.matrix(as.data.frame(ce)[, -1]); rownames(m) <- ce$term
nr <- as.integer(readLines(file.path(OUT, "share_nrow_ead.txt")))
t2 <- readRDS(file.path(OUT, "agreement_ead2.rds"))
v <- m[upper.tri(m)]
mx <- which(m == max(v, na.rm = TRUE), arr.ind = TRUE)[1, ]
d <- data.frame(id = c("T1","T2","T3","T4","T5","T6","T4_cand2","median21","mean21","max21","n_pairs_below_0.73"),
  value = c(m["ARD","AoW"], m["Polity","CPR"], m["LIED","RoW"], nr, t2$n[t2$coded_by == 7], sum(t2$n[t2$coded_by >= 1]),
            sum(t2$n), median(v), mean(v), max(v), sum(v < 0.73)),
  source = c(rep("corr_ea.rds",3), "share_nrow_ead.txt", rep("agreement_ead2.rds",3), rep("corr_ea.rds",4)),
  note = c("","","","Share_Common_Sample.R nrow(ead)","coded_by==7","sum n coded_by>=1","sum n of ead2 tally (Figure 3 sample)",
           "median of 21 distinct correlations","mean of 21","largest pair", paste0("largest pair is ", rownames(m)[mx[1]], "-", colnames(m)[mx[2]])))
write.csv(d, file.path(OUT, "targets_extracted.csv"), row.names = FALSE)
print(format(d, digits = 15))
