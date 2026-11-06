---
name: "4geeks-pending-work"
description: "Show what 4Geeks coursework remains to complete: pending tasks grouped by type and cohort."
---

# 4Geeks Pending Work

Mostra specificamente cosa resta da completare: tutti i task in stato PENDING, raggruppati per tipo e coorte.

## Quando usarla
"cosa mi manca?", "cosa devo ancora fare?", "quali assignment non ho completato?", "dimmi i task pending".

## Dipendenze (niente duplicazioni)
- **Skill foundation: `4geeks-student`** — helper condiviso (`scripts/4geeks_api.py`), token, sicurezza, endpoint. NON ripetere qui.
- Questa skill aggiunge SOLO: filtro `task_status=PENDING`, raggruppamento, report di priorità.

## Esecuzione
```bash
python3 scripts/pending_work.py
```

## Logica
1. `GET /v1/assignment/user/me/task?task_status=PENDING&limit=100` + paginazione `offset` fino a `count`.
2. Raggruppa per coorte e per `task_type` (LESSON, EXERCISE, PROJECT, QUIZ).
3. Stampa: per ogni coorte, il numero di task pending per tipo, poi la lista dei titoli con id e data creazione (i più vecchi prima → priorità).
4. Conteggio totale finale.

## Output atteso
"RESTANO DA FARE: N task pending" + dettaglio per coorte/tipo + lista ordinata per anzianità.

## Sicurezza
- SOLA LETTURA, sempre consentita. Mai stampare il token.
