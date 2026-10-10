import csv,sys
k=sys.argv[1]
rows=list(csv.DictReader(open(f"batches/batch{k}_results.csv")))
out=["| Paper | Field | Class A | Class B | Final | Confidence | Robustness (A) | Bugs A/B |","|---|---|---|---|---|---|---|---|"]
for r in rows:
    t=r["paper_title"][:60]+("..." if len(r["paper_title"])>60 else "")
    out.append(f"| {r['paper_id']} {t} ([paper]({r['paper_doi']}), [data]({r['dataset_doi']})) | {r['field']} | {r['class_A']} | {r['class_B']} | {r['final_class']} | {r['confidence']} | {r['robustness_A']} | {r['n_bugs_A']} / {r['n_bugs_B']} |")
open(f"batches/batch{k}_table.md","w").write("\n".join(out)+"\n")
