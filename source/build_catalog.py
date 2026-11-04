# Rebuilds source/catalog.js (course catalog + requirement definitions).
# Usage: git clone --depth 1 https://github.com/cornell-dti/course-plan.git /tmp/course-plan
#        python scripts/catalog/build_catalog.py /tmp/course-plan
# Programs missing from DTI's data are defined by hand further down; edit them there.
import json, re, os, sys
HERE=os.path.dirname(os.path.abspath(__file__))
B=os.path.join(sys.argv[1] if len(sys.argv)>1 else '../course-plan','src')+'/'
full=json.load(open(B+'assets/courses/full-courses.json'))
dec=json.load(open(B+'requirements/decorated-requirements.json'))
ROS=json.load(open(B+'assets/courses/rosters.json'))
rank={r:i for i,r in enumerate(ROS)}

def offered(s):
    if not s: return ''
    s=s.lower(); o=''
    if 'fall' in s: o+='F'
    if 'spring' in s: o+='S'
    if 'winter' in s: o+='W'
    if 'summer' in s: o+='U'
    return o
# catalog: one row per subject+number, keep latest roster
rows={}
for v in full.values():
    for c in v:
        code=c['subject']+' '+c['catalogNbr']
        prev=rows.get(code)
        if prev and rank.get(prev['roster'],0)>=rank.get(c['roster'],0): continue
        rows[code]=c
cids=sorted({c['crseId'] for c in rows.values()})
cidx={c:i for i,c in enumerate(cids)}
cat=[]
for code,c in sorted(rows.items(), key=lambda kv:(kv[1]['subject'],kv[1]['catalogNbr'])):
    eg=c.get('enrollGroups') or [{}]
    mn=min((g.get('unitsMinimum') or 0) for g in eg); mx=max((g.get('unitsMaximum') or 0) for g in eg)
    distr=(c.get('catalogDistr') or '')
    distr=','.join(sorted(set(re.findall(r'[A-Z]+(?:-[A-Z]+)?',distr))))
    attr=','.join(re.findall(r'CU-[A-Z]+',c.get('catalogAttribute') or ''))
    cat.append([c['subject'],c['catalogNbr'],c['titleLong'],mn,mx,cidx[c['crseId']],distr,offered(c.get('catalogWhenOffered')),c['roster'],c['acadCareer'],attr])
code2cid={r[0]+' '+r[1]:r[5] for r in cat}
# cross-listed rows share distribution codes and attributes
byc={}
for r in cat: byc.setdefault(r[5],[]).append(r)
for rs in byc.values():
    dd=sorted({t for r in rs for t in r[6].split(',') if t}); aa=sorted({t for r in rs for t in r[10].split(',') if t})
    for r in rs: r[6]=','.join(dd); r[10]=','.join(aa)
# renumbered or renamed courses: same title and either the same subject or the same number
# (PAM 2300 -> PUBPOL 2300, CS 1340 -> INFO 1260 style moves are caught when titles match)
GENERIC=re.compile(r'special topics|independent|research|thesis|honors|seminar|internship|practicum|directed|reading|topics in|studio|colloquium|workshop|project', re.I)
def ntitle(t): return re.sub(r'[^a-z0-9 ]','',t.lower()).strip()
bytitle={}
for r in cat:
    if GENERIC.search(r[2]) or len(ntitle(r[2]))<8: continue
    bytitle.setdefault(ntitle(r[2]),[]).append(r)
links={}
for t,rs in bytitle.items():
    cids_=sorted({r[5] for r in rs})
    if len(cids_)<2 or len(cids_)>3: continue
    for x in rs:
        for y in rs:
            if x[5]!=y[5] and x[1][:1]==y[1][:1] and (x[0]==y[0] or x[1]==y[1]):
                links.setdefault(x[5],set()).add(y[5])
links={k:sorted(v) for k,v in links.items()}
print('linked courses',len(links))
print('courses',len(cat),'cids',len(cids))

