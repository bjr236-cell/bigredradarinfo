"""Hand-maintained major requirements, transcribed from the Cornell Courses of Study (2026-27).
Each program: id, name, src (catalog URL), reqs. Helpers keep the definitions short.
  S(name, k, *codes)            k courses from a list
  SF(name, k, **filter)         k courses matching a filter (subj, lo, hi, minCr, not, codes, any)
  C(name, credits, **filter)    credits matching a filter
  R(name, slots, d, w, dbl)     a requirement made of slots (all must be met)
  PICK(name, n, slots, d)       any n of the slots
  OPT(name, {option: (d, slots)})  choose-one-option requirement (concentrations, tracks)
  CHECK(name, d)                checkbox (not checkable from a course list)
"""
def S(n, k, *codes): return {'n': n, 'k': k, 'f': {'codes': list(codes)}}
def SF(n, k, **f):
    if 'not_' in f: f['not'] = f.pop('not_')
    return {'n': n, 'k': k, 'f': f}
def C(n, credits, **f):
    if 'not_' in f: f['not'] = f.pop('not_')
    return {'n': n, 'k': credits, 'f': f, 'cr': 1}
def R(n, slots, d='', w=None, dbl=False, src=None):
    if isinstance(slots, dict): slots = [slots]
    crs = [s.pop('cr', None) for s in slots]
    r = {'n': n, 't': 'cr' if any(crs) else 'c', 'd': d, 'slots': slots}
    if w: r['w'] = w
    if dbl: r['dbl'] = 1
    if src: r['src'] = src
    return r
def PICK(n, m, slots, d='', w=None):
    r = R(n, slots, d, w); r['min'] = m; return r
def OPT(n, opts, d='', w=None):
    o = {}
    for k, (dd, slots) in opts.items():
        crs = [s.pop('cr', None) for s in slots]
        o[k] = {'t': 'cr' if any(crs) else 'c', 'd': dd, 'slots': slots}
    r = {'n': n, 't': 'tg', 'd': d, 'opts': o}
    if w: r['w'] = w
    return r
def CHECK(n, d): return {'n': n, 't': 'sc', 'd': d}
def major(pid, name, src, reqs, schools=None):
    for r in reqs: r.setdefault('src', src)
    p = {'id': 'maj:' + pid, 'kind': 'major', 'name': name, 'origin': 'new', 'src': src, 'verified': '2026-27', 'reqs': reqs}
    if schools: p['schools'] = schools
    return p
MAJORS = []
# titles the catalog data can't resolve yet (new courses), with codes taken from the same catalog page
TITLE_CODES = {'Designing and Conducting Experiments in Firms': ['AEM 3105'], 'Attention Markets and Advertising Strategy': ['AEM 4550']}

# ---------------- Government (BA) ----------------
_AM = "1111 2011 2031 2152 2162 2274 3032 3042 3061 3072 3112 3121 3122 3132 3141 3161 3189 3251 3252 3261 3547 3557 3583 3999 4011 4021".split()
_CP = "1313 2012 2264 2274 2444 2543 2553 3251 3273 3282 3284 3293 3313 3323 3353 3394 3443 3547 3557 3583 3613 3614 3623 3805".split()
_IR = "1817 2264 2817 2847 3172 3547 3557 3617 3777 3857 3867 3947 3967 4827".split()
_PT = "1615 1616 1626 2635 2655 2665 2785 3072 3265 3596 3686 3715 3726 3736 3796 3805".split()
_SEM = "4000 4011 4021 4037 4194 4503 4827 4949 4959".split()
G = lambda nums: ["GOVT " + n for n in nums]
_src = 'https://catalog.cornell.edu/programs/government-ba/'
MAJORS.append(major('GOVT', 'Government', _src, [
  R('Introductory courses', S('Two intro courses', 2, *G(["1111", "1313", "1615", "1616", "1817"])),
    'Two of GOVT 1111, 1313, 1615 (or 1616), and 1817.', w='Only one of GOVT 1615 and 1616 counts.'),
  R('30 additional GOVT credits', C('GOVT credits', 30, subj=['GOVT'], lo=1000, hi=9999),
    'Thirty more credits of GOVT coursework, including the seminar and subfield courses below. At most one 1000-level course; no FWS.',
    w='The one-intro-course cap and the FWS exclusion are not checked. Courses must be taken under the GOVT code.'),
  R('Government seminar', S('Seminar', 1, *G(_SEM)), 'One Government seminar (GOVT-SEM). Counts inside the 30 credits.', dbl=True),
  PICK('Three of four subfields', 3, [S('American (GOVT-AM)', 1, *G(_AM)), S('Comparative (GOVT-CP)', 1, *G(_CP)),
    S('International Relations (GOVT-IR)', 1, *G(_IR)), S('Political Theory (GOVT-PT)', 1, *G(_PT))],
    'At least one course in three of the four subfields. These count inside the 30 credits.'),
]))
MAJORS[-1]['reqs'][-1]['dbl'] = 1

# ---------------- Economics (BA) ----------------
_src = 'https://catalog.cornell.edu/programs/economics-ba/'
_NOT = ['ECON 4997', 'ECON 4998', 'ECON 4999']
MAJORS.append(major('ECON', 'Economics', _src, [
  R('Introductory courses', [S('ECON 1110', 1, 'ECON 1110'), S('ECON 1120', 1, 'ECON 1120')],
    'ECON 1110 and 1120, each with a B- or better. AP credit (5) counts only with the department placement exam.'),
  R('Core courses', [S('ECON 3030', 1, 'ECON 3030'), S('ECON 3040', 1, 'ECON 3040'),
    S('ECON 3110 or 3130', 1, 'ECON 3110', 'ECON 3130'), S('ECON 3120 or 3140', 1, 'ECON 3120', 'ECON 3140')],
    'All four must be taken at Cornell.'),
  R('4000-level electives', SF('ECON 4000-level', 3, subj=['ECON'], lo=4000, hi=4999, not_=_NOT), 'At least three ECON courses at the 4000 level.'),
  R('Other electives', SF('ECON electives', 3, subj=['ECON'], lo=2400, hi=6999, not_=_NOT),
    'Three more ECON courses to reach 12 total: 3000- or 4000-level, approved graduate courses, and at most one numbered 2400-2999.',
    w='The one-course cap on 2400-2999 and the approved list of graduate courses are not checked. ECON 4997-4999 never count.'),
]))

# ---------------- Computer Science (BA and BS share the major) ----------------
_src = 'https://catalog.cornell.edu/programs/computer-science-ba/'
_CSX = ['CS 4090', 'CS 4997', 'CS 4998', 'CS 4999']
MAJORS.append(major('CS', 'Computer Science', _src, [
  R('Math', [S('Calculus I', 1, 'MATH 1110', 'MATH 1910'), S('Calculus II', 1, 'MATH 1120', 'MATH 1920'),
    S('Linear algebra', 1, 'MATH 2210', 'MATH 2940')], 'Calculus I and II (AP/CASE credit counts) and linear algebra.'),
  R('Programming', [S('Intro programming', 1, 'CS 1110', 'CS 1112'), S('CS 2110 or 2112', 1, 'CS 2110', 'CS 2112')],
    'CS 1110 or 1112 (AP CS A 5 counts), then CS 2110 or 2112.'),
  R('CS core', [S('CS 2800 or 2802', 1, 'CS 2800', 'CS 2802'), S('CS 3110', 1, 'CS 3110'), S('CS 3410 or 3420', 1, 'CS 3410', 'CS 3420'),
    S('CS 3700 or 3780', 1, 'CS 3700', 'CS 3780'), S('CS 4410 or 4414', 1, 'CS 4410', 'CS 4414'), S('CS 4820', 1, 'CS 4820')]),
  R('Practicum or project', S('Practicum', 1, 'CS 3152', 'CS 4121', 'CS 4152', 'CS 4321', 'CS 4411', 'CS 4621', 'CS 4701', 'CS 4740',
    'CS 5150', 'CS 5152', 'CS 5412', 'CS 5414', 'CS 5625', 'CS 5643'), 'One practicum or project course (2+ credits).', dbl=True),
  R('CS electives (4000+)', SF('CS 4000+', 2, subj=['CS'], lo=4000, hi=9999, minCr=3, not_=_CSX),
    'Two CS courses at 4000 or above. CS 3700/3780 also count if not used for the core.'),
  R('Technical electives', SF('Technical electives', 3, lo=3000, hi=9999, minCr=3, subj=None, any=[
      {'subj': ['CS', 'ECE', 'MATH', 'ORIE', 'STSCI', 'INFO', 'PHYS', 'MAE', 'CHEME', 'BTRY', 'ENGRD'], 'lo': 3000, 'hi': 9999}]),
    'Three 3000+ technical courses with a qualifying prerequisite (see the CS department list). At most one may be 2000-level.',
    w='The planner counts 3000+ courses in technical subjects; the department list decides. Petition any course it misses.'),
  R('External specialization', SF('External specialization', 3, lo=3000, hi=9999, minCr=3, subj=None,
      any=[{'lo': 3000, 'hi': 9999}], not_=['LING 4474', 'INFO 3300', 'INFO 4300', 'INFO 5300']),
    'Three 3000+ courses of 3+ credits outside CS, forming a coherent area. Cross-listed courses must be taken under the non-CS code.',
    w='Coherence is up to your advisor. CS-parented courses do not count.'),
  R('Major-approved elective', SF('Any 3+ credit course', 1, minCr=3, any=[{'lo': 2000, 'hi': 9999}]), 'One 3+ credit academic course (no PE, 1000-level, AP, or ROTC).'),
]))
# external specialization and electives must exclude CS
for r in MAJORS[-1]['reqs']:
    for s in r.get('slots', []):
        if r['n'] in ('External specialization',):
            s['f']['any'][0]['notSubj'] = ['CS']
        s['f'].pop('subj', None) if s['f'].get('subj') is None else None

# ---------------- Electrical and Computer Engineering (BS) ----------------
_src = 'https://catalog.cornell.edu/programs/electrical-computer-engineering-bs/'
_TECH = ['MATH', 'PHYS', 'CHEM', 'CS', 'ORIE', 'MAE', 'CEE', 'BME', 'CHEME', 'MSE', 'AEP', 'BEE', 'EAS', 'STSCI', 'BTRY', 'ENGRD', 'INFO', 'BIOMG', 'BIOG', 'BIOEE', 'BIONB']
MAJORS.append(major('ECE', 'Electrical and Computer Engineering', _src, [
  R('Math and physics for ECE', [S('MATH 2940', 1, 'MATH 2940'), S('PHYS 2214', 1, 'PHYS 2214', 'PHYS 2218')],
    'Linear algebra and Physics III, both needed by the end of sophomore year.'),
  R('Required ECE courses', [S('ECE 2100', 1, 'ECE 2100', 'ENGRD 2100'), S('ECE 2300', 1, 'ECE 2300', 'ENGRD 2300'), S('ECE 2720', 1, 'ECE 2720', 'ENGRD 2720')]),
  R('ECE foundation courses', [S('ECE 3030 or 3150', 1, 'ECE 3030', 'ECE 3150'), S('ECE 3100 or 3250', 1, 'ECE 3100', 'ECE 3250'),
    S('One more foundation course', 1, 'ECE 3030', 'ECE 3100', 'ECE 3140', 'ECE 3150', 'ECE 3250')], 'At least three foundation courses.'),
  R('Culminating design experience', S('CDE course', 1, 'ECE 4530', 'ECE 4740', 'ECE 4760', 'ECE 4670', 'ECE 4750')),
  R('ECE electives', [SF('4000-level ECE', 2, subj=['ECE'], lo=4000, hi=9999, minCr=3, not_=['ECE 4999']), SF('3000-level ECE', 3, subj=['ECE'], lo=3000, hi=9999, minCr=3, not_=['ECE 4999'])],
    'Five more ECE courses (17 credits, not counting the CDE): two at 4000+ and three at 3000+.'),
  R('Outside-ECE technical electives', [C('3000+ lecture', 3, subj=_TECH, lo=3000, hi=9999), C('Other technical', 6, subj=_TECH, lo=2000, hi=9999)],
    'Nine credits of technical courses outside ECE, at least three at 3000+. Up to 3 credits of project team or independent study can count.',
    w='Whether a course counts as "technical" is the offering major\'s call. Petition anything the planner misses.'),
  CHECK('Advisor-approved electives (6 credits)', 'Six credits of almost any credit-bearing work: courses, project teams, research. Not PE or AEW.'),
]))

# ---------------- Engineering common curriculum (college) ----------------
_ENGSRC = 'https://catalog.cornell.edu/programs/electrical-computer-engineering-bs/#collegeofengineeringgraduationrequirementstext'
_LS = ['CA', 'LA', 'LAD', 'ALC', 'SCD', 'HA', 'HST', 'KCM', 'ETM', 'SBA', 'SSC', 'GLC', 'FL', 'D']
ENGINEERING = {'id': 'col:EN', 'kind': 'college', 'name': 'Engineering (ENG)', 'origin': 'new', 'src': _ENGSRC, 'verified': '2026-27', 'reqs': [
  R('Mathematics', [S('MATH 1910', 1, 'MATH 1910'), S('MATH 1920', 1, 'MATH 1920'), S('MATH 2930 or 2940', 1, 'MATH 2930', 'MATH 2940')],
    'MATH 1910, 1920, and 2930 or 2940 (your major may require both, plus another math course). C- or better in each.', src=_ENGSRC),
  R('Physics', [S('PHYS 1112 or 1116', 1, 'PHYS 1112', 'PHYS 1116'), S('PHYS 1110', 1, 'PHYS 1110'), S('PHYS 2213 or 2217', 1, 'PHYS 2213', 'PHYS 2217')],
    'PHYS 1112, 1110, and 2213 (or honors). PHYS 2214 depends on your major.', src=_ENGSRC),
  R('Chemistry', S('CHEM 2090', 1, 'CHEM 2090', 'CHEM 2070'), 'CHEM 2090 with lab 2091.', src=_ENGSRC),
  R('Computing', S('CS 1110 or 1112', 1, 'CS 1110', 'CS 1112'), src=_ENGSRC),
  R('First-Year Writing Seminars', {'n': 'FWS', 'k': 2, 'f': {'codes': []}}, 'Two FWS courses.', src=_ENGSRC),
  R('Introduction to engineering (ENGRI)', SF('ENGRI', 1, subj=['ENGRI']), src=_ENGSRC),
  PICK('Engineering distributions (ENGRD)', 2, [
    S('Scientific computing', 1, 'ENGRD 2110', 'ENGRD 2112', 'ENGRD 2140', 'ENGRD 3200', 'CS 2110', 'CS 2112', 'ECE 2400'),
    S('Materials science', 1, 'ENGRD 2610', 'ENGRD 2620'), S('Mechanics', 1, 'ENGRD 2020'),
    S('Probability and statistics', 1, 'ENGRD 2700', 'ENGRD 2720', 'ECE 2720'),
    S('Electrical sciences', 1, 'ENGRD 2100', 'ENGRD 2300', 'ENGRD 2550', 'ECE 2100', 'ECE 2300'),
    S('Thermodynamics and energy', 1, 'ENGRD 2111', 'ENGRD 2190', 'ENGRD 2210'),
    S('Earth and life sciences', 1, 'ENGRD 2250', 'ENGRD 2400', 'ENGRD 2510', 'ENGRD 2600'),
    S('Biology and chemistry', 1, 'ENGRD 2202', 'CHEM 3890', 'ENGRD 2520', 'BIOMG 3300', 'BIOMG 3310', 'BIOMG 3350')],
    'Two ENGRD courses from two different categories.'),
  R('Engineering communication', S('Communication course', 1, 'ENGRC 3025', 'ENGRC 3026', 'ENGRC 3027', 'ENGRC 3340', 'ENGRC 3350', 'ENGRC 3500', 'ENGRC 3600', 'ENGRC 3700',
    'ENGRC 3023', 'ENGRC 3120', 'ENGRC 3152', 'ENGRC 3610', 'ENGRC 4152', 'ENGRC 4590', 'ENGRC 3341', 'BEE 4530', 'BEE 4730', 'BEE 4590', 'BME 4190',
    'BME 4390', 'BME 4490', 'CHEME 4320', 'ECE 4920', 'MAE 4272', 'MSE 4030', 'ORIE 4100', 'COMM 3020', 'COMM 3030', 'HADM 3670'),
    'One engineering communication course or approved option. May also count elsewhere.', dbl=True, src=_ENGSRC),
  R('Liberal studies', [C('Liberal studies credits', 18, distr=_LS, minCr=1), SF('Race and equity (Group 7)', 1, distr=['SCD-AS', 'D-AG'])],
    'At least six courses (18+ credits) from at least three of the seven groups, two at 2000+, and at least one Group 7 course (SCD-AS or D-AG).',
    w='The three-group, 2000-level, and six-course rules are not checked. Distribution codes are missing for many courses; mark the ones that count.', src=_ENGSRC),
  CHECK('Advisor-approved electives (6 credits)', 'Six credits approved by your faculty advisor.'),
]}
ENGINEERING['reqs'][-1]['src'] = _ENGSRC

# ---------------- Operations Research and Engineering (BS) ----------------
_src = 'https://catalog.cornell.edu/programs/operations-research-engineering-bs/'
_ORX = ['ORIE 3120', 'ORIE 3300', 'ORIE 3310', 'ORIE 3500', 'ORIE 3510', 'ORIE 4580', 'ORIE 4152', 'ORIE 5142', 'ORIE 5920', 'ORIE 9000']
MAJORS.append(major('ORIE', 'Operations Research and Engineering', _src, [
  R('Math', [S('MATH 1910', 1, 'MATH 1910'), S('MATH 1920', 1, 'MATH 1920'), S('MATH 2940', 1, 'MATH 2940'),
    S('MATH 2930, CS 2800, or MATH 3040', 1, 'MATH 2930', 'CS 2800', 'MATH 3040')]),
  R('Physics III or substitute', S('PHYS 2214 or substitute', 1, 'PHYS 2214', 'PHYS 2218', 'CHEM 2080', 'CHEM 2150', 'MATH 2930', 'CS 2800', 'MATH 3040', 'MATH 3110', 'MATH 3360'),
    'PHYS 2214 or an approved substitute (a math course only if not used for the math requirement).'),
  R('Engineering distributions for ORE', [S('ENGRD 2700', 1, 'ENGRD 2700'), S('CS 2110', 1, 'ENGRD 2110', 'CS 2110')]),
  R('Required ORIE courses', [S('ORIE 3120', 1, 'ORIE 3120'), S('ORIE 3300', 1, 'ORIE 3300'), S('ORIE 3310', 1, 'ORIE 3310'),
    S('ORIE 3500', 1, 'ORIE 3500'), S('ORIE 3510', 1, 'ORIE 3510'), S('ORIE 4580', 1, 'ORIE 4580'),
    S('Accounting or advanced math', 1, 'ORIE 3150', 'MATH 3110', 'MATH 4130', 'MATH 4310', 'MATH 4330')],
    'Any 6000+ ORIE course also works for the accounting/advanced-math slot.'),
  R('ORIE electives', C('ORIE 4000+', 9, any=[{'subj': ['ORIE'], 'lo': 4000, 'hi': 9999, 'not': _ORX}, {'codes': ['ORIE 3320', 'ORIE 3741']}]),
    'Nine credits of ORIE courses at 4000+ that are not required courses (ORIE 3320 and 3741 also count).',
    w='Caps on ORIE 4990 (3 cr) and research/project credit (3 cr) are not checked.'),
  R('Focused electives: Data, Decisions, and AI', [S('Three focused courses', 3, 'ORIE 3320', 'ORIE 3741', 'ORIE 4570', 'ORIE 4740', 'CS 3700')],
    'Three of: Optimization for AI, Learning with Big Messy Data, Reinforcement Learning with OR Applications, Statistical Data Mining I, Foundations of Causal Inference, CS 3700. Plus one AI-minor elective and CS 1340.',
    w='These overlap with ORIE and major-approved electives. The causal inference course and the AI-minor elective are not in the data; petition them.', dbl=True),
  R('Major-approved electives', C('Technical 2000+', 12, subj=['ORIE', 'CS', 'MATH', 'ECON', 'STSCI', 'BTRY', 'ECE', 'CEE', 'MAE', 'INFO', 'AEM', 'HADM', 'NBA'], lo=2000, hi=9999),
    'Twelve credits of approved technical courses at 2000+; at least 6 from Category A and 6 from outside ORIE.',
    w='The approved list and its categories are on the ORIE website; the planner counts technical subjects at 2000+.'),
  CHECK('Advisor-approved electives (6 credits)', 'Six credits agreed on with your faculty advisor.'),
]))

# ---------------- Mechanical Engineering (BS) ----------------
_src = 'https://catalog.cornell.edu/programs/mechanical-engineering-bs/'
_MAE_APPROVED = [f'MAE {n}' for n in ("3050 4060 4070 4150 4160 4230 4440 4540 4640 4650 4660 5680 4020 4120 4580 4590 5010 5430 "
  "3120 3130 4130 4240 4450 4670 4700 4721 5720 3780 4180 4190 4220 4320 4341 4351 4630 4730 4760 4770 4780 4810 5120 5350 5910 "
  "4360 4510 4530 5310 3870 4860 5070 5210").split()]
