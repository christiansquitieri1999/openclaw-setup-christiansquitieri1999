---
name: "4geeks-upcoming-events"
description: "List upcoming 4Geeks events (live classes, workshops) from the BreatheCode events API."
---

# 4Geeks Upcoming Events

Elenca i prossimi eventi 4Geeks (live class, workshop) a cui Christian può partecipare.

## Quando usarla
"che eventi ci sono?", "prossimi eventi 4Geeks?", "ci sono workshop in programma?", "quando è il prossimo live?"

## Prompt naturale di esempio (come richiesto dalla foto)
> "Che eventi 4Geeks ci sono in programma nelle prossime settimane?"

## Dipendenze (niente duplicazioni)
- **Skill foundation: `4geeks-student`** — helper condiviso (`scripts/4geeks_api.py`), token, sicurezza. NON ripetere qui.
- Questa skill aggiunge SOLO: filtro `upcoming`, formattazione eventi, calcolo giorni mancanti.

## Endpoint chiamato
- `GET /v1/events/all?upcoming=true&limit=N` con header `Academy: 6` (verificato: HTTP 200, 4 eventi).
- Senza header: HTTP 200 ma lista non filtrata per academy; con header: contesto corretto.

## Esecuzione
```bash
python3 scripts/upcoming_events.py [--limit N]
```

## Logica
1. Chiama `GET /v1/events/all?upcoming=true&limit=N` con header `Academy: 6`.
2. Per ogni evento: titolo, data/ora inizio (UTC → Europe/Rome), tipo, durata, link se presente.
3. Ordina per data di inizio crescente; calcola "tra X giorni" dalla data odierna.
4. Se lista vuota → "nessun evento in programma".

## Output atteso
Lista leggibile dei prossimi eventi con date locali. SOLA LETTURA, sempre consentita. Mai stampare il token.
