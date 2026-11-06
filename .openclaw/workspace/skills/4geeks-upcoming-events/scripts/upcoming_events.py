#!/usr/bin/env python3
"""4Geeks Upcoming Events - prossimi eventi (skill 4geeks-upcoming-events)."""
import importlib.util
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

HELPER = Path(__file__).resolve().parents[2] / "4geeks-student" / "scripts" / "4geeks_api.py"
if not HELPER.exists():
    sys.exit("ERRORE: skill '4geeks-student' non trovata (helper condivisa mancante).")
spec = importlib.util.spec_from_file_location("g4api", HELPER)
g4 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g4)

limit = 10
if len(sys.argv) > 2 and sys.argv[1] == "--limit":
    limit = int(sys.argv[2])

status, data = g4.api_call("GET", "/v1/events/all", {"upcoming": "true", "limit": str(limit)},)
if not (200 <= status < 300):
    sys.exit(f"❌ HTTP {status}: {data}")

events = data if isinstance(data, list) else data.get("results", [])
if not events:
    print("📅 Nessun evento in programma.")
    sys.exit(0)

rome = timezone(timedelta(hours=1))
now = datetime.now(rome)
print(f"📅 PROSSIMI EVENTI 4GEEKS ({len(events)})\n")
for e in sorted(events, key=lambda x: x.get("starting_at") or ""):
    start = e.get("starting_at") or ""
    try:
        dt = datetime.fromisoformat(start.replace("Z", "+00:00")).astimezone(rome)
        days = (dt - now).days
        when = f"{dt.strftime('%d/%m/%Y %H:%M')} (tra {days} gg)" if days >= 0 else dt.strftime("%d/%m/%Y %H:%M")
    except Exception:
        when = start[:16]
    etype = (e.get("event_type") or {}).get("slug", "?")
    print(f"- {e.get('title')}")
    print(f"    📅 {when} | tipo: {etype}")
    if e.get("url"):
        print(f"    🔗 {e['url']}")
    print()
