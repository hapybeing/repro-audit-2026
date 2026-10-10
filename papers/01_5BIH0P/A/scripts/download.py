"""Download selected small files from DVN/5BIH0P, verify Dataverse checksum, record sha256."""
import json, hashlib, subprocess, sys, os
RAW = "/workspace/audit_runs/01_5BIH0P/A/raw"
meta = json.load(open(os.path.join(RAW, "dataset_meta.json")))["data"]["latestVersion"]
want = set(sys.argv[1:])
rows = []
for f in meta["files"]:
    df = f["dataFile"]
    if df["filename"] not in want: continue
    out = os.path.join(RAW, "files", df["filename"])
    os.makedirs(os.path.dirname(out), exist_ok=True)
    if not os.path.exists(out):
        subprocess.run(["curl", "-sSfL", "-A", "repro-audit-2026", "-o", out,
                        f"https://dataverse.harvard.edu/api/access/datafile/{df['id']}?format=original"], check=True)
    b = open(out, "rb").read()
    ck = df.get("checksum", {})
    h = hashlib.new(ck["type"].lower().replace("-", ""), b).hexdigest() if ck else None
    ok = (h == ck.get("value")) if ck else None
    print(df["id"], df["filename"], len(b), "dv_checksum_ok=", ok)
    if ok is False: sys.exit("checksum mismatch " + df["filename"])
