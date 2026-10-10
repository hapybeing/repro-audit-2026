"""Agent B: compare secondary (non-target) printed values from PREREG.md 'Secondary context' with the
tables our run produced (outputs/Table_2_*.tex, Table_3_*.tex) and the proportions from 02 (attempt 2).
Paper values below are copied from PREREG.md (which copied them from the paper)."""
import csv, json, re, os
B = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
O = os.path.join(B, "outputs")
paper = {
 ("UK", "WHO (recommendation)"): [-1.53, -1.36, -2.26, -1.90, -1.36],
 ("UK", "WHO (recommendation, ratification)"): [-2.01, -2.72, -2.62, -2.56, -2.06],
 ("US", "WHO (recommendation)"): [-1.06, -2.15, -1.31, -1.40, -1.25],
 ("US", "WHO (recommendation, ratification)"): [-1.52, -1.83, -2.05, -1.84, -1.95],
}
files = {"UK": "Table_2_table_main_UK_1.tex", "US": "Table_3_table_main_US_1.tex"}
rows = []
def parse(path):
    d = {}
    for line in open(path):
        if "&" in line and not line.strip().startswith("&"):
            parts = [p.strip().rstrip("\\").strip() for p in line.split("&")]
            d[parts[0]] = parts[1:]
    return d
tabs = {c: parse(os.path.join(O, f)) for c, f in files.items()}
for (c, name), vals in paper.items():
    cells = tabs[c][name]
    for k, (pv, cell) in enumerate(zip(vals, cells)):
        num = float(re.match(r"-?\d+\.\d+", cell).group(0))
        rows.append({"country": c, "row": name, "column": k + 1, "paper": pv, "reproduced_cell": cell,
                     "match": abs(num - pv) < 1e-9, "stars_double": "**" in cell})
# star observation (PREREG inconsistency 6): UK, All neighbors column (column 3)
obs = {"UK_all_neighbors_gender_cell": tabs["UK"]["Gender (male)"][2],
       "UK_all_neighbors_ideology_cell": tabs["UK"]["Ideology (left-right)"][2],
       "US_threatened_ideology_dk_cell": tabs["US"]["Ideology (don't know)"][1]}
props = {}
for r in csv.DictReader(open(os.path.join(O, "Choices_prop_attempt2.csv"))):
    if r["Y"] == "Leave borders open":
        props[r["DataSet"]] = [r["Mean"], r["Q025"], r["Q975"]]
res = {"who_cells": rows, "n_who_cells": len(rows), "n_who_cells_match": sum(r["match"] for r in rows),
       "n_who_cells_double_star": sum(r["stars_double"] for r in rows),
       "star_observations": obs,
       "paper_printed_note": "paper prints UK All-neighbors Gender -0.47 (0.21) and Ideology 1.76 (0.57) without stars; US Ideology (do not know), Threatened neighbors -7.81** (0.00)",
       "leave_open_proportions_reproduced": props,
       "leave_open_proportions_paper": {"United Kingdom": ["0.16", "0.13", "0.18"], "United States": ["0.16", "0.14", "0.18"]}}
res["leave_open_match"] = all(props[k] == v for k, v in res["leave_open_proportions_paper"].items())
json.dump(res, open(os.path.join(O, "secondary_check.json"), "w"), indent=1)
print(res["n_who_cells_match"], "of", res["n_who_cells"], "WHO cells match;", obs, "leave-open match:", res["leave_open_match"])
