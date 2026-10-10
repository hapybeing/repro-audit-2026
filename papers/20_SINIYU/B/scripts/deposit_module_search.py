"""Agent B: search the whole deposit (every file and every archive member) for the
interp_radar module (source, compiled .so, or f2py signature file) and for any
Table 1 / volume-matching code. Also checks PyPI (an uncited location) by name.
Writes outputs/deposit_module_search.json. No analysis code is run."""
import json, os, re, tarfile, subprocess, datetime, urllib.request
DL = "/workspace/audit_runs/20_SINIYU/B/dl"
RAR = "/workspace/audit_runs/20_SINIYU/B/rarx"
out = {"run_utc": datetime.datetime.utcnow().isoformat() + "Z", "members": [], "name_hits": [], "content_hits": []}
name_pat = re.compile(r"interp_radar|\.f90$|\.f$|\.F90$|\.so$|\.pyf$|\.pyd$", re.I)
content_pat = re.compile(rb"interp_radar|volume.?match|warren|corrcoef|pearson|\.corr\(", re.I)
for fn in sorted(os.listdir(DL)):
    p = os.path.join(DL, fn)
    out["members"].append(fn)
    if name_pat.search(fn): out["name_hits"].append(fn)
    if fn.endswith(".tar.gz"):
        with tarfile.open(p) as t:
            for m in t.getmembers():
                full = fn + "::" + m.name
                out["members"].append(full)
                if name_pat.search(m.name): out["name_hits"].append(full)
                if m.isfile() and m.size < 5_000_000 and re.search(r"\.(py|ncl|txt|log|sh|f90|f)$", m.name):
                    data = t.extractfile(m).read()
                    for mm in set(content_pat.findall(data)):
                        out["content_hits"].append({"file": full, "match": mm.decode(errors="replace")})
    elif fn.endswith(".py"):
        data = open(p, "rb").read()
        for mm in set(content_pat.findall(data)):
            out["content_hits"].append({"file": fn, "match": mm.decode(errors="replace")})
    elif fn.endswith(".part1.rar"):
        lst = subprocess.run(["unrar-free", "-t", p], capture_output=True, text=True, cwd=DL)
        out["rar_listing"] = lst.stdout.strip().splitlines()[-6:]
for fn in os.listdir(RAR):
    out["members"].append("FY3G_PMR.rar::" + fn)
# PyPI by name (NOT a location the article cites; informational only)
for name in ["interp_radar", "interp-radar"]:
    try:
        r = urllib.request.urlopen(urllib.request.Request(f"https://pypi.org/pypi/{name}/json", headers={"User-Agent": "repro-audit-2026"}), timeout=30)
        out.setdefault("pypi", {})[name] = r.status
    except Exception as e:
        out.setdefault("pypi", {})[name] = str(e)
out["n_members"] = len(out["members"])
out["module_found"] = any("interp_radar" in h.lower() for h in out["name_hits"]) 
out["interp_radar_content_hits_are_only_imports_or_calls"] = all(h["match"].lower()=="interp_radar" for h in out["content_hits"] if "interp" in h["match"].lower())
json.dump(out, open("/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/20_SINIYU/B/outputs/deposit_module_search.json", "w"), indent=1)
print(json.dumps({k: out[k] for k in ["n_members", "name_hits", "content_hits", "module_found", "pypi"]}, indent=1))
