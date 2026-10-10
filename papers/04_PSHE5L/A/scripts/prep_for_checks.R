# Sources the environment-patched primary script (as deposited data prep, Q15 code 8 kept) and saves
# the prepared data frame and the structural model syntax for the robustness checks.
.libPaths(c("/workspace/audit_runs/04_PSHE5L/A/rlib", .libPaths()))
source("/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/04_PSHE5L/A/scripts/patched_primary.R")
saveRDS(list(rural = as.data.frame(rural), model = mediation_model_violence_ctrls2),
        "/workspace/audit_runs/04_PSHE5L/A/checks_input.rds")
cat("saved; nrow", nrow(rural), "\n")
