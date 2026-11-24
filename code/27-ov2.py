import pymupdf as fitz, re, glob, os, json, collections, difflib
from seg import seg_paper
from extract import qp_text, SER
STOP={'do','not','write','in','this','area','turn','over','dont'}
def info(tier):
    out={}
    for fn in sorted(glob.glob(f'pdf/*{tier}-que-*.pdf')):
        ser=os.path.basename(fn).split('__')[0]; pp=re.search(r'-(\d)'+tier+'-',fn).group(1); key=SER[ser][0]
        d=fitz.open(fn); qs,_=seg_paper(fn)
        for n,q in qs.items():
            pages=qp_text(d,qs,n,q)
            toks=[]
            for pn,ws in pages:
                for w in ws:
                    t=w[4].lower()
                    if w[0]<40 and w[4].isdigit(): continue
                    toks.append(t)
            toks=[t for t in toks if t not in STOP and not re.fullmatch(r'\.{3,}',t) and not re.fullmatch(r'[.…]+',t)]
            if toks and toks[0]==str(n): toks=toks[1:]
            # figure signature
            sig=[]
            (sp,sy)=q['start'];(ep,ey)=q['end']
            for pn in range(sp,ep+1):
                p=d[pn]; y0=sy-2 if pn==sp else 30; y1=ey+2 if pn==ep else p.rect.height-45
                dr=[x for x in p.get_drawings() if x['rect'].y0>=y0 and x['rect'].y1<=y1 and x['rect'].x0>45 and x['rect'].width<500]
                im=[i for i in p.get_image_info() if i['bbox'][1]>=y0 and i['bbox'][3]<=y1]
                sig.append((len(dr),len(im)))
            out[f'{key}-{pp}{tier}-{n}']=(toks,sig,q.get('total'))
    return out
H=info('h');F=info('f')
cands=json.load(open('work/private/overlap_final.json'))
res=[]
for s,h,f,hm,fm in cands:
    a=H[h][0];b=F[f][0]
    r=difflib.SequenceMatcher(None,a,b,autojunk=False).ratio()
    hs=sum(x[0] for x in H[h][1]);fs=sum(x[0] for x in F[f][1]); hi=sum(x[1] for x in H[h][1]);fi=sum(x[1] for x in F[f][1])
    res.append((h,f,round(r,3),hs,fs,hi,fi,hm))
json.dump(res,open('work/private/overlap_ordered.json','w'))
print(collections.Counter((r[2]>=0.99, abs(r[3]-r[4])<=max(2,0.1*max(r[3],r[4])) and r[5]==r[6]) for r in res))
