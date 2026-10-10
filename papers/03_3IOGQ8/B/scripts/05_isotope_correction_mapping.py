"""Agent B code review evidence: parse the isotope-correction block of the authors' Rmd and list, for each corrected
channel k, which neighbour intensity j is multiplied by which coefficient. Compare with the standard first-order
correction, in which the signal leaking from reagent j into channel k is I_j * impurity_j(at offset k-j), i.e. the
coefficient comes from the NEIGHBOUR's row, not from channel k's own row. Usage: <rmd> <out_json>"""
import re, sys, json
src = open(sys.argv[1], encoding="utf-8").read().replace("\r\n", "\n")
lines = src.split("\n")
vec = {m.group(1): [float(x) for x in m.group(2).split(",")] for m in re.finditer(r"^(TMT1\d\d) <- c\(([^)]*)\)", src, re.M)}
offsets = [-2, -1, 0, 1, 2]  # per the Rmd comment: reference c(-2, -1, monoisotopic, +1, +2)
start = next(i for i, l in enumerate(lines) if "`126_corrected` =" in l)
block = "\n".join(lines[start:start + 30])
out = []
for m in re.finditer(r"`(1\d\d)_corrected` = \(`\1_intensity` \* (TMT1\d\d)\[3\]\) - sum\(c\((.*?)\),\s*na\.rm", block, re.S):
    k = int(m.group(1)); terms = re.findall(r"`(1\d\d)_intensity` \* (TMT1\d\d)\[(\d)\]", m.group(3))
    for j, row, idx in terms:
        j = int(j); idx = int(idx)
        code_coef = vec[row][idx - 1]
        std_off = k - j  # offset of channel k relative to reagent j
        std_coef = vec[f"TMT{j}"][offsets.index(std_off)] if std_off in offsets else None
        out.append({"corrected_channel": k, "neighbour_intensity": j, "code_uses": f"{row}[{idx}]",
                    "code_coef": code_coef, "code_row_is_own_channel": row == f"TMT{k}",
                    "standard_coef_neighbour_row": f"TMT{j}[{offsets.index(std_off)+1}]" if std_off in offsets else None,
                    "standard_coef": std_coef, "differs": code_coef != std_coef})
res = {"rmd_line_of_block_start": start + 1, "coefficient_vectors": vec, "terms": out,
       "n_terms": len(out), "n_terms_differing": sum(t["differs"] for t in out)}
json.dump(res, open(sys.argv[2], "w"), indent=1)
for t in out: print(t)
print("block starts at Rmd line", start + 1, "; terms differing:", res["n_terms_differing"], "of", len(out))
