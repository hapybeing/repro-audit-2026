"""Build the sampling frame: every Harvard Dataverse dataset released 2023-01-01..2026-12-31
that contains at least one R or Python code file (by Dataverse file content type).
Output: selection/frame_raw.csv (one row per dataset). Deterministic given the API state on the run date."""
import json, time, urllib.parse, urllib.request, csv, datetime, sys
BASE="https://dataverse.harvard.edu/api/search"
TYPES={"type/x-r-syntax":"R","text/x-r-notebook":"R","text/x-r-markdown":"R",
       "text/x-python":"Python","text/x-python-script":"Python","application/x-ipynb+json":"Python"}
DATE='dateSort:[2023-01-01T00:00:00Z TO 2026-12-31T23:59:59Z]'
import os, hashlib
from concurrent.futures import ThreadPoolExecutor
CACHE="selection/.api_cache"; os.makedirs(CACHE,exist_ok=True)
def page(ct,start):
    fn=f"{CACHE}/{hashlib.md5(ct.encode()).hexdigest()[:8]}_{start:06d}.json"
    if os.path.exists(fn): return json.load(open(fn))
    q=urllib.parse.urlencode([("q","*"),("type","file"),("fq",f'fileContentType:"{ct}"'),("fq",DATE),("per_page","1000"),("start",str(start)),("sort","date"),("order","asc")])
    for attempt in range(5):
        try:
            d=json.load(urllib.request.urlopen(urllib.request.Request(BASE+"?"+q,headers={"User-Agent":"repro-audit-2026 (research; github.com/hapybeing)"}),timeout=120))["data"]
            json.dump(d,open(fn,"w")); print(ct,start,file=sys.stderr); return d
        except Exception as e:
            print("retry",e,file=sys.stderr); time.sleep(5)
    raise SystemExit("failed "+ct+str(start))
jobs=[]
for ct in TYPES:
    tot=page(ct,0)["total_count"]
    jobs+=[(ct,s) for s in range(0,tot,1000)]
with ThreadPoolExecutor(6) as ex: results=list(ex.map(lambda j:(j[0],page(*j)),jobs))
ds={}
for ct,d in results:
    lang=TYPES[ct]
    for it in d["items"]:
        pid=it.get("dataset_persistent_id")
        if not pid: continue
        r=ds.setdefault(pid,{"dataset_doi":pid.replace("doi:",""),"title":it.get("dataset_name",""),"link":"https://doi.org/"+pid.replace("doi:",""),"langs":set(),"n_code_files":0,"any_restricted_code":False})
        r["langs"].add(lang); r["n_code_files"]+=1
        if it.get("restricted"): r["any_restricted_code"]=True
rows=sorted(ds.values(),key=lambda r:r["dataset_doi"])
with open("selection/frame_raw.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(["dataset_doi","title","link","code_language","n_code_files","any_restricted_code"])
    for r in rows: w.writerow([r["dataset_doi"],r["title"],r["link"],"+".join(sorted(r["langs"])),r["n_code_files"],r["any_restricted_code"]])
json.dump({"built_utc":datetime.datetime.utcnow().isoformat()+"Z","n_datasets":len(rows),"query_date_filter":DATE,"content_types":TYPES},open("selection/frame_meta.json","w"),indent=1)
print("datasets",len(rows))
