"""Agent B: read published SI values (context only; NOT reproduced values). Usage: <si_xlsx> <out_json>"""
import sys, json, openpyxl
wb = openpyxl.load_workbook(sys.argv[1], read_only=True, data_only=True)
res = {"note": "Published values read from the paper's SI xlsx. Context only, not reproduced values.", "sheets": {}}
for ws in wb.worksheets:
    rows = list(ws.iter_rows(values_only=True)); hdr = rows[0]; data = [r for r in rows[1:] if r and r[0] is not None]
    entry = {"n_data_rows": len(data)}
    for r in data:
        if r[0] == "K9ac K14ac K23ac K27me2":
            d = dict(zip(hdr, r)); fc = d["cumulative_log2-fold_change"]
            entry["K9ac_K14ac_K23ac_K27me2"] = {"cumulative_log2-fold_change": fc, "cumulative_norm_p_value": d["cumulative_norm_p_value"],
                "pct_increase_100x(2^fc-1)": 100 * (2 ** fc - 1),
                "pct_increase_from_var_over_ctrl": 100 * (d["cumulative_var_percent"] / d["cumulative_ctrl_percent"] - 1),
                "mean_log2-fold_change": d["mean_log2-fold_change"], "median_log2-fold_change": d["median_log2-fold_change"],
                "mean_norm_p_value": d["mean_norm_p_value"], "median_norm_p_value": d["median_norm_p_value"]}
    res["sheets"][ws.title] = entry
json.dump(res, open(sys.argv[2], "w"), indent=1); print(json.dumps(res, indent=1))
