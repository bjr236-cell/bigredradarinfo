#!/usr/bin/env python3
"""Writes data/programs/coverage.json: every undergraduate major and minor in Cornell's catalog
(Courses of Study program index, 2026-27) and whether this dataset covers it.
The catalog index was read through 'Statistics & Biometry (BS)'; later entries (T-Z) are marked as such."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
U = "https://catalog.cornell.edu/programs/"
# (catalog name, catalog slug, dataset id or None)
MAJORS = [
 ("Africana Studies (BA)", "africana-studies-ba", None), ("Agricultural Sciences (BS)", "agricultural-sciences-bs", None),
 ("American Studies (BA)", "american-studies-ba", "maj:AMST"), ("Animal Science (BS)", "animal-science-bs", "maj:ANSC"),
 ("Anthropology (BA)", "anthropology-ba", "maj:ANTHR"), ("Applied Economics and Management (BS)", "applied-economics-management-bs", "maj:AEM"),
 ("Archaeology (BA)", "archaeology-ba", None), ("Architecture (BAR)", "architecture-barch", "maj:BARCH"),
 ("Asian Studies (BA)", "asian-studies-ba", None), ("Astronomy (BA)", "astronomy-ba", "maj:ASTRO"),
 ("Atmospheric Sciences (BS)", "atmospheric-science-bs", "maj:AS"), ("Biological Engineering (BS)", "biological-engineering-bs", "maj:BE"),
 ("Biological Sciences (BA)", "biological-sciences-ba", "maj:BIO"), ("Biological Sciences (BS)", "biological-sciences-bs", "maj:BIO"),
 ("Biology & Society (BA, BS)", "biology-society-ba", "maj:BSOC"), ("Biomedical Engineering (BS)", "biomedical-engineering-bs", "maj:BME"),
 ("Chemical Engineering (BS)", "chemical-engineering-bs", "maj:CHEME"), ("Chemistry (BA)", "chemistry-ba", "maj:CHEM"),
 ("China and Asia-Pacific Studies (BA)", "china-asia-pacific-studies-ba", None), ("Civil Engineering (BS)", "civil-engineering-bs", "maj:CE"),
 ("Classics (BA)", "classics-ba", None), ("Cognitive Science (BA)", "cognitive-science-ba", "maj:COGST"),
 ("College Scholar (BA)", "college-scholar-ba", None), ("Communication (BS)", "communication-bs", "maj:COMM"),
 ("Comparative Literature (BA)", "comparative-literature-ba", None), ("Computer Science (BA)", "computer-science-ba", "maj:CS"),
 ("Computer Science (BS)", "computer-science-bs", "maj:CS"), ("Design and Environmental Analysis (BS)", "design-environmental-analysis-bs", "maj:DEA"),
 ("Earth and Atmospheric Sciences (BA)", "earth-atmospheric-sciences-ba", "maj:EAS"),
 ("Earth and Atmospheric Sciences (BS, CALS)", "earth-atmospheric-sciences-easag-bs", "maj:EAS"),
 ("Earth and Atmospheric Sciences (BS, Engineering)", "earth-atmospheric-sciences-easen-bs", "maj:EAS"),
 ("Economics (BA)", "economics-ba", "maj:ECON"), ("Electrical and Computer Engineering (BS)", "electrical-computer-engineering-bs", "maj:ECE"),
 ("Engineering Physics (BS)", "engineering-physics-bs", "maj:EP"), ("English (BA)", "english-ba", "maj:ENGL"),
 ("Entomology (BS)", "entomology-bs", None), ("Environment & Sustainability (BA)", "environment-sustainability-ba", "maj:ENVS"),
 ("Environment & Sustainability (BS)", "environment-sustainability-bs", "maj:ENVS"), ("Environmental Engineering (BS)", "environmental-engineering-bs", "maj:ENV"),
 ("Fashion Design and Management (BS)", "fashion-design-management-bs", "maj:FSAD"), ("Feminist, Gender, & Sexuality Studies (BA)", "fgss-ba", None),
 ("Fiber Science (BS)", "fiber-science-bs", None), ("Fine Arts (BFA)", "art-bfa", "maj:BFA"), ("Food Science (BS)", "food-science-bs", "maj:FDSC"),
 ("French (BA)", "french-ba", "maj:FREN"), ("German Studies (BA)", "german-studies-ba", "maj:GERST"),
 ("Global & Public Health Sciences (BS, CALS)", "global-public-health-sciences-bs", "maj:GPHS"),
 ("Global & Public Health Sciences (BS, Human Ecology)", "global-public-health-sciences-hum-ecol-bs", "maj:GPHS"),
 ("Global Development (BS)", "global-development-bs", "maj:GDEV"), ("Government (BA)", "government-ba", "maj:GOVT"),
 ("Health Care Policy (BS)", "health-care-policy-major-bs", "maj:HCP"), ("History (BA)", "history-ba", "maj:HIST"),
 ("History of Architecture and Urban Development (BS)", "history-architecture-urban-development-bs-haud", None),
 ("History of Art (BA)", "history-art-ba", None), ("Hotel Administration (BS)", "hotel-management-bs", "maj:HADM"),
 ("Human Biology, Health, and Society (BS)", "human-biology-health-society-bs", None), ("Human Development (BS)", "human-development-bs", "maj:HD"),
 ("Independent Major", "independent-major", None), ("Industrial and Labor Relations (BS)", "industrial-labor-relations-bs", "maj:ILR"),
 ("Information Science (BA)", "information-science-ba", "maj:INFO"), ("Information Science (BS)", "information-science-bs", "maj:INFO"),
 ("Information Science, Systems, and Technology (BS)", "information-science-systems-technology-bs", "maj:ISST"),
 ("Interdisciplinary Studies (BS)", "interdisciplinary-studies-bs", None), ("Italian (BA)", "italian-ba", None),
 ("Jewish Studies (BA)", "jewish-studies-ba", "maj:JWST"), ("Landscape Architecture (BS)", "landscape-architecture-bs", None),
 ("Linguistics (BA)", "linguistics-ba", "maj:LING"), ("Materials Science and Engineering (BS)", "materials-science-engineering-bs", "maj:MSE"),
 ("Mathematics (BA)", "mathematics-ba", "maj:MATH"), ("Mechanical Engineering (BS)", "mechanical-engineering-bs", "maj:ME"),
 ("Music (BA)", "music-ba", None), ("Near Eastern Studies (BA)", "near-eastern-studies-ba", None),
 ("Nutritional Sciences (BS)", "nutritional-sciences-bs", "maj:NS"), ("Operations Research and Engineering (BS)", "operations-research-engineering-bs", "maj:ORIE"),
 ("Performing and Media Arts (BA)", "performing-media-arts-ba", None), ("Philosophy (BA)", "philosophy-ba", "maj:PHIL"),
 ("Physics (BA)", "physics-ba", "maj:PHYS"), ("Plant Sciences (BS)", "plant-sciences-bs", None),
 ("Policy Analysis and Management (BS)", "policy-analysis-management-bs", "maj:PAM"), ("Psychology (BA)", "psychology-ba", "maj:PSYCH"),
 ("Public Policy (BA)", "public-policy-ba", "maj:PPBA"), ("Public Policy (BS)", "public-policy-bs", "maj:PUBPOL"),
 ("Religious Studies (BA)", "religious-studies-ba", None), ("Science & Technology Studies (BA)", "science-technology-studies-ba", "maj:STS"),
 ("Sociology (BA)", "sociology-ba", None), ("Spanish (BA)", "spanish-ba", "maj:SPAN"),
 ("Statistical Science (BA)", "statistics-data-science-ba", "maj:STSCI"), ("Statistics & Biometry (BS)", "biometry-statistics-bs", "maj:STSCI"),
 # after the point where the catalog index was read; from the earlier catalog index
 ("Urban and Regional Studies (BS)", "urban-regional-studies-bs-urs", "maj:URS"), ("Viticulture and Enology (BS)", "viticulture-enology-bs", "maj:VIEN"),
]
MINORS = [
 ("Actuarial Science", "actuarial-science-minor", None), ("Aerospace Engineering", "aerospace-engineering-minor", "min:AEROSPACE"),
 ("Africana Studies", "africana-minor", None), ("American Indian and Indigenous Studies", "american-indian-indigenous-studies-minor", None),
 ("ASL/Deaf Studies", "asl-deaf-studies-minor", None), ("American Studies", "american-studies-minor", None),
 ("Animal Science", "animal-science-minor", "min:ANIMALSCIENCE"), ("Anthropology", "anthropology-minor", None),
 ("Applied Economics", "applied-economics-minor", "min:APPLIEDECON"), ("Applied Exercise Science", "applied-exercise-science-minor", None),
 ("Applied Mathematics", "applied-mathematics-minor", "min:APPLIEDMATH"), ("Arabic", "arabic-minor", None),
 ("Archaeology", "archaeology-minor", None), ("Architecture", "architecture-minor-for-non-departmental-students", None),
 ("Artificial Intelligence", "artificial-intelligence-minor", "min:AI"), ("Asian American Studies", "asian-american-studies-minor", None),
 ("Astrobiology", "astrobiology-minor", None), ("Astronomy", "astronomy-minor", "min:ASTRO"), ("Atmospheric Sciences", "atmospheric-science-minor", None),
 ("Biological Engineering", "biological-engineering-minor", None), ("Biological Sciences", "biological-sciences-minor", None),
 ("Biomedical Engineering", "biomedical-engineering-minor", None), ("Biometry and Statistics", "biometry-statistics-minor", None),
 ("Business", "business-minor", "min:BU"), ("Business for Engineers", "dyson-business-minor-engineers", "min:DBME"),
 ("Business for Life Sciences", "dyson-business-minor-life-sciences", None), ("Caribbean Studies", "caribbean-studies-minor", None),
 ("China and Asia-Pacific Studies", "china-asia-pacific-studies-minor", None), ("Civil Infrastructure", "civil-infrastructure-minor", None),
 ("Classical Civilization", "classical-civilization-minor", None), ("Classics", "classics-minor", None), ("Climate Change", "climate-change-minor", "min:CLIMATECHANGE"),
 ("Cognitive Science", "cognitive-science-minor", "min:COGSCI"), ("Communication", "communications-minor", None),
 ("Community Food Systems", "community-food-systems-minor-cfs", None), ("Comparative Literature", "comparative-literature-minor", None),
 ("Computer Science", "computer-science-minor", "min:CS"), ("Creative Writing", "creative-writing-minor", None),
 ("Crime, Prisons, Education, and Justice", "crime-prisons-education-justice-minor", None), ("Crop Management", "crop-management-minor", None),
 ("Dance", "dance-minor", None), ("Data Science in Astronomy", "data-science-astronomy-minor", None), ("Data Science", "data-science-minor", "min:DS"),
 ("Demography", "demography-minor", "min:DEMOG"), ("Design and Environmental Analysis", "design-environmental-analysis-minor", "min:DEA"),
 ("Design Innovation and Strategy", "design-innovation-strategy-minor", None), ("Earth and Atmospheric Sciences", "earth-atmospheric-sciences-minor", "min:EAS"),
 ("East Asian Studies", "east-asian-studies-minor", None), ("Education", "education-minor", None),
 ("Electrical and Computer Engineering", "electrical-computer-engineering-minor", "min:ECE"), ("Engineering Communications", "engineering-communications-minor", None),
 ("Engineering Entrepreneurship", "engineering-entrepreneurship-minor", None), ("Engineering Management", "engineering-management-minor", None),
 ("English", "english-minor", None), ("Entomology", "entomology-minor", None), ("Entrepreneurship", "entrepreneurship-minor", None),
 ("Environment & Sustainability", "environment-sustainability-minor", None), ("Environmental Engineering", "environmental-engineering-minor", None),
 ("European Studies", "european-studies-minor", None), ("Fashion Studies", "fashion-studies-minor", None),
 ("Feminist, Gender, & Sexuality Studies", "fgss-minor", None), ("Fiber Science", "fiber-science-minor", None), ("Film", "film-minor", None),
 ("Fine Arts", "fine-arts-minor-for-non-departmental-students", None), ("Food and Agricultural Business", "food-agricultural-business-minor", None),
 ("Food Science", "food-science-minor", None), ("French Studies", "french-minor", None), ("Fungal Biology", "fungal-biology-minor", None),
 ("Game Design", "game-design-minor", "min:GAMEDESIGN"), ("German Studies", "german-studies-minor", None), ("Gerontology", "gerontology-minor", None),
 ("Global Asia Studies", "global-asia-studies-minor", None), ("Global Development", "global-development-minor", None),
 ("Global Health", "global-health-minor", None), ("Health Policy", "health-policy-minor", "min:HP"), ("Healthy Futures", "healthy-futures-minor", None),
 ("History", "history-minor", "min:HISTM"), ("History of Art", "history-art-minor", None),
 ("History of Capitalism", "history-capitalism-interdisciplinary-minor", None), ("Horticulture", "horticulture-minor", None),
 ("Human Development", "human-development-minor", "min:HD"), ("Inequality Studies", "inequality-studies-minor", "min:INEQ"),
 ("Information Science", "information-science-minor", "min:ISST"), ("International Markets and Development", "international-markets-development-minor", None),
 ("International Relations", "international-relations-minor", None), ("Italian", "italian-minor", None), ("Jewish Studies", "jewish-studies-minor", None),
 ("Latin American Studies", "latin-american-studies-minor", None), ("Latina/o Studies", "latina-o-studies-minor", None),
 ("Law & Society", "law-society-minor", "min:LAWSOC"), ("Leadership", "leadership-minor", None),
 ("Lesbian, Gay, Bisexual, & Transgender", "lgbt-minor", None), ("Linguistics", "linguistics-minor", "min:LING"),
 ("Materials Science and Engineering", "materials-science-engineering-minor", None), ("Mathematics", "mathematics-minor", "min:MATH"),
 ("Mechanical Engineering", "mechanical-engineering-minor", None), ("Media Studies", "media-studies-minor", None),
 ("Medieval Studies", "medieval-studies-minor", None), ("Migration Studies", "migration-studies-minor", None),
 ("Minority, Indigenous, and Third World Studies", "mitws-minor", None), ("Moral Psychology", "moral-psychology-minor", None),
 ("Music", "music-minor", None), ("Near Eastern Studies", "near-eastern-studies-minor", None), ("Nutrition and Health", "nutrition-health-minor", None),
 ("Operations Research and Management Science", "operations-research-management-science-minor", "min:ORMS"),
 ("Performing and Media Arts", "performing-media-arts-minor", None), ("Philosophy", "philosophy-minor", "min:PHIL"), ("Physics", "physics-minor", None),
 ("Plant Breeding", "plant-breeding-minor", None), ("Plant Sciences", "plant-sciences-minor", None),
 ("Policy Analysis and Management", "policy-analysis-management-minor", "min:PAM"),
 ("Portuguese and Brazilian Studies", "portuguese-brazilian-studies-minor", None), ("Psychology", "psychology-minor", "min:PSYCH"),
 ("Public History", "public-history-minor", None), ("Public Policy", "public-policy-minor", "min:POLICY"),
 ("Public Service Studies", "public-service-studies-minor", None), ("Real Estate (for Nolan)", "real-estate-minor-nolan-school-ug-students", None),
 ("Real Estate (for non-Nolan)", "real-estate-minor-non-nolan-ug-students", None), ("Religious Studies", "religious-studies-minor", None),
 ("Robotics", "robotics-minor", "min:ROBOTICS"), ("Russian", "russian-minor", None), ("Sanskrit Studies", "sanskrit-studies-minor", None),
 ("Science & Technology Studies", "science-technology-studies-minor", None),
 ("Science Communication and Public Engagement", "science-communication-public-engagement-minor", None),
 ("Smart Cities", "smart-cities-minor", None), ("Soil Science", "soil-science-minor", None), ("South Asian Studies", "south-asian-studies-minor", None),
 ("Southeast Asian Studies", "southeast-asian-studies-minor", None), ("Spanish", "spanish-minor", "min:SPAN"),
]
ids = {}
for f in ("majors", "minors"):
    for p in json.load(open(os.path.join(ROOT, "data", "programs", f + ".json")))["programs"]:
        ids[p["id"]] = p["status"]
def rows(items, kind):
    out = []
    for name, slug, pid in items:
        st = ids.get(pid, "missing") if pid else "missing"
        out.append({"name": name, "type": kind, "catalog_url": U + slug + "/", "status": st, "dataset_id": pid if st != "missing" else None})
    return out
all_rows = rows(MAJORS, "major") + rows(MINORS, "minor")
extra = [{"id": k, "status": v} for k, v in ids.items() if k not in {p for _, _, p in MAJORS + MINORS}]
doc = {"source": "Cornell Courses of Study 2026-27, Programs A-Z (courses.cornell.edu/programs/programs.pdf)",
       "note": "Undergraduate majors and minors only. The catalog index was read through 'Statistics & Biometry (BS)'; any later entries "
               "(T-Z) other than the two majors listed are not included here.",
       "summary": {k: {s: sum(1 for r in all_rows if r["type"] == k and r["status"] == s) for s in ("verified", "unverified", "missing")} for k in ("major", "minor")},
       "programs": all_rows, "in_dataset_but_not_in_index": extra}
json.dump(doc, open(os.path.join(ROOT, "data", "programs", "coverage.json"), "w"), indent=1)
print(json.dumps(doc["summary"]), "| not matched to the index:", extra)
