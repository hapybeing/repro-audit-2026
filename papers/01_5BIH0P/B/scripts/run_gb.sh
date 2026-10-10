#!/bin/bash
# exact gmx_MMPBSA sander inputs, one system at a time (light on shared CPUs)
export AMBERHOME=$(cd ..; pwd)/amber; export PATH=$AMBERHOME/bin:$PATH; export OMP_NUM_THREADS=1
date > progress.txt; for s in ligand receptor complex; do
  case $s in complex) p=COM; m=com;; receptor) p=REC; m=rec;; ligand) p=LIG; m=lig;; esac
  nice -n 10 sander -O -i _GMXMMPBSA_gb_decomp_$m.mdin -o B_${s}_gb.mdout -p $p.prmtop -c _GMXMMPBSA_dummy$s.inpcrd -y _GMXMMPBSA_$s.mdcrd.0 -r B_restrt_$s > B_${s}_sander.stdout 2> B_${s}_stderr.txt
  echo "$s done $(date)" >> progress.txt
done
