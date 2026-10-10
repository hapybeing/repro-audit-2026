import json,re,subprocess,datetime,urllib.request,hashlib
now=lambda: datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
out=[]
url="https://dataverse.harvard.edu/api/datasets/:persistentId/?persistentId=doi:10.7910/DVN/914AN0"
req=urllib.request.Request(url,headers={"User-Agent":"repro-audit-2026"})
t=now(); r=urllib.request.urlopen(req); body=r.read(); st=r.status
d=json.loads(body)["data"]["latestVersion"]
names=[(f.get("directoryLabel","") + "/" + f["dataFile"]["filename"]).lstrip("/") for f in d["files"]]
out.append(f"[{t}] GET {url} -> HTTP {st}, {len(names)} files: {names}")
tarlist=subprocess.run(["tar","-tJf","deposit/Replication_IO.tar.xz"],capture_output=True,text=True).stdout.split()
t2=now(); out.append(f"[{t2}] tar -tJf Replication_IO.tar.xz -> {len(tarlist)} entries")
for q in ["LICENSE","front_ref.RDS","fronts_ref.RDS"]:
    out.append(f"  query '{q}': dataverse hits={sum(q.lower() in n.lower() for n in names)}, tar hits={sum(q.lower() in n.lower() for n in tarlist)}")
code=open("deposit/code/run2_main.R").read()+open("deposit/code/master.R").read()+open("deposit/code/run1_setup.R").read()
reads=sorted(set(re.findall(r'(?:readRDS|source)\("([^"]+)"\)',code)))
out.append("Files read by code (readRDS/source calls):")
for p in reads:
    base=p.split("/")[-1]
    dv=any(n.endswith(base) and n.split("/")[0]==p.split("/")[0] for n in names)
    tr=any(n.endswith(p) for n in tarlist)
    out.append(f"  {p}: in Dataverse (same dir/name)={dv}; in tar={tr}")
open("read_check.txt","w").write("\n".join(out)+"\n"); print("\n".join(out))