_TECHSUBJ = ['MAE', 'CS', 'ECE', 'ORIE', 'CEE', 'BME', 'CHEME', 'MSE', 'AEP', 'BEE', 'ENGRD', 'MATH', 'PHYS', 'CHEM', 'BIOMG', 'BIOG', 'BIOEE', 'BIONB', 'BIOMI', 'EAS', 'STSCI', 'BTRY']
MAJORS.append(major('ME', 'Mechanical Engineering', _src, [
  R('Required major courses', [S('ENGRD 2020', 1, 'ENGRD 2020', 'MAE 2020'), S('ENGRD 2210', 1, 'ENGRD 2210', 'MAE 2210'), S('MAE 2250', 1, 'MAE 2250'), S('MAE 2030', 1, 'MAE 2030'),
    S('Circuits: MAE 3780, ENGRD 2100, or PHYS 3360', 1, 'MAE 3780', 'ENGRD 2100', 'ECE 2100', 'PHYS 3360'), S('MAE 3230', 1, 'MAE 3230'), S('MAE 3240', 1, 'MAE 3240'),
    S('MAE 3270', 1, 'MAE 3270'), S('MAE 3260', 1, 'MAE 3260'), S('MAE 4272', 1, 'MAE 4272'), S('MAE 4300', 1, 'MAE 4300')],
    'MAE 4272 also satisfies the engineering communication requirement.'),
  R('Senior design elective', S('Senior design', 1, 'MAE 4291', 'MAE 4021', 'MAE 4121', 'MAE 4131', 'MAE 4161', 'MAE 4221', 'MAE 4231', 'MAE 4341', 'MAE 4351',
    'MAE 4441', 'MAE 4631', 'MAE 4641', 'MAE 4671', 'MAE 4721', 'MAE 4861'), 'A 3+ credit section of MAE 4291, or one 4-credit senior design course.'),
  R('Major-approved electives', C('Upper-level MAE electives', 9, codes=_MAE_APPROVED),
    'Three upper-level major-approved electives, at least 9 credits. MAE 3780 does not count again if used as the circuits course.'),
  R('Math elective', S('Upper-level math', 1, 'ENGRD 2700', 'CEE 3040', 'ENGRD 3200', 'BTRY 3010', 'CS 2800'), 'One approved math course taken after MATH 2940.'),
  R('Probability and statistics', S('Prob/stats course', 1, 'ENGRD 2700', 'CEE 3040', 'ECE 3100', 'BTRY 3010', 'ECON 3110', 'CS 2800'),
    'One course; it can also count as your math, technical, or advisor-approved elective. AP Statistics (4 or 5) also satisfies this.', dbl=True),
  R('Technical elective', SF('Technical elective', 1, subj=_TECHSUBJ, lo=2000, hi=9999, minCr=3, not_=['MAE 4980', 'MAE 4610']),
    'Any engineering, math, or science course at an appropriate (usually 2000+) level. No BSOC, economics, or business.'),
  CHECK('Advisor-approved electives (6 credits)', 'Six credits approved by your advisor. ENGRG 3400, MAE 4900, and 2000+ minor or liberal studies courses are pre-approved.'),
]))

# ---------------- Chemical Engineering (BS) ----------------
_src = 'https://catalog.cornell.edu/programs/chemical-engineering-bs/'
MAJORS.append(major('CHEME', 'Chemical Engineering', _src, [
  R('First-year chemistry', S('CHEM 2080 or 2150', 1, 'CHEM 2080', 'CHEM 2150'), 'CHEM 2090 (college requirement) then CHEM 2080 with lab, or CHEM 2150 with AP credit.'),
  R('Math and physics', [S('MATH 2930', 1, 'MATH 2930'), S('MATH 2940, CEE 3040, or ENGRD 2700', 1, 'MATH 2940', 'CEE 3040', 'ENGRD 2700'), S('PHYS 2213', 1, 'PHYS 2213', 'PHYS 2217')]),
  R('Chemistry for ChemE', [S('CHEM 3890', 1, 'CHEM 3890'), S('CHEME 2200', 1, 'CHEME 2200'), S('CHEM 2900', 1, 'CHEM 2900'),
    S('Organic chemistry', 1, 'CHEM 3570', 'CHEM 3590'), S('CHEM 2510', 1, 'CHEM 2510')],
    'CHEM 3890 and ENGRD 2190 double as your engineering distributions.'),
  R('Required ChemE courses', [S('ENGRD 2190', 1, 'ENGRD 2190', 'CHEME 2190'), S('CHEME 3230', 1, 'CHEME 3230'), S('CHEME 3130', 1, 'CHEME 3130'), S('CHEME 3240', 1, 'CHEME 3240'),
    S('CHEME 3010', 1, 'CHEME 3010'), S('CHEME 3320', 1, 'CHEME 3320'), S('CHEME 3720', 1, 'CHEME 3720'), S('CHEME 3900', 1, 'CHEME 3900'),
    S('CHEME 4320', 1, 'CHEME 4320'), S('CHEME 4620', 1, 'CHEME 4620')], 'CHEME 4320 also meets the engineering communication requirement.'),
  R('Biology elective', S('Biology option', 1, 'CHEME 2880', 'CHEME 5430', 'BIOMI 2900', 'BIOMG 3300', 'BIOMG 3350', 'BIOMG 3310', 'BIOMG 1350', 'BIOG 1440', 'BIOG 1445'),
    'One of seven options: AP Bio 5, CHEME 2880, CHEME 5430, 8 credits of pre-med biology, BIOMI 2900, BIOMG 3300/3350, or BIOMG 3310 + 3320.',
    w='The two-course options (pre-med sequence, BIOMG 3310 + 3320) are counted as soon as one course is planned.'),
  R('Advanced ChemE electives', C('Advanced CHEME', 6, subj=['CHEME'], lo=4000, hi=6999, not_=['CHEME 4320', 'CHEME 4620']),
    'Six credits of specifically approved advanced CHEME courses.', w='Only courses on the CHEME approved list count; check the department page.'),
  R('Major-approved electives', C('Major-approved', 6, subj=['CHEME', 'CHEM', 'MATH', 'PHYS', 'BIOMG', 'BIOMI', 'BME', 'MSE', 'CS', 'ORIE', 'ECE', 'MAE', 'BEE', 'CEE'], lo=2000, hi=9999),
    'The rest of the 12 credits of major-approved electives (the biology elective counts toward the 12). Needs your CHEME advisor\'s approval.'),
  CHECK('Advisor-approved electives (6 credits)', 'Six credits approved by your CHEME faculty advisor.'),
]))

def T(n, k, *titles, credits=False, prefer=None):
    """Slot defined by course titles; build_catalog resolves titles to codes from the catalog."""
    s = {'n': n, 'k': k, 'f': {'titles': list(titles)}}
    if prefer: s['f']['prefer'] = prefer
    if credits: s['cr'] = 1
    return s

# ---------------- Applied Economics and Management (Dyson, BS) ----------------
_src = 'https://catalog.cornell.edu/programs/applied-economics-management-bs/'
_QM = ['VBA for Data Analysis and Business Modeling', 'Python Programming for Data Analysis and Business Modeling', 'R Programming for Business Analytics and Data Visualization',
       'Business Statistics', 'Designing and Conducting Experiments in Firms', 'Risk Simulation and Monte Carlo Methods', 'Introduction to Econometrics', 'Strategic Thinking',
       'Predictive Analytics for Business Strategy', 'Applied Econometrics', 'Probability and Statistics', 'Econometrics', 'Game Theory I', 'Probability Models and Inference']
_P = ['AEM', 'ECON', 'HADM', 'NBA', 'ILRST', 'STSCI', 'BTRY', 'ORIE', 'CS', 'INFO', 'DEA', 'FSAD', 'LAW', 'ENGRG', 'BEE']
MAJORS.append(major('AEM', 'Applied Economics and Management (Dyson)', _src, [
  R('Economics and management core', [S('ECON 1110', 1, 'ECON 1110'), S('ECON 1120', 1, 'ECON 1120'), S('AEM 2200', 1, 'AEM 2200'), S('AEM 2225', 1, 'AEM 2225'),
    S('AEM 2240', 1, 'AEM 2240'), S('AEM 2420', 1, 'AEM 2420'), S('AEM 2600', 1, 'AEM 2600'), S('AEM 2601', 1, 'AEM 2601'), S('AEM 2700', 1, 'AEM 2700'),
    S('AEM 3200', 1, 'AEM 3200'), S('AEM 3205', 1, 'AEM 3205'), S('AEM 3230', 1, 'AEM 3230')], 'Only one core course may be taken S/U.'),
  R('Quantitative methods', [S('Calculus', 1, 'MATH 1110', 'MATH 1120', 'MATH 1910', 'MATH 1920', 'MATH 2210', 'MATH 2220', 'MATH 2230', 'MATH 2310', 'MATH 2930', 'MATH 2940'),
    S('AEM 2010', 1, 'AEM 2010'), S('AEM 2100', 1, 'AEM 2100'), T('Quantitative methods elective', 1, *_QM, prefer=_P)]),
  PICK('Applied economics (two categories)', 2, [S('Sustainable Business and Economic Policy', 1, 'AEM 2500', 'AEM 4500', 'AEM 4510'),
    S('Economic Analysis', 1, 'AEM 3105', 'AEM 3310', 'AEM 4100', 'AEM 4140', 'AEM 4160', 'AEM 4550'),
    S('International Markets and Development', 1, 'AEM 2300', 'AEM 2350', 'AEM 4300', 'AEM 4315', 'AEM 4350', 'AEM 4420', 'AEM 4450', 'AEM 4485', 'AEM 4545'),
    S('Food and Agricultural Economics', 1, 'AEM 2310', 'AEM 4150', 'AEM 4210')], 'At least six credits from two different categories.'),
  R('Grand Challenges', [S('Introduction: AEM 1101', 1, 'AEM 1101'), S('Project preparation', 1, 'AEM 3000', 'AEM 4401'),
    S('Project', 1, 'AEM 3260', 'AEM 3385', 'AEM 4000', 'AEM 4001', 'AEM 4002', 'AEM 4003', 'AEM 4004', 'AEM 4006', 'AEM 4375', 'AEM 4875', 'AEM 4876')],
    'Taken in order: introduction (waived for transfers), 1.5 credits of project preparation, then 3 credits of project.'),
  OPT('Concentration', {
    'Accounting': ('AEM 3360 and 3370 plus 9 credits of accounting electives.', [S('AEM 3360', 1, 'AEM 3360'), S('AEM 3370', 1, 'AEM 3370'),
      T('Accounting electives (9 cr)', 9, 'Financial Statements Analysis', 'Systems and Analytics in Accounting', 'Advanced Accounting', 'Cost Accounting and Management Control',
        'Auditing and Assurance', 'Federal Income Taxation', 'Fraud Examination', 'Federal Income Taxation of Low Income Taxpayers', 'Federal Income Taxation of Real Estate Ventures',
        'Federal Income Taxation of Business Entities, Estates and Trusts', 'Advanced Financial Statement Analysis', 'Financial Modeling',
        'Federal Income Taxation of Corporations and Shareholders', 'Federal Income Taxation of Flow Through Entities, Estates and Trusts', credits=True, prefer=_P)]),
    'Applied Economics': ('ECON 3040, 12 credits of applied economics electives, and 3 credits of quantitative methods.', [S('ECON 3040', 1, 'ECON 3040'),
      T('Applied economics electives (12 cr)', 12, 'International Trade and Finance', 'Business and Economics of Food', 'Introduction To The Economics Of Development',
        'Environmental and Resource Economics', 'Introduction to Business Regulation', 'The Behavioral Economics of Firms', 'Microeconomics for Management and Consulting',
        'Behavioral Economics and Managerial Decisions', 'Price Analysis', 'Strategic Pricing', 'Futures, Options and Financial Derivatives', 'International Trade Policy',
        'Economics of Developing Countries', 'Political Economy of the WTO', 'Emerging Markets', 'Toward a Sustainable Global Food System: Food Policy for Developing Countries',
        'Economics of Food and Malnutrition', 'Resource Economics', 'Environmental Economics', 'Money and Finance in the Digital Age', 'Attention Markets and Advertising Strategy', credits=True, prefer=_P),
      T('Quantitative methods (3 cr)', 3, *_QM, credits=True, prefer=_P)]),
    'Business Analytics': ('Statistics or econometrics, a programming course, database management, and 6 credits of analytics electives.', [
      T('Business Statistics or Econometrics', 1, 'Business Statistics', 'Introduction to Econometrics', 'Data Analysis and Visualization', prefer=_P),
      T('Programming', 1, 'VBA for Data Analysis and Business Modeling', 'Python Programming for Data Analysis and Business Modeling', 'R Programming for Business Analytics and Data Visualization', 'Database Management Systems', prefer=_P),
      T('Database management', 1, 'Introduction to Database Management Systems', prefer=_P),
      T('Analytics electives (6 cr)', 6, 'Designing and Conducting Experiments in Firms', 'Introduction to Machine Learning in Business', 'Customer Analytics and Strategy',
        'Risk Simulation and Monte Carlo Methods', 'Systems and Analytics in Accounting', 'Data Driven Marketing', 'Predictive Analytics for Business Strategy', 'AI for Business Applications',
        'Python Programming and its Applications in Statistics', credits=True, prefer=_P)]),
    'Entrepreneurship': ('AEM 2220 plus ideation (3), strategy (3), industries and topics (4.5), and practicum (1.5). At least 6 of the 15 credits from AEM.', [S('AEM 2220', 1, 'AEM 2220'),
      T('Ideation (3 cr)', 3, 'Introduction to Design and Innovation', 'Design and Innovation', 'Creativity Sprint: An Entrepreneurship Hackathon', 'Making a Difference by Design',
        'Human Centered Design Methods', 'Human-Computer Interaction Design', 'Developing an Entrepreneurial Mindset', 'The Business Idea Factory', 'Leading Agile Innovation', credits=True, prefer=_P),
      T('Entrepreneurial strategy (3 cr)', 3, 'Entrepreneurial Marketing and Strategy', 'The Business Laboratory and New Venture Management', 'Strategic Management of Technology and Innovation',
        'Business Model Innovation and Design', 'The Business of Entrepreneurship', credits=True, prefer=_P),
      T('Industries and topics (4.5 cr)', 4.5, 'Digital Business Strategy', 'The Startup and Venture Capital Experience', "Social Entrepreneurship Practicum: Anabel's Grocery",
        'Innovation And New Product Management', 'Research and Strategy in Emerging Markets', 'Entrepreneurial Finance and Private Equity', 'Digital Platform Strategy',
        'Digital Innovation in Media Markets & Creative Industries', 'Fiber Science and Apparel Design Futures', 'Textiles, Apparel, and Innovation', 'Communication for Entrepreneurs',
        'Entrepreneurial Management', 'Nonprofit Social Enterprise and Food Justice', 'Law for Entrepreneurs', 'Entrepreneurship for Scientists and Engineers', credits=True, prefer=_P),
      T('Practicum (1.5 cr)', 1.5, 'The Business Laboratory and New Venture Management', 'Creativity Sprint: An Entrepreneurship Hackathon', "Social Entrepreneurship Practicum: Anabel's Grocery",
        'Research and Strategy in Emerging Markets', 'Undergraduate Experience in Entrepreneurship', 'Nonprofit Social Enterprise and Food Justice', 'Leading Agile Innovation',
        'Actualizing Your Startup - Part I', 'Actualizing Your Startup - Part II', credits=True, prefer=_P)]),
    'Finance': ('AEM 4570, AEM 4670, and 9 credits of finance electives.', [S('AEM 4570', 1, 'AEM 4570'), S('AEM 4670', 1, 'AEM 4670'),
      T('Finance electives (9 cr)', 9, 'Financial Statements Analysis', 'Corporate Financial Reporting I', 'Risk Simulation and Monte Carlo Methods', 'Futures, Options and Financial Derivatives',
        'Behavioral Finance', 'Behavioral Finance I', 'Behavioral Finance II', 'Fixed-Income Securities', 'Valuation of Capital Investment', 'International Financial Management',
        'Money and Finance in the Digital Age', 'Entrepreneurial Finance and Private Equity', 'Financial Markets and Institutions', 'Impact Finance', credits=True, prefer=_P)]),
    'Food Business Management': ('AEM 2310, AEM 2480, and food business electives.', [S('AEM 2310', 1, 'AEM 2310'), S('AEM 2480', 1, 'AEM 2480'),
      T('Food business electives (9 cr)', 9, 'Introduction to Agricultural Finance', 'Farm Business Management', 'Cooperative Business Management', 'Supply Chain Strategy and Supermarket Simulation',
        'Consumer Behavior', 'Introduction to Operations Management', 'Customer Analytics and Strategy', 'Price Analysis', 'Futures, Options and Financial Derivatives', 'Retail Strategy',
        'Toward a Sustainable Global Food System: Food Policy for Developing Countries', 'Food Marketing Fellows', 'Retail and Supply Chain Strategy', 'Predictive Analytics for Business Strategy', credits=True, prefer=_P)]),
    'International Markets and Development': ('AEM 2300 or 2350, then 12 credits of electives (at least 6 from category A).', [S('AEM 2300 or 2350', 1, 'AEM 2300', 'AEM 2350'),
      T('Methods and topics (12 cr)', 12, 'Rating Nations: Economic Performance and Other Indicators', 'International Trade Policy', 'Economics of Developing Countries', 'Political Economy of the WTO',
        'Pre-Engagement with Social Enterprises in Emerging Markets', 'Emerging Markets', 'Research and Strategy in Emerging Markets', 'Toward a Sustainable Global Food System: Food Policy for Developing Countries',
        'Economics of Food and Malnutrition', 'Money and Finance in the Digital Age', 'Introduction to Econometrics', 'Applied Econometrics', 'Econometrics', 'Data Mining and Machine Learning',
        'Python Programming and its Applications in Statistics', 'Introduction to International and Comparative Labor', 'Evaluation of International Programs and Projects', 'International Institutions', credits=True, prefer=_P)]),
    'Marketing': ('AEM 4410, consumer behavior, and 9 credits of marketing electives.', [S('AEM 4410', 1, 'AEM 4410'), S('Consumer Behavior', 1, 'AEM 3440', 'HADM 3470'),
      T('Marketing electives (9 cr)', 9, 'Food and Consumer Packaged Goods Industry Dynamics', 'Entrepreneurial Marketing and Strategy', 'Supply Chain Strategy and Supermarket Simulation',
        'Customer Analytics and Strategy', 'Innovation And New Product Management', 'Digital Marketing', 'Behavioral Economics and Managerial Decisions', 'Price Analysis', 'Strategic Pricing',
        'Retail Strategy', 'Data Driven Marketing', 'Food Marketing Fellows', 'Retail and Supply Chain Strategy', 'Attention Markets and Advertising Strategy', 'Brand Management', credits=True, prefer=_P)]),
    'Strategy': ('Nine credits of strategy upper core and six credits of strategy electives.', [
      T('Strategy upper core (9 cr)', 9, 'Digital Business Strategy', 'Strategic Pricing', 'Strategic Thinking', 'Predictive Analytics for Business Strategy', 'Digital Platform Strategy',
        'Digital Innovation in Media Markets & Creative Industries', credits=True, prefer=_P),
      T('Strategy electives (6 cr)', 6, 'Managing People', 'Negotiation Strategies and Skills', 'Design and Innovation', 'Organizational Behavior', 'Entrepreneurial Marketing and Strategy',
        'Cooperative Business Management', 'Supply Chain Strategy and Supermarket Simulation', 'Leadership and Management in Sports', 'The Behavioral Economics of Firms',
        'Introduction to Operations Management', 'Customer Analytics and Strategy', 'Innovation And New Product Management', 'Research and Strategy in Emerging Markets',
        'Attention Markets and Advertising Strategy', 'Sustainable Business', 'Strategic Management of Technology and Innovation', 'Business Management Simulation', credits=True, prefer=_P)]),
    'Sustainable Business and Economic Policy': ('AEM 2500 plus business (3), analytical (6), and quantitative (3) electives.', [S('AEM 2500', 1, 'AEM 2500'),
      T('Business and management (3 cr)', 3, 'Corporate Sustainability', 'Environmental Finance and Markets', 'Financial Markets and Sustainability', 'Sustainable Business', 'Strategies for Sustainability', credits=True, prefer=_P),
      T('Analytical (6 cr)', 6, 'Resource Economics', 'Environmental Economics', 'Cost-Benefit Analysis for Sustainability', credits=True, prefer=_P),
      T('Quantitative (3 cr)', 3, 'Excursions in Computational Sustainability', 'VBA for Data Analysis and Business Modeling', 'Python Programming for Data Analysis and Business Modeling',
        'R Programming for Business Analytics and Data Visualization', 'Business Statistics', 'Introduction to Econometrics', 'Empirical Methods for Applied Economists', 'Applied Econometrics',
        'Econometrics', 'Statistical Methods for the Social Sciences II', 'Python Programming and its Applications in Statistics', credits=True, prefer=_P)]),
  }, 'At least one concentration (at most two). Core courses cannot also count toward a concentration.',
    w='Some concentration categories have caps (e.g. only 3 credits of IMD category B, C, or D) that are not checked.'),
], schools=['AG', 'BU']))

