"""Seeded random order + scripted eligibility screening (PROTOCOL.md sections 2-4).
Reads selection/frame_raw.csv; writes selection/order.csv, selection/screening.csv, selection/selected.csv."""
import csv, json, re, sys, time, urllib.request, urllib.parse, datetime
import numpy as np
SEED=20261009; N_TARGET=25; MAX_BYTES=5*1024**3
UA={"User-Agent":"repro-audit-2026 (research; github.com/hapybeing/repro-audit-2026)"}
BAD_EXT=(".do",".ado",".m",".sps",".sas")
import os, hashlib, difflib
CACHE="selection/.api_cache_screen"; os.makedirs(CACHE,exist_ok=True)
class LookupFailed(Exception): pass
def get(url):
    fn=CACHE+"/"+hashlib.md5(url.encode()).hexdigest()+".json"
    if os.path.exists(fn): return json.load(open(fn))
    for a in range(8):
        try:
            d=json.load(urllib.request.urlopen(urllib.request.Request(url,headers=UA),timeout=60)); json.dump(d,open(fn,"w")); return d
        except urllib.error.HTTPError as e:
            if e.code==404: json.dump(None,open(fn,"w")); return None
            time.sleep(5*(a+1))
        except Exception: time.sleep(5*(a+1))
    raise LookupFailed(url)
def clean_title(t):
    t=re.sub(r'^\s*(replication|reproduction)\s+(data|materials|files|code|package)?\s*(and code|& code)?\s*(for|of)?\s*:?\s*','',t,flags=re.I)
    return t.strip().strip('"\'“”').strip()
def ntitle(t): return re.sub(r"[^a-z0-9 ]","",re.sub(r"<[^>]+>","",(t or "").lower())).strip()
def crossref_match(cands):
    """CHANGELOG #2: when Dataverse lists no DOI, find it on Crossref by title; accept only similarity >= 0.90."""
    for t in cands:
        if len(ntitle(t))<15: continue
        q=urllib.parse.urlencode({"query.bibliographic":t,"rows":"3","filter":"from-pub-date:2022-06-01,type:journal-article"})
        d=get("https://api.crossref.org/works?"+q)
        for it in (d or {}).get("message",{}).get("items",[]):
            ct=(it.get("title") or [""])[0]
            if difflib.SequenceMatcher(None,ntitle(ct),ntitle(t)).ratio()>=0.90: return it["DOI"].lower()
    return None
allrows=list(csv.DictReader(open("selection/frame_raw.csv")))
# CHANGELOG_METHOD 2026-10-09 #1: keep only datasets hosted on Harvard Dataverse (DOI prefix 10.7910); others are harvested copies.
rows=sorted([r for r in allrows if r["dataset_doi"].startswith("10.7910/")],key=lambda r:r["dataset_doi"])
with open("candidates.csv","w",newline="") as f:
    w=csv.DictWriter(f,list(allrows[0].keys())); w.writeheader(); w.writerows(rows)
