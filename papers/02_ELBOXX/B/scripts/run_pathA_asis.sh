#!/bin/bash
# Path A as-is: authors' replication.R, unchanged, current system date.
# Run inside a folder holding replication.R, analysis_data_creation.R and the three original CSVs.
export R_LIBS_USER=/workspace/audit_runs/02_ELBOXX/B/rlib
Rscript replication.R > console.txt 2>&1
