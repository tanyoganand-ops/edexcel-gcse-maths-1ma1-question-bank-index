import csv,json,re
PAT=[
('Solve linear equations',r'linear equation|solve.*equation',['A04']),
('Solve quadratics by factorising or formula',r'quadratic equation|factoris.*solve|quadratic formula',['A06']),
('Complete the square and turning point',r'complet\w* the square|turning point',['A06','A18']),
('Simultaneous equations (linear or linear-quadratic)',r'simultaneous',['A07']),
('Rearrange formulae',r'rearrang|subject',['A05']),
('Inequalities and regions',r'inequalit|region',['A08']),
('Sequences and nth term',r'nth term|sequence',['A12']),
('Iteration',r'iterat',['A16']),
('Algebraic proof',r'prove|proof|show that',['A15']),
('Functions: composite and inverse',r'composite|inverse function|function',['A13']),
('Algebraic fractions',r'algebraic fraction|simplif.*fraction',['A14']),
('Straight-line graphs and equations',r'gradient|straight line|perpendicular|parallel',['A09']),
('Percentage change and reverse percentages',r'percentage|reverse|multiplier',['N09']),
('Compound interest and growth/decay',r'compound|interest|growth|decay|depreciat',['R06','N09']),
('Ratio sharing',r'ratio',['R01']),
('Direct and inverse proportion',r'proportion',['R02']),
('Speed, density and pressure',r'speed|density|pressure',['R04','R05']),
('Bounds and error intervals',r'bound|error interval',['N11','N12']),
('Standard form',r'standard form',['N06']),
('Surds and rationalising',r'surd|rationalis',['N05']),
('Recurring decimals to fractions',r'recurring',['N08']),
('Indices',r'indic|power',['N04']),
('Pythagoras',r'pythagoras',['G05']),
('Right-angled trigonometry',r'trigonometr|sine|cosine|tangent ratio',['G06']),
('Sine rule, cosine rule and area formula',r'sine rule|cosine rule|area of.*triangle.*sin',['G07']),
('3D trigonometry and bearings',r'3D|three-dimensional|bearing',['G08','R08']),
('Circle theorems',r'circle theorem|angle at the centre|cyclic|tangent|segment',['G09']),
('Vectors and vector proofs',r'vector',['G13']),
('Transformations',r'transform|enlarg|reflect|rotat|translat',['G11']),
('Similarity, congruence and scale factors',r'similar|congruen|scale factor',['G10','R07']),
('Loci and constructions',r'locus|loci|construct|bisector',['G12']),
('Probability trees',r'tree|without replacement',['P02']),
('Venn diagrams and conditional probability',r'venn|conditional|set notation',['P03','P04']),
('Averages from tables',r'mean|median|mode|average|range',['S01']),
('Histograms',r'histogram|frequency density',['S05']),
('Cumulative frequency and box plots',r'cumulative|box plot|quartile',['S04']),
('Scatter graphs',r'scatter|correlation|line of best fit',['S03']),
]
def assign():
    rows=list(csv.DictReader(open('repo/docs/higher-classification.csv')))
    out={}
    for name,rx,tops in PAT:
        out[name]=[r for r in rows if r['primary_topic'] in tops and re.search(rx,r['method_note'],re.I)]
    return out
if __name__=='__main__':
    for k,v in assign().items(): print(len(v),k)
