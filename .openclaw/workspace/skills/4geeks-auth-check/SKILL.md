---
name: "4geeks-auth-check"
description: "Verify 4Geeks student token validity and active session via BreatheCode API."
---

# 4Geeks Auth Check

Verifica che il token studente 4Geeks sia valido e che la sessione API sia attiva.

## Quando usarla
Christian chiede: "il token funziona?", "la connessione a 4Geeks è attiva?", "verifica l'accesso".

## Dipendenze (niente duplicazioni)
- **Skill foundation: `4geeks-student`** — fornisce helper condiviso (`scripts/4geeks_api.py`), gestione token (`~/.4geeks_token`, 0600) e regole di sicurezza. NON ripetere qui credenziali/regole: valgono quelle della foundation.
- Questa skill aggiunge SOLO: verifica sessione + report esito.

## Esecuzione
```bash
python3 scripts/check_auth.py
```

## Logica
1. Chiama `GET /v1/admissions/user/me` tramite la helper condivisa (sola lettura).
2. `200` → sessione attiva: stampa nome, email, user id, ruoli, numero coorti, data iscrizione.
3. `401/403` → token non valido/revocato: istruisci Christian a rigenerarlo e risalvare `~/.4geeks_token` (stessa procedura del setup iniziale).
4. Errore di rete/timeout → API irraggiungibile: NON concludere che il token sia invalido; segnala l'errore di rete.

## Output atteso
- ✅ sessione attiva (dati profilo) oppure ❌ token non valido (HTTP + motivo) oppure ⚠️ errore di rete.

## Sicurezza
- SOLA LETTURA, sempre consentita. Mai stampare il token (la helper non lo stampa mai).
