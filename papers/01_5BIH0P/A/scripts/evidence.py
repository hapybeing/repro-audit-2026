"""Evidence for 'no paper target is reproducible from DVN/5BIH0P': paper text scan + deposit inventory +
authors' xvg2csv.py re-run comparison. Writes outputs/paper_evidence.json, deposit_inventory.json, xvg2csv_check.json."""
import json, re, os, hashlib, glob
A = "/workspace/audit_runs/01_5BIH0P/A"
OUT = "/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/01_5BIH0P/A/outputs"
x = open(f"{A}/raw/paper_fulltext.xml", encoding="utf-8").read()
t = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", x))
def ctx(m, w=160): return t[max(0, m.start()-w): m.end()+w]
pe = {"source": "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC10950042/fullTextXML",
      "mentions_2XWT": [ctx(m) for m in re.finditer(r"2XWT", t, re.I)],
      "computed_numbers_in_text": {k: [ctx(m) for m in re.finditer(re.escape(k), t)][:1] for k in
                                   ["0.36 nm", "1.52 nm", "−114.2", "−126.3", "about 30%"]},
      "complexes_with_computed_numbers": {k: len(re.findall(k, t)) for k in ["5DK3", "6UMT"]},
      "mentions_xtc": len(re.findall(r"xtc", t, re.I)),
      "abstract_claim_trajectories": [ctx(m) for m in re.finditer(r"MD trajectories are freely available", t)],
      "table1_note": "2XWT appears only as a Table 1 row (seeds=5, duration=200 ns, footnote b: free binding energy calculations available)"}
json.dump(pe, open(f"{OUT}/paper_evidence.json", "w"), indent=1, ensure_ascii=False)

meta = json.load(open(f"{A}/raw/dataset_meta.json"))["data"]["latestVersion"]
names = sorted(f["dataFile"]["filename"] for f in meta["files"])
ext = {}
for n in names:
    e = n.split(".")[-1] if "." in n else ""
    ext[e] = ext.get(e, 0) + 1
inv = {"dataset": "doi:10.7910/DVN/5BIH0P", "version": f'{meta["versionNumber"]}.{meta["versionMinorNumber"]}',
       "n_files": len(names), "total_bytes": sum(f["dataFile"]["filesize"] for f in meta["files"]),
       "restricted_files": [f["dataFile"]["filename"] for f in meta["files"] if f.get("restricted")],
       "extension_counts": ext,
       "xtc_files": [n for n in names if n.endswith(".xtc")],
       "trr_files": [n for n in names if n.endswith(".trr")],
       "pdb_snapshots": [n for n in names if re.search(r"\d+ns\.pdb$", n)],
       "python_files": [n for n in names if n.endswith(".py")],
       "shell_files": [n for n in names if n.endswith(".sh")],
       "files_named_in_analysis_headers_but_absent": [n for n in ["dynamic-nopbc.xtc", "dynamic-nopbc-2.xtc", "system_reduced.xtc", "COM_traj_0.xtc", "md_0_10.xtc"] if n not in names],
       "filenames_with_pdb_id_prefix_other_than_2xwt": [n for n in names if re.match(r"^\d[a-z0-9]{3}-", n.lower()) and not n.lower().startswith("2xwt")],
       "dataset_title": [f["value"] for f in meta["metadataBlocks"]["citation"]["fields"] if f["typeName"] == "title"][0]}
json.dump(inv, open(f"{OUT}/deposit_inventory.json", "w"), indent=1)

chk = {}
for csvf in sorted(glob.glob(f"{A}/run_xvg/*.csv")):
    b = os.path.basename(csvf)[:-4]
    tab = f"{A}/raw/files/{b}.tab"
    h1 = hashlib.sha256(open(csvf, "rb").read()).hexdigest(); h2 = hashlib.sha256(open(tab, "rb").read()).hexdigest()
    first = open(csvf).readline().strip()
    xv = open(f"{A}/run_xvg/{b}.xvg").read()
    chk[b] = {"rerun_csv_sha256": h1, "deposited_tab_original_sha256": h2, "byte_identical": h1 == h2,
              "csv_header_line": first, "xvg_xaxis_label": (re.findall(r'xaxis\s+label "([^"]*)"', xv) or [None])[0],
              "xvg_subtitle": (re.findall(r'@ subtitle "([^"]*)"', xv) or [None])[0],
              "xvg_legend_lines": len(re.findall(r"^@ s\d+ legend", xv, re.M)),
              "gmx_command": (re.findall(r"#   (gmx .*)", xv) or [None])[0],
              "first_data_row": [l for l in xv.splitlines() if l and l[0] not in "#@"][0].split(),
              "last_data_row": [l for l in xv.splitlines() if l and l[0] not in "#@"][-1].split()}
json.dump(chk, open(f"{OUT}/xvg2csv_check.json", "w"), indent=1)
print(json.dumps({"inv": inv, "xvg": chk, "n2xwt": len(pe["mentions_2XWT"])}, indent=1))
