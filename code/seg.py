import pymupdf as fitz, re, glob, os, json, sys
def lines_of(page):
    ws=page.get_text('words')
    ws.sort(key=lambda w:(round(w[1]/3),w[0]))
    return ws
def seg_paper(fn):
    d=fitz.open(fn); qs={}; cur=None; expected=1; totals={}
    anyerr=[]
    for pn in range(len(d)):
        p=d[pn]; W=p.rect.width; H=p.rect.height
        ws=p.get_text('words')
        # total markers
        txt_lines={}
        for w in ws: txt_lines.setdefault(round(w[1]),[]).append(w)
        items=[]
        for y,l in txt_lines.items():
            l.sort(key=lambda w:w[0]); s=' '.join(w[4] for w in l)
            items.append((l[0][1],l,s))
        items.sort(key=lambda t:t[0])
        for y,l,s in items:
            if y>H-60 and re.fullmatch(r'\d+',s.strip()): continue
            m=re.search(r'Total for Question (\d+) is (\d+) mark',s)
            if m:
                n=int(m.group(1)); totals[n]=int(m.group(2))
                if n in qs: qs[n]['end']=(pn,l[0][3]); qs[n]['total']=int(m.group(2))
                continue
            f=next((w for w in l if w[0]>25),l[0])
            if re.fullmatch(r'\d{1,2}',f[4]) and f[0]<62 and int(f[4])==expected and len(l)>1 or (re.fullmatch(r'\d{1,2}',f[4]) and f[0]<62 and int(f[4])==expected and pn>0):
                n=int(f[4])
                if n not in qs:
                    qs[n]={'start':(pn,f[1]),'parts':[]}; cur=n; expected+=1
                continue
            if cur is not None and cur in qs:
                pm=re.match(r'\(([a-z])\)$',f[4])
                if pm and f[0]<110: qs[cur]['parts'].append([pm.group(1),pn,round(y)])
                mm=[w for w in l if re.fullmatch(r'\((\d{1,2})\)',w[4]) and w[0]>440]
                for w in mm: qs[cur].setdefault('pm',[]).append(int(w[4][1:-1]))
    return qs,len(d)
if __name__=='__main__':
    res={}
    for fn in sorted(glob.glob('pdf/*h-que-*.pdf')):
        qs,n=seg_paper(fn); tot=sum(q.get('total',0) for q in qs.values())
        bad=[k for k,q in qs.items() if 'total' not in q or ('pm' in q and sum(q['pm'])!=q['total'])]
        print(os.path.basename(fn),len(qs),tot,'bad',bad)
