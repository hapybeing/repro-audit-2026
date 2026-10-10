#!/usr/bin/env python3
"""Agent A, paper 17_T1NXVQ: download the files listed in PREREG.md from Harvard Dataverse (public API, no sign-in).
Writes RUNDIR/replication/<deposit path>; the two deposited model files go to RUNDIR/deposited_models/ (comparison only).
Checks md5 against Dataverse and sha256 against PREREG.md; writes checksums to the A folder."""
import json, os, re, hashlib, subprocess, sys
REPO = "/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo"
P = f"{REPO}/papers/17_T1NXVQ"
RUN = "/workspace/audit_runs/17_T1NXVQ/A"
prereg = open(f"{P}/PREREG.md").read()
rows = re.findall(r"^\| `([^`]+)` \| (\d+) \| (\d+) \| ([0-9a-f]{64}) \|", prereg, re.M)
meta = {str(f["dataFile"]["id"]): f for f in json.load(open(f"{P}/data_statement_raw/dataverse_T1NXVQ.json"))["data"]["latestVersion"]["files"]}
out = []
ok = True
for path, fid, size, sha in rows:
    if path.startswith("data/models/"):
        dest = f"{RUN}/deposited_models/{os.path.basename(path)}"
    else:
        dest = f"{RUN}/replication/{path}"
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    url = f"https://dataverse.harvard.edu/api/access/datafile/{fid}" + ("?format=original" if path.endswith(".tab") else "")
    if not (os.path.exists(dest) and hashlib.sha256(open(dest, "rb").read()).hexdigest() == sha):
        subprocess.run(["curl", "-sL", "--retry", "3", "--max-time", "600", "-A", "repro-audit-2026", url, "-o", dest], check=True)
    b = open(dest, "rb").read()
    s = hashlib.sha256(b).hexdigest(); m = hashlib.md5(b).hexdigest()
    md5_dv = meta[fid]["dataFile"].get("md5") or meta[fid]["dataFile"]["checksum"]["value"]
    tab = path.endswith(".tab")
    match = (s == sha)
    ok &= match
    out.append(f"{s}  {os.path.relpath(dest, RUN)}  (datafile {fid}, {len(b)} bytes, sha256_matches_prereg={match}, md5_matches_dataverse={m == md5_dv}{', original format of ingested .tab' if tab else ''}) {url}")
open(f"{P}/A/checksums.sha256", "w").write("\n".join(out) + "\n")
print(len(rows), "files; all sha256 match PREREG:", ok)
