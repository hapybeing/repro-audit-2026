#!/bin/bash
# Re-checks SI Table A5 cells for T3 and T4 against the SI .doc (catdoc -w keeps the tab-separated column order).
cd /workspace/audit_runs/21_LEFTNE/B/dl
sha256sum SI.doc
catdoc -w SI.doc > SI.txt
n=$(grep -n "Table A5: Regressing" SI.txt | tail -1 | cut -d: -f1)
echo "--- header row"; sed -n "$((n+1))p" SI.txt
echo "--- Trump row (cells tab separated: None, Balanced, Party, ...)"; awk -v s=$n 'NR>s && /^Trump\t/{print; getline; print; getline; print; exit}' SI.txt
echo "--- Trump:Party row (None and Balanced cells blank)"; awk -v s=$n 'NR>s && /^Trump:Party/{print; getline; print; exit}' SI.txt
echo "--- N row"; awk -v s=$n 'NR>s && /^N\t/{print; exit}' SI.txt