# ---------------- CALS college requirements (2025+ curriculum) ----------------
_CALSSRC = 'https://catalog.cornell.edu/programs/applied-economics-management-bs/#collegetext'
_CALS_PREFIX = 'AGSCI AIIS ALS ANSC BEE BIOG BIOAP BIOCB BIOEE BIOMG BIOMI BIOMS BIONB BIOSM COMM EAS EDUC ENTOM ENVS FDSC GDEV INFO LA LEAD NS NTRES PLSCI STSCI VIEN BSOC'.split()
CALS = {'id': 'col:AG', 'kind': 'college', 'name': 'Agriculture and Life Sciences (CALS)', 'origin': 'new', 'src': _CALSSRC, 'verified': '2026-27', 'reqs': [
  R('75 CALS credits', C('CALS credits', 75, subj=_CALS_PREFIX), 'Seventy-five credits in CALS prefixes (55 for transfers). AEM counts only for AEM majors; up to two FWS courses count.',
    w='AEM credit for Dyson majors and the FWS allowance are not added automatically.', src=_CALSSRC),
  R('Agriculture, Food Systems & Human Nutrition', SF('AFS-AG', 1, distr=['AFS-AG'], minCr=3), src=_CALSSRC),
  R('Biological Sciences', SF('BSC-AG', 1, distr=['BSC-AG'], minCr=3), 'BIO-AG and BIO-AS do not count.', src=_CALSSRC),
  R('Physical Sciences', SF('PSC-AG', 1, distr=['PSC-AG'], minCr=3), src=_CALSSRC),
  R('Sustainability Challenges', SF('SCH-AG', 1, distr=['SCH-AG'], minCr=3), src=_CALSSRC),
  R('Data Literacy', [SF('Data Literacy Statistics', 1, distr=['DLS-AG'], minCr=3), SF('Data Literacy General or Statistics', 1, distr=['DLG-AG', 'DLS-AG'], minCr=3)], src=_CALSSRC),
  R('Ethics', SF('ETH-AG', 1, distr=['ETH-AG'], minCr=3), 'KCM and ETM codes do not count.', src=_CALSSRC),
  R('Human Diversity', SF('D-AG', 1, distr=['D-AG', 'SCD-AS', 'SCD-HA', 'D-HE'], minCr=3), src=_CALSSRC),
  PICK('Cultural, Social & Historical Understanding', 2, [
    SF('Cultural Analysis', 1, distr=['CA-AG', 'ALC-AS', 'ALC-HA', 'ALC-AAP', 'CA-HE', 'CA-AAP', 'GLC-AS'], minCr=3), SF('Foreign Language', 1, distr=['FL-AG', 'FL'], minCr=3),
    SF('Historical Analysis', 1, distr=['HA-AG', 'HA-AAP', 'HST-AAP', 'HST-AS', 'HST-HA', 'HA-HE'], minCr=3), SF('Literature and the Arts', 1, distr=['LA-AG', 'ALC-AS', 'ALC-HA', 'ALC-AAP', 'LA-AAP'], minCr=3),
    SF('Social and Behavioral Analysis', 1, distr=['SBA-AG', 'SSC-AS', 'SBA-HE', 'SBA-AAP', 'SSC-AAP'], minCr=3)], 'Two courses from two different categories.'),
  R('Written and Oral Expression', {'n': 'Written Expression (incl. FWS)', 'k': 6, 'f': {'distr': ['WRT-AG']}, 'cr': 1, 'fws': 1},
    'Nine credits, at least six in Written Expression (FWS counts). One Oral Expression course may count if your major allows.', w='Oral Expression credits are not added here.', src=_CALSSRC),
  R('E3 Learning Milestone', SF('Engaged/experiential course', 1, any=[{'attr': ['CU-CEL']}, {'distr': ['EEE-AG']}]),
    'One course with the CU-CEL attribute or EEE-AG code, or an approved non-course experience.', src=_CALSSRC),
]}

# ---------------- Hotel Administration (Nolan, BS) ----------------
_src = 'https://catalog.cornell.edu/programs/hotel-management-bs/'
_HCORE = "1210 2210 2220 2221 1150 2810 3870 1361 2351 1740 1650 3650 1350 2011 2021 2560 1410 2430 4410".split()
_NONJCB = ['AEM', 'HADM', 'NBA', 'NBAY', 'NCC', 'NCCY', 'BUS']
MAJORS.append(major('HADM', 'Hotel Administration (Nolan)', _src, [
  R('Core courses', [S(f'HADM {n}', 1, f'HADM {n}') for n in _HCORE], '58 credits of Nolan core, ideally two-thirds done in the first two years.'),
  R('HADM electives', C('Upper-level HADM', 12, subj=['HADM'], lo=3000, hi=9999, not_=['HADM 4960']),
    'Twelve credits of HADM at 3000+, letter-graded. The Real Estate minor can fulfill this.',
    w='Only 3 credits of HADM 4910/4930/4940/4970/4971/4980/4990 count here; that cap is not checked.'),
  PICK('Non-JCB distribution electives', 3, [
    SF('Arts, Literature & Culture / Historical Analysis', 1, distr=['ALC-AS', 'HST-AS', 'HA-HE', 'LAD-HE', 'LA-AAP', 'HA-AAP', 'ALC-AAP', 'HA-AG', 'LA-AG'], minCr=3),
    SF('Global Citizenship / Social Difference', 1, distr=['GLC-AS', 'SCD-AS', 'CA-HE', 'CA-AAP', 'CA-AG', 'D-HE', 'D-AG'], minCr=3),
    SF('Social Science', 1, distr=['SSC-AS', 'SBA-HE', 'SBA-AAP', 'SBA-AG'], minCr=3),
    SF('Mathematics and Data Science', 1, distr=['SMR-AS', 'SDS-AS', 'MQR-AAP'], minCr=3),
    SF('Biological and Physical Science', 1, distr=['BIO-AS', 'PHS-AS', 'PBS-HE', 'PBS-AAP', 'BIO-AG', 'BIOLS-AG', 'BIONLS-AG'], minCr=3)],
    'Fifteen credits outside the SC Johnson College, with at least 3 credits in three of five categories.',
    w='The 15-credit total and the outside-JCB rule are not checked. Distribution codes are missing for many courses; mark the ones that count.'),
  R('Distribution electives', C('Any distribution-coded course', 18, distr=['ALC', 'HST', 'HA', 'LA', 'LAD', 'GLC', 'SCD', 'CA', 'D', 'SSC', 'SBA', 'SMR', 'SDS', 'MQR', 'BIO', 'PHS', 'PBS', 'BIOLS', 'BIONLS', 'ETM', 'KCM', 'FL', 'ETH']),
    'Eighteen credits of courses carrying any Cornell distribution code.'),
  R('First-Year Writing', {'n': 'FWS', 'k': 1, 'f': {'codes': []}, 'fws': 1}, 'One FWS in your first or second semester.'),
  CHECK('Ethics course', 'One 3-credit course from the Nolan ethics list.'),
  CHECK('Diversity & Inclusion course', 'One 3-credit course from the Nolan D&I list.'),
  CHECK('Practice credit (800 hours)', 'Two units of work experience, paid or unpaid.'),
]))

# ---------------- Industrial and Labor Relations (BS) ----------------
_src = 'https://catalog.cornell.edu/programs/industrial-labor-relations-bs/'
_ILRCORE = ['ILRID 1510', 'ILRID 1525', 'ILRID 1535', 'ILRGL 1100', 'ILRGL 2010', 'ILRGL 2050', 'ILRLE 2400', 'ECON 1110', 'ECON 1120']
MAJORS.append(major('ILR', 'Industrial and Labor Relations', _src, [
  R('Core courses', [S(c, 1, c) for c in _ILRCORE] + [S('Diversity, equity, and inclusion', 1, 'ILRID 2510', 'EDUC 2610'),
    S('International and comparative labor', 1, 'ILRGL 2300', 'ILRGL 2350')], 'All core courses for a letter grade.'),
  R('Statistics', C('STA-IL credits', 7, distr=['STA-IL'], any=[{'distr': ['STA-IL']}, {'codes': ['ILRST 2100', 'ILRST 2110', 'ILRST 2120']}]),
    'Seven credits of courses with the STA-IL code (usually ILRST 2100 plus a second course).'),
  R('Writing', [{'n': 'First-Year Writing Seminar', 'k': 1, 'f': {'codes': []}, 'fws': 1}, SF('Sophomore Writing Seminar (SOW-IL)', 1, distr=['SOW-IL']),
    SF('Advanced Writing Intensive (AWI-IL)', 1, distr=['AWI-IL'])],
    'An FWS, a sophomore writing seminar, and an advanced writing-intensive elective. Some core sections double as the sophomore seminar.', dbl=True),
  R('Science and technology', SF('SCT-IL', 1, distr=['SCT-IL'], minCr=3), 'Three credits with the SCT-IL code.'),
  R('In-college ILR advanced electives', C('ICE-IL credits', 24, distr=['ICE-IL']),
    'At least 24 of the 40 advanced elective credits from ICE-IL courses, letter-graded.', w='Independent study is capped at 8 credits; not checked.'),
  R('Required ILR elective areas', [SF('Quantitative Policy (QP-IL)', 1, distr=['QP-IL']), SF('International & Comparative Labor (ICL-IL)', 1, distr=['ICL-IL']),
    SF('Labor History (LH-IL)', 1, distr=['LH-IL'])], 'Three credits in each, counted inside the 24 ICE-IL credits.', dbl=True),
  R('Remaining advanced electives', C('ICE-IL or OCE-IL credits', 16, distr=['ICE-IL', 'OCE-IL', 'OCL-IL']),
    'The other 16 advanced elective credits can be more ICE-IL courses or approved out-of-college (OCE-IL) courses, including up to 12 language credits (OCL-IL).'),
]))
ILR_COLLEGE_NOTE = 'ILR requirements are part of the major; the school has no separate distribution list.'

# ---------------- Global Development (BS) ----------------
_src = 'https://catalog.cornell.edu/programs/global-development-bs/'
G2 = lambda *n: ['GDEV ' + x for x in n]
_SED = G2('2010', '2202', '3150', '3240', '3400', '3700', '2300', '2710', '3020', '3030', '3260', '3280', '4050', '4340', '4450', '4770', '2155', '2100', '2210', '2410',
          '3142', '4011', '4200', '4223', '2295', '3140', '3300', '3390', '3500', '3501', '3502', '3680', '3740', '3900', '4045', '4080', '4190', '4295') + \
       ['AEM 2000', 'AEM 2350', 'AEM 2500', 'AEM 2300', 'AEM 4300', 'AEM 4350', 'AEM 4420', 'EDUC 2710', 'PUBPOL 3280', 'CRP 4770', 'EDUC 2155', 'EDUC 2200',
        'EDUC 2210', 'EDUC 2410', 'EDUC 3142', 'EDUC 4010', 'EDUC 4200', 'EDUC 4223']
_AFS_FOUND = ['ANSC 2000', 'BIOEE 4690', 'PLSCI 2110', 'PLSCI 2440', 'PLSCI 3210', 'PLSCI 4140', 'GDEV 4140']
_AFS_SPEC = ['ANSC 2120', 'BIOEE 4780', 'ENTOM 2030', 'ENTOM 2031', 'PLSCI 2600', 'PLSCI 3010', 'PLSCI 3025', 'PLSCI 3150', 'PLSCI 3350', 'PLSCI 3550', 'PLSCI 3800',
             'PLSCI 4020', 'PLSCI 4175', 'PLSCI 4230', 'VIEN 3610']
_AFS_SOC = ['AEM 4485', 'NS 3060', 'NTRES 3330'] + G2('2202', '2295', '2300', '2450', '3020', '3030', '3140', '3170', '3260', '3300', '3400', '3500', '3501', '3502',
                                                    '3680', '3740', '3900', '4045', '4080', '4190', '4295', '4450', '4880')
_ED_SOC = G2('3150', '3170', '3240', '3390', '3680')
_ED_BIO = ['EAS 1101', 'ENVS 1201', 'EAS 2680', 'NTRES 3220', 'NTRES 3240', 'GDEV 3260']
_ED_MORE = ['BEE 2000', 'NTRES 3330', 'PUBPOL 3670', 'SOC 3650'] + G2('2010', '2202', '2295', '2300', '2450', '3020', '3030', '3140', '3150', '3170', '3240', '3260', '3300',
            '3390', '3400', '3500', '3501', '3502', '3680', '3740', '4045', '4080', '4190', '4295', '4340', '4850')
MAJORS.append(major('GDEV', 'Global Development', _src, [
  R('Core', [S('GDEV 1102', 1, 'GDEV 1102'), S('GDEV 1105', 1, 'GDEV 1105'), S('GDEV 1300', 1, 'GDEV 1300'), S('GDEV 2065', 1, 'GDEV 2065'), S('GDEV 2130', 1, 'GDEV 2130'),
    S('GDEV 2202 or 2450', 1, 'GDEV 2202', 'GDEV 2450'), S('GDEV 4961', 1, 'GDEV 4961'),
    S('Additional methods course', 1, 'GDEV 3140', 'GDEV 3300', 'GDEV 3680', 'GDEV 3740', 'GDEV 4045', 'GDEV 4080', 'GDEV 4190', 'GDEV 4295')],
    'Eight core courses (21 credits). Any GDEV X55X course also counts as the methods course. C or better, letter grade.'),
  R('Engaged learning', [S('GDEV 2105 (pre-internship)', 1, 'GDEV 2105'), S('GDEV 3105 (post-internship)', 1, 'GDEV 3105')],
    'Pre- and post-internship courses around an 8-week field-based experience and a pre-departure portfolio.'),
  CHECK('8-week field experience', 'A domestic or international field-based internship of at least eight weeks.'),
  OPT('Focused electives', {
    'Social & Economic Development': ('GDEV 2450 and 3010, plus five electives (15+ credits; 3 with a GDEV prefix, 3 at 3000+).',
      [S('GDEV 2450', 1, 'GDEV 2450'), S('GDEV 3010', 1, 'GDEV 3010'), S('Five electives', 5, *_SED)]),
    'Agriculture & Food Systems': ('GDEV 2300 or 3400, PLSCI 4730, plus five electives: two foundational, two social/economic/health, one from any list.',
      [S('GDEV 2300 or 3400', 1, 'GDEV 2300', 'GDEV 3400'), S('PLSCI 4730', 1, 'PLSCI 4730'), S('Foundational plant & ag sciences', 2, *_AFS_FOUND),
       S('Social, economic & health', 2, *_AFS_SOC), S('One more from any list', 1, *(_AFS_FOUND + _AFS_SPEC + _AFS_SOC))]),
    'Environment & Development': ('One social science and one biophysical science course, plus five electives (2 with a GDEV prefix, 3 at 3000+).',
      [S('Social science', 1, *_ED_SOC), S('Biophysical science', 1, *_ED_BIO), S('Five electives', 5, *(_ED_SOC + _ED_BIO + _ED_MORE))]),
  }, 'A course may only fulfill one major requirement.', w='The GDEV-prefix and 3000-level counts within electives are not checked.'),
]))

# ---------------- English (BA) ----------------
_src = 'https://catalog.cornell.edu/programs/english-ba/'
MAJORS.append(major('ENGL', 'English', _src, [
  R('Ten courses', SF('English courses', 10, subj=['ENGL'], lo=1000, hi=4999, minCr=3, not_=['ENGL 2800', 'ENGL 2880', 'ENGL 2860']),
    'Ten full-semester courses (30+ credits), C or better. At most two 1000-level; FWS, ENGL 2800, and ENGL 2880 do not count. Cross-listed courses count under any code.',
    w='Up to three related non-ENGL courses can count with advisor approval; petition them.'),
  R('Two 4000-level seminars', SF('ENGL 4000-level seminars', 2, subj=['ENGL'], lo=4000, hi=4999, minCr=3, not_=['ENGL 4930', 'ENGL 4940']),
    'At least two of the ten must be 4000-level Cornell ENGL seminars.', dbl=True),
  CHECK('Two courses before 1800', 'Literatures in English before 1800. Look for the designation in the course description.'),
  CHECK('Two courses after 1800', 'Literatures in English after 1800.'),
  CHECK('Global South', 'One course on African, African Diaspora, Asian Diaspora, South Asian, or Caribbean literature in English.'),
  CHECK('Literatures of the Americas', 'Two courses, at least one on American Indian/Indigenous, African American, Asian American, Pacific Islander, or Latina/o literature.'),
  CHECK('Concentration', 'Three courses related by topic, theme, period, genre, or approach; worked out with your advisor in your final year.'),
]))
MAJORS[-1]['reqs'][0]['w'] += ' A course can cover at most two categories.'

# ---------------- History (BA) ----------------
_src = 'https://catalog.cornell.edu/programs/history-ba/'
H = lambda s: ['HIST ' + n for n in s.split()]
_HAN = H('1591 1621 1622 1740 1920 2132 2133 2208 2315 2435 2548 2562 2575 2750 2931 2932 2981 2996 3021 3525 3705 3950 3960 4020 4075 4076 4127 4129 4168 4408 4772 4773 4931 4963')
_HEU = H('1510 1511 1631 1650 1660 2082 2083 2085 2086 2151 2154 2155 2158 2165 2259 2285 2325 2333 2441 2567 2615 2650 2656 2689 2690 2691 2701 2807 2811 2812 2815 2852 2853 2854 2860 2958 2970 3012 3081 3200 3255 3415 3616 3662 3709 3802 3835 3953 4084 4116 4172 4277 4629 4634 4655 4665 4672 4673 4761 4910 4950')
_HGS = H('1561 1590 1950 1960 1965 1970 1975 1976 2010 2253 2307 2417 2452 2461 2515 2541 2542 2543 2556 2627 2637 2672 2674 2688 2715 2727 3448 3519 3542 3653 4041 4091 4303 4338 4423 4542 4543 4666 4667')
_HNA = H('1540 1576 1585 1595 1620 1770 1800 1802 1820 1850 1985 1986 2023 2035 2043 2055 2091 2212 2220 2251 2297 2301 2353 2354 2369 2371 2381 2391 2392 2482 2526 2581 2640 2641 2655 2660 2665 2680 2765 2792 2920 2955 3181 3410 3430 3436 3480 3571 3590 3602 3740 3770 3801 3806 3884 4023 4030 4109 4203 4204 4243 4262 4265 4551 4590 4674 4735 4851')
_HPE = H('1510 1561 1621 1631 1650 1660 1690 1710 1740 1950 1970 1985 1986 2010 2055 2082 2083 2085 2091 2155 2208 2259 2325 2381 2391 2441 2562 2590 2615 2616 2631 2650 2656 2660 2665 2688 2689 2749 2807 2811 2812 2852 2853 2854 2860 2931 2970 3175 3200 3448 3616 3770 3802 3950 4041 4116 4204 4345 4665 4761 4910 4931 4950 4963')
_HTR = H('1600 1690 1710 1930 1951 2006 2031 2064 2195 2207 2213 2462 2590 2616 2631 2710 2749 2760 2881 2905 2969 3175 3345 3626 3825 3980 4131 4196 4231 4345 4422 4466 4474 4711')
_SEM4 = {'subj': ['HIST'], 'lo': 4003, 'hi': 4999}
MAJORS.append(major('HIST', 'History', _src, [
  R('Nine history courses', SF('History courses', 9, subj=['HIST'], lo=1000, hi=4999, minCr=3),
    'At least nine 3-4 credit history courses (30+ credits), C or better. Cross-listed courses count. FWS courses do not. A single course can meet several requirements below.',
    w='Up to 2-3 approved study abroad or transfer courses can count; petition them.'),
  R('History before 1800', S('Pre-1800 (HIST-HPE)', 3, *_HPE), 'Three courses on history before 1800.', dbl=True),
  PICK('World areas (four of five)', 4, [S('Asia (HIST-HAN)', 1, *_HAN), S('North America (HIST-HNA)', 1, *_HNA), S('Europe (HIST-HEU)', 1, *_HEU),
    S('Global South (HIST-HGS)', 1, *_HGS), S('Transregional/Comparative (HIST-HTR)', 1, *_HTR)], 'One course in each of four of the five world-area categories.'),
  R('Seminars', [{'n': '4000-level seminar', 'k': 1, 'f': {'any': [_SEM4, {'codes': ['HIST 4000']}]}},
    {'n': 'Second seminar (sophomore or 4000-level)', 'k': 1, 'f': {'any': [_SEM4, {'codes': ['HIST 4000']}, {'subj': ['HIST'], 'lo': 2006, 'hi': 2499}]}}],
    'Two HIST seminars, at least one at the 4000 level. Sophomore seminars are HIST 2006-2499.', dbl=True),
]))
MAJORS[-1]['reqs'][2]['dbl'] = 1

# ---------------- Mathematics (BA) ----------------
_src = 'https://catalog.cornell.edu/programs/mathematics-ba/'
M_ = lambda s: ['MATH ' + n for n in s.split()]
_M3 = {'subj': ['MATH'], 'lo': 3000, 'hi': 4979}
_MODEL = ['MATH 3610', 'CS 2110', 'PHYS 1116', 'PHYS 2208', 'PHYS 2213', 'PHYS 2217']
def _conc(d, math_k, other_n, other_codes, other_k):
    return (d, [SF('MATH 3000+ courses', math_k, **_M3), S(other_n, other_k, *other_codes)])
