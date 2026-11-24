import pymupdf as fitz, re, glob, os, json
from seg import seg_paper
from extract import qp_text, SER
def texts(tier):
    out={}
    for fn in sorted(glob.glob(f'pdf/*{tier}-que-*.pdf')):
        ser=os.path.basename(fn).split('__')[0]; pp=re.search(r'-(\d)'+tier+'-',fn).group(1); key=SER[ser][0]
        d=fitz.open(fn); qs,_=seg_paper(fn)
        for n,q in qs.items():
            t=' '.join(w[4] for pn,ws in qp_text(d,qs,n,q) for w in ws)
            t=re.sub(r'\(Total for Question.*','',t)
            out[f'{key}-{pp}{tier}-{n}']=(t,q.get('total'))
    return out
def norm(t): return re.sub(r'[^a-z0-9£%.]+',' ',t.lower()).split()
H=texts('h'); F=texts('f')
json.dump({'H':H,'F':F},open('work/private/qtext_hf.json','w'))
def sh(a,b):
    A=set(zip(a,a[1:],a[2:])); B=set(zip(b,b[1:],b[2:]))
    if not A or not B: return 0
    return len(A&B)/min(len(A),len(B))
pairs=[]
for h,(ht,hm) in H.items():
    hs,hp,hq=h.split('-'); hn=norm(ht)
    best=None
    for f,(ft,fm) in F.items():
        fs,fp,fq=f.split('-')
        if fs!=hs: continue
        s=sh(hn,norm(ft))
        if best is None or s>best[0]: best=(s,f,hm,fm)
    if best and best[0]>=0.5: pairs.append((h,best[1],round(best[0],2),best[2],best[3]))
json.dump(pairs,open('work/private/overlap_pairs.json','w'))
print(len(pairs)); 
import collections
print(collections.Counter(round(p[2],1) for p in pairs))
print([p for p in pairs if p[3]!=p[4]][:10])
