"""Static checks supporting code observations on codes/figure6/O_B_Ku.py. They do NOT run the authors' script
(it stops at line 17, missing module), so any effect on T1/T2 stays unverified."""
import json, sys, numpy as np, xarray as xr
out = sys.argv[1]
res = {}
# Obs 1: lines 419-420. After line 419 sets cells >6000 to NaN, the test on line 420 is False everywhere (NaN > x is False).
rz = np.array([100., 5999., 6000., 6001., 9000., -9999.])
obs = np.ones_like(rz)
rz[rz > 6000.] = np.nan          # line 419
mask420 = rz > 6000.             # line 420 condition
obs[mask420] = np.nan
res["obs1_line420_mask_true_count_on_toy_array"] = int(mask420.sum())
res["obs1_obs_cells_masked_on_toy_array"] = int(np.isnan(obs).sum())
# Obs 2: lines 343-345. Line 344 builds B_value with ZH<0 set to 0, line 345 overwrites B_value with raw ZH.
ds = xr.open_dataset("/workspace/audit_runs/20_SINIYU/A/data/swath_spaceborn_mu3.nc")
zh = ds["ZH"].values
res["obs2_swath_ZH_shape"] = list(zh.shape)
res["obs2_swath_ZH_n_finite"] = int(np.isfinite(zh).sum())
res["obs2_swath_ZH_n_below_0"] = int((zh < 0).sum())
res["obs2_swath_ZH_n_nan"] = int(np.isnan(zh).sum())
res["note"] = "Effect on T1/T2 cannot be measured because interp_radar_ppi is not deposited; unverified observations."
json.dump(res, open(out, "w"), indent=1); print(json.dumps(res, indent=1))
