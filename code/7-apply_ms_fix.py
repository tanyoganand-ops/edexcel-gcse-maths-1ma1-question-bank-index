"""Corrects four Foundation scheme-entry boundaries found by reading the scheme pages as images.
Run from the scratch root after extract.py. Needs the Pearson PDFs locally; the corrected text stays in the private file."""
import json,re,subprocess
P='work/private/foundation_scored.json'
F=json.load(open(P)); by={x['id']:x for x in F}
def page(f,p): return subprocess.run(['pdftotext','-f',str(p),'-l',str(p),'-layout','pdf/'+f,'-'],capture_output=True,text=True).stdout
def clean(t): return re.sub(r'\s+',' ',t).strip()
FIX={
 'nov2023-2f-17':('November-2023__1ma1-2f-rms-20240111.pdf',10,r'^\s*17\s',r'^\s*18\s',['B2','B1','B1']),
 'nov2023-2f-18':('November-2023__1ma1-2f-rms-20240111.pdf',10,r'^\s*18\s',r'^\s*19\s',['B2','B1','B1']),
 'nov2023-2f-19':('November-2023__1ma1-2f-rms-20240111.pdf',10,r'^\s*19\s',None,['M1','M1','C2']),
 'jun2025-3f-30':('June-2025__1ma1-3f-rms-20250821.pdf',22,r'^\s*30\s',None,['M1','M1','A1']),
}
for q,(f,p,a,b,codes) in FIX.items():
    lines=page(f,p).split('\n'); s=next(i for i,l in enumerate(lines) if re.match(a,l))
    e=next((i for i in range(s+1,len(lines)) if b and re.match(b,lines[i])),len(lines))
    x=by[q]; x['ms_text']=clean(' '.join(lines[s:e])); x['ms_codes']=codes; x['ms_pages']=[p]
    print(q,len(x['ms_text']),codes)
json.dump(F,open(P,'w'))
