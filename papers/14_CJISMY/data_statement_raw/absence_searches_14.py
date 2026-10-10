"""Repeatable searches for files read by deposited 14_CJISMY scripts but absent from doi:10.7910/DVN/CJISMY.
Public APIs only, no sign-in. Hit rule: a file whose name equals the missing file name (case-insensitive), in a
dataset/repository linked to the authors or this article, counts as a hit."""
import json, datetime, urllib.request, urllib.parse, urllib.error
UA={"User-Agent":"repro-audit-2026","Accept":"application/json"}
R=[]
def now(): return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
def get(u):
    t=now()
    try:
        r=urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=60); return t,r.status,r.read().decode("utf-8","replace")
    except urllib.error.HTTPError as e: return t,e.code,""
    except Exception as e: return t,"error: "+type(e).__name__,""
missing=["helper_functions_eo2_extraction_analysis.R","GeoEPR-2019.csv","EPR_merged.csv","gpw_v4_population_count_rev11_2000_30_min.tif","data.csv"]
# 1. Harvard Dataverse file search, whole installation
for fn in missing:
    u="https://dataverse.harvard.edu/api/search?"+urllib.parse.urlencode({"q":f'fileName:"{fn}"',"type":"file","per_page":"100"})
    t,s,b=get(u); tot=None; rel=[]
    if s==200:
        d=json.loads(b)["data"]; tot=d["total_count"]
        rel=[{"file":i["name"],"dataset":i.get("dataset_name"),"doi":i.get("dataset_persistent_id")} for i in d["items"]
             if i["name"].lower()==fn.lower() and any(k in (i.get("dataset_name") or "").lower() for k in ["intra-ethnic","self-determination","epr-o","gremler"])]
    R.append({"source":"Harvard Dataverse Search API","query":f'fileName:"{fn}" type=file',"url":u,"utc":t,"http":s,"total_results":tot,"relevant_hits":rel})
# 2. Same Dataverse, datasets by author name
u="https://dataverse.harvard.edu/api/search?"+urllib.parse.urlencode({"q":'authorName:"Gremler"',"type":"dataset","per_page":"100"})
t,s,b=get(u); tot=None; rel=[]
if s==200:
    d=json.loads(b)["data"]; tot=d["total_count"]; rel=[{"name":i["name"],"doi":i.get("global_id")} for i in d["items"]]
R.append({"source":"Harvard Dataverse Search API","query":'authorName:"Gremler" type=dataset',"url":u,"utc":t,"http":s,"total_results":tot,"relevant_hits":rel,"note":"lists every dataset by this author; relevant if a second deposit could hold the missing files"})
# 3. OSF project cited in the article (preregistration) file list
u="https://api.osf.io/v2/nodes/8z6ng/files/osfstorage/"
t,s,b=get(u); tot=None; rel=[]
if s==200:
    d=json.loads(b); tot=d["links"]["meta"]["total"]; rel=[x["attributes"]["name"] for x in d["data"]]
R.append({"source":"OSF API (node cited in article footnote 1)","query":"osfstorage root listing of node 8z6ng","url":u,"utc":t,"http":s,"total_results":tot,"relevant_hits":[n for n in rel if n.lower() in [m.lower() for m in missing]],"note":"all files: "+", ".join(rel)})
u="https://api.osf.io/v2/nodes/8z6ng/children/"
t,s,b=get(u); tot=None
if s==200: tot=json.loads(b)["links"]["meta"]["total"]
R.append({"source":"OSF API","query":"child components of node 8z6ng","url":u,"utc":t,"http":s,"total_results":tot,"relevant_hits":[]})
# 4. GitHub repository search (code search needs sign-in, so not used)
for q in ["helper_functions_eo2_extraction_analysis","EPR-O disagreement self-determination","Gremler EPR"]:
    u="https://api.github.com/search/repositories?"+urllib.parse.urlencode({"q":q})
    t,s,b=get(u); tot=None; rel=[]
    if s==200:
        d=json.loads(b); tot=d["total_count"]; rel=[i["full_name"] for i in d["items"][:20]]
    R.append({"source":"GitHub repository search API (unauthenticated)","query":q,"url":u,"utc":t,"http":s,"total_results":tot,"relevant_hits":rel,"note":"relevant_hits lists returned repo names (first 20) for inspection"})
# 5. DataCite record of the EPR-O DOI the article names
u="https://api.datacite.org/dois/10.7802/2767"
t,s,b=get(u); att={}
if s==200: att=json.loads(b)["data"]["attributes"]
R.append({"source":"DataCite API","query":"doi 10.7802/2767","url":u,"utc":t,"http":s,"total_results":1 if s==200 else 0,"relevant_hits":[],"note":f"title={att.get('titles')}, publisher={att.get('publisher')}, url={att.get('url')}"})
json.dump(R,open("/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/14_CJISMY/data_statement_raw/absence_searches.json","w"),indent=1)
for r in R: print(r["utc"],r["source"],"|",r["query"],"|",r["http"],"|",r["total_results"],"|",r["relevant_hits"],"|",r.get("note","")[:200])
