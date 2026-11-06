#!/usr/bin/env python3
"""4Geeks Auth Check - verifica token e sessione (skill 4geeks-auth-check)."""
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

status, data = g4.api_call("GET", "/v1/admissions/user/me")
if 200 <= status < 300:
    print("✅ Sessione ATTIVA - token valido")
    print(f"   Utente : {data.get('first_name')} {data.get('last_name')} (id {data.get('id')})")
    print(f"   Email  : {data.get('email')}")
    print(f"   Ruoli  : {', '.join(r.get('role') for r in data.get('roles', []))}")
    print(f"   Coorti : {len(data.get('cohorts', []))}")
    print(f"   Iscritto dal: {str(data.get('date_joined', '?'))[:10]}")
    sys.exit(0)
elif status in (401, 403):
    print(f"❌ Token NON valido o revocato (HTTP {status}) - {data.get('detail', '')}")
    print("   → Christian deve rigenerare il token dal pannello 4Geeks e risalvare ~/.4geeks_token")
    sys.exit(1)
else:
    print(f"⚠️ Risposta inattesa HTTP {status}: {json.dumps(data)[:200]}")
    sys.exit(1)
