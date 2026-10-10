"""Re-runnable searches behind the absence claims for 20_SINIYU (pre-registration, 2026-10-10).
Usage: python3 absence_searches_20.py   (writes absence_searches.json next to this file)
Public APIs only, no sign-in. A 'relevant hit' is any file or repository whose name contains the searched
module/file name (case-insensitive), or for VMM code, any item that names FY-3G/FY3G together with volume matching."""
import json, time, datetime, urllib.request, urllib.parse, urllib.error, os
UA = {"User-Agent": "repro-audit-2026", "Accept": "application/json"}
RECS = []
def now(): return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
def get(url):
    t = now()
    try:
        r = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60)
        return t, r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return t, e.code, ""
    except Exception as e:
        return t, "error: " + type(e).__name__, ""
def rec(source, query, url, t, st, total, rel, note=""):
    RECS.append(dict(source=source, query=query, url=url, utc=t, http=st, total_results=total, relevant_hits=rel, note=note))
    print(source, "|", query, "|", st, "| total", total, "| relevant", len(rel))

# 1. Harvard Dataverse file search (all of Harvard Dataverse)
for q, key in [("fileName:interp_radar*", "interp_radar"), ('"interp_radar_ppi"', "interp_radar"), ('"interp_radar_shift"', "interp_radar"),
               ("fileName:VAR_COLOR*", "var_color"), ("fileName:temp_inno*", "temp_inno"), ("fileName:*o_b_thin*", "o_b_thin")]:
    url = "https://dataverse.harvard.edu/api/search?" + urllib.parse.urlencode([("q", q), ("type", "file"), ("per_page", "100")])
    t, st, b = get(url); tot, rel = None, []
    if st == 200:
        d = json.loads(b)["data"]; tot = d["total_count"]
        rel = [{"file": i["name"], "dataset_doi": i.get("dataset_persistent_id")} for i in d["items"] if key in i["name"].lower()]
    rec("Harvard Dataverse Search API (type=file)", q, url, t, st, tot, rel); time.sleep(1)

# 2. Full file list of the audited deposit
url = "https://dataverse.harvard.edu/api/datasets/:persistentId/versions/:latest/files?persistentId=doi:10.7910/DVN/SINIYU"
t, st, b = get(url); names = []
if st == 200: names = [f["dataFile"]["filename"] for f in json.loads(b)["data"]]
rel = [n for n in names if any(k in n.lower() for k in ["interp", "vmm", "match", "table", "var_color", "inno", "met_out", "cts"])]
rec("Dataverse file list doi:10.7910/DVN/SINIYU", "all files (latest version)", url, t, st, len(names), rel, "files: " + ", ".join(names))

# 3. Zenodo records search
for q in ['"interp_radar_ppi"', '"interp_radar_shift"', 'interp_radar', 'FY-3G Ku-band volume matching', 'FY-3G 1D Bayesian retrieval CMA-MESO']:
    url = "https://zenodo.org/api/records?" + urllib.parse.urlencode({"q": q, "size": 25})
    t, st, b = get(url); tot, rel = None, []
    if st == 200:
        d = json.loads(b); tot = d["hits"]["total"]
        for h in d["hits"]["hits"]:
            title = h["metadata"].get("title", ""); files = [f["key"] for f in h.get("files", [])]
            if "interp_radar" in q and any("interp_radar" in f.lower() for f in files):
                rel.append({"title": title, "doi": h.get("doi"), "files": files})
            if "interp_radar" not in q and ("fy-3g" in title.lower() or "fy3g" in title.lower()):
                rel.append({"title": title, "doi": h.get("doi"), "files": files})
    rec("Zenodo records API", q, url, t, st, tot, rel); time.sleep(1)

# 4. GitHub repository search (code search needs sign-in, so only repository names/descriptions are searched)
for q in ["interp_radar", "interp_radar_ppi", "FY3G PMR", "FY-3G radar assimilation", "Ku-band 1D Bayesian retrieval"]:
    url = "https://api.github.com/search/repositories?" + urllib.parse.urlencode({"q": q, "per_page": 100})
    t, st, b = get(url); tot, rel = None, []
    if st == 200:
        d = json.loads(b); tot = d["total_count"]
        rel = [{"repo": i["full_name"], "desc": i.get("description")} for i in d["items"]
               if "interp_radar" in (i["full_name"] + str(i.get("description"))).lower() or "fy3g" in i["full_name"].lower().replace("-", "")]
    rec("GitHub repository search API (unauthenticated)", q, url, t, st, tot, rel, "returned: " + ", ".join(i["full_name"] for i in (json.loads(b)["items"] if st == 200 else []))); time.sleep(3)

json.dump(RECS, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "absence_searches.json"), "w"), indent=1)
