# diffs/ for 20_SINIYU agent A

No file of the authors was edited, so there are no .diff files.

Path-only fixes, done as symlinks in the run directory /workspace/audit_runs/20_SINIYU/A/run/figure6/ (PREREG section 2, steps 1 to 3; batch4_class_decisions.md item 1):
- `FY3G_PMR.HDF` -> `data/FY3G_PMR.HDF4` (single member of the RAR5 set, extracted with `unrar-free -x FY3G_PMR.part1.rar`, "All OK"). The script opens `./FY3G_PMR.HDF`.
- `gep00/postvar.nc` -> `data/postvar.nc`. The script opens `./gep00/postvar.nc` (line 249).
- `gep00/swath_spaceborn.nc` -> `data/swath_spaceborn_mu3.nc`. The script opens `./gep00/swath_spaceborn.nc` (line 330).

Not applied, because the run stopped at line 17 before they could matter:
- the output-only `np.save('outputs/ob_data.npy', data)` line after line 492 (PREREG step 6);
- the memory fallback (PREREG section 2);
- dropping the SciencePlots style line (not needed: SciencePlots 2.2.2 installed).

No replacement for the missing `interp_radar` module was written (batch 4 brief; batch4_class_decisions.md item 5).
