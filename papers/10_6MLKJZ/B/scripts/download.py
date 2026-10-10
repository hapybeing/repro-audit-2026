import json,subprocess,os,hashlib
d=json.load(open('meta.json'))['data']['latestVersion']
out=open('checksums.sha256','w'); log=open('download_log.tsv','w')
for f in d['files']:
    df=f['dataFile']; dirl=f.get('directoryLabel','')
    name=df.get('originalFileName') or f['label']
    url=f"https://dataverse.harvard.edu/api/access/datafile/{df['id']}"
    if df.get('originalFileName'): url+='?format=original'
    p=os.path.join('files',dirl,name); os.makedirs(os.path.dirname(p),exist_ok=True)
    r=subprocess.run(['curl','-sS','-L','-A','repro-audit-2026','-o',p,'-w','%{http_code}',url],capture_output=True,text=True)
    h=hashlib.sha256(open(p,'rb').read()).hexdigest()
    out.write(f"{h}  {dirl}/{name}\n"); log.write(f"{df['id']}\t{url}\t{r.stdout}\t{os.path.getsize(p)}\t{dirl}/{name}\n")
