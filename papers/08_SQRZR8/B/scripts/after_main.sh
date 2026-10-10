#!/bin/bash
# Waits for main run to finish, then runs extraction and robustness (one R process at a time).
while ! grep -q "^exit" /workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/08_SQRZR8/B/outputs/main_rep_stdout.txt; do sleep 10; done
export R_LIBS_USER=/workspace/audit_runs/08_SQRZR8/B/rlib
Rscript /workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/08_SQRZR8/B/scripts/extract_targets.R > /workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/08_SQRZR8/B/outputs/extract_targets_log.txt 2>&1
Rscript /workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/08_SQRZR8/B/scripts/robustness.R > /workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/08_SQRZR8/B/outputs/robustness_log.txt 2>&1
echo AFTER_DONE >> /workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/08_SQRZR8/B/outputs/robustness_log.txt
