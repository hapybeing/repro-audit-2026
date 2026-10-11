# Wrapper for the authors' Appendix A1 script (run in RUNDIR). browseURL made a no-op (PREREG allowed fix).
browseURL <- function(...) invisible(NULL)
dir.create("outputs", showWarnings = FALSE)
source("Framing Labor Action_Appendix A1.R", echo = TRUE, max.deparse.length = Inf)
saveRDS(list(m1 = m1, m4 = m4, m7 = m7, m10 = m10), "outputs/models_appendix.rds")
saveRDS(dta, "outputs/dta_prepared.rds")
writeLines(capture.output(sessionInfo()), "outputs/sessionInfo_appendix.txt")
