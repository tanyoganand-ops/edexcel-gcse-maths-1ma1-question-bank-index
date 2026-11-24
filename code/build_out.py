import csv,json,re,os,collections,statistics
D='repo/docs/'; O='repo/'
os.makedirs(O+'topic-packs',exist_ok=True)
rows=list(csv.DictReader(open(D+'higher-classification.csv')))
priv={q['id']:q for q in json.load(open('work/private/higher_classified.json'))}
topics={}
for l in open(D+'TOPIC-SCHEME.md'):
    m=re.match(r'\| ([A-Z]\d\d) \| ([^|]+) \| ([^|]+) \| ([^|]+) \|',l)
    if m: topics[m.group(1)]=dict(strand=m.group(2).strip(),title=m.group(3).strip(),refs=m.group(4).strip())
# difficulty (heuristic, public-safe inputs only)
byp=collections.defaultdict(list)
for r in rows: byp[(r['series'],r['paper'])].append(r)
def pct(vals,v): return sum(1 for x in vals if x<=v)/len(vals)
allm=[int(r['total_marks']) for r in rows]
for k,l in byp.items():
    mx=max(int(r['question_no']) for r in l)
    for r in l: r['_pos']=int(r['question_no'])/mx
def mix(r):
    c=priv[r['question_id']]['ms_codes']; c=eval(c) if isinstance(c,str) else c
    t=sum(int(re.sub(r'\D','',x) or 1) for x in c) or 1
    p=sum(int(re.sub(r'\D','',x) or 1) for x in c if x[0] in 'PC')
    return p/t
for r in rows:
    r['_score']=round(0.5*r['_pos']+0.3*pct(allm,int(r['total_marks']))+0.2*mix(r),3)
hard={r['question_id'] for r in csv.DictReader(open(D+'hardest-15pct.csv'))}
# packs
idx=[]
for t,info in sorted(topics.items()):
    own=[r for r in rows if r['primary_topic']==t]; sec=[r for r in rows if t in re.split(r'[;, ]+',r['secondary_topics']) and r['primary_topic']!=t]
    own.sort(key=lambda r:(r['series'],int(r['paper']),int(r['question_no'])))
    L=[f"# {t}: {info['title']}\n",f"Strand: {info['strand']}. Specification refs: {info['refs']}.\n",f"Primary questions: {len(own)} ({sum(int(r['total_marks']) for r in own)} marks). Also tagged as a secondary topic on {len(sec)} more.\n",
       "Question ids are series-paper-tier-number, for example jun2019-1h-1 is the June 2019 paper 1H question 1. Find the papers on Pearson's past-paper page (linked in the README). Method notes are this project's own words.\n",
       "| Question | Marks | Calc | Confidence | Also on Foundation | In hardest 15% (any part) | Method note |","|---|---|---|---|---|---|---|"]
    for r in own: L.append(f"| {r['question_id']} | {r['total_marks']} | {r['calculator']} | {r['confidence']} | {r['also_on_foundation'] or ''} | {'yes' if r['question_id'] in hard else ''} | {r['method_note']} |")
    if sec:
        L+=["","Secondary tags:",""]+[f"- {r['question_id']} (primary {r['primary_topic']}, {r['total_marks']} marks)" for r in sorted(sec,key=lambda r:r['question_id'])]
    open(O+f'topic-packs/{t}.md','w').write('\n'.join(L)+'\n')
    idx.append((t,info['title'],len(own),sum(int(r['total_marks']) for r in own),sum(1 for r in own if r['question_id'] in hard)))
open(O+'topic-packs/INDEX.md','w').write("# Topic packs (Higher)\n\n| Topic | Title | Questions | Marks | In hardest 15% |\n|---|---|---|---|---|\n"+'\n'.join(f"| [{a}]({a}.md) | {b} | {c} | {d} | {e} |" for a,b,c,d,e in idx)+'\n')
# ms mining: mark-type share per topic (aggregate numbers only)
M=['# Marking-scheme mining (Higher), aggregates only\n','Share of each topic\'s scheme marks by type, counted from the scheme\'s own mark labels. M = method, A = accuracy, B = independent, P = process, C = communication. No scheme wording is reproduced.\n','| Topic | Questions | Marks | M | A | B | P | C |','|---|---|---|---|---|---|---|---|']
for t,info in sorted(topics.items()):
    own=[r for r in rows if r['primary_topic']==t]; c=collections.Counter()
    for r in own:
        cs=priv[r['question_id']]['ms_codes']; cs=eval(cs) if isinstance(cs,str) else cs
        for x in cs: c[x[0]]+=int(re.sub(r'\D','',x) or 1)
    tot=sum(c.values()) or 1
    M.append(f"| {t} | {len(own)} | {tot} | "+' | '.join(f"{round(100*c[k]/tot)}%" for k in 'MABPC')+' |')
open(D+'MS-MINING.md','w').write('\n'.join(M)+'\n')
print(len(topics),n,sum(1 for q in qj if q['alsoOn']))
