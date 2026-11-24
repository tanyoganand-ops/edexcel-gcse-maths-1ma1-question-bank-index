import csv,json,re,math,collections
D='repo/docs/'
priv={q['id']:q for q in json.load(open('work/private/higher_classified.json'))}
cls={r['question_id']:r for r in csv.DictReader(open(D+'higher-classification.csv'))}
parts=list(csv.DictReader(open(D+'higher-parts.csv')))
ER={}
for r in csv.DictReader(open(D+'examiner-insights.csv')): ER[r['question_id']]=r['what_went']
G9={'A14','A15','A13','A16','G09','G10','G13','G08','N12','S05','P04','R07','A17','A18','N05','G07'}
CW=[('show that','Show that'),('prove','Prove'),('work out','Work out'),('solve','Solve'),('explain','Explain'),('give a reason','Give a reason'),('expand and simplify','Expand and simplify'),('describe fully','Describe fully'),('describe','Describe'),('calculate','Calculate'),('write down','Write down'),('estimate','Estimate'),('find','Find'),('draw','Draw'),('factorise','Factorise'),('simplify','Simplify'),('complete','Complete'),('plot','Plot'),('sketch','Sketch'),('compare','Compare'),('express','Express')]
def cw(t):
    tl=t.lower(); return list(dict.fromkeys(n for k,n in CW if re.search(r'\b'+k+r'\b',tl)))[:4]
def qtype(r,q,c):
    t=q['text'].lower()
    if re.search(r'\bprove\b|\bshow that\b',t): return 'proof'
    if int(r['total_marks'])>=4 and c['P']>=2: return 'problem-solving'
    if q['drawing_items'] and int(q['drawing_items'])>2: return 'graph/diagram'
    if r['primary_topic'][0]=='S': return 'data'
    return 'multi-step' if int(r['total_marks'])>=3 else 'short'
mpos={}
for r in cls.values(): mpos[(r['series'],r['paper'])]=max(mpos.get((r['series'],r['paper']),0),int(r['question_no']))
info={}
for qid,r in cls.items():
    q=priv[qid]; codes=eval(q['ms_codes']) if isinstance(q['ms_codes'],str) else q['ms_codes']
    c=collections.Counter()
    for x in codes: c[x[0]]+=int(re.sub(r'\D','',x) or 1)
    tot=sum(c.values()) or 1
    t=q['text'].lower()
    info[qid]=dict(cw=cw(q['text']),typ=qtype(r,q,c),pshare=(c['P']+c['C'])/tot,proof=bool(re.search(r'\bprove\b|\bshow that\b',t)),fig=bool(q['drawing_items'] and int(q['drawing_items'])>0),pos=int(r['question_no'])/mpos[(r['series'],r['paper'])])
# parts-level difficulty rows: units with marks>0 or whole-question
units=[]
for p in parts:
    if p['row_type'] in('stem (no marks)',) or p['row_type'].startswith('parent'): continue
    if p['marks_counted'] in('0','unknown') and not p['row_type'].startswith('question-level'): continue
    units.append(p)
allm=sorted(int(u['marks_counted']) for u in units)
def pct(v): return sum(1 for x in allm if x<=v)/len(allm)
rowsH=[]
for u in units:
    qid=u['question_id']; i=info[qid]; r=cls[qid]
    s=0.35*i['pos']+0.25*pct(int(u['marks_counted']))+0.15*i['pshare']+(0.1 if i['proof'] else 0)+(0.1 if u['topic'] in G9 else 0)+(0.05 if ER.get(qid)=='less' else 0)
    rowsH.append(dict(row_id=u['row_id'],question_id=qid,part=u['part'],topic=u['topic'],marks=u['marks_counted'],paper=f"{r['series']}-{r['paper']}h",score=round(s,3),er='less' if ER.get(qid)=='less' else '',proof='yes' if i['proof'] else '',g9='yes' if u['topic'] in G9 else ''))
grp=collections.defaultdict(list)
for x in rowsH: grp[(x['paper'],x['topic'])].append(x)
sel=[]
for k,l in grp.items():
    l.sort(key=lambda x:-x['score']); n=max(1,math.ceil(0.15*len(l))); sel+=l[:n]
sel.sort(key=lambda x:(x['topic'],x['paper'],-x['score']))
w=csv.DictWriter(open(D+'hardest-parts.csv','w',newline=''),fieldnames=list(sel[0].keys()));w.writeheader();w.writerows(sel)
hardq={x['question_id'] for x in sel}
top=sorted(rowsH,key=lambda x:-x['score'])[:round(0.15*len(rowsH))]
w=csv.DictWriter(open(D+'hardest-15pct.csv','w',newline=''),fieldnames=list(top[0].keys()));w.writeheader();w.writerows(top)
hardo={x['question_id'] for x in top}
print(len(rowsH),len(sel),len(grp),len(hardq))
# questions.json
specrefs={}
for l in open(D+'TOPIC-SCHEME.md'):
    m=re.match(r'\| ([A-Z]\d\d) \| ([^|]+) \| ([^|]+) \| ([^|]+) \|',l)
    if m: specrefs[m.group(1)]=(m.group(2).strip(),m.group(3).strip(),m.group(4).strip())
import csv as _c
mp={}
for r in _c.DictReader(open(D+'mark-patterns.csv')): mp[r['question_id']]=r
qj=[]
for qid,r in cls.items():
    q=priv[qid]; i=info[qid]; st=specrefs[r['primary_topic']]
    qj.append(dict(id=qid,tier='Higher',paper=int(r['paper']),series=r['series'],year=q['year'],session=q['session'],calculator=r['calculator'],questionNumber=int(r['question_no']),marks=int(r['total_marks']),
      topic=st[0],subTopic=r['primary_topic']+' '+st[1],specRef=st[2],secondaryTags=[s for s in re.split(r'[;, ]+',r['secondary_topics']) if s],commandWords=i['cw'],questionType=i['typ'],keywords=[],hasFigure=i['fig'],
      position={'questionNumber':int(r['question_no']),'fractionOfPaper':round(i['pos'],3)},alsoOn=({'foundation':r['also_on_foundation']} if r['also_on_foundation'] else None),overlapStatus=r['overlap_status'] or None,
      sourceFile=q['qp_file'],sourcePages=q['qp_pages'] if not isinstance(q['qp_pages'],str) else json.loads(q['qp_pages']),confidence=r['confidence'],flags=[f for f,c in [('show-that-or-prove',i['proof']),('alternative-method-in-scheme',bool(mp[qid]['alternative_method_noted'])),('question-level-marks-only',qid=='nov2019-1h-8')] if c],
      hardestPartPerPaperTopic=qid in hardq,hardestOverall15pct=qid in hardo,methodNote=r['method_note']))
json.dump(qj,open('repo/questions.json','w'),indent=1,ensure_ascii=False)
print(qj[5]['commandWords'],collections.Counter(x['questionType'] for x in qj))
