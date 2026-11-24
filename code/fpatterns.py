import json,csv,re
# Foundation mark-pattern table from the private scheme slices; own regex flags
F=json.load(open('work/private/foundation_scored.json'))
OV={'jun2025-3f-30':['M1','M1','A1'],'nov2023-2f-17':['B2','B1'],'nov2023-2f-18':['B2','B1'],'nov2023-2f-19':['M1','M1','C2'],'jun2022-1f-18':['M1','A1'],'jun2024-2f-26':['M1','M1','A1','C1'],'jun2025-1f-17':['P1','P1','C1'],'nov2020-1f-7':['C1','C1','C1','C1']}
RX=dict(oe_noted=r'\boe\b',ft_noted=r'\bft\b|follow through|follow-through',ISW_noted=r'\bISW\b',cao_noted=r'\bcao\b',dep_noted=r'\bdep\b',alternative_method_noted=r'alternative|\balt\b',special_case_noted=r'\bSC',acceptance_noted=r'accept|allow')
def val(c): return int(re.sub(r'\D','',c) or 1)
rows=[]
for x in F:
    i=x['id']; tot=int(x['total']); codes=[c for c in x['ms_codes'] if re.match(r'[A-Z]+\d',c)]; note=''
    if i in OV: codes=OV[i]; note='codes re-read from the scheme page (parser slice or alternative route; first route counted)'
    s=sum(val(c) for c in codes)
    if s!=tot and s>tot and s%tot==0 and x['ms_alt_present']:
        run=0;keep=[]
        for c in codes:
            if run>=tot: break
            keep.append(c); run+=val(c)
        if run==tot: codes=keep; note='alternative-method codes dropped (first route counted)'
        s=sum(val(c) for c in codes)
    if s!=tot and not note: note='code sum %d differs from question marks %d; not reconciled'%(s,tot)
    cnt={k:0 for k in 'MABPC'}
    for c in codes:
        k=c[0]
        if k in cnt: cnt[k]+=val(c)
    t=x['ms_text']
    r=dict(question_id=i,marks=tot,code_sequence=' '.join(codes),**cnt)
    for k,rx in RX.items(): r[k]='yes' if re.search(rx,t,re.I) else ''
    r['check_note']=note; rows.append(r)
w=csv.DictWriter(open('repo/docs/foundation-mark-patterns.csv','w',newline=''),fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
import collections
print(len(rows),collections.Counter(r['check_note'][:30] for r in rows))
print([r['question_id'] for r in rows if 'not reconciled' in r['check_note']])
