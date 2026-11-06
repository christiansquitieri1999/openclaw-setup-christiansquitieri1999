#!/usr/bin/env python3
"""4Geeks Pending Work - cosa resta da completare (skill 4geeks-pending-work)."""
import importlib.util
import sys
from collections import defaultdict
from pathlib import Path

HELPER = Path(__file__).resolve().parents[2] / "4geeks-student" / "scripts" / "4geeks_api.py"
if not HELPER.exists():
    sys.exit("ERRORE: skill '4geeks-student' non trovata (helper condivisa mancante).")
spec = importlib.util.spec_from_file_location("g4api", HELPER)
g4 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g4)


def fetch_all(path, query):
    items, offset = [], 0
    while True:
        q = dict(query)
        q["limit"] = 100
        q["offset"] = offset
        status, data = g4.api_call("GET", path, q)
        if not (200 <= status < 300):
            sys.exit(f"ERRORE HTTP {status}: {data}")
        results = data.get("results", [])
        items.extend(results)
        if len(items) >= data.get("count", len(items)) or not results:
            break
        offset += 100
    return items


pending = fetch_all("/v1/assignment/user/me/task", {"task_status": "PENDING"})
print(f"🕓 RESTANO DA FARE: {len(pending)} task pending\n")

by_cohort = defaultdict(list)
for t in pending:
    cn = (t.get("cohort") or {}).get("name", "?")
    by_cohort[cn].append(t)

for cohort, tasks in sorted(by_cohort.items(), key=lambda x: -len(x[1])):
    by_type = defaultdict(list)
    for t in tasks:
        by_type[t.get("task_type", "?")].append(t)
    print(f"📚 {cohort} ({len(tasks)} pending)")
    for ttype, tt in sorted(by_type.items(), key=lambda x: -len(x[1])):
        print(f"   [{ttype}] {len(tt)}:")
        for t in sorted(tt, key=lambda x: x.get("created_at", "")):
            print(f"      - {t.get('title')} | id {t.get('id')} | creato {str(t.get('created_at', '?'))[:10]}")
    print()
