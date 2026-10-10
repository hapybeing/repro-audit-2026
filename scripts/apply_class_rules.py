"""Apply CHANGELOG_METHOD #4 (and later class readings) to batch K results. Usage: python3 scripts/apply_class_rules.py K

Writes batches/batch{K}_results_rule4.csv and batches/batch{K}_counts_rule4.json.
counts_main uses each paper's class_rule4. Alternative counts swap in one paper's alt_class at a time (other papers keep
class_rule4), and, from batch 2 on, all alternatives together. An alt_class outside A to E (for example
"no computational target") means the paper is set aside in that alternative.
Batch 1 keeps its original key names and set of alternatives, so its output file is byte-identical to revision 3."""
import csv, json, sys
from collections import Counter
k = sys.argv[1]
rows = list(csv.DictReader(open(f"batches/batch{k}_results.csv")))
rules = json.load(open(f"batches/batch{k}_class_rules.json"))
out = []
for r in rows:
    ru = rules[r["paper_id"]]
    out.append({"paper_id": r["paper_id"], "paper_doi": r["paper_doi"], "dataset_doi": r["dataset_doi"],
                "class_agents_A": r["class_A"], "class_agents_B": r["class_B"],
                "class_rule4": ru["class_rule4"], "alternative": ru["alt_label"], "evidence": ru["evidence"],
                "robustness_A": r["robustness_A"]})
with open(f"batches/batch{k}_results_rule4.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)

pids = [o["paper_id"] for o in out]
def counts(swap):
    """swap: set of paper ids whose alt_class replaces class_rule4."""
    c = Counter()
    for p in pids:
        cl = rules[p]["alt_class"] if p in swap else rules[p]["class_rule4"]
        if cl in list("ABCDE"): c[cl] += 1
    return {x: c.get(x, 0) for x in "ABCDE"}, sum(c.values())

main, n_main = counts(set())
res = {"rule": rules["_rule"], "counts_main": main, "n_main": n_main}
if k == "1":
    # Revision 3 key names and alternatives, unchanged.
    excl, n_excl = counts({"01_5BIH0P"})
    res["counts_excluding_no_target"] = excl; res["n_excluding_no_target"] = n_excl
    res["counts_if_uncited_OSF_counted"] = counts({"04_PSHE5L"})[0]
    res["counts_if_02_run_as_is"] = counts({"02_ELBOXX"})[0]
else:
    alts = [p for p in pids if rules[p]["alt_class"] != rules[p]["class_rule4"]]
    res["alternatives"] = {p: {"class_rule4": rules[p]["class_rule4"], "alt_class": rules[p]["alt_class"],
                               "alt_label": rules[p]["alt_label"]} for p in alts}
    for p in alts:
        c, n = counts({p})
        res[f"counts_if_{p}_alt"] = c; res[f"n_if_{p}_alt"] = n
    c, n = counts(set(alts))
    res["counts_all_alternatives"] = c; res["n_all_alternatives"] = n
json.dump(res, open(f"batches/batch{k}_counts_rule4.json", "w"), indent=1)
print(json.dumps(res, indent=1))