pool={}; poolList=[]
def enc(ids):
    xs=sorted({cidx[i] for i in ids if i in cidx})
    key=tuple(xs)
    if key in pool: return pool[key]
    prev=0; out=[]
    for x in xs: out.append(format(x-prev,'x')); prev=x
    pool[key]=len(poolList); poolList.append(','.join(out)); return pool[key]

def conv_slots(r, counting):
    slots=[]
    names=r.get('slotNames') or (['Credits'] if counting=='credits' else ['Courses'])
    for i,ids in enumerate(r.get('courses',[])):
        slots.append({'n':names[i] if i<len(names) else 'Slot %d'%(i+1),'k':r['perSlotMinCount'][i],'p':enc(ids)})
    return slots
def conv_req(r):
    fb=r['fulfilledBy']
    o={'n':r['name'],'d':r.get('description',''),'src':r.get('source','')}
    if r.get('checkerWarning'): o['w']=r['checkerWarning']
    if r.get('allowCourseDoubleCounting'): o['dbl']=1
    if r.get('minNumberOfSlots'): o['min']=r['minNumberOfSlots']
    if r.get('conditions'):
        cond={}
        for cid,cc in r['conditions'].items():
            if int(cid) in cidx and cc.get('colleges'): cond[cidx[int(cid)]]=cc['colleges']
        if cond: o['cond']=cond
    if fb=='self-check': o['t']='sc'
    elif fb=='toggleable':
        o['t']='tg'; o['opts']={}
        for name,opt in r['fulfillmentOptions'].items():
            so={'d':opt.get('description',''),'t':'cr' if opt['counting']=='credits' else 'c','slots':conv_slots(opt,opt['counting'])}
            if opt.get('minNumberOfSlots'): so['min']=opt['minNumberOfSlots']
            o['opts'][name]=so
    else:
        o['t']='cr' if fb=='credits' else 'c'
        o['slots']=conv_slots(r,fb)
    return o

progs=[]
for sec,kind in [('university','university'),('college','college'),('major','major'),('minor','minor')]:
    for k,v in dec[sec].items():
        reqs=[conv_req(r) for r in v['requirements']]
        p={'id':kind[:3]+':'+k,'kind':kind,'name':v['name'],'reqs':reqs,'origin':'dti'}
        if v.get('schools'): p['schools']=v['schools']
        progs.append(p)

# ---- hand-authored programs (Cornell catalog 2025-26) ----
def ids_codes(codes):
    return enc([cids[code2cid[c]] for c in codes if c in code2cid])
fws_pool=None
for r in dec['college']['AS2']['requirements']:
    if 'Writing' in r['name']: fws_pool=enc(r['courses'][0])
missing=[]
def C(*codes):
    for c in codes:
        if c not in code2cid: missing.append(c)
    return ids_codes(codes)
