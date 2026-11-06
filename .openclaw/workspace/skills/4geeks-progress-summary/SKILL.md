---
name: "4geeks-progress-summary"
description: "Give an overview of 4Geeks course progress: completed vs pending per cohort and overall completion."
---

# 4Geeks Progress Summary

Panoramica di quanto Christian è avanti nel corso: completati vs pendenti per coorte e percentuale complessiva.

## Quando usarla
"come sono messo?", "quanto sono avanti?", "qual è il mio progresso?", "summary del corso".

## Dipendenze (niente duplicazioni)
- **Skill foundation: `4geeks-student`** — helper condiviso (`scripts/4geeks_api.py`), token, sicurezza, endpoint. NON ripetere qui.
- Questa skill aggiunge SOLO: aggregazione complessiva, percentuali, report per coorte.

## Esecuzione
```bash
python3 scripts/progress_summary.py
```

## Logica
1. `GET /v1/assignment/user/me/task?limit=100` + paginazione completa (TUTTI i task, non solo un tipo).
2. Aggrega per coorte:
   - totale task, completati (`APPROVED` o `revision_status=APPROVED`), pending (`PENDING`), consegnati (`DONE`/`delivered_at`), respinti (`REJECTED`).
   - % completamento = APPROVED / totale.
3. Percentuale complessiva (tutte le coorti).
4. Stampa: summary per coorte (ordinata per % crescente → le più indietro prima) + totale generale + insight testuale (es. "Sei al 62% — restano N task: M pending + K da sistemare").

## Output atteso
Overview numerica chiara, pronta da riportare in chat.

## Sicurezza
- SOLA LETTURA, sempre consentita. Mai stampare il token.