MAJORS.append(major('MATH', 'Mathematics', _src, [
  R('Prerequisites', [S('Linear algebra', 1, 'MATH 2210', 'MATH 2230', 'MATH 2940', 'MATH 2310'), S('Multivariable calculus', 1, 'MATH 2220', 'MATH 2240', 'MATH 1920'),
    S('Programming', 1, 'CS 1110', 'CS 1112', 'CS 2110', 'CS 2112')], 'B- or better in linear algebra and multivariable calculus (B+ for MATH 2310); C- in programming.'),
  R('Algebra (two courses)', S('Algebra', 2, *M_('3320 3340 3360 4310 4330 4340 4370 4500'))),
  R('Analysis (two courses)', S('Analysis', 2, *M_('3110 3210 3270 4130 4140 4180 4200 4210 4220 4250 4260 4280'))),
  OPT('Concentration (five courses)', {
    'Mathematics': ('Four more MATH 3000+ courses, one in geometry/topology, plus one course dealing with mathematical models.',
      [S('Geometry/topology', 1, *M_('3210 4500 4520 4530 4540')), SF('More MATH 3000+', 3, **_M3), S('Mathematical models', 1, *_MODEL)]),
    'Applied Mathematics': ('Three MATH 3000+ courses and one modeling course (plus one more of either). Across the major, one course from three of the four groups: differential equations, discrete math, numerical methods, probability/statistics.',
      [SF('MATH 3000+', 3, **_M3), S('Mathematical models', 1, *(_MODEL + ['CS 4820', 'ECON 4020', 'ORIE 3300', 'ORIE 4350', 'CS 4620', 'CS 4670', 'MAE 4700', 'ECON 3130', 'ECON 4130', 'ORIE 3500', 'STSCI 3080', 'STSCI 3100', 'STSCI 4030'])),
       SF('One more MATH 3000+ or model course', 1, any=[_M3, {'codes': _MODEL}])]),
    'Computer Science': _conc('One MATH 3000+ and three CS courses with significant math (plus one more of either).', 1, 'CS with math content',
      ['CS 3220', 'CS 3700', 'CS 3780', 'CS 4110', 'CS 4160', 'CS 4210', 'CS 4220', 'CS 4620', 'CS 4670', 'CS 4740', 'CS 4744', 'CS 4756', 'CS 4775', 'CS 4783', 'CS 4787', 'CS 4789',
       'CS 4810', 'CS 4814', 'CS 4820', 'CS 4830', 'CS 4850', 'CS 4852', 'CS 4860'], 3),
    'Economics': _conc('One MATH 3000+, three economics courses with math content, and one more from math, economics, or OR.', 1, 'Economics with math content',
      ['ECON 3130', 'ECON 6190', 'ECON 3140', 'ECON 6200', 'ECON 3825', 'ECON 4020', 'ECON 4130', 'ECON 4140', 'ECON 4907', 'ECON 6090', 'ECON 6100', 'ECON 6130', 'ECON 6140'], 3),
    'Mathematical Biology': _conc('Three biology courses with math content and two MATH 3000+ courses.', 2, 'Biology with math content',
      ['BIOCB 3620', 'BIOCB 4381', 'BIOCB 4810', 'BIOCB 4830', 'BIOCB 4840', 'BIOCB 4910', 'BIOEE 3550', 'BIONB 4220', 'BME 3110', 'BME 3300', 'BTRY 3080', 'BTRY 4090', 'NTRES 4120'], 3),
    'Mathematical Physics': _conc('One MATH 3000+ and three physics courses using advanced math (plus one more of either).', 1, 'Physics with advanced math',
      ['PHYS 3316', 'PHYS 3317', 'PHYS 3318', 'PHYS 3327', 'PHYS 4230', 'PHYS 4443', 'PHYS 4444', 'PHYS 4445', 'PHYS 4454', 'PHYS 4481', 'PHYS 4488', 'AEP 4340', 'AEP 4400'], 3),
    'Operations Research': _conc('One MATH 3000+ and three OR courses focused on mathematical techniques (plus one more of either).', 1, 'Operations research',
      ['ORIE 3300', 'ORIE 3310', 'ORIE 3500', 'ORIE 3510', 'ORIE 3741', 'ORIE 4330', 'ORIE 4350', 'ORIE 4580', 'ORIE 4600', 'ORIE 4630', 'ORIE 4740', 'ORIE 4742', 'ORIE 5600', 'ORIE 5610', 'ORIE 5640'], 3),
    'Statistics': ('MATH 4710 and 4720, one more MATH 3000+, and two statistics courses from other departments.',
      [S('MATH 4710', 1, 'MATH 4710'), S('MATH 4720', 1, 'MATH 4720'), SF('One more MATH 3000+', 1, **_M3),
       S('Statistics in other departments', 2, 'BIOCB 4381', 'BIOCB 4830', 'CS 3700', 'CS 3780', 'CS 4740', 'CS 4789', 'ECON 3140', 'ORIE 3741', 'ORIE 4740', 'STSCI 3100', 'STSCI 3510',
         'STSCI 3740', 'STSCI 3900', 'STSCI 4030', 'STSCI 4060', 'STSCI 4100', 'STSCI 4110', 'STSCI 4140', 'STSCI 4270', 'STSCI 4520', 'STSCI 4550', 'STSCI 4780')]),
  }, 'Nine courses in all (items 1-3). No course counts twice.'),
  R('At least 5 MATH courses at 3000+', SF('MATH 3000+ on transcript', 5, **_M3), 'At least five MATH-prefix courses at 3000+, two of them at 4000+. MATH 4900, 4980, 4997 and 5000-level courses do not count.', dbl=True),
]))
MAJORS[-1]['reqs'][-1]['slots'][0]['f']['not'] = ['MATH 4900', 'MATH 4980', 'MATH 4997']

# ---------------- Statistical Science (BA) / Biometry and Statistics (BS) ----------------
_src = 'https://stat.cornell.edu/node/2432'
_STX = ['STSCI 4970', 'STSCI 4980', 'STSCI 4990', 'BTRY 4980', 'BTRY 4990']
_STEL = ['STSCI 3740', 'STSCI 3900', 'STSCI 3090', 'BTRY 3090', 'STSCI 3100', 'BTRY 3100', 'ILRST 3100', 'BIOCB 4381', 'BIOCB 4830', 'BIOCB 4840', 'BIOCB 4910',
         'MATH 4260', 'MATH 4740', 'ECON 4110', 'ECON 4130', 'NTRES 6700', 'INFO 3300', 'INFO 4310', 'ORIE 3120', 'ORIE 3300', 'ORIE 3310', 'ORIE 3510', 'STSCI 3510',
         'ORIE 4580', 'ORIE 4741', 'ORIE 3741', 'ORIE 4742', 'CS 3220', 'CS 4220', 'CS 3780', 'CS 4320', 'CS 4740', 'CS 4786', 'CS 4787', 'CS 4789']
MAJORS.append(major('STSCI', 'Statistical Science / Biometry and Statistics', _src, [
  R('Math and computing', [S('Calculus I', 1, 'MATH 1110'), S('Calculus II', 1, 'MATH 1120', 'MATH 1220', 'MATH 1910'), S('Multivariable calculus', 1, 'MATH 1920', 'MATH 2220', 'MATH 2230', 'MATH 2130', 'CS 2110'),
    S('Linear algebra', 1, 'MATH 2310', 'MATH 2940', 'MATH 2210', 'MATH 2240'), S('Intro computing', 1, 'CS 1110', 'CS 1112')],
    'The Data Science Track swaps multivariable calculus for CS 2110.'),
  R('Statistics core', [S('Statistical Methods I', 1, 'BTRY 3010', 'STSCI 2200', 'AEM 2100', 'BTRY 6010', 'ENGRD 2700', 'HADM 2010', 'STSCI 2100', 'ILRST 2100', 'MATH 1710',
      'PUBPOL 2100', 'PUBPOL 2101', 'PSYCH 2500', 'SOC 3010', 'STSCI 2150'),
    S('Statistical Methods II', 1, 'BTRY 3020', 'STSCI 3200'), S('Probability', 1, 'BTRY 3080', 'STSCI 3080', 'MATH 4710', 'ECON 3130', 'ORIE 3500'),
    S('Linear Models', 1, 'BTRY 4030', 'STSCI 4030', 'ECON 3140'), S('Theory of Statistics', 1, 'BTRY 4090', 'STSCI 4090', 'MATH 4720'), S('Statistical Computing', 1, 'STSCI 4520')],
    'C- or better, letter grades. AP Statistics (4 or 5) can waive Statistical Methods I for A&S students.'),
  R('Electives with statistical content', [SF('STSCI/BTRY electives', 3, any=[{'subj': ['STSCI', 'BTRY'], 'lo': 4000, 'hi': 9999, 'not': _STX}, {'codes': [c for c in _STEL if c.split()[0] in ('STSCI', 'BTRY', 'ILRST')]}], minCr=3),
    SF('Other electives', 2, any=[{'subj': ['STSCI', 'BTRY'], 'lo': 4000, 'hi': 9999, 'not': _STX}, {'codes': _STEL}], minCr=3)],
    'Five 3+ credit electives, at least three STSCI/BTRY (or cross-listed). Rules for May 2028 graduates and later.',
    w='Students graduating by December 2027 follow the older two-methods-plus-three-external-electives rule.'),
]))

# ---------------- Biological Sciences (BA/BS) ----------------
_src = 'https://catalog.cornell.edu/programs/biological-sciences-ba/'
B_ = lambda *c: list(c)
_ANIMAL_LEC = ['ANSC 2400', 'ANSC 3410', 'ANSC 4270', 'BIOAP 2140', 'BIOAP 4140', 'BIOMG 3850', 'BIOMG 4000', 'BIOMG 4390', 'BIOMS 4150', 'BIONB 3220', 'BIONB 3920', 'NS 3310']
_ANIMAL_LAB = ['BIOAP 4130', 'BIOAP 3190', 'BIOMG 4400', 'BIONB 4300']
_GGD = ['BIOMG 3800', 'BIOMG 4880', 'BIOMG 6870', 'BIOMI 4850', 'BIONB 3950', 'PLSCI 3430', 'BIOMG 4000', 'BIOMG 4870', 'BIOCB 4830', 'BIOMG 3850', 'BIOMG 4610',
        'PLSCI 4220', 'BIOEE 4530', 'BIOMG 4810', 'NTRES 3400', 'BIOMG 4380', 'BIOMG 4390', 'BIOMG 6330', 'BIOMG 6390', 'BIOMG 4400', 'BIOG 4990']
_MICRO = ['BIOMI 2600', 'BIOMI 2950', 'BIOMI 3210', 'BIOMI 3500', 'BIOMI 4040', 'BIOMI 4090', 'BIOMI 4200', 'BIOMI 4300', 'BIOMI 4310', 'BIOMI 4850', 'BIOMI 6200',
          'BIOMI 6300', 'BIOMS 4340', 'CEE 4510', 'FDSC 3940', 'FDSC 3950', 'FDSC 4260', 'NS 4200', 'PLSCI 4300', 'PLSCI 5700', 'VIEN 4650']
_NUTR = ['NS 3060', 'NS 3150', 'NS 3320', 'NS 3410', 'NS 3420', 'NS 3450', 'NS 4140', 'NS 4200', 'NS 4210', 'NS 4300', 'NS 4330', 'NS 4410', 'NS 4430', 'NS 5510', 'NS 6310', 'NS 6320']
MAJORS.append(major('BIO', 'Biological Sciences', _src, [
  R('Introductory biology cluster', [S('Two of cell, physiology, ecology', 2, 'BIOMG 1350', 'BIOG 1440', 'BIOG 1445', 'BIOEE 1610', 'BIOSM 1610'),
    S('Investigative lab', 1, 'BIOG 1500', 'BIOSM 1500'), S('Evolution and diversity', 1, 'BIOEE 1780', 'BIOEE 1781', 'BIOSM 1780')],
    'AP Biology does not place out of any cluster course.'),
  R('Chemistry', [S('General chemistry', 1, 'CHEM 2070', 'CHEM 2150'), S('General chemistry II (or CHEM 2150)', 1, 'CHEM 2080', 'CHEM 2150'),
    S('Organic chemistry', 1, 'CHEM 1570', 'CHEM 3570', 'CHEM 3590')],
    'CHEM 2070/2080 with labs, or CHEM 2150. Organic: CHEM 1570, 3570 with 3580 or 2510, or 3590-3600.', w='Two-course organic options count once the first course is planned.'),
  R('Mathematics', [S('Calculus I', 1, 'MATH 1106', 'MATH 1110'), S('Statistics, Calc II, or finite math', 1, 'AEM 2100', 'BTRY 3010', 'ECON 3130', 'MATH 1710', 'PSYCH 2500',
      'SOC 3010', 'STSCI 2150', 'MATH 1120', 'MATH 1910', 'MATH 1105')], 'Statistics is strongly encouraged for the second course. Cornell STSCI 2100 does not count.'),
  R('Physics', S('Two-semester physics', 2, 'PHYS 1101', 'PHYS 1102', 'PHYS 2207', 'PHYS 2208', 'PHYS 1112', 'PHYS 2213'), 'PHYS 1101-1102, 2207-2208, or 1112 (+1110) and 2213; mixing parts is allowed.'),
  R('Genetics and genomics', [S('BIOMG 2800', 1, 'BIOMG 2800'), S('BIOMG 2801', 1, 'BIOMG 2801')]),
  R('Biochemistry', S('Biochemistry', 1, 'BIOMG 3300', 'BIOMG 3310', 'BIOMG 3350'), 'BIOMG 3300, 3310 + 3320, or 3350 (3350 not for Biochemistry or MCB concentrators).'),
  OPT('Concentration', {
    'Animal Physiology': ('BIOAP 3110 and 3160, plus 7 credits (4 of them lab).', [S('BIOAP 3110', 1, 'BIOAP 3110'), S('BIOAP 3160', 1, 'BIOAP 3160'),
      S('Physiology lab', 1, *_ANIMAL_LAB), C('More physiology (lecture or lab)', 3, codes=_ANIMAL_LEC + _ANIMAL_LAB)]),
    'Biochemistry': ('Organic lab, physical chemistry + cell biology, biochemistry lab, and one more biochemical course.', [S('Organic lab', 1, 'CHEM 2510', 'CHEM 3010'),
      S('PChem', 1, 'CHEM 3870', 'CHEM 3890'), S('Cell biology or PChem II', 1, 'BIOMG 4320', 'CHEM 3900'), S('BIOMG 4400', 1, 'BIOMG 4400'),
      S('Additional course', 1, 'BIOMG 4380', 'BIOMG 6310', 'CHEM 3880', 'CHEM 4500', 'BIOG 4990')]),
    'Biodiversity and Systematics': ('13 credits: at least 7 from Group A and 3 from Group B; two courses with labs.', [
      C('Group A', 7, codes=['BIOEE 2740', 'BIOEE 4700', 'BIOEE 4750', 'BIOEE 4752', 'BIOEE 4760', 'BIOMI 2900', 'BIOMI 2911', 'BIOMI 3310', 'PLSCI 2300', 'PLSCI 2410', 'PLSCI 2470',
        'PLSCI 2480', 'ENTOM 2120', 'ENTOM 2150', 'ENTOM 3150', 'ENTOM 3310', 'ENTOM 3311', 'PLSCI 4300', 'PLSCI 3190']),
      C('Group B', 3, codes=['BIOEE 4530', 'BIOEE 4790', 'EAS 4795', 'EAS 2250', 'EAS 2680', 'EAS 3010', 'ENTOM 4610', 'PLSCI 4400'])]),
    'Computational Biology': ('Programming, a math course, a bridging course, and an advanced course.', [S('Programming', 1, 'CS 1110', 'CS 1112', 'CS 2024'),
      S('Mathematics', 1, 'BTRY 3080', 'MATH 2210', 'MATH 2310', 'MATH 2940', 'MATH 4200', 'MATH 4210', 'MATH 4710', 'MATH 4740'),
      S('Bridging course', 1, 'BIOCB 3620', 'BIOCB 4381', 'BIOCB 4810', 'BIOCB 4830', 'BIOCB 4840', 'BIOCB 4910', 'BIOEE 3550', 'BIOMG 4311', 'BIOMG 4810', 'BIOMG 4870', 'BIONB 3300',
        'BIONB 4220', 'BIONB 4740', 'BME 3110', 'ENTOM 4610', 'NTRES 3100', 'NTRES 4100', 'NTRES 4120', 'PLSCI 4000', 'PLSCI 4400', 'STSCI 3740'),
      S('Advanced course', 1, 'BIOCB 3620', 'BIOCB 4381', 'BIOMI 4300', 'BTRY 3080', 'BTRY 4090', 'CS 2110', 'CS 4210', 'CS 4220', 'CS 3780', 'MATH 4200', 'MATH 4210', 'MATH 4710', 'MATH 4740', 'ORIE 3500', 'ORIE 3510')]),
    'Ecology and Evolutionary Biology': ('Core courses in ecology, evolution, and biodiversity, one field/lab course, 13 credits total. BIOEE 1610 must be one of your cluster courses.', [
      S('Ecology core', 1, 'BIOEE 3610', 'BIOEE 4460', 'BIOEE 4550', 'BIOEE 4560', 'BIOEE 4570', 'BIOEE 4660', 'BIOEE 4780', 'NTRES 3100'),
      S('Evolution core', 1, 'BIOEE 4530', 'BIOEE 4800', 'BIOMG 4610', 'ENTOM 4610'),
      S('Biodiversity core', 1, 'BIOEE 2740', 'BIOEE 3730', 'BIOEE 4700', 'BIOEE 4750', 'BIOEE 4752', 'BIOEE 4760', 'BIOEE 4762', 'ENTOM 3310', 'PLSCI 2480', 'PLSCI 4300'),
      S('Field or lab', 1, 'BIOEE 1560', 'BIOEE 2150', 'BIOEE 2526', 'BIOEE 2740', 'BIOEE 3610', 'BIOEE 3611', 'BIOEE 3780', 'BIOEE 4461', 'BIOEE 4571', 'BIOEE 4661', 'BIOEE 4701',
        'BIOEE 4751', 'BIOEE 4761', 'ENTOM 3310', 'ENTOM 3311', 'NTRES 3400', 'PLSCI 2301', 'PLSCI 2410', 'PLSCI 3190')]),
    'Genetics, Genomics and Development': ('13 credits from the GGD list.', [C('GGD courses', 13, codes=_GGD)]),
    'Human Nutrition': ('NS 3310 plus 9 credits of biological aspects of nutrition.', [S('NS 3310', 1, 'NS 3310'), C('Nutrition courses', 9, codes=_NUTR)]),
    'Marine Biology': ('One introductory course and 12 credits from Groups A and B (one from each), plus a field component.', [
      S('Introductory', 1, 'BIOEE 1540', 'BIOEE 1560', 'BIOEE 1610', 'BIOSM 1500', 'BIOSM 1610'),
      S('Group A', 1, 'BIOAP 3300', 'BIOEE 2740', 'BIOEE 3730', 'BIOEE 4760', 'BIOMI 3500', 'BIOSM 1780', 'BIOSM 3210', 'BIOSM 3330', 'BIOSM 3450', 'BIOSM 4650', 'EAS 3555'),
      S('Group B', 1, 'BIOEE 4570', 'BIOEE 4571', 'BIOEE 4790', 'BIOSM 2800', 'BIOSM 3750', 'NTRES 3110', 'NTRES 3111')]),
    'Microbiology': ('BIOMI 2900 and 2911 plus 7 credits from the list.', [S('BIOMI 2900', 1, 'BIOMI 2900'), S('BIOMI 2911', 1, 'BIOMI 2911'), C('Microbiology electives', 7, codes=_MICRO)]),
    'Molecular and Cell Biology': ('BIOMG 4320, a molecular lab, and 6 more credits.', [S('BIOMG 4320', 1, 'BIOMG 4320'), S('Molecular lab', 1, 'BIOMG 4400', 'BIONB 4300'),
      C('Additional credits', 6, any=[{'subj': ['BIOMG'], 'lo': 3000, 'hi': 6999, 'not': ['BIOMG 4980', 'BIOMG 4981', 'BIOMG 4982']},
        {'codes': ['BIOG 4990', 'BIOMS 4150', 'BIOMS 4250', 'BIOMI 4090', 'BIOMI 4850', 'BIONB 3950', 'PLSCI 3420', 'PLSCI 3430', 'PLSCI 4220', 'PLSCI 4540', 'PLSCI 4620']}])]),
    'Neurobiology and Behavior': ('BIONB 2210 and 2220, one 3000+ BIONB course, and more NBB courses (15 credits).', [S('BIONB 2210', 1, 'BIONB 2210'), S('BIONB 2220', 1, 'BIONB 2220'),
      SF('BIONB 3000+', 1, subj=['BIONB'], lo=3000, hi=4999, minCr=3), C('More NBB credits', 4, subj=['BIONB'], lo=3000, hi=4999)]),
    'Plant Biology': ('Plant evolutionary biology or plant biotechnology option; see the catalog.', [SF('Plant biology courses', 4, subj=['PLSCI'], lo=2000, hi=6999, minCr=2)]),
    'General Biology': ('Three courses from three different concentrations, a lab/field course, and two 3000+ courses (13 credits).', [
      SF('Upper-level biology', 2, subj=['BIOMG', 'BIOEE', 'BIONB', 'BIOMI', 'BIOAP', 'BIOCB', 'BIOMS', 'BIOSM', 'PLSCI', 'ENTOM', 'NS'], lo=3000, hi=6999, minCr=2),
      SF('More concentration courses', 1, subj=['BIOMG', 'BIOEE', 'BIONB', 'BIOMI', 'BIOAP', 'BIOCB', 'BIOMS', 'BIOSM', 'PLSCI', 'ENTOM', 'NS'], lo=2000, hi=6999, minCr=2)],
      ),
  }, 'One concentration (12-17 credits). Core courses cannot count toward it.', w='The Plant Biology option lists are approximated as 2000+ PLSCI courses; check the catalog.'),
]))