perm=np.random.default_rng(SEED).permutation(len(rows))
order=[rows[i] for i in perm]
with open("selection/order.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(["rank","dataset_doi","title","code_language"])
    for k,r in enumerate(order,1): w.writerow([k,r["dataset_doi"],r["title"],r["code_language"]])
def norm_doi(s):
    m=re.search(r"10\.\d{4,9}/[^\s\"<>]+",s or ""); return m.group(0).rstrip(".,;)").lower() if m else None
scr=[]; sel=[]
F=["rank","dataset_doi","dataset_link","title","code_language","subject","paper_doi","paper_title","journal","pub_year","E1_article","E2_open_text","E3_no_restricted","E4_no_stata_matlab_spss_sas","E5_size_ok","E6_licence","licence","total_bytes","eligible","reason"]
for k,r in enumerate(order,1):
    if len(sel)>=N_TARGET: break
    rec={f:"" for f in F}; rec.update(rank=k,dataset_doi=r["dataset_doi"],dataset_link=r["link"],title=r["title"],code_language=r["code_language"])
    d=get("https://dataverse.harvard.edu/api/datasets/:persistentId/?persistentId=doi:"+urllib.parse.quote(r["dataset_doi"]))
    reasons=[]
    if not d: rec.update(eligible=False,reason="dataset metadata not retrievable"); scr.append(rec); continue
    v=d["data"]["latestVersion"]; cit={f["typeName"]:f["value"] for f in v["metadataBlocks"]["citation"]["fields"]}
    rec["subject"]="; ".join(cit.get("subject",[]))
    lic=v.get("license",{}); rec["licence"]=lic.get("name","") if isinstance(lic,dict) else str(lic)
    files=v.get("files",[]); names=[(f.get("directoryLabel","")+"/"+f["dataFile"].get("filename","")).lower() for f in files]
    tot=sum(f["dataFile"].get("filesize",0) for f in files); rec["total_bytes"]=tot
    rec["E3_no_restricted"]=not any(f.get("restricted") for f in files)
    rec["E4_no_stata_matlab_spss_sas"]=not any(n.endswith(BAD_EXT) for n in names)
    rec["E5_size_ok"]=tot<=MAX_BYTES
    rec["E6_licence"]=not v.get("termsOfAccess")  # no access-request terms; redistribution decided per paper from licence
    if not rec["licence"]: rec["licence"]="custom terms: "+(v.get("termsOfUse","")[:120].replace("\n"," "))
    pdoi=None
    for p in cit.get("publication",[]):
        for key in ("publicationIDNumber","publicationURL","publicationCitation"):
            if key in p: pdoi=pdoi or norm_doi(p[key]["value"])
    if not pdoi:
        cands=[clean_title(r["title"])]
        for p in cit.get("publication",[]):
            if "publicationCitation" in p:
                m=re.findall(r'["“]([^"”]{15,})["”]',p["publicationCitation"]["value"]); cands+=m
        pdoi=crossref_match(cands)
        if pdoi: rec["reason"]="paper DOI found via Crossref title match"
    rec["paper_doi"]=pdoi or ""
    e1=e2=False
    if pdoi:
        oa=get("https://api.openalex.org/works/doi:"+urllib.parse.quote(pdoi))
        if oa:
            rec["paper_title"]=oa.get("title",""); rec["pub_year"]=oa.get("publication_year","")
            src=((oa.get("primary_location") or {}).get("source") or {})
            rec["journal"]=src.get("display_name","")
            e1=(src.get("type")=="journal") and oa.get("type") in ("article","review","letter") and 2023<=(oa.get("publication_year") or 0)<=2026
            e2=bool((oa.get("open_access") or {}).get("is_oa"))
        else: reasons.append("paper DOI not found in OpenAlex")
    else: reasons.append("no related-publication DOI")
    rec["E1_article"]=e1; rec["E2_open_text"]=e2
    checks=["E1_article","E2_open_text","E3_no_restricted","E4_no_stata_matlab_spss_sas","E5_size_ok","E6_licence"]
    reasons+= [c for c in checks if not rec[c]]
    rec["eligible"]=all(rec[c] for c in checks); rec["reason"]="; ".join(([rec["reason"]] if rec["reason"] else [])+reasons)
    scr.append(rec)
    if rec["eligible"]: sel.append(rec)
    print(k,rec["eligible"],rec["reason"],file=sys.stderr); time.sleep(0.1)
subj=set(s["subject"].split("; ")[0] for s in sel)
with open("selection/screening.csv","w",newline="") as f:
    w=csv.DictWriter(f,F); w.writeheader(); w.writerows(scr)
with open("selection/selected.csv","w",newline="") as f:
    w=csv.DictWriter(f,["audit_pos","batch"]+F); w.writeheader()
    for i,s in enumerate(sel,1): w.writerow(dict(audit_pos=i,batch=(i-1)//5+1,**s))
json.dump({"seed":SEED,"run_utc":datetime.datetime.now(datetime.UTC).isoformat()+"Z","n_screened":len(scr),"n_selected":len(sel),"primary_subjects":sorted(subj)},open("selection/selection_meta.json","w"),indent=1)
print("screened",len(scr),"selected",len(sel),"subjects",subj)
