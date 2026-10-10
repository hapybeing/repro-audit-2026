#!/bin/bash
# Path A with date fix: authors' replication.R unchanged, sourced by driver_pathA.R (which only saves the objects afterwards).
# Run inside a folder holding replication.R, analysis_data_creation.R and the three original CSVs.
# Environment fix: peacesciencer::create_stateyears() (mry = TRUE) ends the state-year frame at
# (current calendar year - 1). The process clock is set to the authors' LOG.pdf run date with libfaketime.
export R_LIBS_USER=/workspace/audit_runs/02_ELBOXX/B/rlib
faketime '2025-05-06 13:14:00' Rscript /workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/02_ELBOXX/B/scripts/driver_pathA.R /workspace/audit_runs/02_ELBOXX/B/objs > console.txt 2>&1
