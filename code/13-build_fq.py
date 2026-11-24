import csv,json,re,collections
exec(open('build2.py').read().split('# parts-level')[0].split("priv=")[0])  # imports only
D='repo/docs/'
priv={q['id']:q for q in json.load(open('work/private/foundation_scored.json'))}
cls={r['question_id']:r for r in csv.DictReader(open(D+'foundation-classification.csv'))}
mp={r['question_id']:r for r in csv.DictReader(open(D+'foundation-mark-patterns.csv'))}
hq={r['question_id'] for r in csv.DictReader(open(D+'foundation-hardest-parts.csv'))}
ho={r['question_id'] for r in csv.DictReader(open(D+'foundation-hardest-15pct.csv'))}
src=open('build2.py').read()
CWl=re.search(r'^CW=.*$',src,re.M).group(0); exec(CWl)
def cw(t):
    tl=t.lower(); return list(dict.fromkeys(n for k,n in CW if re.search(r'\b'+k+r'\b',tl)))[:4]
spec={}
for l in open(D+'TOPIC-SCHEME.md'):
    m=re.match(r'\| ([A-Z]\d\d) \| ([^|]+) \| ([^|]+) \| ([^|]+) \|',l)
    if m: spec[m.group(1)]=(m.group(2).strip(),m.group(3).strip(),m.group(4).strip())
mpos={}
for r in cls.values(): k=(r['series'],r['paper']); mpos[k]=max(mpos.get(k,0),int(r['question_no']))
STOP=set('and the of for a to in with or by on at as an is'.split())
out=[]
for qid,r in cls.items():
    q=priv[qid]; st=spec[r['primary_topic']]; c=cw(q['text'])
    kw=sorted({w for w in re.findall(r'[a-z]+',(st[1]).lower()) if w not in STOP and len(w)>2}|{x.lower() for x in c})
    t=q['text'].lower()
    typ='proof' if re.search(r'\bshow that\b',t) else ('data' if r['primary_topic'][0]=='S' else ('graph/diagram' if q['drawing_items'] and int(q['drawing_items'])>2 else ('multi-step' if int(r['total_marks'])>=3 else 'short')))
    out.append(dict(id=qid,tier='Foundation',paper=int(r['paper']),series=r['series'],year=q['year'],session=q['session'],calculator=r['calculator'],questionNumber=int(r['question_no']),marks=int(r['total_marks']),
     topic=st[0],subTopic=r['primary_topic']+' '+st[1],specRef=st[2],secondaryTags=[s for s in re.split(r'[;, ]+',r['secondary_topics']) if s],commandWords=c,questionType=typ,keywords=kw,hasFigure=bool(q['drawing_items'] and int(q['drawing_items'])>0),
     position={'questionNumber':int(r['question_no']),'fractionOfPaper':round(int(r['question_no'])/mpos[(r['series'],r['paper'])],3)},alsoOn=({'higher':r['also_on_higher']} if r['also_on_higher'] else None),overlapStatus=r['overlap_status'],
     sourceFile=q['qp_file'],sourcePages=json.loads(q['qp_pages']) if isinstance(q['qp_pages'],str) else q['qp_pages'],confidence=r['confidence'],labelMethod=r['class_method'],
     flags=[f for f,cnd in [('show-that',typ=='proof'),('alternative-method-in-scheme',bool(mp[qid]['alternative_method_noted'])),('question-level-marks-only',qid=='nov2019-1f-27')] if cnd],
     hardestPartPerPaperTopic=qid in hq,hardestOverall15pct=qid in ho,methodNote=r['method_note'],methodNoteStatus=('inherited from verified Higher twin' if r['class_method'].startswith('inherited') else ('written from scheme' if r['method_note'] else 'unfinished'))))
json.dump(out,open('repo/questions-foundation.json','w'),indent=1,ensure_ascii=False)
print(len(out),sum(1 for o in out if not o['keywords']),collections.Counter(o['questionType'] for o in out))