def F(*codes): return {'codes':list(codes)}
SRC_PP='https://catalog.cornell.edu/programs/public-policy-bs/'
brooks={'id':'col:PP','kind':'college','name':'Brooks School of Public Policy','origin':'new','src':SRC_PP,'reqs':[
 {'n':'First-Year Writing Seminars','t':'c','src':SRC_PP,'d':'Two FWS courses, completed within your first two semesters.','slots':[{'n':'FWS','k':2,'p':fws_pool}]},
 {'n':'Mathematics','t':'c','src':SRC_PP,'d':'Any 3-credit Cornell MATH course except MATH 1101 and MATH 1710. AP Calculus BC 4-5 or IB HL Math 6-7 also satisfy this; AP Calc AB does not.','slots':[{'n':'Math course','k':1,'f':{'subj':['MATH'],'minCr':3,'not':['MATH 1101','MATH 1710'],'lo':1000,'hi':4999}}]},
 {'n':'Natural Science I','t':'c','src':SRC_PP,'d':'One course from the approved biology, chemistry (with lab), or physics list.','slots':[{'n':'Natural science','k':1,'f':F('BIOG 1140','BIOG 1440','BIOG 1445','BIOMG 1350','BIOEE 1610','CHEM 1560','CHEM 2070','CHEM 2080','PHYS 1101','PHYS 2207','EAS 1600','PHYS 1102','PHYS 2208')}],'w':'Chemistry options need their paired lab (e.g. CHEM 2071). AP credit is handled by adding it as a custom course.'},
 {'n':'Natural Science II','t':'c','src':SRC_PP,'d':'Any 3-4 credit course with a BIO, PBS, BIOLS-AG, or BIONLS-AG distribution code. AP credit is not accepted.','slots':[{'n':'Science course','k':1,'f':{'distr':['BIO','PBS','BIOLS-AG','BIONLS-AG'],'minCr':3}}],'w':'Distribution codes are missing for many courses in this data. Mark any course that qualifies below.'},
 {'n':'Language','t':'sc','src':SRC_PP,'d':'Language study per the Exploratory Studies language list, or approved AP/IB/CASE credit.'},
 {'n':'Historical Analysis','t':'c','src':SRC_PP,'d':'Any course with an HA or HST distribution code.','slots':[{'n':'HA / HST course','k':1,'f':{'distr':['HA','HST']}}],'w':'Distribution codes are missing for many courses in this data. Mark any course that qualifies below.'},
 {'n':'Human Ecology Electives','t':'cr','dbl':1,'src':SRC_PP,'d':'9 credits with subject DEA, FSAD, HD, HE, or NS (excluding FWS, HE 1006/1105/1110/1115/1200, and 4030). May overlap with other requirements. AP Psych 4-5 may count.','slots':[{'n':'Credits','k':9,'f':{'subj':['DEA','FSAD','HD','HE','NS'],'not':['HE 1006','HE 1105','HE 1110','HE 1115','HE 1200'],'notNum':['4030']}}]},
 {'n':'120 credits total','t':'total','k':120,'src':SRC_PP,'d':'Minimum credits for the degree. Up to 12 S/U credits count; special studies are capped at 12.'},
]}
ppbs={'id':'maj:PUBPOL','kind':'major','name':'Public Policy (B.S.)','origin':'new','src':SRC_PP,'schools':['PP'],'reqs':[
 {'n':'Public Policy Core','t':'c','src':SRC_PP,'d':'Eight required core courses (28 credits). Core courses cannot be taken abroad.','slots':[
   {'n':'PUBPOL 1111','k':1,'f':F('PUBPOL 1111')},{'n':'PUBPOL 2030','k':1,'f':F('PUBPOL 2030')},{'n':'PUBPOL 2040','k':1,'f':F('PUBPOL 2040')},
   {'n':'PUBPOL 2101','k':1,'f':F('PUBPOL 2101')},{'n':'PUBPOL 2301','k':1,'f':F('PUBPOL 2301')},{'n':'PUBPOL 2370','k':1,'f':F('PUBPOL 2370')},
   {'n':'PUBPOL 3100','k':1,'f':F('PUBPOL 3100')},{'n':'Ethics (PUBPOL 3830 or 2830)','k':1,'f':F('PUBPOL 3830','PUBPOL 2830')}]},
 {'n':'Introductory Microeconomics','t':'c','src':SRC_PP,'d':'ECON 1110, or AP Micro 5 / IB HL Econ 6 (add exam credit as a custom course).','slots':[{'n':'Intro micro','k':1,'f':F('ECON 1110')}]},
 {'n':'Intermediate Microeconomics','t':'c','src':SRC_PP,'d':'PUBPOL 2000 or ECON 3030.','slots':[{'n':'Intermediate micro','k':1,'f':F('PUBPOL 2000','ECON 3030')}]},
 {'n':'Government','t':'c','src':SRC_PP,'d':'One of GOVT 1111, GOVT 1313, or GOVT 1817.','slots':[{'n':'Intro government','k':1,'f':F('GOVT 1111','GOVT 1313','GOVT 1817')}]},
 {'n':'Political Science','t':'c','src':SRC_PP,'d':'Two of PUBPOL 2320, PUBPOL 2857, PUBPOL 3583.','slots':[{'n':'Political science','k':2,'f':F('PUBPOL 2320','PUBPOL 2857','PUBPOL 3583')}]},
 {'n':'Introduction to Sociology','t':'c','src':SRC_PP,'d':'SOC 1101 or PUBPOL 2250 (2250 counts here or as an elective, not both).','slots':[{'n':'Intro sociology','k':1,'f':F('SOC 1101','PUBPOL 2250')}]},
 {'n':'Public Policy Electives','t':'cr','src':SRC_PP,'d':'22 credits of 2000-4000 level PUBPOL courses beyond the core. Excludes PUBPOL 4030, 4980, 4990; max 3 credits from 4000/4010/4020. At least one elective must carry the CU-CEL (engaged learning) attribute.','slots':[{'n':'Credits','k':22,'f':{'subj':['PUBPOL'],'lo':2000,'hi':4999,'not':['PUBPOL 4030','PUBPOL 4980','PUBPOL 4990']}}],'w':'The 3-credit cap on special studies is not enforced.'},
 {'n':'Engaged Learning (CU-CEL)','t':'c','dbl':1,'src':SRC_PP,'d':'At least one PUBPOL elective with the CU-CEL attribute. Overlaps with electives.','slots':[{'n':'CEL course','k':1,'f':{'subj':['PUBPOL'],'attr':['CU-CEL']}}]},
]}
SRC_DEM='https://catalog.cornell.edu/programs/demography-minor/'
dem={'id':'min:DEMOG','kind':'minor','name':'Demography','origin':'new','src':SRC_DEM,'reqs':[
 {'n':'Demographic Introductory Course','t':'c','src':SRC_DEM,'d':'GDEV 2010 or PUBPOL 2030.','slots':[{'n':'Intro','k':1,'f':F('GDEV 2010','PUBPOL 2030')}]},
 {'n':'Statistics','t':'c','src':SRC_DEM,'d':'One approved statistics course.','slots':[{'n':'Statistics','k':1,'f':F('AEM 2100','ILRST 2100','PUBPOL 2100','PUBPOL 2101','SOC 3010')}]},
 {'n':'Demographic Overview Course','t':'c','src':SRC_DEM,'d':'One course from the overview list.','slots':[{'n':'Overview','k':1,'f':F('AMST 2070','AMST 3800','CRP 5250','GDEV 2130','GDEV 3140','GDEV 3280','GDEV 4080','PUBPOL 3180','PUBPOL 3230','PUBPOL 3250','PUBPOL 3360','PUBPOL 3620','SOC 2310','SOC 3030')}]},
 {'n':'Additional Population Courses','t':'c','src':SRC_DEM,'d':'Two more from the additional list (or more overview courses). At least two courses in the minor must be outside your major department; B- or better in each.','slots':[{'n':'Population courses','k':2,'f':F('AMST 2710','AMST 3800','COMM 3250','COMM 4760','CRP 3430','CRP 3840','CRP 3900','CRP 4080','CRP 4680','ECON 3480','ECON 3710','ECON 3711','ECON 3760','GDEV 2130','GDEV 3060','GDEV 3390','GDEV 3700','GDEV 4080','GDEV 4770','PUBPOL 2050','PUBPOL 2208','PUBPOL 2370','PUBPOL 3050','PUBPOL 3120','PUBPOL 3151','PUBPOL 3230','PUBPOL 4160','SOC 2250','SOC 3380','SOC 3580','CRP 5250','GDEV 2010','GDEV 3140','GDEV 3280','PUBPOL 3180','PUBPOL 3250','PUBPOL 3360','PUBPOL 3620','SOC 2310','SOC 3030','AMST 2070')}],'w':'The two-courses-outside-your-department rule is not checked.'},
]}
SRC_H='https://catalog.cornell.edu/programs/history-minor/'
hist={'id':'min:HISTM','kind':'minor','name':'History','origin':'new','src':SRC_H,'reqs':[
 {'n':'Five History courses','t':'c','src':SRC_H,'d':'Five 3-4 credit courses offered or cross-listed in History, letter grade C or better. FWS courses and AP/transfer credit do not count.','slots':[{'n':'HIST courses','k':5,'f':{'subj':['HIST'],'minCr':3,'lo':1000,'hi':4999}}]},
 {'n':'History seminar (2000+)','t':'sc','src':SRC_H,'d':'One of the five must be a seminar at the 2000 level or above. Mark this once you have one planned.'},
]}
SRC_LS='https://catalog.cornell.edu/programs/law-society-minor/'
LS=json.load(open(os.path.join(HERE,'lawsoc.json')))
lawsoc={'id':'min:LAWSOC','kind':'minor','name':'Law & Society','origin':'new','src':SRC_LS,'reqs':[
 {'n':'Five approved courses','t':'cats','k':5,'minCats':3,'maxPer':2,'src':'https://philosophy.cornell.edu/law-society-courses','d':'Five 3-4 credit courses from the approved list, covering at least 3 of the 5 categories with no more than 2 per category. B- or better. PHIL 2990 counts in any category.','w':'The no-more-than-2-per-department rule is not checked. Special-topics sections (e.g. INFO 4940 LEC 003) need a petition.',
  'cats':[{'n':c['n'],'f':{'codes':c['codes']}} for c in LS]},
 {'n':'Two EPL events','t':'sc','src':SRC_LS,'d':'Attend two Ethics & Public Life events and list them on the completion form.'},
]}
# INFO minor? ok. Replace university swim with self-check
for p in progs:
    if p['id']=='uni:UNI':
        for r in p['reqs']:
            if r['n']=='Swim Test': r.clear(); r.update({'n':'Swim Test','t':'sc','d':'Pass the swim test (usually during orientation) or complete Beginning Swimming.','src':'https://scl.cornell.edu/pe/'})

