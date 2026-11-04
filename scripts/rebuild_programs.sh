#!/bin/sh
# Rebuild every program's requirements after editing source/majors.py (or to pick up new courses).
#   1. source/build_catalog.py -> source/catalog.js   (needs Cornell DTI's public CoursePlan data; cloned once into .cache/)
#   2. scripts/export_json.py   -> data/courses.json, data/programs/*.json
#   3. scripts/coverage_list.py -> data/programs/coverage.json
set -e
cd "$(dirname "$0")/.."
[ -d .cache/course-plan ] || git clone --depth 1 https://github.com/cornell-dti/course-plan .cache/course-plan
python3 source/build_catalog.py .cache/course-plan
python3 scripts/export_json.py
python3 scripts/coverage_list.py
