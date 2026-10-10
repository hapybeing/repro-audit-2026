# Code review check: main_rep.R lines 194 and 273-292 map "Result 1..8" to arm labels by position in
# setdiff(unique(data$condition), "control"). Writes the actual order next to the hard-coded labels.
import csv, json, sys
data = sys.argv[1]; out = sys.argv[2]
seen = []
for r in csv.DictReader(open(data)):
    if r["condition"] not in seen: seen.append(r["condition"])
arms = [s for s in seen if s != "control"]
hard = ["Public Surv","Public Both","Personal. Surv & Public Censor","Personal. Censor & Public Surv",
        "Personal. Both","Public Censor","Personal. Censor","Personal. Surv"]
norm = lambda s: s.replace("Personal.","Personal").replace(" & ","").replace(" ","").lower()
rows = [{"result": f"Result {i+1}", "arm_in_data_order": a, "hardcoded_label": h, "consistent": norm(a)==norm(h)} for i,(a,h) in enumerate(zip(arms,hard))]
json.dump({"rows": rows, "all_consistent": all(r["consistent"] for r in rows)}, open(out,"w"), indent=1)
print(json.dumps(rows, indent=1))
