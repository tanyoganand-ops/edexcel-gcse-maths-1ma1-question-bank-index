import json,re
R={q['id']:q for q in json.load(open('work/private/higher_classified.json'))}
def align(qid):
    q=R[qid]; parts=[p for p in q['parts'] if p['part'] and p['marks']>0]
    codes=q['ms_codes']
    try: nums=[int(re.sub(r'\D','',c) or 1) for c in codes]
    except: return None
    if sum(nums)!=q['total'] or sum(p['marks'] for p in parts)!=q['total']: return None
    # code index boundaries
    segs=[];i=0
    for p in parts:
        acc=0;start=i
        while i<len(nums) and acc<p['marks']: acc+=nums[i]; i+=1
        if acc!=p['marks']: return None
        segs.append((p['part'],start,i))
    # text positions
    t=q['ms_text']; pos=[];ptr=0
    for c in codes:
        m=re.compile(r'(?<![A-Za-z0-9])'+re.escape(c)+r'(?![0-9])').search(t,ptr)
        if not m: return None
        pos.append(m.start()); ptr=m.end()
    out={}
    for k,(pt,s,e) in enumerate(segs):
        a=pos[s]; b=pos[segs[k+1][1]] if k+1<len(segs) else len(t)
        out[pt]=(' '.join(codes[s:e]),re.sub(r'\s+',' ',t[a:b]))
    return out
if __name__=='__main__':
    ids=json.load(open('work/mp_ids.json'))
    ok=[i for i in ids if align(i)]
    print(len(ok),len(ids))
    nl=sum(len(align(i)) for i in ok); print('parts aligned',nl)
