#!/usr/bin/env python3
"""4Geeks My Projects - progetti assegnati con stato (skill 4geeks-my-projects)."""
import importlib.util
import sys
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


def stato(t):
    if t.get("task_status") == "PENDING":
        return "pending"
    if t.get("task_status") == "APPROVED" or t.get("revision_status") == "APPROVED":
        return "graded ✅"
    if t.get("task_status") == "REJECTED" or t.get("revision_status") == "REJECTED":
        return "graded ❌ (da sistemare)"
    if t.get("task_status") == "DONE" or t.get("delivered_at"):
        return "submitted"
    return str(t.get("task_status", "?"))


projs = fetch_all("/v1/assignment/user/me/task", {"task_type": "PROJECT"})
counts = {}
print(f"📦 PROGETTI TOTALE: {len(projs)}\n")
for p in projs:
    s = stato(p)
    counts[s] = counts.get(s, 0) + 1
    cohort = (p.get("cohort") or {}).get("name", "?")
    print(f"- {p.get('title')} [{s}]")
    print(f"    coorte: {cohort} | id: {p.get('id')} | creato: {str(p.get('created_at', '?'))[:10]}")
    if p.get("github_url"):
        print(f"    github: {p['github_url']}")
    if p.get("live_url"):
        print(f"    live: {p['live_url']}")
print("\n📊 RIEPILOGO:")
for k, v in counts.items():
    print(f"   {k}: {v}")
