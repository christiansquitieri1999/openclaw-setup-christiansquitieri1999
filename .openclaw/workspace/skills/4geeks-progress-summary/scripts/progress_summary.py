#!/usr/bin/env python3
"""4Geeks Progress Summary - panoramica avanzamento (skill 4geeks-progress-summary)."""
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


def is_approved(t):
    return t.get("task_status") == "APPROVED" or t.get("revision_status") == "APPROVED"


def is_pending(t):
    return t.get("task_status") == "PENDING"


def is_submitted(t):
    return t.get("task_status") == "DONE" or (t.get("delivered_at") and not is_approved(t))


def is_rejected(t):
    return t.get("task_status") == "REJECTED" or t.get("revision_status") == "REJECTED"


all_tasks = fetch_all("/v1/assignment/user/me/task", {})
print(f"📊 PROGRESSO COMPLESSIVO — {len(all_tasks)} task totali\n")

by_cohort = defaultdict(list)
for t in all_tasks:
    cn = (t.get("cohort") or {}).get("name", "?")
    by_cohort[cn].append(t)

rows = []
for cohort, tasks in by_cohort.items():
    total = len(tasks)
    appr = sum(1 for t in tasks if is_approved(t))
    pend = sum(1 for t in tasks if is_pending(t))
    sub = sum(1 for t in tasks if is_submitted(t))
    rej = sum(1 for t in tasks if is_rejected(t))
    pct = round(100 * appr / total) if total else 0
    rows.append((pct, cohort, total, appr, pend, sub, rej))

for pct, cohort, total, appr, pend, sub, rej in sorted(rows):
    print(f"{pct:3d}% | {cohort[:55]:<55} | tot {total:3d} | ✅ {appr:3d} | 🕓 {pend:3d} | 📤 {sub:3d} | ❌ {rej:2d}")

grand = len(all_tasks)
g_appr = sum(1 for t in all_tasks if is_approved(t))
g_pend = sum(1 for t in all_tasks if is_pending(t))
g_sub = sum(1 for t in all_tasks if is_submitted(t))
g_rej = sum(1 for t in all_tasks if is_rejected(t))
g_pct = round(100 * g_appr / grand) if grand else 0
print(f"\n🔢 TOTALE: {grand} task | ✅ {g_appr} completati ({g_pct}%) | 🕓 {g_pend} pending | 📤 {g_sub} consegnati | ❌ {g_rej} respinti")
print(f"\n💡 Sei al {g_pct}% — restano {g_pend + g_rej} task da gestire ({g_pend} pending + {g_rej} da sistemare).")
