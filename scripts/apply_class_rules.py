"""Apply CHANGELOG_METHOD #4 to batch K results. Usage: python3 scripts/apply_class_rules.py 1"""
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
main = Counter(o["class_rule4"] for o in out)
excl01 = Counter(rules[o["paper_id"]]["class_rule4"] for o in out if rules[o["paper_id"]]["alt_class"] != "no computational target")
osf = Counter(rules[o["paper_id"]]["alt_class"] if o["paper_id"].startswith("04") else o["class_rule4"] for o in out)
clock = Counter(rules[o["paper_id"]]["alt_class"] if o["paper_id"].startswith("02") else o["class_rule4"] for o in out)
res = {"rule": rules["_rule"],
       "counts_main": {c: main.get(c, 0) for c in "ABCDE"}, "n_main": sum(main.values()),
       "counts_excluding_no_target": {c: excl01.get(c, 0) for c in "ABCDE"}, "n_excluding_no_target": sum(excl01.values()),
       "counts_if_uncited_OSF_counted": {c: osf.get(c, 0) for c in "ABCDE"},
       "counts_if_02_run_as_is": {c: clock.get(c, 0) for c in "ABCDE"}}
json.dump(res, open(f"batches/batch{k}_counts_rule4.json", "w"), indent=1)
print(json.dumps(res, indent=1))
