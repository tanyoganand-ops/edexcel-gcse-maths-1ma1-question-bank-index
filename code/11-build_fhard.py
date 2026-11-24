"""Foundation difficulty proxy (heuristic, NOT measured difficulty). No examiner data used."""
import csv,json,re,math,collections
D='repo/docs/'
priv={q['id']:q for q in json.load(open('work/private/foundation_scored.json'))}
cls={r['question_id']:r for r in csv.DictReader(open(D+'foundation-classification.csv'))}
parts=list(csv.DictReader(open(D+'foundation-parts.csv')))
mpos={}
for r in cls.values(): k=(r['series'],r['paper']); mpos[k]=max(mpos.get(k,0),int(r['question_no']))
def pshare(q):
    codes=q['ms_codes'] if isinstance(q['ms_codes'],list) else []
    c=collections.Counter()
    for x in codes: c[x[0]]+=int(re.sub(r'\D','',x) or 1)
    return (c['P']+c['C'])/(sum(c.values()) or 1)
units=[p for p in parts if p['marks_counted'] not in('0',)]
allm=sorted(int(u['marks_counted']) for u in units)
pct=lambda v:sum(1 for x in allm if x<=v)/len(allm)
rows=[]
for u in units:
    q=u['question_id']; r=cls[q]; pos=int(r['question_no'])/mpos[(r['series'],r['paper'])]
    proof=bool(re.search(r'\bshow that\b',priv[q]['text'].lower()))
    s=0.35*pos+0.25*pct(int(u['marks_counted']))+0.15*pshare(priv[q])+(0.1 if proof else 0)
    rows.append(dict(row_id=u['row_id'],question_id=q,part=u['part'],topic=u['topic'],marks=u['marks_counted'],paper=f"{r['series']}-{r['paper']}f",score=round(s,3),proof='yes' if proof else ''))
grp=collections.defaultdict(list)
for x in rows: grp[(x['paper'],x['topic'])].append(x)
sel=[]
for k,l in grp.items():
    l.sort(key=lambda x:-x['score']); sel+=l[:max(1,math.ceil(0.15*len(l)))]
sel.sort(key=lambda x:(x['topic'],x['paper'],-x['score']))
w=csv.DictWriter(open(D+'foundation-hardest-parts.csv','w',newline=''),fieldnames=list(sel[0].keys()));w.writeheader();w.writerows(sel)
top=sorted(rows,key=lambda x:-x['score'])[:round(0.15*len(rows))]
w=csv.DictWriter(open(D+'foundation-hardest-15pct.csv','w',newline=''),fieldnames=list(top[0].keys()));w.writeheader();w.writerows(top)
print(len(rows),len(sel),len(grp),len(top),'rule: round(0.15*%d)=%d'%(len(rows),round(0.15*len(rows))))
