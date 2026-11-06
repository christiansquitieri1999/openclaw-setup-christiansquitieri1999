---
name: "4geeks-my-projects"
description: "Retrieve assigned 4Geeks projects with current status: pending, submitted, graded."
---

# 4Geeks My Projects

Recupera i progetti assegnati a Christian con il loro stato: pending / submitted / graded.

## Quando usarla
"che progetti ho?", "quali sono i miei progetti?", "a che punto sono i progetti?".

## Dipendenze (niente duplicazioni)
- **Skill foundation: `4geeks-student`** — helper condiviso (`scripts/4geeks_api.py`), token, sicurezza, endpoint. NON ripetere qui.
- Questa skill aggiunge SOLO: filtro `task_type=PROJECT`, mappatura stato, report.

## Esecuzione
```bash
python3 scripts/my_projects.py
```

## Logica
1. `GET /v1/assignment/user/me/task?task_type=PROJECT&limit=100` + paginazione `offset` fino a `count`.
2. Mappatura stato:
   - `PENDING` → **pending** (da consegnare)
   - `DONE` o `delivered_at` valorizzato → **submitted** (consegnato, in revisione)
   - `APPROVED` (o `revision_status=APPROVED`) → **graded ✅**
   - `REJECTED` (o `revision_status=REJECTED`) → **graded ❌ da sistemare**
3. Stampa: riepilogo conteggi + lista per progetto (titolo, coorte, stato, id, date, link github/live se presenti).

## Output atteso
"Progetti totali: N — X pending · Y submitted · Z graded" + lista dettagliata.

## Sicurezza
- SOLA LETTURA, sempre consentita. Mai stampare il token.
