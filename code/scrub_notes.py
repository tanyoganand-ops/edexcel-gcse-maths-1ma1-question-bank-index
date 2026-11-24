"""Public-scope scrub: removes question-specific numbers and answer values from method notes (keeps mark structure)."""
import csv,re,sys
V='[value]'
def scrub(t):
    t=re.sub(r'\s*\([^()]*\d[^()]*\)','',t)                       # parentheticals with figures
    t=re.sub(r'(?<![A-Za-z])[-\u2212£]?\d[\w.,/^\u00b0%]*(?:\s*(?:percent|degrees|minutes|hours|metres|kilometres|centimetres|squared|cubed|cm|km|kg|g|m|d\.p\.|s\.f\.|decimal places?|significant figures?)\b)?',V,t)
    t=re.sub(r'(?:\[value\])(?:\s*(?:[-+=x/\u00d7\u00f7<>\u2264\u2265,]|and|or|to|then|divided by|times|plus|minus|from)\s*(?:\[value\]))+',V,t)
    t=re.sub(r'\b(?:[a-z]\s*=\s*)?\[value\](?:,\s*[a-z]\s*=\s*\[value\])*',V,t)
    t=re.sub(r'\b(\[value\])(?:\s+\1)+',V,t)
    t=re.sub(r'\b\[value\] (?:and|or) \[value\]\b',V,t)
    return re.sub(r'\s+',' ',t).strip()
if __name__=='__main__':
    p='repo/docs/foundation-method-notes.csv'
    rows=list(csv.reader(open(p,newline='')))
    for r in rows[1:]: r[1]=scrub(r[1])
    csv.writer(open(p,'w',newline='')).writerows(rows)
