#!/usr/bin/env python3
"""4Geeks Task Detail - delivery status di un task (skill 4geeks-task-detail)."""
import importlib.util
import json
import sys
from pathlib import Path

HELPER = Path(__file__).resolve().parents[2] / "4geeks-student" / "scripts" / "4geeks_api.py"
if not HELPER.exists():
    sys.exit("ERRORE: skill '4geeks-student' non trovata (helper condivisa mancante).")
spec = importlib.util.spec_from_file_location("g4api", HELPER)
g4 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g4)

if len(sys.argv) < 2:
    sys.exit("Uso: python3 task_detail.py <task_id>")
tid = sys.argv[1]

status, d = g4.api_call("GET", f"/v1/assignment/task/{tid}")
if not (200 <= status < 300):
    sys.exit(f"❌ HTTP {status}: {d}")

cohort = (d.get("cohort") or {}).get("name", "?")
print(f"📋 TASK #{d.get('id')} — {d.get('title')}")
print(f"   Coorte : {cohort}")
print(f"   Tipo   : {d.get('task_type')}")
print(f"   Stato  : {d.get('task_status')} | Revisione: {d.get('revision_status')}")
if d.get("github_url"):
    print(f"   GitHub : {d['github_url']}")
if d.get("live_url"):
    print(f"   Live   : {d['live_url']}")
for label, key in [("Aperto", "opened_at"), ("Letto", "read_at"), ("Consegnato", "delivered_at"), ("Revisionato", "reviewed_at")]:
    if d.get(key):
        print(f"   {label:<10}: {str(d[key])[:16]}")
desc = (d.get("description") or "").strip()
if desc:
    trunc = desc[:300] + ("..." if len(desc) > 300 else "")
    print(f"\n   Descrizione: {trunc}")
