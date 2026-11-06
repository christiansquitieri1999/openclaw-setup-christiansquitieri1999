---
name: "4geeks-task-detail"
description: "Get full details and delivery status for a specific 4Geeks task: urls, revision, feedback, dates."
---

# 4Geeks Task Detail

Dettaglio completo di un singolo task/progetto 4Geeks: stato consegna, URL, revisione, date.

## Quando usarla
"com'è messo il delivery di X?", "dammi i dettagli del task 996403", "a che punto è il progetto Y?", "che URL ha il mio progetto?"

## Prompt naturale di esempio (come richiesto dalla foto)
> "Com'è messo il delivery di Backend Architecture Proposal? Mostrami github, live URL e stato revisione."

## Dipendenze (niente duplicazioni)
- **Skill foundation: `4geeks-student`** — helper condiviso (`scripts/4geeks_api.py`), token, sicurezza. NON ripetere qui.
- Questa skill aggiunge SOLO: chiamata a dettaglio task + report leggibile.

## Endpoint chiamato
- `GET /v1/assignment/task/{task_id}` — dettaglio completo del task (verificato: HTTP 200 senza header Academy).

## Esecuzione
```bash
python3 scripts/task_detail.py <task_id>
```

## Logica
1. Chiama `GET /v1/assignment/task/{task_id}` con l'helper condiviso.
2. Stampa report:
   - titolo, id, coorte, tipo task, stato (`task_status`), stato revisione (`revision_status`)
   - `github_url`, `live_url` (se presenti)
   - `opened_at`, `read_at`, `delivered_at`, `reviewed_at` (se presenti)
   - descrizione (troncata a ~300 char se lunga)
3. Se 404 → task non trovato; se 403 → permesso mancante.

## Output atteso
Report leggibile con stato consegna e URL. SOLA LETTURA, sempre consentita. Mai stampare il token.
