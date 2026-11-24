import csv,json,collections
from fdata import P as P1
from fdata2 import P2
from frx import RX
import re,sys
sys.path.insert(0,'repo/code')
from scrub_notes import scrub
P=P1+P2
D='repo/docs/'
cl=list(csv.DictReader(open(D+'foundation-classification.csv')))
mp={r['question_id']:r for r in csv.DictReader(open(D+'foundation-mark-patterns.csv'))}
F={x['id']:x for x in json.load(open('work/private/foundation_scored.json'))}
out=['# Answer templates (Foundation), by pattern\n',
'How to read this. Each pattern has: when it appears, a set-out skeleton (this project\'s own teaching advice, not Pearson wording), what each example scheme awards (described in our own words, with scheme file and PDF page), and "seen in" counts from our data (two kinds, defined next).\n',
'Evidence status: marking lines describe only the listed example schemes (scheme file, printed PDF page) and are not general rules; other questions in the pattern may differ. No Foundation examiner report was found, so there are no examiner claims and no "common errors" evidence. All skeleton advice is UNVERIFIED teaching advice from this project.\n',
'Seen-in counts come in two kinds. The pattern count requires a primary topic in the pattern\'s topic codes and a keyword match in the question wording (a heuristic, not a read of each question). The topic count is only the number of questions with those primary topics.\n']
rows=[];ev=[]
for name,tops,when,skel,ex in P:
    n=sum(1 for r in cl if r['primary_topic'] in tops)
    nk=[r for r in cl if r['primary_topic'] in tops and re.search(RX[name],re.sub(r'\s+',' ',F[r['question_id']]['text']),re.I)]
    nk_n=len(nk)
    out.append(f'<section>\n\n## {name}\n')
    out.append(f'- Seen in: {nk_n} questions with a primary topic in {", ".join(tops)} and wording that matches the pattern keywords (heuristic, may include a few false matches and miss some); {n} questions have one of those primary topics (topic count, not a pattern count).')
    out.append(f'- When it appears: {when}')
    out.append(f'- Teaching advice (ours, set-out skeleton): {skel}')
    out.append('- What the example schemes show (one line per scheme; conditions apply to that scheme only):')
    for q,txt in ex:
        p=F[q]; pg=', '.join(str(x) for x in p['ms_pages'])
        out.append(f"    - {q} (scheme file {p['ms_file']}, PDF page {pg}; marks {mp[q]['code_sequence']}): {scrub(txt)}")
        ev.append([name,q,p['ms_file'],pg,mp[q]['code_sequence'],'FETCHED (scheme page text read; paraphrased)'])
    out.append('\n</section>\n')
    for r in cl:
        if r['primary_topic'] in tops: rows.append([name,r['question_id'],r['total_marks'],r['primary_topic'],'keyword+topic' if r in nk else 'topic only'])
out.append('## Not covered\n- Examples are one to three schemes per pattern, not every question. Every primary topic present in the Foundation data has at least one pattern, but patterns for topics with only one or two questions (for example compound interest, frequency polygons, error intervals) rest on one or two schemes and have thin evidence.\n- Topic-to-pattern grouping is this project\'s own; some questions (for example multi-topic word problems) fit several patterns.\n- Scheme text is paraphrased; the scheme itself is not in the public repo.\n- Mark codes are as printed (M, A, B, P, C, SC); what each requires is from the listed scheme only.')
open(D+'FOUNDATION-TEMPLATES.md','w').write('\n'.join(out))
w=csv.writer(open(D+'foundation-template-patterns.csv','w',newline=''));w.writerow(['pattern','question_id','marks','primary_topic','match']);w.writerows(rows)
w=csv.writer(open(D+'foundation-templates-evidence.csv','w',newline=''));w.writerow(['pattern','question_id','scheme_file','pdf_page','mark_codes','tag']);w.writerows(ev)
print(len(P),len(ev),len(rows))
