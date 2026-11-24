import csv,re,os,collections
D='repo/docs/'; O='repo/topic-packs-foundation/'; os.makedirs(O,exist_ok=True)
rows=list(csv.DictReader(open(D+'foundation-classification.csv'))); parts=list(csv.DictReader(open(D+'foundation-parts.csv')))
topics={}
for l in open(D+'TOPIC-SCHEME.md'):
    m=re.match(r'\| ([A-Z]\d\d) \| ([^|]+) \| ([^|]+) \| ([^|]+) \|',l)
    if m: topics[m.group(1)]=dict(strand=m.group(2).strip(),title=m.group(3).strip(),refs=m.group(4).strip())
hard={r['question_id'] for r in csv.DictReader(open(D+'foundation-hardest-15pct.csv'))}
qtop={r['question_id']:r['primary_topic'] for r in rows}
odd=[p for p in parts if p['topic']!=qtop[p['question_id']] and p['marks_counted']!='0']
idx=[]
for t,info in sorted(topics.items()):
    own=sorted([r for r in rows if r['primary_topic']==t],key=lambda r:(r['series'],int(r['paper']),int(r['question_no'])))
    sec=[r for r in rows if t in re.split(r'[;, ]+',r['secondary_topics']) and r['primary_topic']!=t]
    po=[p for p in odd if p['topic']==t]
    L=[f"# {t}: {info['title']} (Foundation)\n",f"Strand: {info['strand']}. Specification refs: {info['refs']}.\n",f"Primary questions: {len(own)} ({sum(int(r['total_marks']) for r in own)} marks). Secondary on {len(sec)} more. Parts labelled {t} inside questions with another primary topic: {len(po)}.\n",
     "Question ids are series-paper-tier-number, for example jun2019-1f-1 is June 2019 paper 1F question 1. Papers are on Pearson's past-paper page (linked in the README). Labels are this project's own; confidence is high, medium or low by the rule in docs/CONFIDENCE-RULE.md. Method notes exist only for questions inherited from a verified Higher twin.\n",
     "| Question | Marks | Calc | Confidence | Also on Higher | In hardest 15% (any part) | Label basis |","|---|---|---|---|---|---|---|"]
    for r in own: L.append(f"| {r['question_id']} | {r['total_marks']} | {r['calculator']} | {r['confidence']} | {r['also_on_higher'] or ''} | {'yes' if r['question_id'] in hard else ''} | {'inherited from Higher twin' if r['class_method'].startswith('inherited') else 'own label'} |")
    if sec: L+=["","Secondary tags:",""]+[f"- {r['question_id']} (primary {r['primary_topic']}, {r['total_marks']} marks)" for r in sorted(sec,key=lambda r:r['question_id'])]
    if po: L+=["","Parts with this topic inside other questions:",""]+[f"- {p['row_id']} ({p['marks_counted']} marks)" for p in po]
    open(O+f'{t}.md','w').write('\n'.join(L)+'\n'); idx.append((t,info['title'],len(own),sum(int(r['total_marks']) for r in own),sum(1 for r in own if r['question_id'] in hard)))
open(O+'INDEX.md','w').write("# Topic packs (Foundation)\n\n| Topic | Title | Questions | Marks | In hardest 15% |\n|---|---|---|---|---|\n"+'\n'.join(f"| [{a}]({a}.md) | {b} | {c} | {d} | {e} |" for a,b,c,d,e in idx)+'\n')
print(len(idx),sum(i[2] for i in idx),sum(i[3] for i in idx),len(odd))
