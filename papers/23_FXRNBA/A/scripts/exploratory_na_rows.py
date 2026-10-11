# EXPLORATORY (not pre-registered, never changes the class): PREREG inconsistency 1.
# Counts 13km station-days (2013-2023) that have all Model 3 variables but are dropped by the extra
# na.omit columns in seattle_main (wind direction, other crime counts). Plain csv, no analysis.
import csv, json, sys
f = sys.argv[1]; out = sys.argv[2]
m3 = ["Daily Mean PM2.5 Concentration", "smokePM_dummy", "Simple Assault", "Aggravated Assault",
      "AWND", "PRCP", "TMAX", "TMIN", "Holiday", "Station", "date"]
extra = ["WDF2", "Robbery", "Burglary/Breaking & Entering", "Theft From Motor Vehicle", "Motor Vehicle Theft",
         "Intimidation", "Person", "Property"]
na = lambda v: v is None or v.strip() in ("", "NA")
n = m3ok = both = 0; by_col = {c: 0 for c in extra}; wdf_out = 0
for r in csv.DictReader(open(f, newline="")):
    y = int(r["date"][:4])
    if y < 2013 or y > 2023: continue
    n += 1
    if any(na(r[c]) for c in m3): continue
    m3ok += 1
    bad = [c for c in extra if na(r[c])]
    if not na(r["WDF2"]) and not (0 <= float(r["WDF2"]) <= 360): wdf_out += 1; bad.append("WDF2_out_of_range")
    for c in bad:
        if c in by_col: by_col[c] += 1
    if not bad: both += 1
res = {"label": "EXPLORATORY, not pre-registered", "rows_2013_2023": n, "rows_complete_model3_vars": m3ok,
       "rows_complete_model3_and_extra_vars": both, "rows_dropped_only_by_extra_columns": m3ok - both,
       "missing_by_extra_column_among_model3_complete": by_col, "wdf2_out_of_0_360": wdf_out}
json.dump(res, open(out, "w"), indent=1); print(json.dumps(res, indent=1))
