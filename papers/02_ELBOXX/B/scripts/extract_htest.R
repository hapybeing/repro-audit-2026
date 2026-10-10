# Extract r, CI, t, df, p, N from saved htest objects (Path A driver run, Path B shortcut)
# and from the text log of the plain as-is run. Writes outputs/targets_extracted.csv
args <- commandArgs(trailingOnly = TRUE)
B <- args[1]; S <- args[2]  # S = scratch folder holding the .rds objects (they contain data, kept out of REPO)
row <- function(route, test, h, n) data.frame(route = route, test = test,
  r = unname(h$estimate), ci_lo = h$conf.int[1], ci_hi = h$conf.int[2],
  t = unname(h$statistic), df = unname(h$parameter), p = h$p.value, n = n)
out <- list()
f <- file.path(S, "pathA_fixed_objects.rds")
if (file.exists(f)) { o <- readRDS(f)
  out[[length(out)+1]] <- row("A_fixed_date2025", "M1", o$test1, nrow(o$d))
  out[[length(out)+1]] <- row("A_fixed_date2025", "M2", o$test2, sum(o$d$pub_def == 1)) }
f <- file.path(S, "pathB_objects.rds")
if (file.exists(f)) { o <- readRDS(f)
  out[[length(out)+1]] <- row("B_shortcut", "M1", o$test1, nrow(o$d))
  out[[length(out)+1]] <- row("B_shortcut", "M2", o$test2, sum(o$d$pub_def == 1)) }
res <- do.call(rbind, out)
write.csv(res, file.path(B, "outputs", "targets_extracted.csv"), row.names = FALSE)
print(res, digits = 10)
