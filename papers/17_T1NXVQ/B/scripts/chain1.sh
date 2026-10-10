#!/bin/bash
# wait for LDV fit, then time bootstrap draw seed 1 (baseline)
while pgrep -f "launch.sh pool_ldv" > /dev/null; do sleep 10; done
AUDIT_MODEL=pool_xsec BOOT_FROM=1 BOOT_TO=1 BOOT_TAG=authorseeds BOOT_CAP_MIN=35 /workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/17_T1NXVQ/B/scripts/launch.sh boot_authorseeds_pool_xsec_1 /workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/17_T1NXVQ/B/scripts/boot.R
