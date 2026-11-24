import pymupdf as fitz, re, glob, os
def vwords(p):
    out=[]
    for w in p.get_text('words'):
        r=fitz.Rect(w[:4])*p.rotation_matrix; r.normalize()
        out.append((r.x0,r.y0,r.x1,r.y1)+tuple(w[4:]))
    return out
def vh(p): return (p.rect*p.rotation_matrix).height
def parse_ms(fn):
    d=fitz.open(fn); qs={}; cur=None; expected=1
    for pn in range(len(d)):
        p=d[pn]; ws=vwords(p)
        hdr=[w for w in ws if w[4]=='Question' and w[1]<120]
        mk=[w for w in ws if w[4]=='Mark' and w[1]<120]
        if not hdr or not mk or not any(w[4]=='Answer' and w[1]<120 for w in ws) or not any(w[4]=='Paper:' and w[1]<110 for w in ws): continue
        qx=hdr[0][0]; mx=mk[0][0]; ay=[w for w in ws if w[4]=='Answer' and w[1]<120]
        ax=ay[0][0] if ay else mx-60
        body=[w for w in ws if w[1]>hdr[0][1]+6 and w[1]<vh(p)-35]
        # question number col: x within [qx-5, ax-5)
        lines={}
        for w in body: lines.setdefault(round(w[1]/2),[]).append(w)
        for k in sorted(lines):
            l=sorted(lines[k],key=lambda w:w[0]); f=l[0]
            if f[0]<ax-5 and re.fullmatch(r'\d{1,2}',f[4]) and int(f[4])==expected:
                cur=expected; expected+=1; qs[cur]={'pages':[pn],'marks':[],'parts':[],'start':(pn,f[1]),'branch':0}
                rest=[w for w in l[1:] if w[0]<ax-5]
            elif cur is not None and f[0]<ax-5 and re.fullmatch(r'\d{1,2}',f[4]) and int(f[4])==cur:
                qs[cur]['branch']=99; qs[cur]['alt']=True; rest=[w for w in l[1:] if w[0]<ax-5]
            else: rest=[w for w in l if w[0]<ax-5]
            if cur is None: continue
            if pn not in qs[cur]['pages']: qs[cur]['pages'].append(pn)
            for w in rest:
                m=re.fullmatch(r'\(([a-z])\)',w[4])
                if m:
                    seen=qs[cur].setdefault('seen',set())
                    if m.group(1) in seen and not qs[cur].get('alt'): qs[cur]['alt']=True
                    seen.add(m.group(1)); qs[cur]['parts'].append((m.group(1),pn,w[1])); qs[cur]['branch']=99 if qs[cur].get('alt') else 0
            rt=[w[4] for w in l if w[0]>mx+20]
            if (rt==['OR'] and not any(mx-8<=w[0]<mx+20 for w in l)) or (rt and rt[0].lower()=='alternative' and len(rt)<=4 and qs[cur]['branch']!=99): qs[cur]['branch']+=1
            qs[cur].setdefault('text',[]).extend(w[4] for w in l if w[0]>=ax-5)
            for w in l:
                if mx-8<=w[0]<mx+45:
                    m=re.fullmatch(r'([MABCP])(\d)',w[4])
                    if m: qs[cur]['marks'].append((m.group(1),int(m.group(2)),pn,w[1],qs[cur]['branch'],len(qs[cur]['parts'])))
                    elif re.fullmatch(r'\(?[MABCP]\d',w[4]) : qs[cur]['marks'].append(('alt',0,pn,w[1],qs[cur]['branch'],len(qs[cur]['parts'])))
    return qs
if __name__=='__main__':
    from seg import seg_paper
    import sys
    ok=0;tot=0
    for f in sorted(glob.glob('pdf/*h-que-*.pdf')):
        ser=os.path.basename(f).split('__')[0]; pp=re.search(r'-(\d)h-',f).group(1)
        ms=[m for m in glob.glob(f'pdf/{ser}__1ma1-{pp}h-*ms*') + glob.glob(f'pdf/{ser}__1ma1-{pp}h-rms*')+glob.glob(f'pdf/{ser}__1ma1-{pp}h-msc*')]
        ms=sorted(set(ms))
        qq,_=seg_paper(f); mq=parse_ms(ms[0]) if ms else {}
        bad=[]
        for n,q in qq.items():
            mm=mq.get(n,{}).get('marks',[]); s=sum(m[1] for m in mm); s0=sum(m[1] for m in mm if m[4]==0)
            if n not in mq or q['total'] not in (s,s0): bad.append((n,q['total'],s,s0))
        print(os.path.basename(f),len(qq),len(mq),'mismatch',len(bad),bad[:6])
