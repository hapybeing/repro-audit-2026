# Wrapper for the authors' appendix script (agent B). Run from RUNDIR with R_LIBS_USER set.
# Environment fix only: browseURL made a no-op (PREREG.md section 2). No analysis line changed.
OUT <- Sys.getenv("OUTDIR")
browseURL <- function(...) invisible(NULL)
source("Framing Labor Action_Appendix A1.R", echo = TRUE, max.deparse.length = Inf)
saveRDS(list(m1 = m1, m4 = m4, m7 = m7, m10 = m10), file.path(OUT, "models_appendix.rds"))
saveRDS(dta, file.path(OUT, "dta_after_appendix_script.rds"))
for (f in c("table_1A_new.htm", "table_A2_new.htm", "table_A3_new.htm")) file.copy(f, file.path(OUT, f), overwrite = TRUE)
capture.output(sessionInfo(), file = file.path(OUT, "sessionInfo_appendix.txt"))
cat("APPENDIX_SCRIPT_DONE\n")
