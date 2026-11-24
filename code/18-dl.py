import re,hashlib,os,json,urllib.request,csv,datetime
from concurrent.futures import ThreadPoolExecutor
ser=None; items=[]
for line in open('links.txt'):
    line=line.strip()
    if line.startswith('=='): ser=line.split()[1]; continue
    if line: items.append((ser,line))
os.makedirs('pdf',exist_ok=True)
def get(it):
    s,u=it
    fn=u.split('?')[0].split('/')[-1].lower().replace('_','-')
    path='pdf/'+s+'__'+fn
    if os.path.exists(path) and os.path.getsize(path)>1000: return s,u,path,'ok'
    for a in range(3):
        try:
            r=urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'})
            d=urllib.request.urlopen(r,timeout=60).read()
            if d[:4]==b'%PDF': open(path,'wb').write(d); return s,u,path,'ok'
        except Exception as e: err=str(e)
    return s,u,path,'FAIL'
with ThreadPoolExecutor(8) as ex: res=list(ex.map(get,items))
json.dump(res,open('dl_res.json','w'))
print(len(res),sum(r[3]=='ok' for r in res),[r[2] for r in res if r[3]!='ok'])
