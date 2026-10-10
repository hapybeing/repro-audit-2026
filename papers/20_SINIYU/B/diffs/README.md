# diffs/README.md (20_SINIYU, agent B)

No file of the authors was edited. `rundir/O_B_Ku.py` is a byte-identical copy of `codes/figure6/O_B_Ku.py` from codes.tar.gz (see `paths_symlinks.txt` for the sha256 check).

Path-only environment fixes (symlinks, PREREG section 2 steps 1 to 3; batch4_class_decisions.md item 1), listed in `paths_symlinks.txt`:
- `rundir/FY3G_PMR.HDF` -> `rarx/FY3G_PMR.HDF4` (the single member of the deposited RAR5 set, extracted with `unrar-free -x`, "All OK").
- `rundir/gep00/postvar.nc` -> deposited `postvar.nc`.
- `rundir/gep00/swath_spaceborn.nc` -> deposited `swath_spaceborn_mu3.nc`.

Not applied:
- `interp_radar` (PREREG step 4): not found in the deposit or the locations the data statement names (outputs/deposit_module_search.json; DATA_STATEMENT.md). No replacement written (brief and batch4 decision 5). The run stops at line 17.
- SciencePlots style line 20 (PREREG step 5 allowed fix): with SciencePlots 2.2.2, `plt.style.use(['science','no-latex'])` raises OSError unless `import scienceplots` is executed first (outputs/input_check.json). It was not changed because the script never gets past line 17; a fix would change nothing.
- Output-only `np.save('outputs/ob_data.npy', data)` (PREREG step 6): not applied, line 492 is never reached.