# ---- Information Science (BA/BS share requirements), 2026-27 Courses of Study ----
SRC_INFO='https://catalog.cornell.edu/programs/information-science-ba/'
def one(n,*codes,k=1): return {'n':n,'k':k,'f':F(*codes)}
T4940='INFO 4940'
conc={
 'Behavioral Science':{'d':'A: two courses, B: one, C: one from any Behavior in Context list.','slots':[
   one('A. Understanding Social Behavior','INFO 4430','INFO 4450','INFO 4490','INFO 4500','INFO 4505',T4940,'COMM 4380','PSYCH 3800',k=2),
   one('B. Social Data Analytics','INFO 3300','INFO 3950','INFO 4100','INFO 4300','INFO 4350',T4940,'CS 3780','CS 4740'),
   one('C. Behavior in Context','INFO 3200','INFO 4140',T4940,'INFO 4360','COMM 4940','INFO 3450','INFO 4240','INFO 4400')]},
 'Data Science':{'d':'One course from each of A, B, C, and D.','slots':[
   one('A. Data Analysis','INFO 3300','INFO 3900','INFO 3950',T4940,'CS 3780','ORIE 3120','ORIE 3741','ORIE 4740','STSCI 3740'),
   one('B. Domain Expertise','INFO 2770','INFO 3130','INFO 3350','INFO 3370','INFO 4100','INFO 4120','INFO 4300','INFO 4350',T4940,'CS 4740'),
   one('C. Big Data Ethics, Policy and Society','INFO 3200','INFO 4140','INFO 4145','INFO 4200','INFO 4240','INFO 4250','INFO 4260','INFO 4390','INFO 4561',T4940,'ENGL 3778','PUBPOL 3460'),
   one('D. Data Communication','INFO 3312','INFO 4310','COMM 3150','COMM 3189','COMM 4860','COMM 4940','SOC 3580')]},
 'Digital Culture and Production (Option 1)':{'d':'One course each from A and B, and two from C. Any 3000+ ARCH elective that treats IT as a significant component can count for C with advising approval.','slots':[
   one('A. Digital Culture and History','INFO 2921','INFO 3200','INFO 4140','INFO 4260',T4940,'STS 4040'),
   one('B. Digital Production','INFO 2300','INFO 2310','INFO 3152','INFO 3300','INFO 4320','CS 4620','CS 4758'),
   one('C. Media, Art, Design','INFO 3450','INFO 3660','INFO 4152','INFO 4240','INFO 4400','INFO 4420',T4940,'ART 3705','ARTH 4151','COML 3115',k=2)]},
 'Digital Culture and Production (Option 2)':{'d':'Three courses from A and one from B.','slots':[
   one('A. Digital Culture and History','INFO 2921','INFO 3200','INFO 4140','INFO 4260',T4940,'STS 4040',k=3),
   one('B. Digital Production','INFO 2300','INFO 2310','INFO 3152','INFO 3300','INFO 4320','CS 4620','CS 4758')]},
 'Information Ethics, Law, and Policy':{'d':'One course from each of A, B, C, and D. You can petition the DUS to use an upper-level technical IS course for D.','slots':[
   one('A. Frameworks and Institutions','INFO 4113','INFO 4140','INFO 4200','INFO 4250','INFO 4301',T4940,'HADM 4890','PUBPOL 3460'),
   one('B. Methods and Analysis','INFO 2921','INFO 4240',T4940,'PUBPOL 2300','PUBPOL 2301'),
   one('C. Cases/Topics','COMM 4940','INFO 3200','INFO 4145','INFO 4260','INFO 4390','INFO 4561','STS 4040'),
   one('D. Tools and Technical Domains','INFO 3300','INFO 3350','INFO 3370','INFO 4100','INFO 4120','INFO 4300','INFO 4350')]},
 'Interactive Technologies':{'d':'CS 2110 plus one course from each of A, B, and C.','slots':[
   one('Required: CS 2110','CS 2110'),
   one('A. Building (with Hardware)','INFO 4120','INFO 4320','CS 4758'),
   one('B. Working with Data/Software','INFO 3300','INFO 4340','INFO 4555','CS 3780','CS 4620','CS 5150','ORIE 3120','ORIE 4740','ORIE 3741','STSCI 3740'),
   one('C. Context/Application Domains','INFO 4152','INFO 4310','INFO 4410','INFO 4430','INFO 4505',T4940)]},
 'Networks, Crowds, and Markets':{'d':'A: two courses, B: one, C: one.','slots':[
   one('A. Models','INFO 4220','INFO 4360',T4940,'COMM 3150','ECON 4020','ECON 4610','ECON 4660','ORIE 4350','SOC 3080',k=2),
   one('B. Data','INFO 3300','INFO 3950','INFO 4300','INFO 4350',T4940,'CS 3780','CS 4740','ECON 3120','ECON 3140'),
   one('C. Policy/Values','INFO 4140','INFO 4145','INFO 4200','INFO 4240','INFO 4250',T4940,'COMM 4940','PUBPOL 3460')]},
 'UX (User Experience)':{'d':'One course from each of A, B, C, and D.','slots':[
   one('A. Core Principles of Design','INFO 3450','INFO 4410','INFO 4400',T4940),
   one('B. Design in Context','INFO 2921','INFO 4240','INFO 4420','INFO 4505',T4940),
   one('C. Knowing the User','INFO 4125','INFO 4430','INFO 4450','INFO 4490','COMM 4380','PSYCH 3420'),
   one('D. Knowing the Technology','INFO 3152','INFO 4152','INFO 4310','INFO 4320','INFO 4340','CS 5150')]},
}
infomaj={'id':'maj:INFO','kind':'major','name':'Information Science (B.A. in A&S / B.S. in CALS)','origin':'new','src':SRC_INFO,'reqs':[
 {'n':'Core Courses','t':'c','src':SRC_INFO,'d':'All five core courses.','slots':[one('INFO 1200 or 1260','INFO 1200','INFO 1260'),one('INFO 1300','INFO 1300'),one('INFO 2040','INFO 2040'),one('INFO 2450','INFO 2450'),one('INFO 2950 or 2951','INFO 2950','INFO 2951')]},
 {'n':'Introductory Programming','t':'c','src':SRC_INFO,'d':'CS 1110 or CS 1112. AP Computer Science A (5) also counts.','slots':[one('Programming','CS 1110','CS 1112')]},
 {'n':'Calculus','t':'c','src':SRC_INFO,'d':'MATH 1106, 1110, or 1910. AP Calculus AB or BC (4 or 5) also counts.','slots':[one('Calculus','MATH 1106','MATH 1110','MATH 1910')]},
 {'n':'Statistics','t':'c','src':SRC_INFO,'d':'One approved statistics course. AP Statistics is not accepted.','slots':[one('Statistics','AEM 2100','BTRY 3010','CEE 3040','ECON 3110','ECON 3130','ENGRD 2700','ILRST 2100','MATH 1710','PUBPOL 2100','PSYCH 2500','SOC 3010','STSCI 2100','STSCI 2150','STSCI 2200')]},
 {'n':'Concentration','t':'tg','src':SRC_INFO,'w':'INFO 4940 and COMM 4940 only count when the specific topic is approved by your advisor. Petition if yours was.','opts':{k:{'t':'c','d':v['d'],'slots':v['slots']} for k,v in conc.items()}},
 {'n':'Electives','t':'c','src':SRC_INFO,'d':'Three courses of 3+ credits: any INFO course at 3000 or above, INFO 2300 or 2310 (not both), CS 2110, CS 3110, or CS 3410. Only one semester of INFO 4900 counts.','slots':[{'n':'Electives','k':3,'f':{'any':[{'subj':['INFO'],'lo':3000,'hi':9999,'minCr':3},{'codes':['INFO 2300','INFO 2310','CS 2110','CS 3110','CS 3410']}]}}]},
]}
progs=[p for p in progs if p['id']!='maj:INFO']

