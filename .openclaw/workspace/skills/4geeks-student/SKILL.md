---
name: "4geeks-student"
description: "4Geeks BreatheCode student API: profile, cohorts, tasks, delivery, certificates, activity via stored token."
---

# 4Geeks Student API (BreatheCode)

Connect to Christian's 4Geeks Academy student account through the BreatheCode API using the token stored locally.

## When to use

Use when Christian asks about his 4Geeks bootcamp: progress, projects, tasks, assignments, delivery status, cohort info, certificates, activity. The 4Geeks student platform runs on BreatheCode.

## Credentials & security (non-negotiable rules)

- The token lives in `~/.4geeks_token` (mode `0600`, owner-only).
- **NEVER** print the token, log it, echo it, write it to memory files, transcripts, notes, or commits. Never paste it in chat. Never pass it as a CLI argument.
- If the token file is missing or unreadable: ask Christian to re-create it with the secure one-liner (never ask him to paste the token in chat).
- All authenticated calls use header: `Authorization: Token <TOKEN>` — literal prefix `Token`, one space, then the value.
- Many academy-scoped endpoints also need the **`Academy: 6` header** (4Geeks Madrid). Without it they return 403 `Missing academy_id parameter`. Alternative: query param `academy=6` (numeric id only; slug causes 400).
- Base URL: `https://breathecode.herokuapp.com`
- The gateway has `logging.redactPatterns` for 40-char alphanumeric tokens as defense in depth — never rely on it; keep the token out of tool inputs/outputs entirely.
- **Read-only calls** (GET) are allowed whenever needed. **Write calls** (PUT, POST, PATCH, DELETE) require explicit per-call authorization from Christian — confirm the exact action before executing.

## Helper script

Prefer the helper script (no shell one-liners with the token):

```bash
python3 scripts/4geeks_api.py <METHOD> <path> [-q k=v ...] [-b '{"json":1}']
```

- Reads the token itself from `~/.4geeks_token`; refuses to run if permissions are not `0600`.
- Never prints the token. Prints pretty JSON; exit 0 on 2xx, 1 on non-2xx.
- `<path>` is absolute, e.g. `/v1/assignment/user/me/task`.
- Query params repeatable with `-q`; JSON body with `-b` (for PUT/POST/PATCH).
- Add the `Academy` header when the endpoint is academy-scoped (cohort lists, certificates, activity, events, registry-by-academy).
- If `python3` is unavailable, use a bare `curl` with the header built from the file, but keep the header value out of any logged command (avoid `-v`).

## Certified context (verified 2026-11-06)

- Christian Squitieri, user id `21567`, email `christiansquitieri1999@gmail.com`, github `christiansquitieri1999`.
- Academy: **4Geeks Madrid**, `academy_id = 6`, slug `madrid-spain`. Role: STUDENT.
- Cohorts seen in `/v1/admissions/user/me`:
  - id `1690` — "Advanced personal assistants with Openclaw" (slug `advanced-personal-assitants-with-openclaw`) — ACTIVE
  - id `1810` — "Working with AI coding agents" (slug `working-with-ai-coding-agents-v3`)
  - Tasks reference cohort id `1670` — "Backend development with Coding Agents" (slug `spain-backend-development-with-coding-agents`)
- Task list count: 230 total (paginate!). First task example: id `996403` "Building a Basic AI Agent in Python" (EXERCISE, PENDING).
- **Verified working (HTTP 200)**: `/v1/admissions/user/me`; `/v1/assignment/user/me/task`; `/v1/registry/technology`; `/v1/registry/asset` (with `Academy` header); `/v1/events/all` (with `Academy` header); `/v1/admissions/academy/cohort/me` (with `Academy: 6` header — returns list, currently empty for Christian; cross-check cohorts via `/me`).
- **Verified 403 (missing capability)**: `/v1/certificate/` (`read_certificate`), `/v1/activity/me` (`read_activity`). Do not retry these — report to Christian that his student role lacks those permissions.

