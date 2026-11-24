"""Final public-scope pass: strips question-specific figures from method notes and template example lines. Run last."""
import csv,json,re,sys
sys.path.insert(0,'repo/code')
from scrub_notes import scrub
for f in ('repo/docs/higher-classification.csv','repo/docs/foundation-classification.csv'):
    rows=list(csv.reader(open(f,newline='')));i=rows[0].index('method_note')
    for r in rows[1:]: r[i]=scrub(r[i])
    csv.writer(open(f,'w',newline='')).writerows(rows)
for f in ('repo/questions.json','repo/questions-foundation.json'):
    d=json.load(open(f))
    for q in d: q['methodNote']=scrub(q['methodNote'])
    json.dump(d,open(f,'w'),ensure_ascii=False,indent=1)
for f in ('repo/docs/TEMPLATES.md','repo/docs/FOUNDATION-TEMPLATES.md'):
    L=open(f).read().split('\n')
    for i,l in enumerate(L):
        if l.startswith('    - ') and '): ' in l:
            a,b=l.split('): ',1); L[i]=a+'): '+scrub(b)
    open(f,'w').write('\n'.join(L))
