"""Read the PUBLISHED SI tables (ja4c12585_si_001.xlsx) and record the values that the
notebook would have to reproduce. These are the paper's own numbers, NOT reproductions;
they are saved only to document what the targets refer to and the T1/T2 vs SI relation
noted in PREREG.md. Usage: python3 si_published_values.py <xlsx> <out.json>"""
import json, sys, hashlib, openpyxl

xlsx, out = sys.argv[1], sys.argv[2]
wb = openpyxl.load_workbook(xlsx, read_only=True, data_only=True)
res = {"source_file": xlsx, "sha256": hashlib.sha256(open(xlsx, "rb").read()).hexdigest(),
       "note": "Published SI values (paper side). Not reproduced values.", "sheets": {}}
target = "K9ac K14ac K23ac K27me2"
for ws in wb.worksheets:
    rows = [r for r in ws.iter_rows(values_only=True)]
    if not rows or rows[0][0] != "all_mods":
        continue
    hdr = rows[0]
    data = [r for r in rows[1:] if r and r[0] is not None]
    info = {"n_data_rows": len(data)}
    for r in data:
        if r[0] == target:
            d = dict(zip(hdr, r))
            fc = d["cumulative_log2-fold_change"]
            info["target_row"] = d
            info["pct_increase_from_cum_fc"] = 100 * (2 ** fc - 1)
    res["sheets"][ws.title] = info
json.dump(res, open(out, "w"), indent=1, default=str)
for k, v in res["sheets"].items():
    print(k, v["n_data_rows"], v.get("target_row", {}).get("cumulative_log2-fold_change"), v.get("pct_increase_from_cum_fc"))
