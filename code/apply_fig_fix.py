import csv,json
p='repo/docs/foundation-parts.csv'; R=list(csv.DictReader(open(p))); fn=list(R[0].keys())
view=set(json.load(open('work/f_figview2.json')))
ov={('jun2025-1f-8','b'):'G14',('jun2023-3f-8','b'):'G14',('jun2024-2f-7','c'):'G15',('jun2023-2f-7','c'):'G15',('nov2019-1f-12','b'):'N10',('nov2024-3f-7','a'):'G15',('nov2024-3f-7','b'):'G15'}
n=0
for r in R:
    k=(r['question_id'],r['part'])
    if k in ov and r['topic']!=ov[k]:
        r['topic']=ov[k]; r['topic_source']='part text read and question page viewed; overrides question label'; r['confidence']='low-medium'; n+=1
    elif r['question_id'] in view and r['topic_source'].startswith('part text read: question label kept'):
        r['topic_source']='part text read and question page viewed: label kept'
w=csv.DictWriter(open(p,'w',newline=''),fn);w.writeheader();w.writerows(R)
print(n,len(R),sum(int(r['marks_counted']) for r in R))
import collections;print(collections.Counter(r['topic_source'] for r in R))
