#!/usr/bin/env python3
"""
Pull Cornell's Class Roster into one JSON file per term: data/rosters/<TERM>.json

Source: Cornell's public Class Roster API (https://classes.cornell.edu/api/2.0/), one request per second
as Cornell asks. A full term is ~200 subjects, so roughly 4 minutes per term.

Usage
  python scripts/update_rosters.py                    # the current and upcoming terms (what the scheduled job runs)
  python scripts/update_rosters.py --terms FA26,SP27  # specific terms
  python scripts/update_rosters.py --all              # every term Cornell has (FA14 on; about 3 hours)
  python scripts/update_rosters.py --missing          # every term not already in data/rosters/
  add --since FA23 to --all or --missing to skip older terms (this repo keeps Fall 2023 on)

Also rewrites data/rosters/index.json (which terms exist, when each was pulled, class counts).
Standard library only.
"""
import argparse, datetime, json, os, sys, time, urllib.error, urllib.parse, urllib.request

API = "https://classes.cornell.edu/api/2.0"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data", "rosters")
UA = "cornell-planner-data/1.0 (student project; roster sync)"
_last = [0.0]


def get(path, **params):
    url = f"{API}/{path}?{urllib.parse.urlencode(params)}"
    for attempt in range(5):
        wait = 1.0 - (time.time() - _last[0])
        if wait > 0:
            time.sleep(wait)
        _last[0] = time.time()
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as r:
                body = json.load(r)
            if body.get("status") == "success":
                return body["data"]
            raise RuntimeError(json.dumps(body.get("message") or body)[:200])
        except urllib.error.HTTPError as e:
            # Cornell answers a subject with no classes this term with an error status
            if e.code in (400, 404):
                return {"classes": []}
            if attempt == 4:
                raise
        except Exception:
            if attempt == 4:
                raise
        time.sleep(2 * (attempt + 1))


def hhmm(t):
    """'10:10AM' -> '10:10' (24-hour clock); None when missing."""
    if not t:
        return None
    t = t.strip().upper()
    try:
        return datetime.datetime.strptime(t, "%I:%M%p").strftime("%H:%M")
    except ValueError:
        return t


DAY = {"M": "Mon", "T": "Tue", "W": "Wed", "R": "Thu", "F": "Fri", "S": "Sat", "U": "Sun"}


def days(pattern):
    return [DAY[c] for c in (pattern or "") if c in DAY]


def split_codes(s):
    return [x.strip() for x in (s or "").replace(";", ",").split(",") if x.strip()]


def course(c):
    groups = []
    for g in c.get("enrollGroups") or []:
        sections = []
        for s in g.get("classSections") or []:
            meetings = []
            for m in s.get("meetings") or []:
                meetings.append({
                    "days": days(m.get("pattern")), "pattern": m.get("pattern") or None,
                    "start": hhmm(m.get("timeStart")), "end": hhmm(m.get("timeEnd")),
                    "start_date": m.get("startDt") or None, "end_date": m.get("endDt") or None,
                    "location": " ".join(x for x in [m.get("bldgDescr") or "", m.get("facilityDescr") or ""] if x).strip() or None,
                    "instructors": [{"name": f"{i.get('firstName', '')} {i.get('lastName', '')}".strip(), "netid": i.get("netid")}
                                    for i in m.get("instructors") or []],
                })
            sections.append({
                "class_nbr": s.get("classNbr"), "component": s.get("ssrComponent"), "section": s.get("section"),
                "instruction_mode": s.get("instrModeDescr") or s.get("instructionMode"), "campus": s.get("campusDescr"),
                "location": s.get("locationDescr"), "open_status": s.get("openStatus"),
                "topic": s.get("topicDescription") or None, "consent": s.get("addConsentDescr") or None,
                "notes": [n.get("descrlong") for n in s.get("notes") or [] if n.get("descrlong")],
                "meetings": meetings,
            })
        groups.append({
            "credits": {"min": g.get("unitsMinimum"), "max": g.get("unitsMaximum")},
            "grading": g.get("gradingBasisLong") or g.get("gradingBasis"),
            "components_required": g.get("componentsRequired") or [],
            "components_optional": g.get("componentsOptional") or [],
            "session": g.get("sessionLong"), "session_dates": [g.get("sessionBeginDt"), g.get("sessionEndDt")],
            "cross_listed": [f"{x['subject']} {x['catalogNbr']}" for x in g.get("simpleCombinations") or []],
            "sections": sections,
        })
    attrs = [a.get("crseAttrValue") for a in c.get("crseAttrs") or [] if a.get("crseAttrValue")]
    return {
        "code": f"{c['subject']} {c['catalogNbr']}", "subject": c["subject"], "number": c["catalogNbr"],
        "title": c.get("titleLong"), "title_short": c.get("titleShort"), "crse_id": c.get("crseId"),
        "career": c.get("acadCareer"), "college": c.get("acadGroup"),
        "description": c.get("description"), "outcomes": c.get("catalogOutcomes") or [],
        "credits_text": c.get("catalogCredits") or None,
        "distributions": split_codes(c.get("catalogDistr")), "breadth": split_codes(c.get("catalogBreadth")),
        "attributes": attrs, "satisfies": c.get("catalogSatisfiesReq") or None,
        "when_offered": c.get("catalogWhenOffered") or None, "next_offered": c.get("catalogNextOffered") or None,
        "last_terms_offered": c.get("lastTermsOffered") or None,
        "prerequisites": c.get("catalogPrereqCoreq") or c.get("catalogPrereq") or None,
        "permission": c.get("catalogPermission") or None, "forbidden_overlaps": c.get("catalogForbiddenOverlaps") or None,
        "enrollment_priority": c.get("catalogEnrollmentPriority") or None, "fee": c.get("catalogFee") or None,
        "crosslisted_text": c.get("catalogCrosslistings") or None, "comments": c.get("catalogComments") or None,
        "enroll_groups": groups,
    }


