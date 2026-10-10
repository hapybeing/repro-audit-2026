# FC1-FC3 from the authors' cj() result tables saved by run_authors.R. Usage: Rscript figure_claims.R RUNDIR OUTDIR
suppressMessages(library(jsonlite))
args <- commandArgs(trailingOnly = TRUE); rundir <- args[1]; outdir <- args[2]
d <- readRDS(file.path(rundir, "pooled_df2.rds"))
feats <- c("Gender","Age","Citizenship","Composition","Unemployment","Supportive","Since","Education")
lvmap <- do.call(rbind, lapply(feats, function(f) data.frame(var = f, level = levels(d[[f]]))))
stopifnot(!any(duplicated(lvmap$level)))
mm <- read.csv(file.path(outdir, "cj_marginal_means_grouped_sector.csv"), stringsAsFactors = FALSE)
df <- read.csv(file.path(outdir, "cj_marginal_means_grouped_sector_mmdiff.csv"), stringsAsFactors = FALSE)
mm$var <- lvmap$var[match(mm$level, lvmap$level)]; df$var <- lvmap$var[match(df$level, lvmap$level)]
res <- list()
res$fig1_rows <- nrow(mm); res$fig1_sectors <- unique(mm$sector)
res$fig1_duplicate_level_rows <- sum(duplicated(mm[, c("sector", "level")]))
res$fig2_rows <- nrow(df); res$fig2_contrast <- unique(df$sector)
excl0 <- (df$lower > 0) | (df$upper < 0)
fc1v <- c("Gender","Age","Citizenship","Composition","Unemployment","Supportive")
res$FC1 <- list(count_CI_excludes_0 = sum(excl0 & df$var %in% fc1v), n_levels = sum(df$var %in% fc1v),
  levels_excluding_0 = df$level[excl0 & df$var %in% fc1v], paper_claim = 0,
  same_conclusion = sum(excl0 & df$var %in% fc1v) == 0,
  Since_count = sum(excl0 & df$var == "Since"), Since_levels = df$level[excl0 & df$var == "Since"],
  Education_count = sum(excl0 & df$var == "Education"), Education_levels = df$level[excl0 & df$var == "Education"],
  ci_outside_plot_limits_pm0.1 = df$level[df$lower < -0.1 | df$upper > 0.1])
rng <- aggregate(estimate ~ sector + var, data = mm, FUN = function(x) max(x) - min(x))
names(rng)[3] <- "range"
fc2 <- lapply(split(rng, rng$sector), function(z) { z <- z[order(-z$range), ]; list(ranking = z$var, ranges = z$range, largest = z$var[1]) })
res$FC2 <- list(by_sector = fc2, same_conclusion = all(sapply(fc2, function(z) z$largest == "Composition")))
fc3 <- mm[mm$level %in% c("Syria", "Germany"), c("sector", "level", "estimate", "std.error", "lower", "upper")]
strict <- all(fc3$estimate[fc3$level == "Syria"] < 0.5 & fc3$upper[fc3$level == "Syria"] < 0.5) &&
          all(fc3$estimate[fc3$level == "Germany"] > 0.5 & fc3$lower[fc3$level == "Germany"] > 0.5) && nrow(fc3) == 4
lenient <- all(fc3$estimate[fc3$level == "Syria"] < 0.5) && all(fc3$estimate[fc3$level == "Germany"] > 0.5) && nrow(fc3) == 4
res$FC3 <- list(values = fc3, same_conclusion_strict = strict, same_conclusion_lenient = lenient)
write(toJSON(res, auto_unbox = TRUE, pretty = TRUE, digits = NA), file.path(outdir, "figure_claims.json"))
write.csv(df[, c("sector","var","level","estimate","std.error","lower","upper")], file.path(outdir, "fc1_mmdiff_table.csv"), row.names = FALSE)
cat(toJSON(res, auto_unbox = TRUE, pretty = TRUE, digits = 6))