SRC_ISST='https://infosci.cornell.edu/undergraduate/info-sci-majors/bs-information-science-systems-and-technology/degree-requirements'
_prim={k:{'t':'c','d':conc[k]['d'],'slots':conc[k]['slots']} for k in ('Data Science','Interactive Technologies','Networks, Crowds, and Markets') if k in conc}
isst={'id':'maj:ISST','kind':'major','name':'Information Science, Systems, and Technology (B.S., Engineering)','origin':'new','src':SRC_ISST,'verified':'2026-27','schools':['EN'],'reqs':[
 {'n':'Engineering math','t':'c','src':SRC_ISST,'d':'MATH 1910, 1920, 2940, then MATH 2930, MATH 3040, or CS 2800.','slots':[one('MATH 1910','MATH 1910'),one('MATH 1920','MATH 1920'),one('MATH 2940','MATH 2940'),one('Fourth math','MATH 2930','MATH 3040','CS 2800')]},
 {'n':'Required engineering distributions','t':'c','src':SRC_ISST,'d':'ENGRD 2700 and ENGRD/CS 2110.','slots':[one('ENGRD 2700','ENGRD 2700'),one('ENGRD 2110 / CS 2110','ENGRD 2110','CS 2110')]},
 {'n':'Core','t':'c','src':SRC_ISST,'d':'Core courses cannot also count toward a concentration. ENGRC 3350 no longer counts (2025-26 on).','slots':[one('INFO 1200 or 1260','INFO 1200','INFO 1260'),one('ORIE 3500','ORIE 3500'),one('ORIE 3120','ORIE 3120'),one('INFO 2450','INFO 2450'),
   one('Data science / machine learning','ORIE 4740','ORIE 3741','CS 3780','CS 4786','STSCI 3740')],'w':'The department lists seven core courses; the five shown here are the ones on its core page. Check the ISST checklist for the rest.'},
 {'n':'Primary concentration','t':'tg','src':SRC_ISST,'w':'Uses the Information Science concentration lists; ISST versions may differ slightly.','opts':_prim},
 {'n':'Secondary concentration','t':'sc','src':SRC_ISST,'d':'A second concentration chosen with your advisor.'},
 {'n':'Major-approved electives','t':'c','src':SRC_ISST,'d':'Two approved electives (letter grade).','slots':[{'n':'Electives','k':2,'f':{'any':[{'subj':['INFO'],'lo':3000,'hi':9999,'minCr':3},{'subj':['ORIE','CS'],'lo':3000,'hi':4999,'minCr':3}]}}],'w':'Only major-approved courses count; check the list.'},
]}
progs += [brooks, ppbs, dem, hist, lawsoc, infomaj, isst]
# retired: replaced by newer programs (URS, ENVS, ISST)
progs=[p for p in progs if p['id'] not in ('maj:CRP','maj:ESS','maj:ISST1','maj:ISST2')]
for p in progs:
    for r in p['reqs']:
        if p['id'] in ('col:AS1','col:AS2') and r['n']=='Distribution Requirements' and p['id']=='col:AS2':
            r.pop('min',None); r['dbl2']=2
            for sl in r['slots']: sl['f']={'distr':[sl['n']+'-AS']}
            r['d']='All 10 categories, with at least 8 courses of 3+ credits. A course can cover two categories, but only two courses can do that. Courses can also count toward your major.'
        if re.search(r'writing seminar|\bFWS\b', r['n'], re.I): r['excl']=1

