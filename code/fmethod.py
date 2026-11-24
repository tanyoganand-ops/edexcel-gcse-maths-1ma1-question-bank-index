import csv,collections
D='repo/docs/'
cl={r['question_id']:r for r in csv.DictReader(open(D+'foundation-classification.csv'))}
mp={r['question_id']:r for r in csv.DictReader(open(D+'foundation-mark-patterns.csv'))}
agg=collections.defaultdict(lambda:collections.Counter())
for q,r in cl.items():
    m=mp[q]; a=agg[r['primary_topic']]; a['questions']+=1; a['marks']+=int(r['total_marks'])
    for k in 'MABPC': a[k]+=int(m[k] or 0)
    for k in ['oe_noted','ft_noted','ISW_noted','cao_noted','dep_noted','alternative_method_noted','special_case_noted']: a[k]+= 1 if m[k] else 0
f=['topic','questions','marks','M_marks','A_marks','B_marks','P_marks','C_marks','questions_with_oe','with_ft','with_ISW','with_cao','with_dep','with_alternative_method','with_special_case']
w=csv.writer(open(D+'foundation-method-by-topic.csv','w',newline='')); w.writerow(f)
for t in sorted(agg):
    a=agg[t]; w.writerow([t,a['questions'],a['marks']]+[a[k] for k in 'MABPC']+[a[k] for k in ['oe_noted','ft_noted','ISW_noted','cao_noted','dep_noted','alternative_method_noted','special_case_noted']])
