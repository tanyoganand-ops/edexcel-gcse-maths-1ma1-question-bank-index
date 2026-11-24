import json,re,collections,sys
from scheme import T
CW=['Work out','Show that','Prove','Solve','Explain','Give a reason','Expand and simplify','Expand','Factorise','Simplify','Describe fully','Describe','Calculate','Write down','Estimate','Find','Draw','Sketch','Complete','Construct','Plot','Shade','Determine','Express','Rearrange','Make','Hence','Compare','Verify','Work out the','Circle','Tick','Show','Justify','Convert','Round','Measure','Mark','State','Give']
def words_clean(t): return re.sub(r'\.{3,}|DO NOT WRITE IN THIS AREA|\s+',' ',t).strip()
def classify(r):
    q=words_clean(r['text']).lower(); m=words_clean(r['ms_text']).lower()
    sc={}
    for tid,strand,label,refs,rx in T:
        s=0.0
        for p in rx:
            try:
                a=len(re.findall(p,q,re.I)); b=len(re.findall(p,m,re.I))
            except re.error: continue
            s+=min(a,2)*1.0+min(b,2)*0.7
        if s>0: sc[tid]=s
    return sc
if __name__=='__main__':
    r=json.load(open('work/private/higher_raw.json'))
    none=0;low=0
    for x in r:
        sc=classify(x); top=sorted(sc.items(),key=lambda t:-t[1])
        x['scores']=top[:4]
        if not top: none+=1
        elif top[0][1]<2: low+=1
    print(len(r),'no-match',none,'low(<2)',low)
    json.dump(r,open('work/private/higher_scored.json','w'))