def term_order(t):
    return (int(t[2:]), {"WI": 0, "SP": 1, "SU": 2, "FA": 3}.get(t[:2], 9))


def pull(term):
    subjects = get("config/subjects.json", roster=term)["subjects"]
    out = []
    for i, s in enumerate(subjects, 1):
        data = get("search/classes.json", roster=term, subject=s["value"])
        out.extend(course(c) for c in data.get("classes") or [])
        if i % 25 == 0:
            print(f"  {term}: {i}/{len(subjects)} subjects, {len(out)} classes", flush=True)
    doc = {"term": term, "pulled_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
           "source": API + "/",
           "subjects": [{"code": s["value"], "name": s.get("descrformal") or s.get("descr")} for s in subjects],
           "classes": out}
    os.makedirs(OUT, exist_ok=True)
    tmp = os.path.join(OUT, f".{term}.json.tmp")
    with open(tmp, "w") as f:
        json.dump(doc, f, separators=(",", ":"), ensure_ascii=False)
    os.replace(tmp, os.path.join(OUT, f"{term}.json"))
    return len(out), len(subjects)


def write_index(meta):
    path = os.path.join(OUT, "index.json")
    idx = {"terms": {}}
    if os.path.exists(path):
        try:
            idx = json.load(open(path))
        except Exception:
            pass
    idx.setdefault("terms", {}).update(meta)
    idx["available"] = sorted(idx["terms"], key=term_order)
    with open(path, "w") as f:
        json.dump(idx, f, indent=1, sort_keys=True)


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--terms")
    g.add_argument("--all", action="store_true")
    g.add_argument("--missing", action="store_true")
    ap.add_argument("--since", help="with --all/--missing: oldest term to pull, e.g. FA23")
    a = ap.parse_args()
    rosters = get("config/rosters.json")["rosters"]
    every = [r["slug"] for r in rosters]
    if a.terms:
        terms = [t.strip().upper() for t in a.terms.split(",")]
    elif a.all:
        terms = every
    elif a.missing:
        terms = [t for t in every if not os.path.exists(os.path.join(OUT, f"{t}.json"))]
    else:
        # Cornell's default roster, anything newer, and the one before it (late enrollment changes land there too)
        d = next((i for i, r in enumerate(rosters) if r.get("isDefaultRoster") == "Y"), len(rosters) - 1)
        terms = every[max(0, d - 1):]
    if a.since and (a.all or a.missing):
        terms = [t for t in terms if term_order(t) >= term_order(a.since.upper())]
    print("Pulling:", ", ".join(terms), flush=True)
    failed = 0
    for t in sorted(terms, key=term_order, reverse=True):  # newest first
        t0 = time.time()
        try:
            n, s = pull(t)
            write_index({t: {"classes": n, "subjects": s,
                             "pulled_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")}})
            print(f"{t}: {n} classes from {s} subjects in {time.time() - t0:.0f}s", flush=True)
        except Exception as e:
            failed += 1
            print(f"{t}: FAILED ({e})", flush=True)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
