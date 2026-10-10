"""Scan the paper full text (Europe PMC XML) and supplementary docx/pptx text for any mention of 2XWT / TSH receptor / K1-70
and record the context, to establish whether the paper reports any number for this dataset. usage: paper_scan.py PAPERDIR OUTDIR"""
import re, sys, os, json, zipfile, glob
P, OUT = sys.argv[1:3]
x = open(os.path.join(P, "fulltext.xml"), encoding="utf8").read()
t = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", x))
res = {"fulltext_hits": [], "supp_hits": {}, "table1_row_2XWT": None}
for m in re.finditer(r"2XWT|TSH|K1-70", t, re.I):
    res["fulltext_hits"].append(t[max(0, m.start() - 60): m.end() + 80])
m = re.search(r"2XWT\s*b\s*(\d+)\s*(TSH receptor in complex with autoantibody K1-70 mAb)\s*(\d+)", t)
if m: res["table1_row_2XWT"] = {"n_seeds": int(m.group(1)), "description": m.group(2), "duration_ns": int(m.group(3)), "footnote": "b"}
fb = re.search(r"b\s*Free binding energy[^.]*\.", t); res["table1_footnote_b"] = fb.group(0) if fb else None
res["figures_mentioning_PDB"] = sorted(set(re.findall(r"PDB\s+(\w{4})", t)))
for f in glob.glob(os.path.join(P, "supp", "inner", "suppl_data", "*")):
    if not f.endswith((".docx", ".pptx")): continue
    z = zipfile.ZipFile(f); s = ""
    for n in z.namelist():
        if n.endswith(".xml") and ("word/document" in n or "ppt/slides/slide" in n):
            s += re.sub(r"<[^>]+>", " ", z.read(n).decode("utf8", "ignore"))
    s = re.sub(r"\s+", " ", s)
    res["supp_hits"][os.path.basename(f)] = {"n_chars": len(s), "hits_2XWT_TSH_K1-70": len(re.findall(r"2XWT|TSH|K1-70", s, re.I)),
                                             "n_embedded_images": len([n for n in z.namelist() if "/media/" in n])}
json.dump(res, open(os.path.join(OUT, "paper_scan.json"), "w"), indent=1)
print(json.dumps(res, indent=1))
