"""Agent B: confirm that every input O_B_Ku.py reads (other than the missing module)
is present at the path the script uses and holds the variables it reads.
Metadata only (shapes, dtypes); no analysis step of the authors is run.
Writes outputs/input_check.json."""
import json, os, h5py
from netCDF4 import Dataset
import xarray as xr
R = "/workspace/audit_runs/20_SINIYU/B/rundir"
os.chdir(R)
res = {}
with h5py.File("./FY3G_PMR.HDF", "r") as f:
    for p in ["/Geolocation/Ku/height", "/Geolocation/Ku/Latitude", "/Geolocation/Ku/Longitude", "/PRE/Ku/zFactorMeasured",
              "/PRE/Ku/flagPrecip", "/PRE/Ku/binClutterFreeBottom", "/Geolocation/Ku/dayCount", "/Geolocation/Ku/msCount"]:
        res["FY3G_PMR.HDF:" + p] = [list(f[p].shape), str(f[p].dtype)] if p in f else "MISSING"
d = Dataset("./gep00/postvar.nc")
for v in ["Qv", "t", "Qr", "levels", "latitudes", "longitudes"]:
    res["gep00/postvar.nc:" + v] = [list(d.variables[v].shape), str(d.variables[v].dtype)] if v in d.variables else "MISSING"
d.close()
s = xr.open_dataset("./gep00/swath_spaceborn.nc")
for v in ["heights", "ZH"]:
    res["gep00/swath_spaceborn.nc:" + v] = [list(s[v].dims), list(s[v].shape), str(s[v].dtype)] if v in s else "MISSING"
s.close()
try:
    import interp_radar  # noqa
    res["import interp_radar"] = "OK"
except Exception as e:
    res["import interp_radar"] = f"{type(e).__name__}: {e}"
try:
    import matplotlib.pyplot as plt; plt.style.use(["science", "no-latex"]); res["scienceplots style"] = "OK"
except Exception as e:
    res["scienceplots style"] = f"{type(e).__name__}: {e}"
json.dump(res, open("/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/20_SINIYU/B/outputs/input_check.json", "w"), indent=1)
print(json.dumps(res, indent=1))