# ---------------- Cognitive Science (BA) ----------------
_src = 'https://catalog.cornell.edu/programs/cognitive-science-ba/'
Cg = lambda s: ['COGST ' + n for n in s.split()]
MAJORS.append(major('COGST', 'Cognitive Science', _src, [
  R('Introductory core', S('Intro course', 1, 'COGST 1101', 'COGST 2350', 'COGST 2200'), 'COGST 1101 or 2350 (2200 also counts for admission).'),
  R('Statistical reasoning', S('Statistics', 1, 'BTRY 3010', 'PSYCH 2500', 'SOC 3010', 'STSCI 2150', 'STSCI 2200')),
  R('Structured thinking / data science', S('Structured thinking', 1, 'CS 1380', 'COGST 2310', 'INFO 2950')),
  PICK('Interdisciplinary distribution (three of five)', 3, [
    S('Language Science', 1, *Cg('2150 2264 3330 4240 4270 4280 4425 4740')), S('Evolution and Development', 1, *Cg('2090 2300 4260 4270')),
    S('Computational Cognitive Science', 1, *Cg('3140 3300 3801 4240 4280 4740')), S('Cognitive Neuroscience', 1, *Cg('2230 2264 3250 3300 4230')),
    S('Mind and Culture', 1, *Cg('1112 2621 3160 3420 4050 4150 4310 4625'))],
    'One course in each of three concentrations. These are sample lists; other approved courses count with advisor approval.', w='Only the published sample courses are recognized; petition others your advisor approves.'),
  R('12 courses', SF('Cognitive science courses', 12, subj=['COGST'], lo=1000, hi=6999),
    'At least 12 courses, letter-graded, C- or better. Cross-listed courses count under any code. At most half may also count toward another major or minor.', dbl=True),
  R('40 credits', C('Credits', 40, subj=['COGST'], lo=1000, hi=6999), 'At least 40 credits in the major.', dbl=True),
]))

# ---------------- Chemistry (BA) ----------------
_src = 'https://catalog.cornell.edu/programs/chemistry-ba/'
_CHEM_RES = ['CHEM 4210', 'CHEM 4330', 'CHEM 4430', 'CHEM 4610', 'CHEM 4770']
MAJORS.append(major('CHEM', 'Chemistry', _src, [
  R('General chemistry', S('CHEM 2070/2080 or 2150', 1, 'CHEM 2080', 'CHEM 2150'), 'CHEM 2070 + 2071 and 2080 + 2081, or CHEM 2150.', w='The two-course sequence counts once CHEM 2080 is planned.'),
  R('Organic chemistry', [S('Organic I', 1, 'CHEM 3570', 'CHEM 3590'), S('Organic II', 1, 'CHEM 3580', 'CHEM 3600')], 'CHEM 3570-3580 or 3590-3600.'),
  R('Physical chemistry', [S('PChem I', 1, 'CHEM 3870', 'CHEM 3890'), S('PChem II', 1, 'CHEM 3880', 'CHEM 3900')],
    'CHEM 3870-3880 or 3890-3900 (3890-3900 needs multivariable calculus). Classes of 2025-2027 may use CHEM 3870 alone.'),
  R('Inorganic chemistry', S('CHEM 4100', 1, 'CHEM 4100')),
  R('Core labs', [S('CHEM 2510', 1, 'CHEM 2510', 'CHEM 3010'), S('CHEM 2900 or 3030', 1, 'CHEM 2900', 'CHEM 3030')]),
  R('Math', [S('Calculus I', 1, 'MATH 1110'), S('Calculus II', 1, 'MATH 1120', 'MATH 1910')], 'AP credit can substitute.'),
  R('Physics', S('Calculus-based physics', 2, 'PHYS 2207', 'PHYS 2208', 'PHYS 1112', 'PHYS 2213', 'PHYS 1116', 'PHYS 2217'), 'PHYS 2207-2208, 1112 (+1110) and 2213, or 1116-2217. PHYS 1101-1102 do not count.'),
  R('8 lab credits', C('Laboratory credits', 8, codes=['CHEM 2510', 'CHEM 2900', 'CHEM 3010', 'CHEM 3020', 'CHEM 3030']),
    'Eight lab credits beyond general chemistry, including the core labs. Approved outside lab electives also count. Research courses do not.', dbl=True,
    w='Approved lab electives outside chemistry are listed on the department site; petition them.'),
  R('60 credits in chemistry and related subjects', C('Chemistry and related', 60, any=[{'subj': ['CHEM']}, {'codes': ['MATH 1110', 'MATH 1120', 'MATH 1910', 'MATH 1920', 'MATH 2210', 'MATH 2220',
      'PHYS 2207', 'PHYS 2208', 'PHYS 1112', 'PHYS 1110', 'PHYS 2213', 'PHYS 1116', 'PHYS 2217']}]),
    'Sixty total credits (57 for the classes of 2026-2027): the core plus electives from any CHEM course at 4000+ and the department approved list. At most 4 research credits.', dbl=True,
    w='Approved electives from other departments are on the department site; petition them.'),
]))

# ---------------- Health Care Policy (BS, Brooks) ----------------
_src = 'https://catalog.cornell.edu/programs/health-care-policy-major-bs/'
_HCPEL = ['AMST 3261', 'ECON 3711', 'ECON 3720', 'ECON 3910', 'FGSS 3260', 'GDEV 3280', 'GOVT 3251', 'NS 4570', 'PUBPOL 2050', 'PUBPOL 3011', 'PUBPOL 3110', 'PUBPOL 3180',
          'PUBPOL 3230', 'PUBPOL 3251', 'PUBPOL 3260', 'PUBPOL 3280', 'PUBPOL 3320', 'PUBPOL 3490', 'PUBPOL 3650', 'PUBPOL 3720', 'PUBPOL 3780', 'PUBPOL 3870', 'PUBPOL 4110',
          'PUBPOL 4281', 'PUBPOL 4370', 'SOC 3180', 'SOC 3230']
_PREMED = ['BIOG 1440', 'BIOG 1445', 'BIOG 1500', 'BIOMG 1350', 'BIOMG 3300', 'BIOMG 3310', 'BIOMG 3320', 'BIOMG 3350', 'BIOMI 2900', 'CHEM 2070', 'CHEM 2071', 'CHEM 2080',
           'CHEM 2081', 'CHEM 3530', 'CHEM 3570', 'CHEM 3580', 'NS 3200', 'PHYS 2207', 'PHYS 2208']
_PPEL = {'subj': ['PUBPOL'], 'lo': 2000, 'hi': 4999, 'not': ['PUBPOL 4030', 'PUBPOL 4980', 'PUBPOL 4990']}
MAJORS.append(major('HCP', 'Health Care Policy', _src, [
  R('Public Policy core', [S('PUBPOL 1111', 1, 'PUBPOL 1111'), S('PUBPOL 2000 or ECON 3030', 1, 'PUBPOL 2000', 'ECON 3030'), S('PUBPOL 2101', 1, 'PUBPOL 2101'),
    S('PUBPOL 2301', 1, 'PUBPOL 2301'), S('PUBPOL 2350', 1, 'PUBPOL 2350'), S('PUBPOL 2370', 1, 'PUBPOL 2370'), S('Ethics (PUBPOL 2830/3830)', 1, 'PUBPOL 2830', 'PUBPOL 3830'),
    S('PUBPOL 3100', 1, 'PUBPOL 3100')], 'C- or better. Core PUBPOL courses cannot be taken abroad.'),
  R('Demography', S('Demography', 1, 'PUBPOL 2030', 'PUBPOL 3280')),
  R('Introductory Microeconomics', S('ECON 1110', 1, 'ECON 1110'), 'Or AP Micro 5 / IB HL Econ 7.'),
  R('Introduction to Sociology', S('Intro sociology', 1, 'PUBPOL 2250', 'SOC 1101')),
  R('Engaged learning (CU-CEL)', SF('CEL course', 1, subj=['PUBPOL'], attr=['CU-CEL']), 'At least 3 credits of PUBPOL coursework with the CU-CEL attribute. May overlap with other requirements.', dbl=True),
  R('Health care and health policy electives', C('HCP-EL credits', 12, codes=_HCPEL), 'At least 12 credits with the HCP-EL attribute.'),
  R('Public policy electives', C('PUBPOL 2000-4000', 9, **_PPEL), 'At least 9 credits of 2000-4000 level PUBPOL.'),
  R('Additional health and policy electives', C('Any elective category', 14, any=[{'codes': _HCPEL + _PREMED}, _PPEL]),
    'The remaining 14 of 35 elective credits, from health policy, public policy, or pre-med lists.', w='Only 3 credits of PUBPOL 4000-4020 and 8 credits taken abroad can count; not checked.'),
], schools=['PP']))

# Brooks college requirements for students entering Fall 2026 or later
_SRC26 = 'https://catalog.cornell.edu/programs/health-care-policy-major-bs/#collegetext'
BROOKS26 = {'id': 'col:PP26', 'kind': 'college', 'name': 'Brooks School of Public Policy [entering Fall 2026 and later]', 'origin': 'new', 'src': _SRC26, 'verified': '2026-27', 'reqs': [
  R('First-Year Writing Seminars', {'n': 'FWS', 'k': 2, 'f': {'codes': []}, 'fws': 1}, 'Two FWS courses in your first two semesters. AP English 5 or IB HL English 7 covers one.', src=_SRC26),
  R('Mathematics', SF('Math course', 1, subj=['MATH'], minCr=3, not_=['MATH 1101', 'MATH 1710']), 'Any 3-credit MATH course except MATH 1101 and 1710. AP Calc BC 4-5 counts; AB does not.', src=_SRC26),
  R('Natural Science', SF('Science course', 1, distr=['BIO', 'PBS', 'PHS', 'BSC-AG', 'CHPH-AG', 'OPHLS-AG', 'PSC-AG'], minCr=3),
    'Three credits with a BIO, PBS, or PHS code (or the CALS equivalents). AP Bio 4-5, AP Chem 5, or AP Physics 5 also count.', src=_SRC26),
  R('Historical Analysis', SF('HA / HST course', 1, distr=['HA', 'HST'], minCr=3), src=_SRC26),
  R('Human Ecology Electives', C('Human Ecology credits', 9, any=[{'subj': ['DEA', 'FSAD', 'HD', 'HE', 'NS'], 'not': ['HE 1110', 'HE 1112', 'HE 1115', 'HE 1200'], 'notNum': ['4030']},
    {'codes': ['PSYCH 1101']}]), 'Nine credits in DEA, FSAD, HD, HE, or NS (PSYCH 1101 and AP Psych 4-5 also count). May overlap with other requirements.', dbl=True, src=_SRC26),
  {'n': '120 credits total', 't': 'total', 'k': 120, 'src': _SRC26, 'd': 'Up to 12 S/U credits and 12 special-studies credits count.'},
]}

# ---------------- Communication (BS, CALS) ----------------
_src = 'https://catalog.cornell.edu/programs/communication-bs/'
_COMMCORE = ['Media Communication', 'Communication and Technology', 'Persuasion and Social Influence', 'Communication, Environment, Science, and Health']
MAJORS.append(major('COMM', 'Communication', _src, [
  R('Foundations', [S('COMM 1111', 1, 'COMM 1111'), S('COMM 1101', 1, 'COMM 1101'), S('COMM 1300', 1, 'COMM 1300'), S('COMM 2010', 1, 'COMM 2010'), S('COMM 2310', 1, 'COMM 2310')],
    'COMM 1111 is not required for transfer students.'),
  R('Data literacy', [S('COMM 2820', 1, 'COMM 2820'), SF('Statistics', 1, titles=['Introductory Statistics', 'Introductory Statistics and Data Science'])], 'AP Statistics 5 or transfer credit also counts.'),
  R('Communication core', SF('Core courses', 3, subj=['COMM'], titles=_COMMCORE), 'Three of: Media Communication, Communication and Technology, Persuasion and Social Influence, and Communication, Environment, Science, and Health.'),
  R('Upper-level electives', SF('COMM 3100+', 4, any=[{'subj': ['COMM'], 'lo': 3100, 'hi': 4999, 'not': ['COMM 4980', 'COMM 4960']}, {'subj': ['COMM'], 'titles': _COMMCORE}]),
    'Four COMM courses at 3100+. A fourth core class can be one of them. COMM 4960 and 4980 do not count.'),
  R('Communication practica', SF('COMM 3000-3099', 1, subj=['COMM'], lo=3000, hi=3099)),
], schools=['AG']))

# ---------------- Philosophy (BA) ----------------
_src = 'https://catalog.cornell.edu/programs/philosophy-ba/'
_PHX = {'subj': ['PHIL'], 'lo': 1000, 'hi': 7999, 'not': ['PHIL 1110', 'PHIL 1111', 'PHIL 1112'], 'notNum': ['X9XX']}
MAJORS.append(major('PHIL', 'Philosophy', _src, [
  R('Ancient philosophy', S('Greek and Roman Philosophy', 1, 'PHIL 2200'), 'PHIL 2200, or another course with a large Plato or Aristotle component (petition it).'),
  R('Modern philosophy before 1900', S('Modern Philosophy', 1, 'PHIL 2220'), 'PHIL 2220, or another course mainly on modern philosophy before 1900 (petition it).'),
  R('Eight philosophy courses', [SF('PHIL courses', 8, minCr=3, **_PHX)], 'At least 8 PHIL courses (24+ credits), letter-graded. FWS and X9XX courses do not count.', dbl=True),
  R('Level requirements', [SF('PHIL 2000+', 6, **{**_PHX, 'lo': 2000}), SF('PHIL above 3000', 3, **{**_PHX, 'lo': 3000})],
    'At least six PHIL courses at 2000+ and three above 3000.', dbl=True),
  R('Two more philosophy or related courses', C('Philosophy or related credits', 6, **_PHX), 'Six more credits (usually two courses) in philosophy, or philosophy-adjacent courses your advisor approves. Ten courses and 30 credits in all.',
    w='Philosophy-adjacent courses from other departments need advisor approval; petition them.'),
]))

# ---------------- Anthropology (BA) ----------------
_src = 'https://anthropology.cornell.edu/anthropology-major'
_AN = lambda lo, hi=4999: {'subj': ['ANTHR'], 'lo': lo, 'hi': hi, 'minCr': 3}
MAJORS.append(major('ANTHR', 'Anthropology', _src, [
  R('Subfield courses', [S('Sociocultural', 1, 'ANTHR 1400', 'ANTHR 2400', 'ANTHR 2468'),
    S('Archaeological', 1, 'ANTHR 1200', 'ANTHR 2201', 'ANTHR 2245', 'ANTHR 2430', 'ANTHR 2729'), S('Biological', 1, 'ANTHR 1300', 'ANTHR 2310', 'ANTHR 3235')],
    'One 3+ credit course in each subfield.'),
  R('Anthropological theory', S('ANTHR 3000', 1, 'ANTHR 3000')),
  R('3000-level courses', SF('ANTHR 3000-level', 2, **_AN(3000, 3999)), 'Two more 3000-level courses of 3+ credits.'),
  R('4000-level courses', SF('ANTHR 4000-level', 2, **{**_AN(4000), 'not': ['ANTHR 4263']}),
    'Two 4000-level courses; one must be a senior-year seminar with a research paper or project. ANTHR 4263 is not a seminar.', w='Which course is your senior seminar is not checked.'),
  R('Electives', SF('ANTHR electives', 2, **_AN(1000, 6999)), 'Two more 3+ credit courses; cognate courses count with advisor approval (petition them). Ten courses in all, C- or better, no S/U or FWS.'),
]))

# ---------------- American Studies (BA) ----------------
_src = 'https://catalog.cornell.edu/programs/american-studies-ba/'
MAJORS.append(major('AMST', 'American Studies', _src, [
  R('Twelve American Studies courses', SF('AMST roster courses', 12, subj=['AMST'], minCr=3),
    'Twelve 3-4 credit courses from the AMST roster (cross-listed courses count), C or better. No more than six from one discipline. Two non-cross-listed courses can count with DUS approval.', dbl=True),
  R('42 credits', C('AMST credits', 42, subj=['AMST']), dbl=True),
  R('4000-level seminar', SF('AMST 4000-level seminar', 1, subj=['AMST'], lo=4000, hi=4999, not_=['AMST 4998']), 'AMST 4998 (taught in Washington) does not count.'),
  CHECK('Three pre-1900 courses', 'Three courses with substantial focus on material before 1900.'),
  CHECK('Two American diversity courses', 'Two courses on social justice or inequality (race, class, gender, sexuality).'),
  CHECK('Concentration (six courses)', 'Six courses forming an area of concentration, set with your advisor in your penultimate semester. They can count toward the other requirements.'),
]))

# ---------------- Jewish Studies (BA) ----------------
_src = 'https://catalog.cornell.edu/programs/jewish-studies-ba/'
MAJORS.append(major('JWST', 'Jewish Studies', _src, [
  R('Required courses', [S('Introduction to Judaism', 1, 'JWST 2644'), S('Research in Jewish Studies', 1, 'JWST 4769', 'JWST 4998')],
    'JWST 2644, and JWST 4769 or the honors sequence JWST 4998-4999.'),
  R('Major electives', [SF('JWST 3000+', 4, subj=['JWST'], lo=3000, hi=6999, not_=['JWST 4769', 'JWST 4998', 'JWST 4999']),
    SF('More JWST electives', 3, subj=['JWST'], lo=1000, hi=6999, not_=['JWST 2644', 'JWST 4769', 'JWST 4998', 'JWST 4999'])],
    'Seven electives, at least four at 3000+. Some language courses count toward the major (the catalog limits how many; check with your advisor).',
    w='The related-course requirement and language-course limits are not checked.'),
]))

# ---------------- French (BA) ----------------
_src = 'https://romancestudies.cornell.edu/french-undergraduate'
MAJORS.append(major('FREN', 'French', _src, [
  R('Introduction to French and Francophone Literature and Culture', S('FREN 2310', 1, 'FREN 2310')),
  R('Upper-level courses', [SF('FREN 3000+', 3, subj=['FREN'], lo=3000, hi=6999, minCr=3), SF('FREN 4000+', 1, subj=['FREN'], lo=4000, hi=6999, minCr=3)],
    'Four courses at 3000+, at least one at 4000+ and at least two taught in French.'),
  R('Eight courses at FREN 2095 or above', SF('FREN courses', 8, subj=['FREN'], lo=2095, hi=6999, minCr=3),
    'Eight 3+ credit FREN (or cross-listed) courses at the 2095 level or above, five taught in French. B- or better, no S/U. Up to three courses from abroad.', dbl=True),
  CHECK('Francophone world beyond France', 'At least one course on the Francophone world outside France.'),
]))

# ---------------- Spanish (BA) ----------------
_src = 'https://romancestudies.cornell.edu/spanish-undergraduate'
MAJORS.append(major('SPAN', 'Spanish', _src, [
  R('Core courses', [S('Spain survey or perspectives', 1, 'SPAN 2140', 'SPAN 2235'), S('Latin America survey or perspectives', 1, 'SPAN 2150', 'SPAN 2205'),
    S('Early Modern Iberian Survey', 1, 'SPAN 2170'), S('Advanced Spanish Writing Workshop', 1, 'SPAN 2180')]),
  R('Senior seminar', SF('SPAN 4000-level seminar', 1, subj=['SPAN'], lo=4000, hi=4899, minCr=3), 'One senior seminar (offered each semester).',
    w='Any 4000-level SPAN course is accepted here; confirm it is a designated senior seminar.'),
  R('Electives', SF('SPAN electives', 3, subj=['SPAN'], lo=2096, hi=6999, minCr=3), 'Three 3+ credit electives on the Hispanic world, beyond SPAN 2095. B- or better, no S/U. At most three courses from abroad.'),
]))

# ---------------- German Studies (BA) ----------------
_src = 'https://catalog.cornell.edu/programs/german-studies-ba/'
MAJORS.append(major('GERST', 'German Studies', _src, [
  R('Language competence', SF('GERST 3000-3209', 2, subj=['GERST'], lo=3000, hi=3209), 'Two courses with intensive language work at GERST 3000-3209 or equivalent.'),
  R('The Seminar', S('GERST 4100', 1, 'GERST 4100')),
  R('Advanced German Studies courses', [SF('GERST 3210+', 3, subj=['GERST'], lo=3210, hi=6999, not_=['GERST 4100']),
    SF('German Studies 3210+ (any department)', 2, subj=['GERST'], lo=3210, hi=6999, not_=['GERST 4100'])],
    'Six courses at 3210+, including GERST 4100; four must carry the GERST prefix. Courses with a substantial German component from other departments count with DUS approval (petition them). Eight courses and 25+ credits in all.',
    w='Non-GERST courses need a petition; at most one study-abroad course per semester counts.'),
]))

