#!/bin/bash
# timeboxed AmberTools install attempt via micromamba (conda-forge, linux-aarch64)
set -x
cd /workspace/audit_runs/01_5BIH0P/A
TZ=Asia/Kolkata date '+START %F %T IST'
[ -x bin/micromamba ] || curl -sSL -A "repro-audit-2026" https://micro.mamba.pm/api/micromamba/linux-aarch64/latest | tar -xj bin/micromamba
export MAMBA_ROOT_PREFIX=/workspace/audit_runs/01_5BIH0P/A/mamba
timeout 1700 ./bin/micromamba create -y -p /workspace/audit_runs/01_5BIH0P/A/amberenv -c conda-forge ambertools python=3.11
echo "EXIT $?"
ls amberenv/bin/sander amberenv/bin/MMPBSA.py
TZ=Asia/Kolkata date '+END %F %T IST'
