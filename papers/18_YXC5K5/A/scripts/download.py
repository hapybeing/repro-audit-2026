# Download every file of doi:10.7910/DVN/YXC5K5 (v1.0) per file, verify md5 vs Dataverse metadata, write sha256.
import json, hashlib, urllib.request, os, sys
OUT = "/workspace/audit_runs/18_YXC5K5/A/data"
UA = {"User-Agent": "repro-audit-2026"}
def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120).read()
meta = json.loads(get("https://dataverse.harvard.edu/api/datasets/:persistentId/versions/:latest?persistentId=doi:10.7910/DVN/YXC5K5"))
files = meta["data"]["files"]
rows = []
for f in files:
    df = f["dataFile"]; fid = df["id"]
    tab = df.get("contentType") == "text/tab-separated-values" and "originalFileName" in df
    name = df.get("originalFileName") if tab else df["filename"]
    url = f"https://dataverse.harvard.edu/api/access/datafile/{fid}" + ("?format=original" if tab else "")
    b = get(url)
    md5 = hashlib.md5(b).hexdigest()
    open(os.path.join(OUT, name), "wb").write(b)
    rows.append(dict(id=fid, name=name, url=url, bytes=len(b), md5_ok=(md5 == df["md5"]), sha256=hashlib.sha256(b).hexdigest()))
json.dump(dict(version=meta["data"]["versionNumber"], n=len(rows), files=rows), open("outputs/downloads.json", "w"), indent=1)
with open("checksums.sha256", "w") as fh:
    for r in sorted(rows, key=lambda r: r["name"]): fh.write(f"{r['sha256']}  {r['name']}\n")
print(len(rows), "files; md5 all ok:", all(r["md5_ok"] for r in rows), "version", meta["data"]["versionNumber"])