print('missing codes', missing)
# ---- majors and colleges rebuilt from the 2026-27 Courses of Study (majors.py) ----
sys.path.insert(0, HERE)
import majors as M
def ntitle2(t): return re.sub(r'[^a-z0-9]+',' ',t.lower()).strip()
title_index={}
for r in cat: title_index.setdefault(ntitle2(r[2]),[]).append(r)
unresolved=[]
def fix_slot(s):
    f=s.get('f') or {}
    if 'titles' in f:
        prefer=set(f.pop('prefer',[]) or [])
        codes=[]; left=[]
        for t in f.pop('titles'):
            rs=title_index.get(ntitle2(t),[])
            pick=[r for r in rs if r[0] in prefer] or rs
            if t in M.TITLE_CODES: codes+=M.TITLE_CODES[t]
            elif not pick: unresolved.append(t); left.append(ntitle2(t))
            codes+= [r[0]+' '+r[1] for r in pick]
        f['codes']=sorted(set(f.get('codes',[])+codes))
        if left: f['titles']=left   # matched at runtime against newer catalog data
    if s.pop('fws',None) or (f.get('codes')==[] and not f.get('distr') and not f.get('subj') and not f.get('any')):
        s['p']=fws_pool
        if f.get('codes')==[] and len(f)==1: s.pop('f',None)
    if f.get('subj') is None and 'subj' in f: f.pop('subj')
