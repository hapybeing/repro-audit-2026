"""Re-check the six target cells against the publisher supplement PDF (pdftotext -layout). Writes outputs/supplement_target_check.json."""
import json, re, subprocess, sys
pdf, out = sys.argv[1], sys.argv[2]
txt = subprocess.run(["pdftotext", "-layout", pdf, "-"], capture_output=True, text=True).stdout.splitlines()
def table_block(title):
    i = next(k for k, l in enumerate(txt) if title in l)
    j = next(k for k in range(i, len(txt)) if "Observations" in txt[k])
    return txt[i:j + 1]
def cells(block, row):
    line = next(l for l in block if l.strip().startswith(row))
    return re.findall(r"-?\d+\.\d+|\d{3,}", line)
a1, a2 = table_block("Table A1. DV: Union Influence"), table_block("Table A2. DV: Support for Strike")
res = {
 "T1": {"row": "Table A1 Anti-strike col 1", "pdf_cells": cells(a1, "Anti-strike"), "read": float(cells(a1, "Anti-strike")[0])},
 "T2": {"row": "Table A2 Pro-strike col 1", "pdf_cells": cells(a2, "Pro-strike"), "read": float(cells(a2, "Pro-strike")[0])},
 "T3": {"row": "Table A1 Pro-strike col 1", "pdf_cells": cells(a1, "Pro-strike"), "read": float(cells(a1, "Pro-strike")[0])},
 "T4": {"row": "Table A1 Anti-strike col 4", "pdf_cells": cells(a1, "Anti-strike"), "read": float(cells(a1, "Anti-strike")[3])},
 "T5": {"row": "Table A1 Observations col 1", "pdf_cells": cells(a1, "Observations"), "read": float(cells(a1, "Observations")[0])},
 "T6": {"row": "Table A2 Observations col 1", "pdf_cells": cells(a2, "Observations"), "read": float(cells(a2, "Observations")[0])},
}
tj = {t["id"]: t["paper_value"] for t in json.load(open(sys.argv[3]))}
for k, v in res.items():
    v["targets_json_value"] = tj[k]; v["agrees"] = abs(v["read"] - tj[k]) < 1e-9
res["all_agree"] = all(v["agrees"] for k, v in res.items() if k.startswith("T"))
json.dump(res, open(out, "w"), indent=1); print(json.dumps(res, indent=1))
