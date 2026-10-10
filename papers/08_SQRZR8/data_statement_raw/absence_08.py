"""Repeatable searches for data_preparation_rep.R (named in ReadMe.txt of doi:10.7910/DVN/SQRZR8, not in the file list)."""
import json, datetime, urllib.request, urllib.parse, urllib.error
UA={"User-Agent":"repro-audit-2026","Accept":"application/json"}
import subprocess
def now(): return subprocess.check_output(["date","-u","+%Y-%m-%dT%H:%M:%SZ"]).decode().strip()
def get(url):
    t=now()
    try:
        r=urllib.request.urlopen(urllib.request.Request(url,headers=UA),timeout=60); return t,r.status,r.read().decode("utf-8","replace")
    except urllib.error.HTTPError as e: return t,e.code,""
    except Exception as e: return t,"error: "+type(e).__name__,""
R=[]
def dv(q,extra,label):
    url="https://dataverse.harvard.edu/api/search?"+urllib.parse.urlencode([("q",q),("per_page","100")]+extra)
    t,st,b=get(url); tot=None; hits=[]
    if st==200:
        d=json.loads(b)["data"]; tot=d["total_count"]
        hits=[{"name":i.get("name"),"dataset":i.get("dataset_name"),"doi":i.get("dataset_persistent_id") or i.get("global_id")} for i in d["items"]]
    R.append({"source":"Harvard Dataverse Search API","query":q,"params":extra,"url":url,"utc":t,"http":st,"total_results":tot,"items":hits,"label":label})
dv('fileName:"data_preparation_rep.R"',[("type","file")],"exact file name, all of Harvard Dataverse")
dv('data_preparation_rep',[("type","file")],"free text, files")
dv('"Knowing is Disturbing"',[("type","dataset")],"datasets with the article title")
dv('Guo Kostka digital control',[("type","dataset")],"datasets by authors/topic")
# all versions of the deposit
url="https://dataverse.harvard.edu/api/datasets/:persistentId/versions?persistentId=doi:10.7910/DVN/SQRZR8"
t,st,b=get(url); vers=[]
if st==200:
    for v in json.loads(b)["data"]:
        vers.append({"version":f'{v.get("versionNumber")}.{v.get("versionMinorNumber")}',"state":v.get("versionState"),"files":[f["dataFile"]["filename"] for f in v.get("files",[])]})
R.append({"source":"Harvard Dataverse dataset versions API","query":"all versions of doi:10.7910/DVN/SQRZR8","url":url,"utc":t,"http":st,"total_results":len(vers),"items":vers,"label":"does any version list data_preparation_rep.R"})
json.dump(R,open("absence_searches.json","w"),indent=1)
for r in R: print(r["utc"],r["http"],r["total_results"],r["query"],"|",[ (i.get("name") or i.get("version"), i.get("dataset") or i.get("files")) for i in r["items"]][:10])
