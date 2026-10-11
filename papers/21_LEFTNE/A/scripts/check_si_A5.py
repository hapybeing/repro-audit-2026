"""Re-check SI Table A5 cells for T3 and T4 against the SI .doc itself (catdoc -w text of the Word 97 binary).
Writes outputs/si_A5_check.json with the parsed cells (short excerpt only, no full text saved)."""
import json, re, subprocess, hashlib, sys
DOC = "/workspace/audit_runs/21_LEFTNE/A/si/SI.doc"
OUT = "/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/21_LEFTNE/A/outputs/si_A5_check.json"
sha = hashlib.sha256(open(DOC, "rb").read()).hexdigest()
txt = subprocess.run(["catdoc", "-w", DOC], capture_output=True, text=True).stdout
start = txt.index("Table A5: Regressing")
end = txt.index("Table A6:", start)
block = txt[start:end]
header = block.splitlines()[1].strip().split("\t")
# Rebuild rows: a row starts with a label at line start; cells are tab separated; each cell is "est stars\n(se)".
lines = block.splitlines()[2:]
rows, cur = [], None
label_re = re.compile(r"^(\(Intercept\)|Clinton|Trump|Party|Gender|Edu|N|R2|Clinton:\S+|Trump:\S+)(\t|$)")
for ln in lines:
    m = label_re.match(ln)
    if m:
        cur = [ln]; rows.append(cur)
    elif cur is not None:
        cur.append(ln)
def cells(row):
    joined = "\n".join(row)
    label, rest = joined.split("\t", 1) if "\t" in joined else (joined, "")
    return label.strip(), [c.strip().replace("\n", " ") for c in rest.split("\t")]
parsed = dict(cells(r) for r in rows)
res = {"si_sha256": sha, "expected_sha256_from_PREREG": "64165d965e1bb1072bd5caf7a43ceb501ac0008402400dc9c7d68c2988c42c3e",
       "extraction": "catdoc -w (Debian catdoc), table cells tab separated, each cell 'estimate stars' then '(SE)'",
       "column_headers": header,
       "Trump_row_cells": parsed.get("Trump"), "Trump:Party_row_cells": parsed.get("Trump:Party"), "N_row_cells": parsed.get("N"),
       }
tr = parsed["Trump"][0]; tp = parsed["Trump:Party"][2]
res["T3_cell_None_Trump"] = tr; res["T4_cell_Party_TrumpParty"] = tp
res["T3_value_from_doc"] = float(tr.split()[0]); res["T4_value_from_doc"] = float(tp.split()[0])
res["T3_matches_targets_json_0.15"] = res["T3_value_from_doc"] == 0.15 and "(0.02)" in tr and "***" in tr
res["T4_matches_targets_json_0.22"] = res["T4_value_from_doc"] == 0.22 and "(0.05)" in tp and "***" in tp
res["N_None"] = parsed["N"][0]; res["N_Party"] = parsed["N"][2]
json.dump(res, open(OUT, "w"), indent=1)
print(json.dumps(res, indent=1))
