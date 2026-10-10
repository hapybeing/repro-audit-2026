#!/bin/bash
# Optional PREREG step 2: recompute GB energies with AmberTools MMPBSA.py from the deposited prmtops and
# the 20-frame complex trajectory _GMXMMPBSA_complex.mdcrd.0. Settings from deposited mmpbsa.in / _GMXMMPBSA_info.
# Usage: run_gb_amber.sh <igb>   (5 = authors' setting; 2 = R_c2)
set -u
IGB=$1
A=/workspace/audit_runs/01_5BIH0P/A
W=$A/gb_igb$IGB; mkdir -p $W; cd $W
for f in COM.prmtop REC.prmtop LIG.prmtop _GMXMMPBSA_complex.mdcrd.0; do ln -sf $A/raw/files/$f .; done
cat > gb.in <<EOT
GB igb=$IGB recompute, 20 deposited frames
&general
  startframe=1, endframe=20, interval=1,
  verbose=2, keep_files=0,
/
&gb
  igb=$IGB, saltcon=0.0, surften=0.0072, surfoff=0.0, molsurf=0, probe=1.4,
/
EOT
# Note: the authors' intdiel=1.0 and extdiel=78.5 are rejected by AmberTools 26 MMPBSA.py in &gb
# ("InputError: Unknown variable intdiel in &gb"); both equal the sander defaults, so they are omitted.
export AMBERHOME=$A/amberenv
export PATH=$AMBERHOME/bin:$PATH
export OMP_NUM_THREADS=1
TZ=Asia/Kolkata date '+START %F %T IST'
# AmberTools 26 MMPBSA.py writes extdiel=80.0 into the GB mdin and does not accept extdiel in &gb.
# The authors' sander mdin (echoed in the deposited _GMXMMPBSA_complex_gb.mdout.0) sets no extdiel, i.e. the
# sander default 78.5. So: write the mdin, remove the extdiel=80.0 entry (env fix, diff saved), run with -use-mdins.
MMPBSA.py -O -i gb.in -make-mdins -cp COM.prmtop -rp REC.prmtop -lp LIG.prmtop -y _GMXMMPBSA_complex.mdcrd.0 > make_mdins_stdout.txt 2>&1
cp _MMPBSA_gb.mdin _MMPBSA_gb.mdin.orig
sed -i 's/ extdiel=80.0,//' _MMPBSA_gb.mdin
diff -u _MMPBSA_gb.mdin.orig _MMPBSA_gb.mdin > mdin_extdiel.diff
nice -n 10 MMPBSA.py -O -i gb.in -use-mdins -o FINAL_RESULTS_igb$IGB.dat -eo FINAL_RESULTS_igb$IGB.csv \
  -cp COM.prmtop -rp REC.prmtop -lp LIG.prmtop -y _GMXMMPBSA_complex.mdcrd.0 > mmpbsa_stdout.txt 2>&1
echo "EXIT $?"
TZ=Asia/Kolkata date '+END %F %T IST'
