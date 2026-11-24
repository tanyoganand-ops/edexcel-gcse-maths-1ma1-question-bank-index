import json,collections,glob
from seg import seg_paper
r=json.load(open('work/private/higher_raw.json'))
per=collections.Counter(x['series']+'-'+str(x['paper']) for x in r)
seg_total=0
for f in sorted(glob.glob('pdf/*h-que-*.pdf')):
    seg_total+=len(seg_paper(f)[0])
lettered=sum(1 for x in r for p in x['parts'] if p['part'])
print('top-level questions (seg_paper):',seg_total,' records:',len(r),' papers:',len(per))
print('lettered parts (a),(b)..:',lettered,' questions with no lettered parts:',sum(1 for x in r if not any(p['part'] for p in x['parts'])))
print('papers by question count sum check', sum(per.values()))