# ---------------- Animal Science (BS, CALS) ----------------
_src = 'https://cals.cornell.edu/animal-science/degrees-programs/undergraduate-studies/major-requirements'
MAJORS.append(major('ANSC', 'Animal Science', _src, [
  R('Foundational competency', [S('ANSC 1101', 1, 'ANSC 1101'), S('ANSC 1105', 1, 'ANSC 1105'), S('Domestic Animal Biology', 1, 'BIOAP 1100'),
    S('Animal Nutrition', 1, 'ANSC 2120'), S('Animal Genetics', 1, 'ANSC 2210'), S('Biology of Reproduction', 1, 'ANSC 2400')], 'ANSC 1101 and 1105 are waived for transfer students.'),
  R('Fundamentals of animal management', S('Management course', 1, 'ANSC 2500', 'ANSC 2650', 'ANSC 3000', 'ANSC 3450', 'ANSC 3600', 'ANSC 3800')),
  R('Ethics and animal welfare', S('Ethics or welfare', 1, 'ANSC 3100', 'ANSC 4140')),
  R('Statistics', S('Statistics', 1, 'MATH 1710', 'STSCI 2100', 'STSCI 2150', 'STSCI 2200')),
  R('Sustainability challenges', S('Sustainability course', 1, 'ANSC 2000', 'ANSC 4120', 'ANSC 4880', 'BIOEE 4690', 'GDEV 1300', 'GDEV 3400', 'NTRES 1101', 'NTRES 3220',
    'NTRES 4600', 'PLBRG 2010', 'PLSCS 1900')),
  R('36 Animal Science credits', C('ANSC credits', 36, any=[{'subj': ['ANSC']}, {'codes': ['BIOAP 1100']}]),
    'At least 36 credits of ANSC-coded courses (cross-listed courses and BIOAP 1100 count).', dbl=True),
  CHECK('Concentration', 'One of: Integrative Physiology & Nutrition, Pre-Veterinary Medicine, Dairy Management, Applied Animal Biology & Management, or Animal Ecology & Conservation. Chosen spring of sophomore year; core and concentration courses cannot double count.'),
], schools=['AG']))

# ---------------- Biology & Society (BA/BS) ----------------
_src = 'https://sts.cornell.edu/bio-society'
_BIOSUBJ = ['BIOMG', 'BIOEE', 'BIONB', 'BIOMI', 'BIOAP', 'BIOCB', 'BIOMS', 'BIOG', 'NS', 'ANSC', 'ENTOM', 'PLSCI']
MAJORS.append(major('BSOC', 'Biology & Society', _src, [
  R('Introductory biology (one year)', S('Intro biology', 2, 'BIOMG 1350', 'BIOG 1440', 'BIOG 1445', 'BIOEE 1610', 'BIOEE 1780', 'BIOSM 1610', 'BIOSM 1780'),
    'Two intro biology courses with an average of C or better. AP Biology does not count.'),
  R('Calculus', S('Calculus', 1, 'MATH 1106', 'MATH 1110', 'MATH 1120', 'MATH 1910', 'MATH 1920', 'MATH 2220')),
  R('Statistics', S('Statistics', 1, 'STSCI 2150', 'STSCI 2200', 'STSCI 2100', 'BTRY 3010', 'PSYCH 2500', 'SOC 3010', 'AEM 2100', 'MATH 1710', 'PUBPOL 2100', 'PUBPOL 2101', 'ILRST 2100'),
    w='Other approved statistics courses count by petition.'),
  R('Ethics', S('Ethics', 1, 'BSOC 2051', 'BSOC 2061')),
  R('Biology & Society core', S('Core course', 1, 'BSOC 2468', 'BSOC 2071', 'BSOC 3011', 'NTRES 2320')),
  R('Social science / humanities foundation', SF('Foundation courses', 2, subj=['BSOC', 'STS', 'ANTHR', 'SOC', 'HIST', 'PHIL', 'GOVT', 'PUBPOL', 'ECON', 'ENGL', 'COMM'], lo=2000, hi=4999, minCr=3),
    'Two courses from the BSOC list, from different subject areas.', w='Only courses on the BSOC foundation list count; check the list.'),
  R('Biology foundation and depth', [SF('Biology breadth', 3, subj=_BIOSUBJ, lo=2000, hi=4999, minCr=3), SF('Biology depth', 1, subj=_BIOSUBJ, lo=3000, hi=4999, minCr=3)],
    'Three breadth courses from different areas (anatomy/physiology, behavior, biochem/molecular/cell, diversity, genetics/development, neurobiology, nutrition), plus a depth course that builds on one of them.',
    w='Areas and prerequisites are not checked; use the BSOC approved lists.'),
  R('Theme', SF('Theme courses', 5, lo=2000, hi=4999, minCr=3), 'Five courses forming a coherent theme you design with your advisor, including the senior seminar.',
    w='Any 2000+ course is accepted here; your advisor approves the theme.'),
]))

# ---------------- Environment & Sustainability (BA/BS) ----------------
_src = 'https://catalog.cornell.edu/programs/environment-sustainability-bs/'
_ES_HUM = ['ANTHR 2201', 'ANTHR 2420', 'ANTHR 2482', 'ASIAN 2273', 'BSOC 2061', 'COML 2036', 'ENGL 3795', 'ENGL 4675', 'HIST 2581', 'NTRES 3330', 'PHIL 1440']
_EH = _ES_HUM + ['ANTHR 3230', 'ANTHR 3248', 'ANTHR 3325', 'ANTHR 3422', 'ANTHR 4101', 'ANTHR 4442', 'ASRC 3565', 'CLASS 2729', 'CLASS 3750', 'COML 3111', 'COML 3264', 'COML 3435',
  'COML 4902', 'ENGL 4225', 'ENGL 4795', 'ENVS 2010', 'FREN 4250', 'HIST 2371', 'HIST 4262', 'ARTH 2255', 'ARTH 3620', 'STS 3181', 'STS 4131', 'STS 4460', 'SHUM 3514', 'SPAN 4690']
_EBAE1 = ['BIOEE 3610', 'BIOEE 3690', 'BIOEE 4570', 'BIOEE 4690', 'BIOEE 4780', 'EAS 3030', 'NTRES 3150', 'NTRES 3240', 'NTRES 3250', 'NTRES 4560', 'PLSCI 3210', 'PLSCI 4660', 'PLSCI 4730']
_EBAE2 = ['BIOEE 2740', 'BIOEE 3610', 'BIOEE 3611', 'BIOEE 3730', 'BIOEE 4460', 'BIOEE 4500', 'BIOEE 4660', 'BIOEE 4700', 'BIOEE 4750', 'BIOEE 4760', 'BIOEE 4800', 'BIOMI 2900',
  'BIOMI 3500', 'BIOMI 6300', 'BIOSM 3290', 'BIOSM 3330', 'BIOSM 3450', 'BIOSM 3740', 'BIOSM 4650', 'ENTOM 2120', 'ENTOM 2440', 'ENTOM 3150', 'ENTOM 3440', 'ENTOM 3630', 'ENTOM 3755',
  'ENTOM 4000', 'ENTOM 4550', 'NTRES 3100', 'NTRES 3110', 'NTRES 3150', 'NTRES 3260', 'NTRES 3400', 'NTRES 4100', 'NTRES 4120', 'NTRES 4280', 'PLSCI 2410', 'PLSCI 3010', 'PLSCI 3150',
  'PLSCI 3420', 'PLSCI 4300']
_LAWR1 = ['EAS 1310', 'EAS 2680', 'EAS 3050', 'EAS 3340', 'EAS 3420', 'BEE 4800', 'EAS 2250', 'EAS 3010', 'EAS 3030', 'PLSCI 2600', 'PLSCI 3210', 'PLSCI 3630', 'PLSCI 3650',
  'BEE 3500', 'BEE 3710', 'BEE 4270', 'BEE 4620', 'BEE 4710', 'CEE 3310', 'EAS 3530', 'NTRES 3240']
_LAWR2 = ['BIOEE 3550', 'CRP 4080', 'EAS 2400', 'EAS 2900', 'PLSCI 2200', 'PLSCI 4200']
_LAWR3 = ['BIOEE 4570', 'BIOEE 4780', 'NTRES 3220', 'NTRES 4560', 'PLSCI 4660', 'PLSCI 4720', 'PLSCI 4730']
_EPG_MORE = ['AEM 2000', 'AEM 4500', 'AEM 4510', 'AEM 4880', 'ANTHR 2420', 'ANTHR 3422', 'BIOEE 4690', 'BSOC 2061', 'CEE 5970', 'COML 2036', 'COMM 2850', 'COMM 3210', 'COMM 4860',
  'CRP 3840', 'CRP 4080', 'CRP 5080', 'DEA 1500', 'DEA 4220', 'FSAD 3200', 'GDEV 2010', 'GDEV 2065', 'GDEV 3010', 'GDEV 3020', 'GDEV 3150', 'GDEV 3400', 'GOVT 3781', 'HIST 2581',
  'NS 4450', 'NTRES 3330', 'SOC 3650', 'STS 3181', 'STS 4131']
MAJORS.append(major('ENVS', 'Environment & Sustainability', _src, [
  R('Core curriculum', [S('Foundation', 1, 'NTRES 1101', 'ENVS 1101'), S('Social science', 1, 'NTRES 2201', 'ENVS 2201'),
    S('Biology', 1, 'BIOEE 1610', 'BIOSM 1610', 'BIOEE 1780', 'BIOEE 1781', 'BIOSM 1780'), S('Chemistry/physics', 1, 'CHEM 1560', 'CHEM 2070', 'EAS 1600'),
    S('Statistics', 1, 'AEM 2100', 'BIOEE 1760', 'PSYCH 2500', 'PUBPOL 2100', 'SOC 3010', 'STSCI 2100', 'STSCI 2150', 'STSCI 2200'), S('Humanities', 1, *_ES_HUM),
    S('Economics', 1, 'AEM 1500', 'AEM 2500', 'ENVS 1500', 'ENVS 2500'),
    S('Field/engaged experience', 1, 'BIOEE 2525', 'BIOEE 3233', 'BIOEE 3611', 'BIOEE 4570', 'ENTOM 2120', 'NTRES 2100', 'NTRES 2101', 'NTRES 2150', 'NTRES 2400', 'NTRES 2600', 'NTRES 3020',
      'NTRES 3150', 'NTRES 4560', 'BIOSM 2500', 'BIOSM 3330', 'BIOSM 3340', 'BIOSM 3450', 'BIOSM 3650', 'BIOSM 3740'),
    S('Colloquium', 1, 'ENVS 2000', 'ENVS 2010', 'BEE 2000'),
    S('Capstone', 1, 'BIOSM 3750', 'COML 4103', 'ENGL 4795', 'ENVS 4940', 'GDEV 4850', 'HIST 4262', 'NTRES 4400', 'NTRES 4500', 'NTRES 4600', 'NTRES 4700', 'NTRES 4800')],
    'Ten core courses, 28+ credits, C- or better (one may be S/U). The capstone is for juniors and seniors.'),
  OPT('Focused elective', {
    'Environmental Biology & Applied Ecology': ('Requires BIOEE 1610 and EAS 1600 in the core, plus the courses below.', [
      S('Second biology', 1, 'BIOEE 1780', 'BIOEE 1781', 'BIOSM 1780'), S('Chemistry', 1, 'CHEM 1560', 'CHEM 1570', 'CHEM 2070', 'CHEM 2080'), S('Calculus', 1, 'MATH 1106', 'MATH 1110'),
      S('Quantitative', 1, 'AEM 2770', 'BIOEE 3550', 'CS 1110', 'EAS 2900', 'ENTOM 3030', 'GDEV 4295', 'MATH 1120', 'NTRES 4100', 'NTRES 4120', 'PLSCI 2200', 'STSCI 3110', 'STSCI 3200'),
      S('Genetics', 1, 'NTRES 2830', 'BIOMG 2800'), S('Advanced ecology', 1, 'BIOEE 3610', 'NTRES 3100'), S('List 1: Ecosystems', 1, *_EBAE1), S('List 2: Organisms', 1, *_EBAE2),
      SF('One more at 4000+', 1, codes=_EBAE1 + _EBAE2, lo=4000)]),
    'Environmental Humanities': ('Eight courses (24 credits) from the EH list.', [S('EH courses', 8, *_EH)]),
    'Environmental Policy & Governance': ('Four foundational themes, a methods course, and two more environmental courses.', [
      S('Environment and law', 1, 'CRP 4590', 'LAW 4131', 'LAW 4330', 'LAW 4443', 'LAW 6361', 'LAW 7358', 'PUBPOL 5132'),
      S('Environment and human behavior', 1, 'ANTHR 2420', 'BSOC 2061', 'DEA 1500', 'GDEV 3240', 'NTRES 3330'),
      S('Environment and institutions', 1, 'AEM 4500', 'AEM 4510', 'CRP 3860', 'GOVT 1817', 'GOVT 3613', 'HIST 2581', 'NTRES 3311', 'NTRES 4600'),
      S('Environment and policy', 1, 'BME 4440', 'GOVT 3032', 'GOVT 3583', 'NTRES 4300', 'PUBPOL 3590', 'PUBPOL 3670', 'PUBPOL 3730', 'PUBPOL 3910'),
      S('Methods/tools', 1, 'AEM 2770', 'CRP 3555', 'CRP 4080', 'EAS 2400', 'GDEV 2130', 'GDEV 3140', 'GDEV 3680', 'NTRES 4600', 'PLSCI 2200', 'PLSCI 4200'),
      S('Additional environmental courses', 2, *_EPG_MORE)]),
    'Land, Air & Water Resources': ('Requires BIOEE 1610 and EAS 1600 in the core, plus four required courses and five LAWR electives.', [
      S('Biology', 1, 'BIOG 1440', 'BIOEE 1780', 'BIOEE 1781', 'BIOSM 1780', 'BIOMG 1350'), S('Chemistry', 1, 'CHEM 1560', 'CHEM 2070'), S('Calculus', 1, 'MATH 1106', 'MATH 1110'),
      S('Biogeochemistry', 1, 'EAS 3030', 'PLSCI 3650'), S('List 1: Chemical/physical', 1, *_LAWR1), S('List 2: Informatics', 1, *_LAWR2), S('List 3: Ecosystems', 1, *_LAWR3),
      S('Two more LAWR electives', 2, *(_LAWR1 + _LAWR2 + _LAWR3))]),
    'Sustainable Business & Environmental Economics': ('Requires AEM 2500 in the core, plus economics, calculus, 5.5 credits of resource/environmental economics, and a data course.', [
      S('ECON 1110', 1, 'ECON 1110'), S('ECON 1120', 1, 'ECON 1120'), S('Intermediate micro', 1, 'ECON 3030', 'AEM 2600'), S('Calculus I', 1, 'MATH 1110'),
      C('Resource/environmental economics', 5.5, codes=['AEM 3115', 'AEM 4090', 'AEM 4490', 'AEM 4500', 'AEM 4510', 'ECON 3850', 'AEM 4580', 'AEM 4585', 'AEM 4940', 'NBA 6030', 'NBA 6380']),
      S('Data/econometrics', 1, 'AEM 2770', 'AEM 2840', 'AEM 2850', 'AEM 3100', 'AEM 4110', 'CRP 4080', 'ECON 3120', 'ECON 3140', 'ILRST 2110', 'PLSCI 2200', 'STSCI 4060')]),
    'Student-Designed': ('Eight approved courses (24 credits), six at 3000+.', [SF('Approved courses', 2, lo=1000, hi=6999, minCr=3), SF('3000+ courses', 6, lo=3000, hi=6999, minCr=3)]),
  }, 'One focused elective (7-9 courses, 21+ credits), declared by spring of sophomore year. A course cannot count toward both the core and the focused elective.',
    w='Student-Designed accepts any course; only your approved proposal counts.'),
]))

# ---------------- AAP: Architecture (B.Arch) ----------------
_src = 'https://catalog.cornell.edu/programs/architecture-barch/'
MAJORS.append(major('BARCH', 'Architecture (B.Arch.)', _src, [
  R('Core design studios (years 1-3)', [S('ARCH 1101', 1, 'ARCH 1101'), S('ARCH 1102', 1, 'ARCH 1102'), S('ARCH 2101', 1, 'ARCH 2101'), S('ARCH 2102', 1, 'ARCH 2102'),
    S('ARCH 3101', 1, 'ARCH 3101'), S('ARCH 3102', 1, 'ARCH 3102')], 'Must be taken in Ithaca, C or better to advance.'),
  R('Advanced design studios', [S('ARCH 4101', 1, 'ARCH 4101', 'ARCH 3109'), S('ARCH 4102', 1, 'ARCH 4102'), S('ARCH 5101', 1, 'ARCH 5101', 'ARCH 5104')],
    'At most one non-Ithaca summer studio counts for sequence credit.'),
  R('Design thesis', S('ARCH 5902', 1, 'ARCH 5902'), 'Taken in Ithaca; cannot be repeated.'),
  CHECK('History, theory, technology, structures, and representation', 'The required non-studio architecture courses and electives in the catalog. Not tracked course-by-course here yet.'),
  CHECK('Concentration', 'Optional concentrations: Architecture, Culture, and Society; Architectural Science and Technology; History of Architecture; Theory of Architecture; Visual Representation in Architecture.'),
], schools=['AR']))

# ---------------- AAP: Urban and Regional Studies (BS) ----------------
_src = 'https://catalog.cornell.edu/programs/urban-regional-studies-bs-urs/'
MAJORS.append(major('URS', 'Urban and Regional Studies', _src, [
  R('Required core', [S('AAP 1100 / 1103', 1, 'AAP 1100', 'AAP 1103'), S('CRP 1103', 1, 'CRP 1103'), S('Introduction to Global Urban Studies', 1, 'CRP 1104'),
    S('First-year advising seminar', 1, 'CRP 1106'), S('CRP 2100', 1, 'CRP 2100'), S('CRP 2200', 1, 'CRP 2200')], 'Letter grade, 3+ credits, taken at Cornell.',
    w='Course numbers for the core changed recently; if yours differ, petition.'),
  R('Statistics', S('Statistics', 1, 'CRP 1200', 'PUBPOL 2100', 'PUBPOL 2101', 'AEM 2100', 'STSCI 2100', 'ILRST 2100', 'SOC 3010', 'PSYCH 2500'), 'CRP 1200 or an approved statistics course.'),
  R('Microeconomics', S('Microeconomics', 1, 'ECON 1110')),
  R('Engaged workshop', SF('Engaged learning workshop', 1, subj=['CRP'], attr=['CU-CEL']), 'One engaged workshop course (Ithaca, Rome, or NYC).', w='If your workshop lacks the CU-CEL tag, petition it.'),
  R('Five CRP courses at 3000+', SF('CRP 3000+', 5, subj=['CRP'], lo=3000, hi=4999, minCr=3), 'Five 3+ credit CRP courses at the 3000 level or above, taken at Cornell. A class can meet only one requirement.'),
], schools=['AR']))

# ---------------- AAP: Fine Arts (BFA) ----------------
_src = 'https://catalog.cornell.edu/programs/art-bfa/'
MAJORS.append(major('BFA', 'Fine Arts (B.F.A.)', _src, [
  R('2000-level studios', [S('ART 2501', 1, 'ART 2501'), SF('More 2000-level studios', 3, subj=['ART'], lo=2000, hi=2999, minCr=3, not_=['ART 2501'])],
    'ART 2501 in your first fall, plus three more 2000-level art studios (16 credits).'),
  R('3000-level studios', SF('3000-level studios', 4, subj=['ART'], lo=3000, hi=3999, minCr=3, not_=['ART 3006']), 'Four 3000-level studios, not ART 3006 (16 credits).'),
  R('Elective studios', SF('Elective studios', 2, subj=['ART'], lo=2000, hi=3999, minCr=3, not_=['ART 3006']), 'Two more studios at 2000 or 3000 level (8 credits).'),
  CHECK('Advanced practice and remaining requirements', 'Advanced practice, art history/theory, and other BFA requirements in the catalog (rules shown are for students entering Fall 2025). Not tracked course-by-course yet.'),
], schools=['AR']))

# ---------------- Public Policy (BA, A&S) ----------------
_src = 'https://catalog.cornell.edu/programs/public-policy-ba'
MAJORS.append(major('PPBA', 'Public Policy (B.A.)', _src, [
  R('Prerequisites', [S('Introduction to Public Policy', 1, 'PUBPOL 2301'), S('Introductory Microeconomics', 1, 'ECON 1110'),
    S('Introductory Government', 1, 'GOVT 1111', 'GOVT 1313', 'GOVT 1817'), S('Introductory Sociology', 1, 'SOC 1101', 'PUBPOL 2250', 'SOC 1104'),
    SF('Statistics', 1, any=[{'codes': ['PUBPOL 2101', 'SOC 3010', 'STSCI 3110']}, {'titles': ['Applied Probability and Statistics', 'Probability and Statistics', 'Statistics for Public Policy', 'Statistics for Sociological Research']}])],
    'C- or better before declaring. AP Micro 5 or IB HL Economics 7 covers microeconomics.'),
  R('Public Policy core', [S('Intermediate Microeconomics', 1, 'PUBPOL 2000', 'ECON 3030'), S('Population and Public Policy', 1, 'PUBPOL 2030'),
    S('Economics of the Public Sector', 1, 'PUBPOL 2040'), S('Race, Racism, and Public Policy', 1, 'PUBPOL 2370'), S('Ethics and Public Policy', 1, 'PUBPOL 2830'),
    S('Multiple Regression Analysis', 1, 'PUBPOL 3100')], 'Core courses cannot be taken abroad.'),
  R('Global and comparative policy (two)', S('Two of three', 2, 'PUBPOL 2320', 'PUBPOL 2857', 'PUBPOL 3583', 'GOVT 3583'),
    'Two of: Global Democracy and Public Policy, Global Governance and Policy, Comparative Public Policy.'),
  R('Engaged learning (CU-CEL)', SF('CEL course', 1, subj=['PUBPOL'], attr=['CU-CEL']), 'At least 3 credits of PUBPOL coursework with the CU-CEL attribute. May overlap with another requirement.', dbl=True),
  R('Public Policy electives', C('PUBPOL 2000-4999', 22, subj=['PUBPOL'], lo=2000, hi=4999, not_=['PUBPOL 4030', 'PUBPOL 4980', 'PUBPOL 4990']),
    '22 credits of 2000-4000 level PUBPOL. At most 3 special-studies credits (PUBPOL 4000/4010/4020) and 8 abroad credits per semester.',
    w='The special-studies cap is not checked. At most 12 credits may also count toward an Economics, Government, or Sociology major.'),
], schools=['AS2']))

