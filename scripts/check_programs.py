#!/usr/bin/env python3
"""
Weekly catalog watch.

For every verified program in data/catalog.js, fetch its source page, fingerprint the
requirements text, and compare against the fingerprint saved when the program was last
verified. Also pull Cornell's master program list to spot new or removed majors/minors.

Outputs
  data/catalog-watch-flags.json  {programId: {...}} for programs whose page changed (show a warning in your UI)
  data/catalog-watch.json same data plus baselines (machine-readable)
  watch-report.md         human summary (the workflow turns it into a GitHub issue)

Usage
  python scripts/check_programs.py                 # normal weekly run
  python scripts/check_programs.py --accept maj:PSYCH   # mark a program re-verified (resets its baseline)
  python scripts/check_programs.py --accept all         # re-baseline everything (e.g. after a big rebuild)

Politeness: obeys robots.txt, identifies itself, waits between requests, and never
fetches a page more than once per run.
"""
import argparse, datetime, hashlib, html, json, re, sys, time, urllib.parse, urllib.request, urllib.robotparser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
SOURCE = ROOT / "source" / "catalog.js"
STATE = DATA / "catalog-watch.json"
UA = "CornellCoursePlannerBot/1.0 (catalog change check; student project)"
MASTER_LIST = "https://catalog.cornell.edu/programs/"
DELAY = 2.0
CODE_RE = re.compile(r"\b([A-Z]{2,6})\s?(\d{4})\b")

_robots = {}
def allowed(url):
    p = urllib.parse.urlparse(url)
    base = f"{p.scheme}://{p.netloc}"
    if base not in _robots:
        rp = urllib.robotparser.RobotFileParser(base + "/robots.txt")
        try: rp.read()
        except Exception: rp = None
        _robots[base] = rp
    rp = _robots[base]
    return True if rp is None else rp.can_fetch(UA, url)

def fetch(url):
    if not allowed(url):
        return None, "blocked by robots.txt"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            body = r.read().decode("utf-8", "replace")
        time.sleep(DELAY)
        if not body.strip():
            return None, "empty response (the site may block automated reads)"
        return body, None
    except Exception as e:
        time.sleep(DELAY)
        return None, str(e)[:120]

def page_text(raw):
    raw = re.sub(r"(?is)<(script|style|nav|header|footer)[^>]*>.*?</\1>", " ", raw)
    t = html.unescape(re.sub(r"(?s)<[^>]+>", " ", raw))
    t = re.sub(r"\s+", " ", t)
    # keep the requirements part when the page is a catalog program page
    m = re.search(r"(Program Requirements|Major Requirements|Requirements for the Major|Required Courses).*", t)
    t = m.group(0) if m else t
    # drop the long university boilerplate that follows on catalog pages
    t = re.split(r"University Graduation Requirements|Requirements for All Students", t)[0]
    return t.strip()

def load_progs():
    raw = SOURCE.read_text()
    d = json.loads(raw[raw.index("=") + 1:].rstrip().rstrip(";"))
    out = []
    for p in d["progs"]:
        if p.get("origin") != "new" or not p.get("src"):
            continue
        codes = set()
        def walk(slots):
            for s in slots or []:
                f = s.get("f") or {}
                codes.update(f.get("codes", []))
                for g in f.get("any", []): codes.update(g.get("codes", []))
        for r in p.get("reqs", []):
            walk(r.get("slots"))
            for o in (r.get("opts") or {}).values(): walk(o.get("slots"))
        out.append({"id": p["id"], "name": p["name"], "kind": p["kind"], "src": p["src"].split("#")[0], "codes": codes})
    return out

def master_list():
    raw, err = fetch(MASTER_LIST)
    if not raw:
        return None, err
    names = set(re.findall(r">([^<>]{3,120}?(?:\((?:BA|BS|BFA|BAR)\)|Minor))<", raw))
    return sorted(n.strip() for n in names if "Graduate Minor" not in n), None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--accept", help="program id to re-baseline, or 'all'")
    ap.add_argument("--only", help="check just these ids (comma-separated)")
    a = ap.parse_args()
    state = json.loads(STATE.read_text()) if STATE.exists() else {"programs": {}, "master": []}
    progs = load_progs()
    if a.only:
        keep = set(a.only.split(","))
        progs = [p for p in progs if p["id"] in keep]
    today = datetime.date.today().isoformat()
    report, changed_ids, errors = [], [], []
    pages = {}
    for p in progs:
        if p["src"] not in pages:
            pages[p["src"]] = fetch(p["src"])
        raw, err = pages[p["src"]]
        st = state["programs"].setdefault(p["id"], {})
        st["src"] = p["src"]
        if not raw:
            errors.append(f"- {p['name']}: could not check ({err})")
            st["lastError"] = err
            continue
        text = page_text(raw)
        h = hashlib.sha256(text.encode()).hexdigest()[:16]
        page_codes = {f"{s} {n}" for s, n in CODE_RE.findall(text)}
        if a.accept in ("all", p["id"]) or "baseline" not in st:
            st.update(baseline=h, baselineCodes=sorted(page_codes), changed=False, since=None, added=[], removed=[])
            continue
        st["checked"] = today
        if h != st["baseline"]:
            added = sorted(page_codes - set(st.get("baselineCodes", [])))
            removed = sorted(set(st.get("baselineCodes", [])) - page_codes)
            if not st.get("changed"):
                st["since"] = today
            st.update(changed=True, added=added, removed=removed,
                      missingFromPlanner=sorted(c for c in page_codes - p["codes"] if c in added))
            changed_ids.append(p["id"])
            report.append(f"### {p['name']} (`{p['id']}`)\n{p['src']}\n"
                          + (f"- Course codes now on the page: {', '.join(added)}\n" if added else "")
                          + (f"- Course codes no longer on the page: {', '.join(removed)}\n" if removed else "")
                          + ("- Wording changed; no course-code changes.\n" if not added and not removed else ""))
        else:
            st.update(changed=False)

    # new / removed programs on Cornell's master list
    master, merr = master_list()
    master_notes = []
    if master:
        prev = set(state.get("master", []))
        if prev:
            new, gone = sorted(set(master) - prev), sorted(prev - set(master))
            if new: master_notes.append("New on Cornell's program list: " + "; ".join(new))
            if gone: master_notes.append("No longer on Cornell's program list: " + "; ".join(gone))
        state["master"] = master
    elif merr:
        errors.append(f"- Master program list: could not check ({merr})")

    state["lastRun"] = today
    STATE.write_text(json.dumps(state, indent=1, sort_keys=True))
    public = {k: {x: v.get(x) for x in ("changed", "since", "src", "added", "removed")} for k, v in state["programs"].items() if v.get("changed")}
    (DATA / "catalog-watch-flags.json").write_text(json.dumps(public, indent=1, sort_keys=True))

    lines = [f"# Catalog check, {today}", ""]
    lines += [f"**{len(changed_ids)} program(s) changed since last verified.**", ""] + report if changed_ids else ["No requirement pages changed.", ""]
    if master_notes: lines += ["## Program list", ""] + [f"- {n}" for n in master_notes] + [""]
    if errors: lines += ["## Could not check", ""] + errors + [""]
    lines += ["After updating a program in `source/majors.py`, run `python scripts/check_programs.py --accept <id>` so it stops being flagged."]
    (ROOT / "watch-report.md").write_text("\n".join(lines))
    (ROOT / "watch-changed.txt").write_text("\n".join(changed_ids))
    print("\n".join(lines))
    return 0

if __name__ == "__main__":
    sys.exit(main())
