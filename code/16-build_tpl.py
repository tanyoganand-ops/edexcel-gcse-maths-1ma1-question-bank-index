import csv,json,re,collections
from patterns import PAT
from tdata import T
D='repo/docs/'
priv={q['id']:q for q in json.load(open('work/private/higher_classified.json'))}
rows=list(csv.DictReader(open(D+'higher-classification.csv')))
mp={r['question_id']:r for r in csv.DictReader(open(D+'mark-patterns.csv'))}
def members(name,rx,tops):
    m=[r for r in rows if r['primary_topic'] in tops]
    narrow=[r for r in m if re.search(rx,r['method_note'],re.I)]
    return narrow,m
out=['# Answer templates (Higher), by pattern\n',
'How to read this. Each pattern has: when it appears, a set-out skeleton (this project\'s own teaching advice, not Pearson wording), how the mark scheme awards marks in the examples listed (summarised in our own words, with the scheme file and PDF page), accepted alternatives, common errors, and "seen in" counts from our data.\n',
'Evidence status: the marking-method lines come from the scheme pages of the listed example questions only, not from every question in the pattern. The only examiner report covering Higher papers that we found is June 2019 (general chief examiner report), so common-error lines have an evidence id (T-number in `templates-evidence.csv`) or say none found. Skeleton steps are advice and have no scheme evidence unless stated. See `template-patterns.csv` for every question id per pattern.\n',
'Seen-in counts: "narrow" is the number of questions whose primary topic is in the pattern\'s topics and whose method note names the pattern; "broad" is all questions with that primary topic. Counts are of Higher questions, not de-duplicated against Foundation (the Foundation pass is not done).\n']
evid=list(csv.DictReader(open(D+'templates-evidence.csv')))
evid=[e for e in evid if re.match(r'T\d\d',e['claim_id'])]
ms_rows=[];pat_rows=[]
for name,rx,tops in PAT:
    when,skel,marking,alts,err,ex,er=T[name]
    nar,br=members(name,rx,tops)
    out.append(f'## {name}\n')
    out.append(f'- Seen in: {len(nar)} questions (narrow), {len(br)} (broad). Topics: {", ".join(tops)}.')
    out.append(f'- When it appears: {when}')
    out.append(f'- Set-out skeleton: {skel}')
    out.append(f'- How marks are earned (from the example schemes): {marking}')
    out.append(f'- Accepted alternatives and notes: {alts}')
    out.append(f'- Common errors: {err}' + (f' (evidence {", ".join(er)})' if er else ''))
    refs=[]
    for q in ex:
        p=priv[q]; page=eval(p['ms_pages']) if isinstance(p['ms_pages'],str) else p['ms_pages']
        pg=', '.join(str(x+1) for x in page); refs.append(f"{q} (scheme {p['ms_file']} PDF page {pg}; marks {mp[q]['code_sequence']})")
        ms_rows.append([name,q,p['ms_file'],pg,mp[q]['code_sequence'],'FETCHED (scheme page read; paraphrased)'])
    out.append('- Evidence examples: '+'; '.join(refs)+'\n')
    for r in br: pat_rows.append([name,r['question_id'],'narrow' if r in nar else 'broad',r['total_marks'],r['primary_topic']])
out.append('## Show that and Prove: set-out checklist\n')
out.append('- Structure: define general quantities, work line by line, finish on the exact statement asked for, then state the conclusion in words. (Skeleton is own advice.)\n- Final-line requirement: in the schemes read (jun2023-2h-17, nov2022-1h-16, jun2022-1h-12, jun2023-3h-20, jun2022-1h-13) the last mark is a communication mark for a complete argument or stated conclusion; a recurring-decimal proof with only terminating decimals scored no proof credit (jun2023-3h-20, scheme PDF p13-14).\n- What loses marks: testing particular values instead of a general argument (T08, examiner report June 2019, 1h q13).\n- Number of Higher questions flagged show-that or prove in questions.json: '+str(sum(1 for q in json.load(open('repo/questions.json')) if 'show-that-or-prove' in q['flags']))+'.\n')
out.append('## Not covered\n- Patterns for which no Higher question was found: none; but loci and constructions, 3D trigonometry and iteration have few examples, so their marking lines rest on 2 schemes each.\n- Template PDFs (this file is Markdown), and a private version with quoted scheme lines.\n- The examiner-report side for series other than June 2019.\n')
open(D+'TEMPLATES.md','w').write('\n'.join(out))
w=csv.writer(open(D+'template-patterns.csv','w',newline=''));w.writerow(['pattern','question_id','match','marks','primary_topic']);w.writerows(pat_rows)
# evidence file: ER claims + MS example rows
w=csv.writer(open(D+'templates-evidence.csv','w',newline=''))
w.writerow(['claim_id','template','claim_or_pattern','evidence_question_id','source_page','tag'])
for e in evid: w.writerow([e['claim_id'],e['template'],e['claim'],e['evidence_question_id'],'ER PDF p'+e['er_pdf_page'],e['tag']])
for i,r in enumerate(ms_rows,1): w.writerow([f'M{i:02d}','marking method',r[0],r[1],r[2]+' PDF p'+r[3]+' codes '+r[4],r[5]])
print(len(evid),len(ms_rows),len(pat_rows))
