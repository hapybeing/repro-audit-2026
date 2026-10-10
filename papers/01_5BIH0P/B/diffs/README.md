# Agent B env fixes, 01_5BIH0P

- `xvg2csv.py.diff`: the deposited `xvg2csv.py` (byte-identical to `xvg2csv-1.py`) uses Python 2 `print` statements and fails
  under Python 3 with `SyntaxError: Missing parentheses in call to 'print'`. No python2 interpreter is available in the sandbox.
  The four print statements were converted to `print(...)` calls. No other change; the output CSVs are byte-identical to the
  deposited original CSVs (see outputs/xvg_format_check.json), which shows the fix did not change behaviour.

No change was made to any gmx_MMPBSA / sander input. The AmberTools GB rerun used the deposited `_GMXMMPBSA_gb_decomp_*.mdin`,
`*.prmtop`, `_GMXMMPBSA_dummy*.inpcrd` and `_GMXMMPBSA_*.mdcrd.0` files unmodified.