# ---------------- Psychology (BA) ----------------
_src = 'https://psychology.cornell.edu/major'
MAJORS.append(major('PSYCH', 'Psychology', _src, [
  R('40 psychology credits', C('Psychology credits', 40, any=[{'subj': ['PSYCH']}, {'codes': ['HD 2200', 'HD 2150', 'HD 2170', 'HD 2180', 'HD 3190', 'HD 3250', 'HD 3290', 'HD 3530', 'HD 4550', 'HD 2830', 'HD 2930', 'HD 4765']}]),
    'Forty credits in psychology including prerequisites, C- or better, letter grade except PSYCH 4700/4710. Up to 12 research credits count. FWS and AP do not count.', dbl=True),
  R('Statistics', S('Statistics', 1, 'PSYCH 2500', 'AEM 2100', 'BTRY 3010', 'ECON 3110', 'ECON 3130', 'ILRST 2100', 'MATH 1710', 'PUBPOL 2100', 'PUBPOL 2101', 'SOC 3010', 'STSCI 2100', 'STSCI 2150', 'STSCI 2200'),
    'PSYCH 2500 or an approved statistics course, before senior year.', w='Approved outside statistics courses are listed at cplab.net/psychstats; the list here is partial.'),
  R('Research methods / scientific literacy', S('Methods course', 1, 'HD 2830', 'PSYCH 2830', 'HD 2930', 'PSYCH 2930', 'PSYCH 3020', 'PSYCH 3240', 'HD 4765', 'COMM 2820', 'GOVT 3999', 'STS 2011', 'BIOG 1500')),
  PICK('Breadth (three of four areas)', 3, [
    S('Perception and Cognition', 1, 'PSYCH 1102', 'PSYCH 2050', 'PSYCH 2150', 'HD 2200', 'PSYCH 2580', 'HD 2580', 'PSYCH 3140', 'HD 3190', 'PSYCH 3350', 'PSYCH 3420', 'PSYCH 4150', 'PSYCH 4270', 'PSYCH 4331'),
    S('Development', 1, 'PSYCH 1131', 'HD 1130', 'PSYCH 2090', 'HD 2150', 'HD 2170', 'HD 2180', 'HD 3290', 'HD 4550'),
    S('Cognitive and Behavioral Neuroscience', 1, 'HD 2200', 'PSYCH 2230', 'PSYCH 2300', 'PSYCH 3150', 'PSYCH 3220', 'HD 3250', 'HD 3530', 'PSYCH 4230'),
    S('Social and Personality', 1, 'PSYCH 2100', 'PSYCH 2120', 'PSYCH 2450', 'PSYCH 2650', 'PSYCH 2750', 'PSYCH 2800', 'PSYCH 2940', 'PSYCH 3135', 'PSYCH 3250', 'PSYCH 3450', 'PSYCH 3800', 'PSYCH 4940')],
    'One course in three of the four areas. Rules for students entering the major Fall 2023 or later.'),
  R('Depth', [SF('3000-level content course', 1, subj=['PSYCH'], lo=3000, hi=3999, not_=['PSYCH 3970']), SF('4000-level content course', 1, subj=['PSYCH'], lo=4000, hi=4999, not_=['PSYCH 4700', 'PSYCH 4710'])],
    'One content course at 3000 and one at 4000. Independent study does not count.'),
]))

# ---------------- Human Development (BS, Human Ecology) ----------------
_src = 'https://psychology.cornell.edu/-human-development-major-'
_HDT = ['PSYCH 2090', 'HD 2150', 'HD 2170', 'PSYCH 2170', 'HD 2180', 'PSYCH 2230', 'PSYCH 2820', 'HD 3190', 'PSYCH 3250', 'HD 3290', 'HD 3300', 'PSYCH 3320', 'HD 3450',
        'HD 3460', 'HD 3530', 'HD 4250', 'HD 4260', 'PSYCH 4320', 'HD 4400', 'HD 4490', 'PSYCH 4500', 'HD 4540', 'HD 4550', 'PSYCH 1500', 'PSYCH 2150', 'PSYCH 2750',
        'HD 3310', 'PSYCH 3450', 'HD 4210', 'HD 4340', 'HD 4500', 'HD 4770', 'PSYCH 4770', 'PSYCH 4940', 'PSYCH 4150', 'PSYCH 4270', 'PSYCH 3270', 'PSYCH 3280']
MAJORS.append(major('HD', 'Human Development', _src, [
  R('40 human development credits', C('HD credits', 40, any=[{'subj': ['HD']}, {'codes': [c for c in _HDT if c.startswith('PSYCH')] + ['PSYCH 2500', 'PSYCH 2830', 'PSYCH 2930', 'PSYCH 3020']}]),
    'Forty credits in human development including prerequisites, C- or better, letter grade except HD 4010. Up to 12 research credits count. FWS and AP do not count.', dbl=True,
    w='Psychology courses count when they are cross-listed with HD or on the major lists; check others with your advisor.'),
  R('Introduction to Lifespan Development', S('HD 1130', 1, 'HD 1130', 'PSYCH 1131')),
  R('Statistics', S('Statistics', 1, 'PSYCH 2500', 'AEM 2100', 'BTRY 3010', 'ECON 3110', 'ILRST 2100', 'MATH 1710', 'PUBPOL 2100', 'PUBPOL 2101', 'SOC 3010', 'STSCI 2100', 'STSCI 2150', 'STSCI 2200'),
    'PSYCH 2500 or an approved statistics course, before senior year.', w='Approved outside statistics courses are listed at cplab.net/psychstats.'),
  R('Research methods / scientific literacy', S('Methods course', 1, 'HD 2830', 'PSYCH 2830', 'HD 2930', 'PSYCH 2930', 'PSYCH 3020', 'PSYCH 3420', 'PSYCH 3240', 'HD 4765', 'COMM 2820', 'GOVT 3999', 'STS 2011', 'BIOG 1500')),
  R('Developmental psychology (two)', S('Developmental courses', 2, 'PSYCH 2090', 'HD 2150', 'HD 2170', 'PSYCH 2170', 'HD 2180', 'HD 2510', 'HD 2610')),
  R('Emphasis area course', S('Translational, social/environmental, cross-cultural, person-in-context, or engaged learning', 1, *_HDT), 'One course from any of the five emphasis lists.'),
  R('Depth', [SF('HD/PSYCH 3000-level content course', 1, subj=['HD', 'PSYCH'], lo=3000, hi=3999), SF('HD/PSYCH 4000-level content course', 1, subj=['HD', 'PSYCH'], lo=4000, hi=4999, not_=['HD 4010', 'PSYCH 4700', 'PSYCH 4710'])],
    'One content course at 3000 and one at 4000. Independent study does not count.'),
], schools=['HE']))

# ---------------- Biomedical Engineering (BS) ----------------
_src = 'https://www.duffield.cornell.edu/bme/degree/biomedical-engineering-bs-requirements/'
MAJORS.append(major('BME', 'Biomedical Engineering', _src, [
  R('Required engineering distributions', [S('ENGRD 2111', 1, 'ENGRD 2111'), S('ENGRD 2020', 1, 'ENGRD 2020')], 'ENGRD 2020 is best taken in semester 3 and must be done before semester 5.'),
  R('Required major courses', [S('BIOMG 1350', 1, 'BIOMG 1350'), S('BME 2010', 1, 'BME 2010'), S('BME 2080', 1, 'BME 2080'), S('BME 2000', 1, 'BME 2000'), S('BME 2210', 1, 'BME 2210'),
    S('BME 3010', 1, 'BME 3010'), S('BME 3020', 1, 'BME 3020'), S('BME 3030', 1, 'BME 3030'), S('BME 4010', 1, 'BME 4010'), S('BME 4020', 1, 'BME 4020'),
    S('BME 4080', 1, 'BME 4080'), S('BME 4090', 1, 'BME 4090'), S('Statistics', 1, 'STSCI 2200', 'STSCI 2150', 'ENGRD 2700')],
    'C- or better; only one course below C- allowed in major requirements. AP Biology 5 can substitute for BIOMG 1350.'),
  OPT('Concentration', {
    'Biomaterials and Drug Delivery': ('BME 3210, a practicum lab, CHEM 1570, and 6 elective credits.', [S('BME 3210', 1, 'BME 3210'), S('Practicum', 1, 'BME 4190', 'BME 4490'), S('CHEM 1570', 1, 'CHEM 1570'),
      C('Electives', 6, codes=['BEE 3400', 'BIOAP 4140', 'BIOMS 4140', 'BME 5620', 'MSE 5620', 'BME 5750', 'BME 5760', 'BME 5810', 'MAE 5680', 'BME 4640', 'MAE 4640', 'MSE 4020', 'MAE 6670',
        'BME 5830', 'BME 5850', 'BME 6210', 'CHEME 6310', 'CHEME 5430', 'MAE 4670', 'MSE 4610', 'MSE 5210'])]),
    'Biomedical Imaging and Instrumentation': ('BME 3310, BME 4390, PHYS 2214, and 6 elective credits.', [S('BME 3310', 1, 'BME 3310'), S('BME 4390', 1, 'BME 4390'), S('PHYS 2214', 1, 'PHYS 2214'),
      C('Electives', 6, codes=['AEP 4400', 'BIONB 4320', 'BME 3320', 'BIONB 4910', 'BME 4910', 'ECE 4910', 'BME 3300', 'BIONB 3300', 'PSYCH 3300', 'COGST 3300', 'BME 6330', 'BME 6260', 'BME 6320',
        'BME 6350', 'CS 3110', 'CS 3780', 'CS 5780', 'ECE 3200', 'INFO 3950', 'ECE 3100', 'ECE 3140', 'CS 3420', 'ECE 5725', 'ECE 3250', 'ECE 4250', 'ECE 4300', 'ECE 4320', 'MAE 4320',
        'ECE 4370', 'ECE 4760', 'ECE 5470', 'CS 4670', 'ECE 6690', 'BME 5780', 'HD 4630', 'PHYS 3316', 'BME 6180'])]),
    'Biomedical Mechanics and Mechanobiology': ('BME 3410, BME 4490, PHYS 2214 or CHEM 1570, and 6 elective credits.', [S('BME 3410', 1, 'BME 3410'), S('BME 4490', 1, 'BME 4490'),
      S('PHYS 2214 or CHEM 1570', 1, 'PHYS 2214', 'CHEM 1570'),
      C('Electives', 6, codes=['BEE 3310', 'BME 4410', 'MAE 4650', 'BEE 3500', 'MAE 3240', 'BEE 4530', 'MAE 4530', 'BME 4640', 'MAE 4640', 'BME 5810', 'MAE 5680', 'BME 6410', 'MAE 3230',
        'MAE 3783', 'MAE 4670', 'MAE 4700', 'MAE 6670', 'MSE 4020', 'MAE 3120', 'MAE 4240', 'MSE 4510', 'BME 6650', 'MAE 6650', 'MSE 6650'])]),
    'Molecular, Cellular, and Systems Engineering': ('BME 3110, BME 4190, CHEM 1570, and 6 elective credits.', [S('BME 3110', 1, 'BME 3110'), S('BME 4190', 1, 'BME 4190'), S('CHEM 1570', 1, 'CHEM 1570'),
      C('Electives', 6, any=[{'codes': ['BIOAP 4270', 'ANSC 4270', 'BIOCB 4381', 'BIOCB 4830', 'BIOCB 4840', 'CS 4775', 'BIOMG 4380', 'BIOMG 4390', 'BIOMS 4090', 'BIOMI 4090', 'BIONB 4910', 'BME 4910',
        'BIONB 3950', 'BME 4790', 'BME 5110', 'BME 5830', 'BME 5850', 'BME 6410', 'CHEM 4810', 'CHEME 5430', 'CS 3780', 'ECE 3200', 'ECE 4200', 'INFO 3950']},
        {'subj': ['BME'], 'lo': 3000, 'hi': 4999, 'minCr': 3}])]),
  }, 'One concentration, chosen in junior year. Its required science doubles as the Engineering Common Curriculum\'s major-designated science.'),
], schools=['EN']))

# ---------------- Civil Engineering (BS) ----------------
_src = 'https://www.duffield.cornell.edu/cee/degree/civil-engineering-bs-requirements'
_CE_CAP = ['CEE 4210', 'CEE 6210', 'CEE 4760', 'CEE 4565', 'CEE 4740']
_CE_DES = ['CEE 4640', 'CEE 6648', 'CEE 4745', 'CEE 5746', 'CEE 4800', 'CEE 5740', 'CEE 4200', 'CEE 4350', 'CEE 4665', 'CEE 4880', 'BEE 4880', 'CEE 4795', 'CEE 5710']
_CE_MAE = ['CEE 4510', 'CEE 4520', 'CEE 5200', 'CEE 5240', 'CEE 5735', 'CEE 5950', 'CEE 5980', 'CEE 6300', 'CEE 6530', 'CEE 6640', 'CEE 6735', 'CEE 6790', 'CEE 6930',
           'CEE 4330', 'CEE 4370', 'CEE 4530', 'CEE 6200', 'CEE 6550', 'CEE 6570', 'CEE 6590']
MAJORS.append(major('CE', 'Civil Engineering', _src, [
  R('Required engineering distribution', S('ENGRD 2020', 1, 'ENGRD 2020')),
  R('Required major courses', [S('CEE 3040', 1, 'CEE 3040'), S('CEE 3230', 1, 'CEE 3230'), S('CEE 3310', 1, 'CEE 3310'), S('CEE 3410', 1, 'CEE 3410'),
    S('CEE 3610', 1, 'CEE 3610'), S('CEE 3710', 1, 'CEE 3710'), S('CEE 4780', 1, 'CEE 4780')],
    'At most one passing grade below C- across core, design, elective, and engineering distribution courses.',
    w='The catalog lists nine required courses; check the CEE flowchart for any not shown here.'),
  R('Design courses (three)', [S('Capstone design', 1, *_CE_CAP), S('More design courses', 2, *(_CE_CAP + _CE_DES))],
    'Three design courses including one capstone, covering two distinct engineering contexts.', w='The two-contexts rule is not checked.'),
  R('Major-approved electives', S('Approved electives', 2, *(_CE_MAE + _CE_DES + _CE_CAP)), 'Two major-approved electives (6-8 credits). Extra design courses can count.'),
], schools=['EN']))

# ---------------- Physics (BA) ----------------
_src = 'https://physics.cornell.edu/physics-majors'
MAJORS.append(major('PHYS', 'Physics', _src, [
  R('Introductory sequence', [S('Mechanics', 1, 'PHYS 1112', 'PHYS 1116', 'PHYS 2207'), S('Intro experimental physics', 1, 'PHYS 1110'),
    S('Electricity and magnetism', 1, 'PHYS 2213', 'PHYS 2217'), S('Waves', 1, 'PHYS 2214', 'PHYS 2218')],
    'PHYS 1112-1110-2213-2214 plus 2216, or the augmented 1116-1110-2217-2218 (+2210). PHYS 2207 switchers take 2213, 2214, 2216. PHYS 1110 is not required on the 2207 route.',
    w='PHYS 2210 is required with 2218; PHYS 1110 does not apply to the 2207 route (petition it as waived).'),
  R('Special relativity', S('PHYS 2216 or 1116', 1, 'PHYS 2216', 'PHYS 1116'), 'PHYS 1116 covers relativity and mechanics together.', dbl=True),
  R('Mathematics', [S('Calculus II', 1, 'MATH 1910', 'MATH 1120'), S('Multivariable', 1, 'MATH 1920', 'MATH 2220', 'MATH 2130', 'MATH 2240'),
    S('Differential equations', 1, 'MATH 2930', 'MATH 3270'), S('Linear algebra', 1, 'MATH 2940', 'MATH 2210', 'MATH 2310', 'MATH 2230')],
    'Inside concentrators also take AEP 3200 and AEP 4200 (or equivalent).'),
  R('Upper-level core', [S('PHYS 3316', 1, 'PHYS 3316'), S('PHYS 3317', 1, 'PHYS 3317'), S('Lab (3+ credits)', 1, 'PHYS 4410', 'PHYS 3310', 'PHYS 3330', 'PHYS 3360', 'ASTRO 4410'),
    S('PHYS 3318', 1, 'PHYS 3318'), S('PHYS 3327', 1, 'PHYS 3327')], 'Inside concentrators must take PHYS 4410 for the lab. C- or better.'),
  R('Concentration (15 credits)', C('Concentration credits', 15, lo=3000, hi=6999),
    'At least 15 credits in an inside (physics) or outside concentration agreed with your advisor. At most 4 research credits.',
    w='Any 3000+ course is counted here; your advisor approves the concentration. Outside-concentration courses cannot count toward another major.'),
]))

# ---------------- Nutritional Sciences (BS, CALS or Human Ecology) ----------------
_src = 'https://catalog.cornell.edu/programs/nutritional-sciences-bs'
MAJORS.append(major('NS', 'Nutritional Sciences', _src, [
  R('Nutritional Sciences core', [S('NS 1150', 1, 'NS 1150'), S('NS 2450', 1, 'NS 2450'), S('NS 3450', 1, 'NS 3450'), S('NS 3310', 1, 'NS 3310'), S('NS 3320', 1, 'NS 3320')],
    'Letter grades. A course may meet only one requirement.'),
  R('Advanced electives in nutrition (9 credits)', C('NS 3000+', 9, subj=['NS'], lo=3000, hi=6999, not_=['NS 3200', 'NS 3980', 'NS 4030', 'NS 3410']),
    'Nine credits of NS at 3000+. At most 3 credits of NS 4000/4010/4020/4990. NS 3410 counts only if BIOAP 3110 covers physiology.'),
  R('Introductory chemistry', [S('General Chemistry II (or honors)', 1, 'CHEM 2080', 'CHEM 2150')],
    'CHEM 2070+2080 with labs, AP Chem 5 / IB 6-7 plus CHEM 2080, or AP plus CHEM 2150.', w='The two-course option counts once CHEM 2080 is planned; CHEM 2070 is checked by your advisor.'),
  R('Introductory biology', [S('Investigative lab', 1, 'BIOG 1500', 'BIOSM 1500'),
    S('Two lecture options', 2, 'BIOMG 1350', 'BIOG 1440', 'BIOG 1445', 'BIOEE 1610', 'BIOEE 1780')],
    'Two of: cell/developmental, comparative physiology, ecology/evolution (not two from one category). AP Bio 5 can replace one lecture.'),
  R('Organic chemistry', [S('Organic lecture', 1, 'CHEM 1570', 'CHEM 3570', 'CHEM 3590'), S('Organic lab', 1, 'CHEM 2510', 'CHEM 3010')],
    'CHEM 1570 (not for pre-health), or CHEM 3570-3580, or 3590-3600 (both courses in the sequence).'),
  R('Physiology', S('Physiology', 1, 'NS 3410', 'BIOAP 3110')),
  R('Biochemistry', S('Biochemistry', 1, 'NS 3200', 'BIOMG 3300', 'BIOMG 3310', 'BIOMG 3350'), 'NS 3200, BIOMG 3300, BIOMG 3310+3320 or 3310+BIOMI 2900, or BIOMG 3350.'),
  R('Calculus / advanced math', S('Math', 1, 'MATH 1105', 'MATH 1106', 'MATH 1110', 'MATH 1120'), 'AP Calculus 4+ also counts (BC 4-5 to skip Cornell calculus).'),
  R('Statistics', S('Statistics', 1, 'STSCI 2150', 'STSCI 2200', 'PUBPOL 2100', 'AEM 2100', 'STSCI 2100', 'PSYCH 2500', 'SOC 3010'),
    'AP Statistics is not accepted. NS 3600 requires STSCI 2150 or 2200.'),
  R('Outside Nutritional Sciences (Human Ecology students, 11 credits)', C('DEA/FSAD/HD/HE/PUBPOL credits', 11, any=[{'subj': ['DEA', 'FSAD', 'HD', 'PUBPOL'],
      'not': ['PUBPOL 2100', 'PUBPOL 3120', 'DEA 3550', 'HD 2830']}, {'subj': ['HE'], 'lo': 1500, 'not': ['HE 3400']}]),
    'Human Ecology students only; CALS students can waive this with a petition. Special studies do not count.', dbl=True),
], schools=['HE', 'AG']))

# ======================= MINORS =======================
def minor(pid, name, src, reqs):
    for r in reqs: r.setdefault('src', src)
    return {'id': 'min:' + pid, 'kind': 'minor', 'name': name, 'origin': 'new', 'src': src, 'verified': '2026-27', 'reqs': reqs}

# ---------------- Business Minor (Dyson/JCB) ----------------
_src = 'https://catalog.cornell.edu/programs/business-minor/'
_STATS_T = ['Introductory Statistics', 'Uncertainty Analysis in Engineering', 'Introduction to Statistics for Urban Studies', 'Applied Probability and Statistics', 'Applied Econometrics',
            'Probability and Statistics', 'Eng Probability and Statistics: Modeling and Data Science', 'Introductory Statistics and Data Science', 'Probability Models and Inference',
            'Basic Probability', 'Theory of Statistics', 'Introduction to Statistics', 'Statistics for Public Policy', 'Statistics and Research Design', 'Statistics for Sociological Research',
            'Introductory Statistics for Biology', 'Statistics I']