def fix_prog(p):
    for r in p['reqs']:
        for sl in r.get('slots',[]): fix_slot(sl)
        for o in r.get('opts',{}).values():
            for sl in o.get('slots',[]): fix_slot(sl)
new_progs=M.MAJORS+[M.ENGINEERING, M.CALS, M.BROOKS26]
for p in new_progs:
    fix_prog(p)
    for r in p['reqs']:
        if re.search(r'writing seminar|first-year writing|\bFWS\b', r['n'], re.I): r['excl']=1
if unresolved: print('UNRESOLVED TITLES', sorted(set(unresolved)))
ids={p['id'] for p in new_progs}
for p in progs:
    if p['id']=='col:AG': p['id']='col:AG0'; p['name']='Agriculture and Life Sciences (CALS) [entered before Fall 2025]'
    if p['id']=='col:EN': p['name']='Engineering (ENG) [older requirements]'; p['id']='col:EN0'
progs=[p for p in progs if p['id'] not in ids]+new_progs
print('rebuilt programs:', len(new_progs))

data={'cat':cat,'pools':poolList,'progs':progs,'rosters':ROS,'cids':cids,'links':links,'built':__import__('datetime').date.today().isoformat()}
s=json.dumps(data,separators=(',',':'))
open(os.path.join(HERE,'catalog.js'),'w').write('window.CP_DATA='+s+';\n')
print('bytes',len(s), 'pools',len(poolList), sum(len(x) for x in poolList))
