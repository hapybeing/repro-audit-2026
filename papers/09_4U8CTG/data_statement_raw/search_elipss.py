import json,urllib.request,urllib.parse,datetime
out=[]
qs=[("https://data.sciencespo.fr/api/search",{"q":"elipss_fes2022_v3","type":"file"}),
    ("https://data.sciencespo.fr/api/search",{"q":"elipss_fes2022_cses_v4","type":"file"}),
    ("https://data.sciencespo.fr/api/search",{"q":"French Election Study 2022","type":"dataset"}),
    ("https://data.sciencespo.fr/api/search",{"q":"FES 2022 ELIPSS","type":"dataset"}),
    ("https://data.sciencespo.fr/api/search",{"q":"Persico","type":"dataset"}),
    ("https://dataverse.harvard.edu/api/search",{"q":"\"study1_fes_panel\"","type":"file"}),
    ("https://dataverse.harvard.edu/api/search",{"q":"elipss_fes2022","type":"file"})]
for base,p in qs:
    p=dict(p,per_page=50); url=base+"?"+urllib.parse.urlencode(p)
    t=datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    try:
        r=urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"repro-audit-2026"}),timeout=60)
        st=r.status; d=json.load(r)
        n=d["data"]["total_count"]; items=[{k:i.get(k) for k in ("name","global_id","dataset_persistent_id","file_id","dataset_name","url","published_at")} for i in d["data"]["items"]]
    except Exception as e:
        st=str(e); n=None; items=[]
    out.append({"utc":t,"url":url,"status":st,"count":n,"items":items})
json.dump(out,open("elipss_searches.json","w"),indent=1,ensure_ascii=False)
for o in out: print(o["utc"],o["status"],o["count"],o["url"]); [print("   ",i) for i in o["items"][:10]]
