import pymupdf as fitz, re, glob, os, json
from seg import seg_paper
from msseg import parse_ms, vwords
SER={'June-2019':('jun2019',2019,'June'),'November-2019':('nov2019',2019,'November'),'November-2020':('nov2020',2020,'November'),'November-2021':('nov2021',2021,'November'),'June-2022':('jun2022',2022,'June'),'November-2022':('nov2022',2022,'November'),'June-2023':('jun2023',2023,'June'),'November-2023':('nov2023',2023,'November'),'June-2024':('jun2024',2024,'June'),'November-2024':('nov2024',2024,'November'),'June-2025':('jun2025',2025,'June')}
def qp_text(d,qs,n,q):
    (sp,sy)=q['start']; (ep,ey)=q['end']; out=[]
    for pn in range(sp,ep+1):
        p=d[pn]; H=p.rect.height
        y0=sy-2 if pn==sp else 30; y1=ey+2 if pn==ep else H-45
        ws=[w for w in p.get_text('words') if w[1]>=y0 and w[3]<=y1+3 and not (w[1]>H-60 and re.fullmatch(r'\d+',w[4]))]
        ws.sort(key=lambda w:(round(w[1]/4),w[0]))
        out.append((pn,ws))
    return out
def build(tier='h'):
    recs=[]
    for f in sorted(glob.glob(f'pdf/*{tier}-que-*.pdf')):
        ser=os.path.basename(f).split('__')[0]; pp=re.search(r'-(\d)'+tier+'-',f).group(1)
        key,yr,ses=SER[ser]
        ms=sorted(glob.glob(f'pdf/{ser}__1ma1-{pp}{tier}-*ms*'))[0]
        d=fitz.open(f); qs,_=seg_paper(f); mq=parse_ms(ms); md=fitz.open(ms)
        for n,q in sorted(qs.items()):
            pages=qp_text(d,qs,n,q)
            text=' '.join(w[4] for pn,ws in pages for w in ws)
            # parts and marks
            ev=[]
            for pn,ws in pages:
                for w in ws:
                    if re.fullmatch(r'\([a-z]\)',w[4]) and w[0]<110: ev.append((pn,w[1],'p',w[4][1]))
                    elif re.fullmatch(r'\(\d{1,2}\)',w[4]) and w[0]>440: ev.append((pn,w[1],'m',int(w[4][1:-1])))
                    ev.append((pn,w[1],'t',w[4])) if not(re.fullmatch(r'\([a-z]\)',w[4]) and w[0]<110) else None
            ev.sort(key=lambda e:(e[0],round(e[1]/4)))
            parts=[]; cur=None
            for pn,y,k,v in ev:
                if k=='p': cur={'part':v,'marks':0,'text':[]}; parts.append(cur)
                elif k=='m':
                    if cur is None: cur={'part':'','marks':0,'text':[]}; parts.append(cur)
                    cur['marks']+=v
                else:
                    if cur is None: cur={'part':'','marks':0,'text':[]}; parts.append(cur)
                    cur['text'].append(v)
            # figure detection
            nd=0
            for pn,ws in pages:
                p=d[pn]; r=fitz.Rect(0,(q['start'][1] if pn==q['start'][0] else 30),p.rect.width,(q['end'][1] if pn==q['end'][0] else p.rect.height-45))
                nd+=sum(1 for dr in p.get_drawings() if dr['rect'].intersects(r) and dr['rect'].width>8 and dr['rect'].height>8 and dr['rect'].width<p.rect.width*0.9)
                nd+=len(p.get_images())*0 
            # ms text
            mm=mq.get(n,{}); mstext=''
            if mm:
                for pn in mm['pages']:
                    pass
            recs.append({'id':f"{key}-{pp}{tier}-{n}",'tier':'Higher' if tier=='h' else 'Foundation','paper':int(pp),'series':key,'year':yr,'session':ses,'calc':'no' if pp=='1' else 'yes','q':n,'total':q['total'],
              'qp_file':os.path.basename(f),'ms_file':os.path.basename(ms),'qp_pages':[q['start'][0]+1,q['end'][0]+1],'ms_pages':[x+1 for x in mm.get('pages',[])],
              'text':text,'parts':[{'part':p['part'],'marks':p['marks'],'text':' '.join(p['text'])} for p in parts],'drawing_items':nd,
              'ms_text':' '.join(mm.get('text',[])),'ms_codes':[m[0]+str(m[1]) for m in mm.get('marks',[]) if m[0]!='alt'],'ms_alt_present':any(m[4]!=0 for m in mm.get('marks',[]))})
    return recs
if __name__=='__main__':
    import sys
    r=build('h'); os.makedirs('work/private',exist_ok=True); json.dump(r,open('work/private/higher_raw.json','w'))
    print(len(r), sum(x['total'] for x in r), sum(len(x['parts']) for x in r))
    x=r[30]; print(x['id'],x['total'],x['drawing_items'],[(p['part'],p['marks']) for p in x['parts']],x['text'][:200])