## Endpoints (verified against STUDENT_API_CALLS_REFERENCE)

### Admissions
- `GET /v1/admissions/user/me` — current user; includes `cohorts[]` (each with `cohort{id,slug,name,academy{id,slug,name}}`, `role`, `educational_status`), `roles[]`, `permissions[]`. No academy header needed.
- `GET /v1/admissions/academy/cohort/me` — cohort enrollments. Needs `Academy` header or `academy=<id>`. May return empty array — cross-check with `/me` cohorts field.
- `GET /v1/admissions/public/syllabus` — public syllabi (no auth).

### Assignments / tasks
- `GET /v1/assignment/user/me/task` — list tasks. Useful query params: `task_status` (PENDING, DONE, APPROVED, REJECTED), `task_type` (PROJECT, EXERCISE, LESSON, QUIZ), `cohort`, `limit`, `offset`. Response: `{count, next, previous, last, results[]}` — always paginate with `offset`, use `limit=100`.
- `GET /v1/assignment/task/{task_id}` — full task detail (description, score, feedback, github_url, live_url, delivered_at, review metadata).
- `PUT /v1/assignment/task/{task_id}` — WRITE. Update submission URLs, e.g. `{"github_url": "...", "live_url": "..."}`.
- `POST /v1/assignment/task/{task_id}/deliver` — WRITE. Marks task submitted for review.

### Certificates
- `GET /v1/certificate/` — 403 for Christian's role (`read_certificate` missing).
- `GET /v1/certificate/{token}` — public, no auth; share only over secure channels.

### Activity
- `GET /v1/activity/me` — 403 for Christian's role (`read_activity` missing).
- `GET /v1/activity/cohort/{cohort_id}` — cohort activity (numeric id or slug); likely also permission-gated.

### Registry (learning content)
- `GET /v1/registry/asset` — search assets; query: `asset_type` (LESSON, EXERCISE, PROJECT), `technologies` (slug, e.g. python, react), `difficulty` (BEGINNER, EASY, INTERMEDIATE, HARD), `like` (text), `limit`. Verified 200 with `Academy` header.
- `GET /v1/registry/asset/{asset_slug}` — full asset (readme, technologies, difficulty, repository).
- `GET /v1/registry/asset/me` — assets created/modified by the user.
- `GET /v1/registry/technology` — technology catalog. Verified 200.

### Events
- `GET /v1/events/all` — optional `academy` (id), `upcoming` (bool), `limit`. Verified 200 with `Academy` header (4 events visible).

## Enumerations

- `educational_status`: ACTIVE, GRADUATED, SUSPENDED, DROPPED
- `task_status`: PENDING, DONE, APPROVED, REJECTED
- `task_type`: LESSON, EXERCISE, PROJECT, QUIZ
- Pagination: `limit` + `offset` everywhere.

## Etiquette

- Cache stable responses; avoid bursts of identical requests (rate limiting exists).
- Context filtering: data is limited to cohorts the user is enrolled in.
- When summarizing tasks in chat, group by `task_type` and `task_status`; include cohort name and dates. Do not dump raw JSON unless asked.

## Typical natural-language flows

- "che progetti ho?" → `GET /v1/assignment/user/me/task?task_type=PROJECT&limit=100` → summarize titles/status/cohort/dates.
- "com'è messo il delivery di X?" → `GET /v1/assignment/task/{id}` → report `github_url`, `live_url`, `delivered_at`, `task_status`, `revision_status`, feedback.
- "consegna il progetto X" → WRITE: confirm intent with Christian, then `POST /v1/assignment/task/{id}/deliver`.
- "aggiorna la repo del task X su <url>" → WRITE: confirm, then `PUT /v1/assignment/task/{id}` with `github_url`/`live_url`.
- "mostra certificati / attività / prossimi eventi" → certificate / activity / events endpoints (note: certificates & activity are 403 for this role; events work).
