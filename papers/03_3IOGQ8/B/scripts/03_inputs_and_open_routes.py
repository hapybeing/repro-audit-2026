"""Agent B: inventory of the deposit vs. inputs the code needs, and a search for any open,
sign-in-free source of the Byonic PSM export (PRIDE, ProteomeXchange, MassIVE, paper, preprint, SI).
Usage: python3 03_inputs_and_open_routes.py <scratch_dl_dir> <out_dir>"""
import json, re, sys, urllib.request, urllib.parse, datetime
dl, out = sys.argv[1], sys.argv[2]
UA = {"User-Agent": "repro-audit-2026"}
def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=90).read()

# 1. Deposit file list
meta = json.load(open(f"{dl}/dataset_meta.json"))["data"]["latestVersion"]
files = [{"id": f["dataFile"]["id"], "name": f["dataFile"]["filename"], "bytes": f["dataFile"]["filesize"],
          "md5": f["dataFile"].get("md5"), "restricted": f.get("restricted"),
          "description": f.get("description", "")} for f in meta["files"]]
desc = [x for x in meta["metadataBlocks"]["citation"]["fields"] if x["typeName"] == "dsDescription"][0]["value"][0]["dsDescriptionValue"]["value"]
pc = json.load(open(f"{out}/parse_check.json"))
names = [f["name"] for f in files]
needed = [
  {"input": "Byonic_results.csv (Byonic PSM export)", "code_line": 498,
   "in_deposit": "Byonic_results.csv" in names or any(n.lower().endswith(".csv") for n in names)},
  {"input": "file1/2/3.mzML.gz (spectra, converted from Thermo RAW)", "code_line": 671,
   "in_deposit": any("mzml" in n.lower() for n in names),
   "note": "RAW files are deposited; open converter ThermoRawFileParser exists, but spectra are only read for scans listed in the Byonic export, so they are useless without it"},
  {"input": "MS.Alias.name values identifying each experiment", "code_line": 581,
   "in_deposit": False, "note": "placeholders 'your_ms_experiment_1' for all three experiments; real values live only in the Byonic export"},
]
# 2. Paper, preprint, SI text: repository accession mentions
pat = re.compile(r"PXD\d{6}|MSV\d{9}|JPST\d+|IPX\d+|PDC\d+|massive\.ucsd|proteomexchange|ebi\.ac\.uk/pride|zenodo|figshare|github\.com", re.I)
texts = {"paper_fulltext_PMC11638967": f"{dl}/paper_fulltext.xml", "preprint_fulltext_PMC11451751": f"{dl}/preprint_fulltext.xml",
         "SI_pdf_text": f"{dl}/si/si.txt"}
mentions = {k: sorted(set(m.group(0) for m in pat.finditer(open(v, errors="ignore").read()))) for k, v in texts.items()}
dv_mentions = {k: len(re.findall("3IOGQ8", open(v, errors="ignore").read())) for k, v in texts.items()}
# 3. PRIDE and ProteomeXchange keyword searches (live)
kws = ["sortase", "Whedon", "circular engineered sortase", "cut-and-paste middle-down", "39585806", "jacs.4c12585", "Corin MS275", "Philip Cole"]
pride, px = {}, {}
for k in kws:
    try:
        r = json.loads(get("https://www.ebi.ac.uk/pride/ws/archive/v2/search/projects?pageSize=100&keyword=" + urllib.parse.quote(k)))
        pride[k] = [[p.get("accession"), p.get("title")] for p in r]
    except Exception as e:
        pride[k] = f"ERROR {e}"
    try:
        r = json.loads(get("https://proteomecentral.proteomexchange.org/api/proxi/v0.1/datasets?resultType=compact&pageSize=200&search=" + urllib.parse.quote(k)))
        px[k] = [[d[0], d[1], d[8]] for d in r.get("datasets", [])]
    except Exception as e:
        px[k] = f"ERROR {e}"
# 4. MassIVE full public listing (downloaded to scratch), filtered
mv = json.loads(open(f"{dl}/search/massive_all.json", "rb").read().decode("latin-1"), strict=False)["datasets"]
mpat = re.compile(r"sortase|whedon|cW11|histone H3.*(TMT|middle)|(TMT|middle).*histone H3", re.I)
mv_hits = [[x["dataset"], x["title"], x.get("user"), x.get("pi")] for x in mv
           if mpat.search(" ".join(str(x.get(k, "")) for k in ("title", "description", "keywords", "pi", "user")))]
def relevant(t):
    return bool(re.search(r"sortase.*histone|histone.*sortase|whedon|cW11|middle-down.*H3|H3.*middle-down", t or "", re.I))
any_relevant = any(relevant(" ".join(map(str, row))) for v in list(pride.values()) + list(px.values()) if isinstance(v, list) for row in v) \
               or any(relevant(" ".join(map(str, r))) for r in mv_hits)
res = {"run_utc": datetime.datetime.utcnow().isoformat(), "dataset_description": desc, "deposit_files": files,
       "inputs_needed_by_code": needed, "code_input_calls": pc["input_calls"],
       "repository_mentions_in_texts": mentions, "dataverse_doi_mentions_in_texts": dv_mentions,
       "pride_search": pride, "proteomexchange_search": px,
       "massive_listing_size": len(mv), "massive_filtered_hits": mv_hits,
       "any_search_hit_matching_this_paper": any_relevant,
       "open_route_for_byonic_output_found": False if not any_relevant else "CHECK MANUALLY"}
json.dump(res, open(f"{out}/inputs_and_open_routes.json", "w"), indent=1)
print(json.dumps({k: res[k] for k in ["inputs_needed_by_code", "repository_mentions_in_texts", "dataverse_doi_mentions_in_texts", "massive_listing_size", "massive_filtered_hits", "any_search_hit_matching_this_paper"]}, indent=1))
