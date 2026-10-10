"""Generate compare tables, master_results.csv and batch tables ONLY from saved results.json files.
Usage: python3 scripts/make_tables.py [batch_number]"""
import json, csv, os, sys, glob
REPO=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sel=list(csv.DictReader(open(f"{REPO}/selection/selected.csv")))
def pid(r): return f"{int(r['audit_pos']):02d}_{r['dataset_doi'].split('/')[-1]}"
def load(p,ag):
    f=f"{REPO}/papers/{p}/{ag}/results.json"
    return json.load(open(f)) if os.path.exists(f) else None
def num_eq(a,b,tol=1e-9):
    if a is None or b is None: return None
    return abs(a-b)<=tol*max(1,abs(a),abs(b))
rows=[];flags=[]
batch=int(sys.argv[1]) if len(sys.argv)>1 else None
for r in sel:
    if batch and int(r["batch"])!=batch: continue
    p=pid(r); A=load(p,"A"); B=load(p,"B")
    fl=[]
    if A is None: fl.append("A results missing")
    if B is None: fl.append("B results missing")
    if A and B:
        if A.get("proposed_class")!=B.get("proposed_class"): fl.append(f"class disagreement A={A.get('proposed_class')} B={B.get('proposed_class')}")
        tb={t["id"]:t for t in B.get("targets",[])}
        al=json.load(open(f"{REPO}/batches/id_aliases.json")).get(p,{})
        for c in B.get("internal_checks",[]):
            v=next((c[k] for k in ("reproduced_value","recomputed_mean_from_perframe_csv","recomputed_mean") if k in c),None)
            tb.setdefault(c["id"],{"id":c["id"],"reproduced_value":v})
        tb={**tb,**{a:tb[b] for a,b in al.items() if b in tb}}
        for t in A.get("targets",[]):
            u=tb.get(t["id"])
            if not u: fl.append(f"{t['id']} only in A"); continue
            ra,rb=t.get("reproduced_value"),u.get("reproduced_value")
            if (ra is None)!=(rb is None): fl.append(f"{t['id']}: one agent has no value (A={ra}, B={rb})")
            elif ra is not None:
                d=t.get("paper_rounding_decimals")
                if not isinstance(d,int): d=4
                same=round(ra,d)==round(rb,d) if isinstance(d,int) else num_eq(ra,rb,1e-6)
                if not same: fl.append(f"{t['id']}: A={ra} B={rb} differ beyond paper rounding")
        if len(A.get("bugs",[]))!=len(B.get("bugs",[])): fl.append(f"code review differs: A reported {len(A.get('bugs',[]))} bug(s), B reported {len(B.get('bugs',[]))}")
        rbB={x["id"]:x for x in B.get("robustness",[])}
        for x in A.get("robustness",[]):
            y=rbB.get(x["id"])
            if y and x.get("same_direction_and_significance_as_paper")!=y.get("same_direction_and_significance_as_paper"):
                fl.append(f"{x['id']}: robustness conclusion differs (A={x.get('same_direction_and_significance_as_paper')}, B={y.get('same_direction_and_significance_as_paper')})")
    def tstr(R):
        if not R: return ""
        return "; ".join(f"{t['id']} paper={t.get('paper_value')} repro={t.get('reproduced_value')}" for t in R.get("targets",[]))
    def rstr(R):
        if not R: return ""
        return "; ".join(f"{x['id']}:{'not run' if not x.get('ran') else ('same' if x.get('same_direction_and_significance_as_paper') else ('differs' if x.get('same_direction_and_significance_as_paper') is False else 'n/a'))}" for x in R.get("robustness",[]))
    final_class=""
    if A and B:
        ca,cb=A.get("proposed_class"),B.get("proposed_class")
        if ca==cb: final_class=ca
        elif "D" in (ca,cb): final_class="UNRESOLVED (D needs both runs)"
        else: final_class="UNRESOLVED"
    conf=""
    if A and B: conf="low" if fl else min([A.get("confidence","low"),B.get("confidence","low")],key=["low","medium","high"].index)
    rows.append({"paper_id":p,"batch":r["batch"],"paper_title":r["paper_title"],"journal":r["journal"],"year":r["pub_year"],
        "paper_doi":"https://doi.org/"+r["paper_doi"],"dataset_doi":"https://doi.org/"+r["dataset_doi"],"field":r["subject"],
        "class_A":A.get("proposed_class") if A else "","class_B":B.get("proposed_class") if B else "","final_class":final_class,
        "confidence":conf,"confidence_reason_A":A.get("confidence_reason","") if A else "","confidence_reason_B":B.get("confidence_reason","") if B else "",
        "targets_A":tstr(A),"targets_B":tstr(B),"robustness_A":rstr(A),"robustness_B":rstr(B),
        "n_bugs_A":len(A.get("bugs",[])) if A else "","n_bugs_B":len(B.get("bugs",[])) if B else "",
        "time_min_A":A.get("time_minutes","") if A else "","time_min_B":B.get("time_minutes","") if B else "",
        "class_reason_A":A.get("class_reason","") if A else "","class_reason_B":B.get("class_reason","") if B else "",
        "ab_flags":" | ".join(fl)})
out=f"{REPO}/batches/batch{batch}_results.csv" if batch else f"{REPO}/master_results.csv"
with open(out,"w",newline="") as f:
    w=csv.DictWriter(f,list(rows[0].keys())); w.writeheader(); w.writerows(rows)
from collections import Counter
c=Counter(x["final_class"] or "pending" for x in rows)
json.dump({"counts":dict(c),"n":len(rows)},open(out.replace(".csv","_counts.json"),"w"),indent=1)
print(out, dict(c))
