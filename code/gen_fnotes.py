"""Merges hand-written method notes (docs/foundation-method-notes.csv) into the classification table and sets confidence by docs/CONFIDENCE-RULE.md. Rows without a written note stay blank and are reported as unfinished."""
import csv,json,re,collections
D='repo/docs/'
priv={q['id']:q for q in json.load(open('work/private/foundation_scored.json'))}
C=list(csv.DictReader(open(D+'foundation-classification.csv'))); fn=list(C[0].keys())
P=list(csv.DictReader(open(D+'foundation-parts.csv'))); pfn=list(P[0].keys())
spec={}
for l in open(D+'TOPIC-SCHEME.md'):
    m=re.match(r'\| ([A-Z]\d\d) \| ([^|]+) \| ([^|]+) \|',l)
    if m and m.group(1) not in spec: spec[m.group(1)]=m.group(3).strip().lower()
noise=re.compile(r'\b(DO NOT WRITE IN THIS AREA|AREA|THIS|IN|WRITE|NOT|DO)\b|\.{3,}|\(Total for Question \d+ is \d+ marks?\)|\(\d\)')
def clean(s): return re.sub(r'\s+',' ',noise.sub('',s)).strip()
def structure(codes):
    c=collections.Counter(re.sub(r'\d','',x) for x in codes)
    seq=[]
    if c['B'] and not (c['M'] or c['P']): seq.append('a direct answer mark' if c['B']==1 else f"{c['B']} independent accuracy marks")
    if c['B'] and (c['M'] or c['P']): seq.append('an independent mark alongside the method marks')
    if c['P']: seq.append('process mark'+('s' if c['P']>1 else '')+' for working towards the answer')
    if c['M']: seq.append('method mark'+('s' if c['M']>1 else '')+' for a correct approach')
    if c['A']: seq.append('an accuracy mark that depends on the method')
    if c['C']: seq.append('a communication mark for a reason or statement')
    if c['SC']: seq.append('a special-case mark for a common partial answer')
    return ', '.join(seq) or 'marks as printed'
def cues(t,tl):
    o=[]
    if re.search(r'show that',tl): o.append('a show-that question, so every step has to be written out')
    if re.search(r'\bexplain|give a reason|why\b|describe what|what is wrong|correct\?',tl): o.append('needs a written reason')
    if re.search(r'\bdraw|\bplot|\bsketch|construct|reflect|rotate|enlarge|complete the (diagram|table|graph)|shade|mark the',tl): o.append('answer is drawn or marked on a diagram')
    if re.search(r'\bgive your answer (correct )?to|decimal place|significant|nearest',tl): o.append('has a rounding instruction')
    if re.search(r'table|frequency|pictogram|chart',tl): o.append('uses data given in a table or chart')
    if re.search(r'compare|which is|better value|enough|is .* correct|yes or no',tl): o.append('ends with a decision to state')
    if re.search(r'in terms of|expression|formula',tl): o.append('answer is an algebraic expression')
    return o
def conf_rules():
    pass
parts=collections.defaultdict(list)
for r in P: parts[r['question_id']].append(r)
OCRR={r['question_id'] for r in csv.DictReader(open(D+'foundation-ocr-reviewed.csv'))}
NOTES={r['question_id']:r['method_note'] for r in csv.DictReader(open(D+'foundation-method-notes.csv'))}
POOR=set()
for q,x in priv.items():
    if len(clean(x['text']))<75 and x['total']>=2 and not q.startswith('nov2019-2f'): POOR.add(q)
newc={}
for r in C:
    q=r['question_id']; x=priv[q]; old=r['confidence']
    inherited=r['class_method'].startswith('inherited')
    if inherited: nc='high' if old=='high' else 'medium'
    else:
        srcs=[p['topic_source'] for p in parts[q]]
        reviewed=any(('relabelled' in s or 'read against method' in s or 'question and scheme read' in s or 'part text read' in s or 'page' in s) for s in srcs)
        if q=='nov2019-1f-27' : nc='low'
        elif not reviewed: nc='low'
        elif q in POOR and q not in OCRR: nc='low'
        else: nc='medium'
    r['confidence']=nc; newc[q]=nc
    if not inherited: r['method_note']=NOTES.get(q,'')
w=csv.DictWriter(open(D+'foundation-classification.csv','w',newline=''),fn);w.writeheader();w.writerows(C)
for p in P: p['confidence']=newc[p['question_id']]
w=csv.DictWriter(open(D+'foundation-parts.csv','w',newline=''),pfn);w.writeheader();w.writerows(P)
print(collections.Counter(newc.values()),sum(1 for r in C if not r['method_note']),len(POOR))
