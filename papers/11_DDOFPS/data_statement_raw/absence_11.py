import json,urllib.request,urllib.parse,datetime
UA={"User-Agent":"repro-audit-2026","Accept":"application/json"}
import subprocess
import time
def now():
    g=time.gmtime(); return "%04d-%02d-%02dT%02d:%02d:%02dZ"%(g.tm_year,g.tm_mon,g.tm_mday,g.tm_hour,g.tm_min,g.tm_sec)
R=[]
def get(url):
    t=now()
    try:
        r=urllib.request.urlopen(urllib.request.Request(url,headers=UA),timeout=60); return t,r.status,r.read().decode()
    except urllib.error.HTTPError as e: return t,e.code,""
# 1 deposit file list
u="https://dataverse.harvard.edu/api/datasets/:persistentId/versions?persistentId=doi:10.7910/DVN/DDOFPS"
t,s,b=get(u); vs=json.loads(b)["data"]
names=sorted({f["dataFile"]["filename"] for v in vs for f in v["files"]})
for target in ["bd_doxa_programas.xlsx","bd_doxa_candidatos.xlsx"]:
    R.append({"source":"Dataverse DDOFPS all versions file list","query":f"exact filename {target}","url":u,"utc":t,"http":s,
              "total_results":len(names),"versions":[v["versionNumber"] for v in vs],"relevant_hits":[n for n in names if n==target],
              "near_matches":[n for n in names if n.startswith(target.split('.')[0])],
              "hit_rule":"a file with exactly this name in any version of the deposit"})
# 2 Dataverse search API (files, whole Harvard Dataverse)
for q in ['"bd_doxa_programas.xlsx"','"bd_doxa_candidatos.xlsx"','bd_doxa_programas','bd_doxa_candidatos','bd_doxa_programas_HGPE.xlsx (positive control)'.split(' ')[0],'HGPE_lei.xlsx']:
    u="https://dataverse.harvard.edu/api/search?"+urllib.parse.urlencode({"q":q,"type":"file","per_page":"100"})
    t,s,b=get(u); d=json.loads(b)["data"] if s==200 else {"total_count":None,"items":[]}
    R.append({"source":"Harvard Dataverse Search API (type=file)","query":q,"url":u,"utc":t,"http":s,"total_results":d["total_count"],
              "relevant_hits":[(i.get("name"),i.get("dataset_persistent_id"),i.get("file_id")) for i in d["items"]],
              "hit_rule":"a file named exactly bd_doxa_programas.xlsx or bd_doxa_candidatos.xlsx in any dataset"})
json.dump(R,open("/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/11_DDOFPS/data_statement_raw/absence_searches.json","w"),indent=1,ensure_ascii=False)
for r in R: print(r["query"],r["utc"],r["http"],r["total_results"],r["relevant_hits"],r.get("near_matches",""))
