"""Scan every file in the fresh agent-A download of doi:10.7910/DVN/SINIYU (and the members of its tar.gz archives)
for anything that could supply the module `interp_radar` or Table 1 volume-matching code.
Hit rule: a file name containing 'interp_radar', a Fortran/f2py/compiled extension file (.f, .f90, .F90, .pyf, .so, .pyd),
or a code file whose text contains 'interp_radar' outside an import line, or contains a volume-matching keyword."""
import os, tarfile, json, re, sys
D = "/workspace/audit_runs/20_SINIYU/A/data"
out = sys.argv[1]
ext_hit = re.compile(r"\.(f|f90|F90|F|pyf|so|pyd|for)$")
kw = re.compile(r"vmm|warren|corrcoef|pearson|\.corr\(|volume.?match", re.I)
rec = {"files": [], "import_lines": [], "fortran_or_binary_modules": [], "name_hits": [], "volume_matching_keyword_hits": []}
def scan_text(name, text):
    for i, line in enumerate(text.splitlines(), 1):
        if "interp_radar" in line and line.strip().startswith(("from", "import")):
            rec["import_lines"].append({"file": name, "line": i, "text": line.strip()})
        if kw.search(line):
            rec["volume_matching_keyword_hits"].append({"file": name, "line": i, "text": line.strip()[:120]})
for fn in sorted(os.listdir(D)):
    p = os.path.join(D, fn)
    if os.path.isdir(p):
        continue
    rec["files"].append(fn)
    if "interp_radar" in fn.lower(): rec["name_hits"].append(fn)
    if ext_hit.search(fn): rec["fortran_or_binary_modules"].append(fn)
    if fn.endswith(".py"):
        scan_text(fn, open(p, encoding="utf-8", errors="replace").read())
    if fn.endswith(".tar.gz"):
        with tarfile.open(p) as t:
            for m in t.getmembers():
                if not m.isfile(): continue
                name = fn + ":" + m.name
                rec["files"].append(name)
                if "interp_radar" in m.name.lower(): rec["name_hits"].append(name)
                if ext_hit.search(m.name): rec["fortran_or_binary_modules"].append(name)
                if m.name.endswith((".py", ".ncl")):
                    scan_text(name, t.extractfile(m).read().decode("utf-8", errors="replace"))
rec["n_files_scanned"] = len(rec["files"])
rec["module_found_in_deposit"] = bool(rec["name_hits"] or rec["fortran_or_binary_modules"])
json.dump(rec, open(out, "w"), indent=1)
print(json.dumps({k: v for k, v in rec.items() if k != "files"}, indent=1))
