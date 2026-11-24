import pymupdf as fitz,json,csv
from PIL import Image,ImageDraw
F={x['id']:x for x in json.load(open('work/private/foundation_scored.json'))}
R=list(csv.DictReader(open('repo/docs/foundation-parts.csv')))
ids=json.load(open('work/f_figview2.json'))
def qimg(q,z=0.8):
    x=F[q]; d=fitz.open('pdf/'+x['qp_file']); ps=sorted(set(json.loads(x['qp_pages']) if isinstance(x['qp_pages'],str) else x['qp_pages']))
    ims=[Image.frombytes('RGB',[p.width,p.height],p.samples) for p in (d[i-1].get_pixmap(matrix=fitz.Matrix(z,z)) for i in ps)]
    c=Image.new('RGB',(sum(i.width for i in ims),ims[0].height),'white');xo=0
    for i in ims: c.paste(i,(xo,0)); xo+=i.width
    return c
n=0
for s in range(0,len(ids),5):
    grp=ids[s:s+5]; ims=[qimg(q) for q in grp]
    W=sum(i.width for i in ims)+10*len(ims); H=max(i.height for i in ims)+16
    c=Image.new('RGB',(W,H),'white');xo=0;dr=ImageDraw.Draw(c)
    for q,i in zip(grp,ims): dr.text((xo+4,2),q,fill='red'); c.paste(i,(xo,16)); xo+=i.width+10
    sc=1900/W if W>1900 else 1; c=c.resize((int(W*sc),int(H*sc))); c.save(f'/tmp/fs{n:02d}.png'); n+=1
print(n)
for k,q in enumerate(ids):
    print(k//5,q,[(r['part'],r['topic']) for r in R if r['question_id']==q and r['marks_counted']!='0'])
