#!/bin/bash
# sequential heavy steps after K was fixed (K=3, outputs/bootstrap_K.json)
L=/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/17_T1NXVQ/B/scripts/launch.sh; F=/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/17_T1NXVQ/B/scripts/fit_main.R; B=/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/17_T1NXVQ/B/scripts/boot.R
AUDIT_MODEL=pool_xsec BOOT_FROM=1 BOOT_TO=3 BOOT_TAG=authorseeds BOOT_CAP_MIN=35 $L boot_authorseeds_pool_xsec_2to3 $B
AUDIT_MODEL=pool_ldv BOOT_FROM=1 BOOT_TO=3 BOOT_TAG=authorseeds BOOT_CAP_MIN=35 $L boot_authorseeds_pool_ldv $B
AUDIT_MODEL=pool_xsec AUDIT_CHECK=Rb $L Rb_pool_xsec $F
AUDIT_MODEL=pool_xsec AUDIT_CHECK=Rc $L Rc_pool_xsec $F
AUDIT_MODEL=pool_xsec BOOT_FROM=1001 BOOT_TO=1003 BOOT_TAG=seeds1001 BOOT_CAP_MIN=35 $L boot_seeds1001_pool_xsec $B
AUDIT_MODEL=pool_ldv AUDIT_CHECK=Rb $L Rb_pool_ldv $F
AUDIT_MODEL=pool_ldv AUDIT_CHECK=Rc $L Rc_pool_ldv $F
AUDIT_MODEL=pool_ldv BOOT_FROM=1001 BOOT_TO=1003 BOOT_TAG=seeds1001 BOOT_CAP_MIN=35 $L boot_seeds1001_pool_ldv $B
