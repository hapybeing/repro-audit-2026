"""Run the authors' xvg2csv.py (Python 3 print fix only, diffs/xvg2csv.py.diff) on deposited .xvg files and compare
the result byte-for-byte with the deposited original CSVs behind the Dataverse .tab files. Also record the header
labels written and the Dataverse ingest variable names / case counts (from the DDI metadata) as evidence for code review.
usage: xvg_format_check.py RUNDIR RAWDIR OUTDIR"""
import subprocess, sys, os, shutil, json, hashlib, re
RUN, RAW, OUT = sys.argv[1:4]
res = {}
ddi = {"2xwt-rs3-310k-200ns-rmsd": "ddi_10835643.xml", "2xwt-rs3-400ns-310k-rmsd": "ddi_10835772.xml", "2xwt-rs3-400ns-310k-rmsf": "ddi_10835782.xml"}
for base in ddi:
    shutil.copy(os.path.join(RAW, base + ".xvg"), os.path.join(RUN, base + ".xvg"))
    p = subprocess.run([sys.executable, "xvg2csv.py", base + ".xvg"], cwd=RUN, capture_output=True, text=True)
    mine = open(os.path.join(RUN, base + ".csv"), "rb").read()
    dep = open(os.path.join(RAW, "deposited_" + base + ".csv"), "rb").read()
    xvg = open(os.path.join(RAW, base + ".xvg")).read().splitlines()
    x = open(os.path.join(RAW, ddi[base]), encoding="utf8").read()
    res[base] = {"stdout": p.stdout, "returncode": p.returncode, "identical_to_deposited": mine == dep,
                 "sha256_mine": hashlib.sha256(mine).hexdigest(), "first_line_written": mine.decode().splitlines()[0],
                 "data_rows_in_xvg": sum(1 for l in xvg if l and l[0] not in "#@"),
                 "xvg_axis_and_legend_lines": [l for l in xvg if l.startswith("@") and ("label" in l or l.startswith("@ s"))],
                 "dataverse_ingest_varnames": re.findall(r'<var [^>]*name="([^"]*)"', x),
                 "dataverse_ingest_caseQnty": int(re.search(r"<caseQnty>(\d+)", x).group(1))}
json.dump(res, open(os.path.join(OUT, "xvg_format_check.json"), "w"), indent=1)
print(json.dumps(res, indent=1))
