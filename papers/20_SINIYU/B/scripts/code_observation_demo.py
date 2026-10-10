"""Agent B: toy demonstrations of two code mechanics in codes/figure6/O_B_Ku.py.
They show what the deposited statements do on small arrays; they do NOT show any
effect on the paper's numbers (the script cannot run without interp_radar).
Writes outputs/code_observation_demo.json."""
import json, numpy as np, xarray as xr
out = {}
# O_B_Ku.py lines 419-420: radar_Z_out[radar_Z_out>6000.]=np.nan ; obs_mesh_meso[radar_Z_out>6000.]=np.nan
rz = np.array([1000., 5000., 7000., 9000.]); obs = np.array([20., 30., 40., 50.])
rz[rz > 6000.] = np.nan
with np.errstate(invalid="ignore"):
    mask2 = rz > 6000.
obs[mask2] = np.nan
out["lines_419_420"] = {"radar_Z_out_after_419": [None if np.isnan(v) else v for v in rz],
                        "cells_masked_by_420": int(mask2.sum()),
                        "obs_after_420": [None if np.isnan(v) else v for v in obs]}
# O_B_Ku.py lines 343-345 (same in 1DVAR.py 310-312): clip of negative ZH is overwritten
zh = xr.DataArray(np.array([-5., 10., 25.]))
cond = (zh < 0.)
B_value = xr.where(cond, 0., zh)
B_value = zh / 1.0
out["lines_343_345"] = {"input_ZH": zh.values.tolist(), "B_value_after_345": B_value.values.tolist(),
                        "negative_values_kept": bool((B_value < 0).any())}
json.dump(out, open("/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/20_SINIYU/B/outputs/code_observation_demo.json", "w"), indent=1)
print(json.dumps(out, indent=1))