_MICRO_T = ['Introductory Microeconomics', 'Intermediate Microeconomic Theory', 'Intermediate Microeconomics']
MAJORS.append(minor('BU', 'Business', _src, [
  R('Foundation: statistics and microeconomics', [SF('Statistics', 1, titles=_STATS_T), SF('Microeconomics', 1, titles=_MICRO_T)],
    'At least 3 credits each, completed by your sixth semester.'),
  R('Core: one course in each area', [SF('Management', 1, titles=['Introduction to Business Management', 'Introduction to Management', 'Introduction to Organizations and Management', 'Managing and Leading in Organizations']),
    SF('Marketing', 1, titles=['Marketing', 'Marketing Principles', 'Marketing Management']),
    SF('Financial accounting', 1, titles=['Financial Accounting', 'Financial Accounting Principles']),
    SF('Finance', 1, titles=['Finance', 'Managerial Finance'])], '12 core credits, letter grade, C or better.'),
  R('9 credits in the College of Business', C('AEM / HADM / NBA / NCC credits', 9, subj=['AEM', 'HADM', 'NBA', 'NCC']),
    '9 of the 18 credits must carry an AEM, HADM, NBA, or NCC code. At least 12 credits must sit outside your major\'s core.', dbl=True),
  CHECK('Eligibility', 'Not open to Dyson or Nolan students, or majors that overlap two or more core courses. Sign up by your sixth semester.'),
]))

# ---------------- Computer Science Minor ----------------
_src = 'https://www.cs.cornell.edu/undergrad/csminor'
MAJORS.append(minor('CS', 'Computer Science', _src, [
  R('Programming and data structures', S('One of', 1, 'CS 2110', 'CS 2112', 'ENGRD 2110', 'ENGRD 2112', 'ENGRD 2140', 'ECE 2400')),
  R('Systems or functional programming', S('One of', 1, 'CS 3110', 'CS 3410', 'CS 3420', 'ECE 3140')),
  R('Four more CS courses', SF('CS 3000+ (or CS 2800)', 4, any=[{'subj': ['CS'], 'lo': 3000, 'hi': 9999, 'not': ['CS 4090', 'CS 4997', 'CS 4998', 'CS 4999']},
      {'codes': ['CS 2800', 'CS 2802']}]),
    'Four CS courses at 3000+ (CS 2800 also counts; seminars, CS 4090, 4997, 4998, 4999 do not). Cross-listed courses count only when taken under the CS code. Letter grade, at Cornell.',
    w='Cross-listed courses taken under another code are counted here; the department only accepts them under the CS code.'),
  CHECK('Eligibility', 'Not open to CS or ISST majors.'),
]))

# ---------------- Data Science Minor ----------------
_src = 'https://catalog.cornell.edu/programs/data-science-minor'
_DS_AN = ['AEM 3275', 'ASTRO 3334', 'ASTRO 3340', 'ASTRO 4523', 'BEE 4310', 'CHEME 4660', 'CHEME 5660', 'CS 3780', 'CS 4787', 'CS 4850', 'ECE 3200', 'ECE 4110', 'ECE 4200', 'ECE 4250',
  'ECON 3120', 'ECON 4140', 'ENGRD 2720', 'HADM 3275', 'HADM 4750', 'HD 2930', 'HD 2940', 'INFO 2950', 'INFO 2951', 'INFO 3300', 'INFO 3370', 'INFO 3950', 'MATH 2310', 'ORIE 3741',
  'ORIE 4580', 'ORIE 4740', 'ORIE 4820', 'PUBPOL 3100', 'STSCI 4060', 'STSCI 3200', 'STSCI 4100', 'STSCI 3740', 'STSCI 4110', 'STSCI 4780']
_DS_ETH = ['ALS 1210', 'COMM 4300', 'ENGL 3778', 'ENGRG 3605', 'GOVT 3999', 'INFO 1200', 'INFO 1260', 'CS 1340', 'INFO 3200', 'COMM 3200', 'INFO 3370', 'INFO 4145', 'INFO 4240',
  'INFO 4250', 'INFO 4505', 'INFO 4561', 'NBA 4920', 'PUBPOL 2070', 'PUBPOL 2130', 'PUBPOL 3520', 'PUBPOL 3725', 'STSCI 3600', 'STSCI 4850']
_DS_COM = ['COGST 3420', 'COMM 2450', 'COMM 3010', 'COMM 3150', 'COMM 4360', 'COMM 4860', 'INFO 3312', 'INFO 3950', 'INFO 4310', 'SOC 3580']
_DS_DOM = ['AEM 2770', 'AEM 3100', 'AEM 4060', 'AEM 4110', 'AEM 4225', 'AEM 4435', 'AEM 4620', 'AEM 4660', 'ASTRO 3310', 'BEE 4850', 'BIOCB 3620', 'BIOCB 4381', 'BIOCB 4830',
  'BIOCB 4840', 'BIOEE 3550', 'BIOEE 3611', 'BIOEE 4940', 'BIOMG 4810', 'BIOMG 4870', 'BIONB 3300', 'BIONB 4220', 'BIONB 4380', 'BME 4790', 'CHEME 4660', 'CHEME 5660', 'CHEM 4810',
  'COGST 3140', 'CRP 4080', 'CS 4300', 'INFO 4300', 'CS 4740', 'EAS 3450', 'EAS 5555', 'ECON 3120', 'ECON 3140', 'ECON 3720', 'ECON 3860', 'ECON 4660', 'ENTOM 3030', 'GOVT 3282',
  'HADM 4050', 'HADM 4770', 'ILRHR 4664', 'ILRGL 3330', 'ILROB 4710', 'INFO 3140', 'INFO 3350', 'INFO 4100', 'INFO 4555', 'NS 4300', 'NTRES 3100', 'NTRES 4100', 'NTRES 4120',
  'ORIE 4120', 'ORIE 4126', 'ORIE 4154', 'ORIE 4630', 'ORIE 4656', 'ORIE 4742', 'PLSCI 4000', 'PLSCI 4200', 'PLSCI 4290', 'PUBPOL 2155', 'PUBPOL 3120', 'PUBPOL 3130', 'ECON 3670',
  'PUBPOL 3280', 'GDEV 3280', 'PUBPOL 3400', 'ECON 3610', 'PUBPOL 3550', 'PUBPOL 3600', 'PUBPOL 3670', 'ECON 3850', 'PUBPOL 3780', 'PUBPOL 4080', 'PUBPOL 4101', 'PUBPOL 4110', 'STS 4040']
MAJORS.append(minor('DS', 'Data Science', _src, [
  R('Core statistics', S('One of', 1, 'ECE 3100', 'ENGRD 2700', 'MATH 4710', 'MATH 4720', 'ORIE 3500', 'STSCI 3080', 'STSCI 3110', 'ECON 3110', 'ECON 3130', 'STSCI 2200')),
  R('Core computing', S('One of', 1, 'AEM 2820', 'AEM 2830', 'AEM 2840', 'AEM 2850', 'CS 1110', 'CS 1112', 'CS 3220', 'CS 4320', 'HADM 3710', 'HADM 3740', 'ORIE 3120', 'STSCI 4060', 'STSCI 4520'),
    'If your major already requires intro programming (e.g. CS 1110), take a more advanced course here.', w='The advanced-course rule for majors that require CS 1110 is not checked.'),
  {'n': 'Four courses across three categories', 't': 'cats', 'k': 4, 'minCats': 3, 'maxPer': 2, 'src': _src,
   'd': 'Four courses: at least one from each of three categories (Data Analysis; Big Data Ethics, Policy & Society; Data Communication; Domain Expertise); the fourth from any. Six courses in all, C or better, letter grade, at Cornell. At most two courses may also count toward your major core.',
   'cats': [{'n': 'Data Analysis', 'f': {'codes': _DS_AN}}, {'n': 'Big Data Ethics, Policy & Society', 'f': {'codes': _DS_ETH}},
            {'n': 'Data Communication', 'f': {'codes': _DS_COM}}, {'n': 'Domain Expertise', 'f': {'codes': _DS_DOM}}]},
]))

# ---------------- Artificial Intelligence Minor ----------------
_src = 'https://catalog.cornell.edu/programs/artificial-intelligence-minor/'
_AI_EL = ['BIONB 3500', 'BME 4790', 'CS 4670', 'CS 4701', 'CS 4740', 'COGST 4740', 'LING 4474', 'CS 4750', 'ECE 4770', 'MAE 4760', 'CS 4756', 'CS 4782', 'CS 4783', 'CS 4787', 'CS 4789',
  'CS 4860', 'MATH 4860', 'ECE 4160', 'ENGRG 3605', 'PHIL 2473', 'STS 3605', 'INFO 1170', 'INFO 1260', 'CS 1340', 'INFO 3160', 'INFO 3350', 'INFO 3950', 'INFO 4120', 'INFO 4300',
  'CS 4300', 'INFO 4240', 'STS 4240', 'INFO 4260', 'STS 4260', 'INFO 4310', 'INFO 4410', 'INFO 4470', 'ILRGL 4066', 'AMST 4066', 'LING 4424', 'COGST 4240', 'CS 4744', 'LING 4434',
  'CS 4745', 'MAE 4180', 'CS 4758', 'ECE 4180', 'MAE 4810', 'ECE 4240', 'NBA 4920', 'ORIE 3320', 'ORIE 4160', 'ORIE 4740', 'ORIE 4742', 'ORIE 4570', 'PHIL 2621', 'COGST 2621',
  'PUBPOL 2120', 'PUBPOL 3520', 'PUBPOL 4210', 'INFO 4210', 'STSCI 4030', 'STSCI 4520', 'STSCI 4750']
MAJORS.append(minor('AI', 'Artificial Intelligence', _src, [
  R('Foundations of AI', [S('Machine learning', 1, 'CS 3780', 'ECE 3200', 'ORIE 3741', 'STSCI 3740'), S('Reasoning', 1, 'CS 3700'),
    S('Human-AI interaction', 1, 'INFO 3160', 'INFO 4240', 'STS 4240', 'INFO 4470', 'INFO 3450'),
    S('Ethics, governance & policy', 1, 'ENGRG 3605', 'PHIL 2473', 'STS 3605', 'INFO 1210', 'INFO 1260', 'CS 1340', 'INFO 4210', 'PUBPOL 4210')],
    'Four required foundations. C or better (C- not accepted), letter grade, at Cornell; no substitutions or outside credit.',
    w='INFO 4940 counts for Human-AI Interaction only in the Designing AI Products or Human-AI Interaction Design topics (petition it). INFO 3450 counts only for Dec 2026 / May 2027 graduates.'),
  R('AI electives', S('Two electives', 2, *_AI_EL), 'Two from the approved list. At most two minor courses can also count toward your major requirements.',
    w='INFO 4940 counts only in approved topics; petition it if yours qualifies.'),
]))

# ---------------- Psychology Minor ----------------
_src = 'https://psychology.cornell.edu/minor'
MAJORS.append(minor('PSYCH', 'Psychology', _src, [
  R('18 psychology credits', C('Psychology credits', 18, any=[{'subj': ['PSYCH']}, {'codes': ['HD 2200', 'HD 2150', 'HD 2170', 'HD 2180', 'HD 3190', 'HD 3250', 'HD 3290', 'HD 3530', 'HD 4550', 'HD 1130']}]),
    'Eighteen credits in psychology, letter grade except PSYCH 4700/4710 (up to 6 research credits count). FWS and AP do not count. Not open to Psychology or Human Development majors.', dbl=True),
  PICK('Breadth (three of four areas)', 3, [
    S('Perception and Cognition', 1, 'PSYCH 1102', 'PSYCH 2050', 'PSYCH 2150', 'HD 2200', 'PSYCH 2580', 'HD 2580', 'PSYCH 3140', 'HD 3190', 'PSYCH 3350', 'PSYCH 3420', 'PSYCH 4150', 'PSYCH 4270', 'PSYCH 4331'),
    S('Development', 1, 'PSYCH 1131', 'HD 1130', 'PSYCH 2090', 'HD 2150', 'HD 2170', 'HD 2180', 'HD 3290', 'HD 4550'),
    S('Cognitive and Behavioral Neuroscience', 1, 'HD 2200', 'PSYCH 2230', 'PSYCH 2300', 'PSYCH 3150', 'PSYCH 3220', 'HD 3250', 'HD 3530', 'PSYCH 4230'),
    S('Social and Personality', 1, 'PSYCH 2100', 'PSYCH 2120', 'PSYCH 2450', 'PSYCH 2650', 'PSYCH 2750', 'PSYCH 2800', 'PSYCH 2940', 'PSYCH 3135', 'PSYCH 3250', 'PSYCH 3450', 'PSYCH 3800', 'PSYCH 4940')],
    'One course in three of the four areas.', w='Area lists are taken from the Psychology major; check with your minor advisor for anything not listed.'),
]))

# ---------------- Public Policy Minor (Government, A&S) ----------------
_src = 'https://government.cornell.edu/public-policy-minor'
MAJORS.append(minor('POLICY', 'Public Policy (Government Dept.)', _src, [
  R('Gateway courses', S('GOVT 3032 and GOVT 3583', 2, 'GOVT 3032', 'GOVT 3583', 'PUBPOL 3583'),
    'The catalog lists both GOVT 3032 (Politics of Public Policy in the U.S.) and GOVT 3583 (Comparative Public Policy).',
    w='The catalog lists both courses; confirm with the minor coordinator whether one gateway is enough.'),
  R('Three more qualifying courses', SF('Policy courses', 3, subj=['GOVT'], lo=2000, hi=4999, minCr=3),
    'Five qualifying courses and 15 credits in all. At most one policy course from another department (advisor approval). Government majors may share only one course with the major.',
    w='Any 2000+ GOVT course is counted here; only courses on the department\'s public policy list qualify.'),
]))

# ---------------- Policy Analysis and Management Minor (Brooks) ----------------
_src = 'https://catalog.cornell.edu/programs/policy-analysis-management-minor/'
_PP_NS = ['PUBPOL 4000', 'PUBPOL 4010', 'PUBPOL 4020', 'PUBPOL 4030']
MAJORS.append(minor('PAM', 'Policy Analysis and Management (Brooks)', _src, [
  R('Introduction', S('PUBPOL 2301 or 2300', 1, 'PUBPOL 2301', 'PUBPOL 2300')),
  R('Upper-level PUBPOL (9 credits)', C('PUBPOL 3000-4999', 9, subj=['PUBPOL'], lo=3000, hi=4999, not_=_PP_NS)),
  R('15 PUBPOL credits in all', C('PUBPOL credits', 15, subj=['PUBPOL'], not_=_PP_NS),
    'B- or better, PUBPOL section only (not cross-listed sections), no special studies. Not open to PAM, Public Policy, or Health Care Policy majors; cannot be combined with the Health Policy minor.', dbl=True),
]))

# ---------------- Applied Economics Minor (Dyson/JCB) ----------------
_src = 'https://catalog.cornell.edu/programs/applied-economics-minor'
MAJORS.append(minor('APPLIEDECON', 'Applied Economics', _src, [
  R('Introductory economics', [S('Microeconomics', 1, 'ECON 1110'), S('Macroeconomics', 1, 'ECON 1120')], 'Both, before the core courses.'),
  R('Managerial Economics', S('AEM 2600', 1, 'AEM 2600')),
  R('Applied economics topics', S('Three courses', 3, 'AEM 4140', 'AEM 4315', 'AEM 4485', 'AEM 4500', 'AEM 4510', 'AEM 4550', 'AEM 2350', 'AEM 2310', 'AEM 2500'),
    'Three from the approved list (Economics majors take four). Letter grade, C or better.',
    w='The approved list shown is partial (the catalog list was cut off); petition other courses from the minor\'s list.'),
  R('9 credits in the College of Business', C('AEM / HADM / NBA / NCC credits', 9, subj=['AEM', 'HADM', 'NBA', 'NCC']),
    '9 credits must carry an AEM, HADM, NBA, or NCC code. Not open to Dyson students.', dbl=True),
]))

# ---------------- Global & Public Health Sciences (BS; CALS and Human Ecology versions share these) ----------------
_src = 'https://catalog.cornell.edu/programs/global-public-health-sciences-hum-ecol-bs/'
MAJORS.append(major('GPHS', 'Global & Public Health Sciences', _src, [
  R('Global & Public Health core', [S('NS 1600', 1, 'NS 1600'), S('NS 2060', 1, 'NS 2060'), S('NS 2600', 1, 'NS 2600'), S('NS 3600', 1, 'NS 3600'), S('NS 4600', 1, 'NS 4600')],
    '14 credits. All major requirements must be letter-graded.'),
  CHECK('Supervised experiential learning', 'An approved public health experience (e.g. NS 4060 internship or research, Cornell in Washington NS 4998, study abroad), between spring of sophomore year and the fall of senior year.'),
  R('Social & behavioral health selective', S('One course', 1, 'NS 2450', 'NS 4480', 'NS 4510', 'NS 4570', 'ECON 3910', 'ANTHR 2468', 'COMM 2850', 'COMM 4760', 'HD 4600', 'GDEV 3020',
      'PUBPOL 3180', 'PUBPOL 3280', 'GDEV 3280', 'PUBPOL 4280', 'ECON 3710', 'SOC 4120'), '3+ credits at the 2000 level or above.',
    w='The department updates these lists; newer options are posted on the GPHS requirements page.'),
  R('Biological aspects of public health selective', S('One course', 1, 'NS 3060', 'NS 3150', 'NS 4140', 'NS 4200', 'NS 4210', 'NS 4300', 'NS 4410', 'NS 5510', 'BIOMG 4390',
      'BIOMG 4870', 'BIOMI 2600', 'BIOMI 2950', 'BIOMI 3210', 'BIOMI 4040', 'BIONB 3920', 'ENTOM 4000', 'PLSCI 2100'), '3+ credits at the 2000 level or above.'),
  R('Environmental health selective', S('One course', 1, 'DEA 2700', 'GDEV 3020', 'GDEV 3400', 'BIOMI 2500', 'BIOMI 2950', 'BIOMI 4310', 'BIOMS 4310', 'COMM 2850', 'STS 2851',
      'ENTOM 2100', 'BSOC 2101', 'ENTOM 4520', 'FDSC 3960', 'PLSCI 2100', 'PLSCI 2400', 'PLSCI 4140', 'PLSCI 4450'), '3+ credits at the 2000 level or above.'),
  R('Health policy & practice selective', S('One course', 1, 'NS 4450', 'NS 4500', 'NS 4510', 'NS 4570', 'ECON 3910', 'AMST 2225', 'GOVT 2225', 'ILROB 2220', 'PUBPOL 2220', 'SOC 2220',
      'PHIL 1950', 'ANTHR 4458', 'EDUC 4458', 'FGSS 4458', 'CRP 3430', 'GDEV 3020', 'PUBPOL 2208', 'SOC 2208', 'GDEV 3700', 'SOC 3710', 'GOVT 3032', 'HD 4600',
      'PUBPOL 2030', 'PUBPOL 2350', 'PUBPOL 3110', 'PUBPOL 3230', 'PUBPOL 3650', 'PUBPOL 3780', 'PUBPOL 3870', 'PUBPOL 5870'), '3+ credits at the 2000 level or above.'),
  R('Introductory chemistry', S('General chemistry', 1, 'CHEM 2070', 'CHEM 2080', 'CHEM 1560', 'CHEM 2150'),
    'CHEM 2070-2080 with labs (pre-health), CHEM 2070 alone, CHEM 1560, or CHEM 2150. At least one semester must be taken at Cornell.'),
  R('Introductory biology', [S('Investigative lab', 1, 'BIOG 1500', 'BIOSM 1500'), S('Two lecture options', 2, 'BIOMG 1350', 'BIOG 1440', 'BIOG 1445', 'BIOEE 1610', 'BIOEE 1780')],
    'Two of three lecture categories (not two from one). AP Biology 5 can replace one lecture.'),
  R('Organic chemistry lecture', S('Organic chemistry', 1, 'CHEM 1570', 'CHEM 3530', 'CHEM 3570', 'CHEM 3590'), 'CHEM 1570, 3530, 3570 (+3580 for pre-health), or 3590-3600.'),
  R('Physiology', S('Physiology', 1, 'NS 3410', 'BIOG 1440', 'BIOG 1445', 'NS 1150', 'NS 1220'), 'BIOG 1440/1445 count here only if not used for introductory biology.'),
  R('Biochemistry', S('Biochemistry', 1, 'NS 3200', 'BIOMG 3300', 'BIOMG 3310', 'BIOMG 3350'), 'NS 3200, BIOMG 3300, BIOMG 3310 with 3320 or BIOMI 2900, or BIOMG 3350.'),
  PICK('Social sciences (Human Ecology students)', 2, [S('Anthropology', 1, 'ANTHR 1400'), S('Economics', 1, 'ECON 1110', 'ECON 1120'),
      S('Psychology', 1, 'HD 1130', 'PSYCH 1101'), S('Sociology', 1, 'SOC 1101')],
    'Human Ecology students take one course in two of the four areas. CALS students meet this through CALS distributions instead.'),
  R('Statistics', S('Statistics', 1, 'STSCI 2150', 'BTRY 3010'), 'Must be taken at Cornell; AP Statistics is not accepted.'),
], schools=['HE', 'AG']))
