import pymupdf as fitz, glob, hashlib, re, csv, os, collections
rows=[]
for f in sorted(glob.glob('pdf/*.pdf')):
    b=open(f,'rb').read(); h=hashlib.sha256(b).hexdigest()
    try:
        d=fitz.open(f); n=len(d); t=d[0].get_text()
    except Exception as e: n=-1;t=''
    ref=re.search(r'1MA1/(\d[FH])',t); 
    date=re.search(r'(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\s+\d+\s+\w+\s+\d{4}',t)
    ser=os.path.basename(f).split('__')[0]; typ=re.search(r'-(que|rms|msc|pef)-',f)
    rows.append([os.path.basename(f),ser,typ.group(1) if typ else '',n,len(b),h,ref.group(1) if ref else '',date.group(0) if date else ''])
w=csv.writer(open('manifest_raw.csv','w')); w.writerow(['file','series_listed','type','pages','bytes','sha256','paper_on_p1','exam_date_on_p1']); w.writerows(rows)
c=collections.Counter(r[5] for r in rows); print('dups',[(k[:8],v) for k,v in c.items() if v>1])
for r in rows:
    if r[2]=='que': print(r[0],r[3],r[6],r[7])
