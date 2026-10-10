# R_a (pre-registered): case bootstrap, 1000 replicates, set.seed(20261009) once before the loop.
# Each replicate: sample nrow(rural) rows with replacement, refit with identical options, store est.std
# of b1 (violence ~ polgriev) and indirect1_econgriev. Resumable: all 1000 index vectors are drawn
# up front from the single seed (identical to drawing them sequentially in one loop, since only
# sample() consumes the RNG stream), then replicates are fitted in chunks and appended to the CSV.
# Usage: Rscript R_a_bootstrap_B.R <outcsv> <max_reps_this_call>
source("/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/04_PSHE5L/B/scripts/prep_B.R")
args <- commandArgs(trailingOnly = TRUE); outcsv <- args[1]; maxreps <- as.integer(args[2])
B <- 1000; n <- nrow(rural)
set.seed(20261009)
idx <- lapply(seq_len(B), function(i) sample.int(n, n, replace = TRUE))
done <- if (file.exists(outcsv)) read.csv(outcsv)$rep else integer(0)
todo <- setdiff(seq_len(B), done)[seq_len(min(maxreps, length(setdiff(seq_len(B), done))))]
for (r in todo) {
  row <- tryCatch({
    fit <- suppressWarnings(fit_model(rural[idx[[r]], ]))
    conv <- lavInspect(fit, "converged")
    ss <- standardizedSolution(fit)
    b1 <- ss$est.std[ss$lhs == "violence" & ss$op == "~" & ss$rhs == "polgriev"]
    ind <- ss$est.std[ss$lhs == "indirect1_econgriev" & ss$op == ":="]
    data.frame(rep = r, converged = conv, b1_std = b1, indirect1_std = ind, error = "")
  }, error = function(e) data.frame(rep = r, converged = FALSE, b1_std = NA, indirect1_std = NA,
                                     error = gsub("[\r\n,]", " ", conditionMessage(e))))
  write.table(row, outcsv, sep = ",", append = file.exists(outcsv), col.names = !file.exists(outcsv), row.names = FALSE)
}
cat("done reps this call:", length(todo), "\n")
