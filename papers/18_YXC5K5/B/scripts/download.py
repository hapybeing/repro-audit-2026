# Re-download every file of doi:10.7910/DVN/YXC5K5 via the public Dataverse API (no sign-in), check md5 vs metadata, write sha256.
import json, urllib.request, hashlib, os, sys
S="/workspace/audit_runs/18_YXC5K5/B/data"; UA={"User-Agent":"repro-audit-2026"}
meta=json.load(urllib.request.urlopen(urllib.request.Request("https://dataverse.harvard.edu/api/datasets/:persistentId/?persistentId=doi:10.7910/DVN/YXC5K5",headers=UA)))
files=meta["data"]["latestVersion"]["files"]
json.dump(meta,open(os.path.join(os.path.dirname(S),"dataverse_meta.json"),"w"))
out=[]
for f in files:
    df=f["dataFile"]; fid=df["id"]; name=df["filename"]
    url=f"https://dataverse.harvard.edu/api/access/datafile/{fid}"
    if name.endswith(".tab"):
        name=df.get("originalFileName",name); url+="?format=original"
    b=urllib.request.urlopen(urllib.request.Request(url,headers=UA)).read()
    open(os.path.join(S,name),"wb").write(b)
    md5=hashlib.md5(b).hexdigest(); ok= md5==df["md5"]
    out.append((hashlib.sha256(b).hexdigest(),name,fid,url,ok))
    if not ok: print("MD5 MISMATCH",name,file=sys.stderr)
with open("/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/18_YXC5K5/B/checksums.sha256","w") as fh:
    for s,n,_,_,_ in sorted(out,key=lambda x:x[1]): fh.write(f"{s}  {n}\n")
with open("/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/18_YXC5K5/B/outputs/download_manifest.tsv","w") as fh:
    fh.write("datafile_id\tfile\turl\tmd5_matches_metadata\tsha256\n")
    for s,n,i,u,ok in sorted(out,key=lambda x:x[1]): fh.write(f"{i}\t{n}\t{u}\t{ok}\t{s}\n")
print(len(out),"files; all md5 ok:",all(o[4] for o in out), "version", meta["data"]["latestVersion"]["versionNumber"])
