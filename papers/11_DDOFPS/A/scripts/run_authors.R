# Runs the deposited script unchanged, top to bottom, in RUNDIR (argument 1).
# Environment only: the script file is Latin-1, so it is sourced with encoding = "latin1"
# (keeps the byte 0xB4 on line 177 as U+00B4 before "45"). Data files were copied into RUNDIR
# under the names the script reads (see diffs/README.md).
args <- commandArgs(trailingOnly = TRUE)
rundir <- normalizePath(args[1])
setwd(rundir)
dir.create(file.path(rundir, "plots"), showWarnings = FALSE)
# Graphics device: cairo PNG (one file per plot). The default pdf() device stops with
# "invalid font type" on theme_ipsum_tw() (Titillium Web font not installed); cairo
# substitutes a font instead. Cosmetic only (Figura 1 has no target).
png(file.path(rundir, "plots", "Rplot%03d.png"), type = "cairo", width = 900, height = 650)
source("orig_script.R", encoding = "latin1", echo = TRUE, max.deparse.length = Inf,
       spaced = TRUE)
w <- warnings()
cat("\nWARNINGS_SUMMARY\n"); print(summary(w))
dev.off()
save.image(file.path(rundir, "session_after_script.RData"))
cat("\nSCRIPT_COMPLETED_OK\n")
