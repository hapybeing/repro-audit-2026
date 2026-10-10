# Environment fixes, 01_5BIH0P agent A

1. `xvg2csv.py.diff` (applies identically to `xvg2csv-1.py`, which is byte-identical to `xvg2csv.py`).
   Why: the script is Python 2 (`print "..."` statements). Under Python 3.12 it stops with
   `SyntaxError: Missing parentheses in call to 'print'` (verbatim in `outputs/authors_xvg2csv/xvg2csv_py3_unmodified_error.txt`).
   No python2 interpreter is installed. The four print statements were turned into `print(...)` calls; the text they print is
   the same, and the CSV-writing lines are untouched. With this fix the re-run outputs are byte-identical to the deposited
   original `.tab` files (`outputs/xvg2csv_check.json`).

2. `mmpbsa_gb_mdin_extdiel.diff` (only for the optional AmberTools GB recompute, PREREG section 2 step 2; not the authors' code).
   Why: AmberTools 26 `MMPBSA.py` rejects `intdiel` and `extdiel` in `&gb` (`InputError: Unknown variable intdiel in &gb`,
   saved in `outputs/amber/gb5_attempt1_error.txt`) and writes `extdiel=80.0` into the sander GB mdin by default. The authors'
   sander GB mdin, echoed in the deposited `_GMXMMPBSA_complex_gb.mdout.0`, sets no `extdiel`, so sander used its default 78.5,
   matching `extdiel = 78.5` in their `mmpbsa.in`. The mdin was therefore generated with `MMPBSA.py -make-mdins`, the
   `extdiel=80.0` entry was removed so sander's default 78.5 applies, and the run used `-use-mdins`. `intdiel=1.0` is the sander
   default and needs no change. Remaining known differences from the authors' run: AmberTools 26 vs Amber 21 sander, aarch64 vs
   x86_64, and the authors' mdin also had `gbsa=2` and `idecomp=1` (decomposition), which do not enter the reported
   ESURF (computed from LCPO surface areas by cpptraj) or the GB energy terms.
