# Agent B: reproduce the primary-run data preparation and model strings by sourcing
# lines 7-308 of the environment-patched authors' script (data load, recodes, model
# definitions), without fitting anything. Used by the robustness checks R_a, R_b, R_c.
suppressMessages({library(lavaan); library(tidyverse)})
patched <- Sys.getenv("PATCHED_SCRIPT", "/workspace/audit_runs/04_PSHE5L/B/work/patched_primary.R")
src <- readLines(patched)[7:308]
invisible(capture.output(suppressMessages(eval(parse(text = src), envir = globalenv()))))
stopifnot(nrow(rural) == 1203, exists("mediation_model_violence_ctrls2"))
fit_model <- function(dat, weighted = TRUE) {
  if (weighted) cfa(mediation_model_violence_ctrls2, data = dat, sampling.weights = "WTS", missing = "ML", estimator = "MLR")
  else cfa(mediation_model_violence_ctrls2, data = dat, missing = "ML", estimator = "MLR")
}
