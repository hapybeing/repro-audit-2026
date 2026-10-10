#!/usr/bin/env python3
"""Compare all WHO cells of reproduced Tables 2/3 with the secondary-context values copied in PREREG.md (paper values), and
record the cells mentioned in PREREG inconsistencies 6 and 7. Writes outputs/secondary_check.csv."""
import csv, os
O = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "outputs")
paper = {("UK", "WHO (recommendation)"): [-1.53, -1.36, -2.26, -1.90, -1.36],
         ("UK", "WHO (recommendation, ratification)"): [-2.01, -2.72, -2.62, -2.56, -2.06],
         ("US", "WHO (recommendation)"): [-1.06, -2.15, -1.31, -1.40, -1.25],
         ("US", "WHO (recommendation, ratification)"): [-1.52, -1.83, -2.05, -1.84, -1.95]}
fn = {"UK": "Table_2_table_main_UK_1.tex", "US": "Table_3_table_main_US_1.tex"}
cols = ["Infected neighbor", "Threatened neighbors", "All neighbors", "Entire region", "Entire world"]
def rows(c):
    L = open(os.path.join(O, fn[c])).read().split("\n"); d = {}
    for i, l in enumerate(L):
        if " & " in l and not l.startswith(" ") and not l.startswith("\\"):
            name = l.split(" & ")[0]; cells = [x.strip() for x in l.rstrip("\\").split(" & ")[1:]]
            se = [x.strip() for x in L[i + 1].rstrip("\\").split(" & ")[1:]]
            d[name] = (cells, se)
    return d
out = []
for (c, r), vals in paper.items():
    cells, se = rows(c)[r]
    for j, v in enumerate(vals):
        num = float(cells[j].split("$")[0])
        out.append({"check": "WHO cell", "country": c, "row": r, "column": cols[j], "paper_value": v, "reproduced_cell": cells[j], "reproduced_se": se[j], "match_2dp": num == v, "has_two_stars": "**" in cells[j]})
extra = [("UK", "Gender (male)", 2, "-0.47 (0.21), printed without star per PREREG #6"), ("UK", "Ideology (left-right)", 2, "1.76 (0.57), printed without star per PREREG #6"),
         ("UK", "Health capacity (world-class)", 1, "0.60 (0.31), printed with * per PREREG #6"), ("US", "Ideology (don't know)", 1, "-7.81** (0.00) per PREREG #7")]
for c, r, j, p in extra:
    cells, se = rows(c)[r]
    out.append({"check": "PREREG inconsistency cell", "country": c, "row": r, "column": cols[j], "paper_value": p, "reproduced_cell": cells[j], "reproduced_se": se[j], "match_2dp": "", "has_two_stars": "**" in cells[j]})
w = csv.DictWriter(open(os.path.join(O, "secondary_check.csv"), "w"), fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
print(sum(1 for o in out if o["match_2dp"] is True), "of 20 WHO cells match;", sum(1 for o in out if o["check"] == "WHO cell" and o["has_two_stars"]), "with **")
for o in out[20:]: print(o)
