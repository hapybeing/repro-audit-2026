"""Re-runnable absence searches for 24_U9CKK6 (files read by deposited scripts but not in the deposit).
Usage: python3 absence_searches_24.py OUT.json   Public APIs only, no sign-in.
Hit rule: a hit is a file with the exact file name the script reads (view_party.csv, view_cabinet.csv,
eurobarmeter_challengers_2023.dta) inside doi:10.7910/DVN/U9CKK6 (the only location the article's data
statement names). Hits elsewhere are recorded as 'outside named location' and do not count for rule #4.
"""
import json, sys, time, datetime, urllib.request, urllib.parse, urllib.error

UA = {"User-Agent": "repro-audit-2026", "Accept": "application/json"}
RECS = []

def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def get(url):
    t = now()
    for a in range(3):
        try:
            r = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=90)
            return t, r.status, r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503) and a < 2:
                time.sleep(5); continue
            return t, e.code, ""
        except Exception as e:
            if a < 2:
                time.sleep(5); continue
            return t, "error: " + type(e).__name__, ""

TARGETS = ["view_party.csv", "view_cabinet.csv", "eurobarmeter_challengers_2023.dta"]

# 1. Deposit file list (all versions)
url = "https://dataverse.harvard.edu/api/datasets/:persistentId/versions?persistentId=doi:10.7910/DVN/U9CKK6"
t, st, body = get(url)
files = []
if body:
    for v in json.loads(body)["data"]:
        for f in v["files"]:
            files.append((v.get("versionNumber"), v.get("versionMinorNumber"), f["dataFile"]["filename"]))
for q in TARGETS + [".dta", "parlgov", "eurobar"]:
    hits = [x for x in files if q.lower() in x[2].lower()]
    RECS.append({"source": "Dataverse deposit file list, all versions", "query": q, "url": url, "utc": t,
                 "http": st, "total_results": len(hits), "relevant_hits": hits,
                 "note": "files in all versions: %d" % len(files)})

# 2. Harvard Dataverse search API, files, whole installation
for q in ['"eurobarmeter_challengers_2023"', 'eurobarmeter_challengers_2023.dta', 'name:"view_party.csv"', 'name:"view_cabinet.csv"']:
    url = "https://dataverse.harvard.edu/api/search?" + urllib.parse.urlencode({"q": q, "type": "file", "per_page": "100"})
    t, st, body = get(url)
    total, rel = None, []
    if body:
        d = json.loads(body)["data"]; total = d["total_count"]
        for it in d["items"]:
            pid = it.get("dataset_persistent_id") or ""
            rel.append({"name": it.get("name"), "dataset": pid, "in_named_location": pid.endswith("U9CKK6")})
    RECS.append({"source": "Harvard Dataverse search API (files)", "query": q, "url": url, "utc": t, "http": st,
                 "total_results": total, "relevant_hits": rel, "note": ""})

# 3. Harvard Dataverse search API, datasets, Wratil Eurobarometer challengers
for q in ['Wratil challengers eurobarometer', 'eurobarometer challengers Wratil 2023']:
    url = "https://dataverse.harvard.edu/api/search?" + urllib.parse.urlencode({"q": q, "type": "dataset", "per_page": "50"})
    t, st, body = get(url)
    total, rel = None, []
    if body:
        d = json.loads(body)["data"]; total = d["total_count"]
        rel = [{"name": it.get("name"), "global_id": it.get("global_id")} for it in d["items"]]
    RECS.append({"source": "Harvard Dataverse search API (datasets)", "query": q, "url": url, "utc": t, "http": st,
                 "total_results": total, "relevant_hits": rel, "note": "outside named location; does not count for rule #4"})

json.dump(RECS, open(sys.argv[1], "w"), indent=1)
for r in RECS:
    print(r["utc"], "|", r["source"], "|", r["query"], "|", r["http"], "| total", r["total_results"])
