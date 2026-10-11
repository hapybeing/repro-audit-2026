#!/bin/bash
# Prints main-text Table 1 and Table 3 rows from the publisher PDF text layer (short excerpt only).
cd /workspace/audit_runs/21_LEFTNE/B/dl
sha256sum paper.pdf
pdftotext -layout paper.pdf paper.txt
grep -A6 "Table 1. Mediation analysis through anger" paper.txt
grep -A14 "Table 3. Treatment effects among compliers" paper.txt
