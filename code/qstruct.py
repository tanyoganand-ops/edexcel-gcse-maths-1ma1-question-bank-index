import pymupdf as fitz, re, glob, os, json
from seg import seg_paper
from extract import qp_text, SER
ROM=['i','ii','iii','iv','v','vi']
def leaves(fn):
    d=fitz.open(fn); qs,_=seg_paper(fn); out={}
    for n,q in sorted(qs.items()):
        pages=qp_text(d,qs,n,q)
        ev=[]
        for pn,ws in pages:
            for w in ws:
                t=w[4]
                if w[0]<125 and re.fullmatch(r'\([a-z]\)',t): ev.append((pn,round(w[1]/4),w[0],'L',t[1]))
                elif w[0]<150 and re.fullmatch(r'\((i{1,3}|iv|v|vi)\)',t): ev.append((pn,round(w[1]/4),w[0],'R',t[1:-1]))
                elif w[0]>440 and re.fullmatch(r'\(\d{1,2}\)',t): ev.append((pn,round(w[1]/4),w[0],'M',int(t[1:-1])))
        ev.sort(key=lambda e:(e[0],e[1],e[2]))
        # decide ambiguous (i): roman if a '(ii)' exists later in the question
        hasii=any(e[3]=='R' and e[4]=='ii' for e in ev)
        L=[];cur=None;letter=None
        for pn,y,x,k,v in ev:
            if k=='L' and not (v=='i' and hasii):
                letter=v; cur={'path':v,'marks':0}; L.append(cur)
            elif k=='R' or (k=='L' and v=='i'):
                r='i' if k=='L' else v
                cur={'path':(letter or '')+'('+r+')','marks':0}; L.append(cur)
            elif k=='M':
                if cur is None: cur={'path':'','marks':0}; L.append(cur)
                cur['marks']+=v
        out[n]={'total':q.get('total'),'leaves':L}
    return out
if __name__=='__main__':
    import sys
    tier=sys.argv[1]; res={}
    for fn in sorted(glob.glob(f'pdf/*{tier}-que-*.pdf')):
        ser=os.path.basename(fn).split('__')[0]; pp=re.search(r'-(\d)'+tier+'-',fn).group(1)
        key=SER[ser][0]
        for n,v in leaves(fn).items(): res[f'{key}-{pp}{tier}-{n}']=v
    json.dump(res,open(f'work/leaves_{tier}.json','w'))
    bad=[(k,v['total'],sum(l['marks'] for l in v['leaves'])) for k,v in res.items() if v['total']!=sum(l['marks'] for l in v['leaves'])]
    print(len(res),len(bad),bad[:15])
    print('with roman',sum(1 for v in res.values() if any('(' in l['path'] for l in v['leaves'])))
