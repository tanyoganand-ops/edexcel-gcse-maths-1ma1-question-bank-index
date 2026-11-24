import re
V=r'\[value\]'
def fix(s):
    if '[value]' not in s: return s
    # answer positions
    s=re.sub(r'((?:marks?|awarded|accuracy|method|credit|given|scores?|working|answer|gets?|earns?)\s+for\s+)'+V+r'(?:\s*(?:,|or|and|to|/)\s*'+V+r')+', r'\1the correct values', s)
    s=re.sub(r'((?:marks?|awarded|credit)\s+for\s+)'+V+r'(?!\w)', r'\1the correct value', s)
    s=re.sub(r'(accuracy mark|answer mark|final mark) for '+V, r'\1 for the correct value', s)
    s=re.sub(r'(?i)(ratio)\s+'+V+r'\s*:\s*'+V, r'\1 as given', s)
    s=re.sub(V+r'\s*:\s*'+V+r'(?:\s*:\s*'+V+')?', 'the given ratio', s)
    s=re.sub(V+r'-digit', 'multi-digit', s)
    s=re.sub(r'(?i)\b(the|a|an)\s+'+V, lambda m: m.group(1)+(' given value' if m.group(1).lower()!='an' else ' given value'), s)
    s=re.sub(V+r'(?:\s*(?:,|or|and|to|with|from|between)\s*'+V+r')+', 'the given values', s)
    s=re.sub(r'(?i)(solve|simplify|expand|factorise|rearrange|evaluate|calculate|work out|find|convert|round|divide|multiply|draw|write)\s+'+V, lambda m: m.group(1)+' the given expression or value', s)
    s=re.sub(r'^'+V, 'The given value', s)
    s=re.sub(r'([.:;]\s+)'+V, r'\1The given value', s)
    s=re.sub(V, 'the given value', s)
    s=re.sub(r'(?i)\ba the given', 'a given', s)
    s=re.sub(r'(the (?:correct|given) value)(?:\s+the (?:correct|given) value)+', r'\1', s)
    s=re.sub(r'(the given values?)(?:\s+the given value)+', r'\1', s)
    s=re.sub(r'mx \+ the given value', 'mx + c', s)
    s=re.sub(r'identifying the given value as the (y-)?intercept', 'identifying c as the y-intercept', s)
    s=re.sub(r'answer the given value', 'answer (value omitted)', s)
    s=s.replace('the the','the').replace('The the','The')
    return s

# second pass: notes still carrying 3+ placeholders (or odd phrasing) keep only clauses
# that contain no placeholder, so the public text stays readable.
import re as _re
PH=_re.compile(r'given (value|expression|ratio)|\(value omitted\)|mx \+ c')
ODD=_re.compile(r'given value (the|\w+ given)|given value given|\+ the given|= the given value|\(the given')
FALLBACK='Question-specific working omitted from the public note; see the marks, scheme file and PDF page cited.'
def trim(s):
    if not (s.count('given value')>=2 or s.startswith('The given') or ODD.search(s)): return s
    parts=_re.split(r'(?<=[.;])\s+',s)
    keep=[p for p in parts if not _re.search(r'given (value|expression|ratio)|\(value omitted\)',p)]
    t=' '.join(keep).strip()
    if len(t)<35: return FALLBACK
    return t
