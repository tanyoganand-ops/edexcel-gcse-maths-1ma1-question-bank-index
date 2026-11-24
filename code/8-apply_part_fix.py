import csv,collections,json
p='repo/docs/foundation-parts.csv'
R=list(csv.DictReader(open(p))); fn=list(R[0].keys())
M={'jun2019-2f-16':[('a(i)',1,'B1',None),('a(ii)',1,'B1',None),('b',1,'C1',None),('c',2,'M1 A1','P05')],
'jun2019-3f-11':[('a',3,'P1 P1 A1',None),('b',1,'C1','N10')],
'jun2023-2f-12':[('a',1,'B1',None),('b',1,'C1',None)],
'jun2023-2f-18':[('a',3,'P1 P1 A1',None),('b',3,'P1 P1 A1','R03')],
'jun2023-2f-9':[('a',1,'B1',None),('b',2,'M1 A1','R01')],
'jun2025-2f-20':[('a',2,'M1 A1',None),('b',2,'M1 A1',None)],
'jun2025-2f-8':[('a',1,'B1',None),('b',2,'M1 A1',None)],
'nov2019-2f-18':[('a',3,'M1 M1 A1',None),('b',1,'B1',None)],
'nov2021-1f-17':[('a',4,'P1 P1 P1 A1',None),('b',1,'C1',None)],
'nov2023-2f-13':[('a',1,'C1',None),('b',1,'C1',None)],
'nov2023-2f-18':[('a',2,'B2',None),('b',1,'B1',None)],
'nov2023-3f-22':[('a',3,'M1 M1 A1',None),('b',1,'C1',None)]}
Hp=collections.defaultdict(dict)
for h in csv.DictReader(open('repo/docs/higher-parts.csv')): Hp[h['question_id']][h['part']]=h['topic']
ov={r['foundation_id']:r['higher_id'] for r in csv.DictReader(open('repo/docs/tier-overlap.csv')) if r['status'].startswith('verified')}
out=[];seen=set()
for r in R:
    q=r['question_id']
    if q in M:
        if q in seen: continue
        seen.add(q); qt=r['topic']; conf=r['confidence']
        for part,m,c,t in M[q]:
            t2=t or qt
            out.append({**r,'row_id':f'{q}-{part}','row_type':'roman subpart' if '(' in part else 'lettered part','part':part,'marks_counted':m,'ms_codes':c,'ms_aligned':'yes (scheme page read directly)','topic':t2,'topic_source':'scheme page and question page read directly'+('; overrides question label' if t else ''),'confidence':'medium' if not t else 'low-medium'})
        continue
    if q in ov and r['marks_counted']!='0' and r['row_type'] in('lettered part','roman subpart'):
        ht=Hp[ov[q]].get(r['part'])
        if ht and ht!=r['topic']: r['topic']=ht
        if ht: r['topic_source']='from verified Higher twin part row ('+ov[q]+')'
    out.append(r)
w=csv.DictWriter(open(p,'w',newline=''),fn);w.writeheader();w.writerows(out)
print(len(out),sum(int(r['marks_counted']) for r in out))
