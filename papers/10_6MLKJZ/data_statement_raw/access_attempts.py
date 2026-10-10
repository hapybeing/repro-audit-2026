import json, datetime, urllib.request, urllib.error, hashlib
DOI="10.1177/09520767231210025"
UA={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"}
URLS=[("Sage article full text","https://journals.sagepub.com/doi/full/"+DOI),
("Sage PDF","https://journals.sagepub.com/doi/pdf/"+DOI),
("Sage full-text XML","https://journals.sagepub.com/doi/full-xml/"+DOI),
("Sage Version1 PDF (history link)","https://journals.sagepub.com/history/e3e92517-00f2-48e3-8ad6-5fd7c5fb1a46/09520767231210025.17922236.pdf"),
("Sage supplementary PDF","https://journals.sagepub.com/doi/suppl/"+DOI+"/suppl_file/sj-pdf-1-ppa-10.1177_09520767231210025.pdf"),
("Crossref metadata","https://api.crossref.org/works/"+DOI),
("Europe PMC search","https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:"+DOI+"&format=json"),
("Semantic Scholar","https://api.semanticscholar.org/graph/v1/paper/DOI:"+DOI+"?fields=title,openAccessPdf,externalIds"),
("Wayback availability, Sage PDF","http://archive.org/wayback/available?url=journals.sagepub.com/doi/pdf/"+DOI),
]
out=[]
for name,u in URLS:
    t=datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    try:
        r=urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=60);b,st=r.read(),r.status
    except urllib.error.HTTPError as e: b,st=e.read(),e.code
    except Exception as e: b,st=b"",f"error: {type(e).__name__}"
    s=b[:3000].decode("utf-8","replace")
    what="Cloudflare interstitial ('Just a moment...')" if "Just a moment" in s else s[:300].replace("\n"," ")
    out.append({"route":name,"url":u,"utc":t,"http":st,"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest() if b else None,"what_came_back":what})
    fn=name.replace(" ","_").replace(",","").replace("(","").replace(")","")[:40]
    if st==200: open("raw_"+fn,"wb").write(b)
    print(name,st,len(b),what[:150])
json.dump(out,open("access_attempts.json","w"),indent=1)
