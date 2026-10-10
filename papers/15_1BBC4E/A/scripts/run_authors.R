# Runs one of the authors' three target scripts unchanged, from the R project folder, and saves the target objects.
# Usage: Rscript run_authors.R <which> ; which in comparison|share|agreement
args <- commandArgs(TRUE); which <- args[1]
ROOT <- "/workspace/audit_runs/15_1BBC4E/A/deposit/Replication Data/Replication Files. Electoral Autocracy. Hybrid Regimes. Multiparty Autocracy. Same. same but different"
OUT <- "/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/15_1BBC4E/A/outputs"
setwd(ROOT)
pdf(file.path(OUT, paste0("figures_", which, ".pdf")), width = 12, height = 8)
f <- switch(which, comparison = "Scripts/Comparing Indices/Comparison.R",
            share = "Scripts/Comparing Indices/Share_Common_Sample.R",
            agreement = "Scripts/Comparing Indices/Agreement across all.R")
source(f, echo = TRUE, max.deparse.length = Inf, print.eval = TRUE)
if (which == "comparison") { saveRDS(corr.ea, file.path(OUT, "corr_ea.rds")); write.csv(as.data.frame(corr.ea), file.path(OUT, "corr_ea_fullprec.csv"), row.names = FALSE) }
if (which == "share") { saveRDS(ead, file.path(OUT, "share_ead.rds")); writeLines(as.character(nrow(ead)), file.path(OUT, "share_nrow_ead.txt")) }
if (which == "agreement") { saveRDS(ead2, file.path(OUT, "agreement_ead2.rds")); write.csv(as.data.frame(ead2), file.path(OUT, "agreement_ead2_tally.csv"), row.names = FALSE) }
dev.off()
cat("corrr version:", as.character(packageVersion("corrr")), "\n")
