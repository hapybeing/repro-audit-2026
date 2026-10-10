# Driver for Path A: runs the authors' replication.R unchanged via source(),
# then saves the htest objects and the rebuilt d for extraction.
# Usage (in a folder holding the authors' files): Rscript driver_pathA.R <outdir>
args <- commandArgs(trailingOnly = TRUE)
options(audit_outdir = args[1])  # kept in options(): replication.R starts with rm(list = ls())
cat("Sys.Date() seen by R:", format(Sys.Date()), "\n")
source("replication.R")
# replication.R leaves d, test1, test2, pubdef in the global env
saveRDS(list(test1 = test1, test2 = test2, d = d, sysdate = Sys.Date(),
             peacesciencer = as.character(packageVersion("peacesciencer"))),
        file.path(getOption("audit_outdir"), "pathA_fixed_objects.rds"))
cat("saved\n")
