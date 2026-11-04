# Skills Design

Design approved before implementation. Scope: two custom OpenClaw skills and one
custom skill with native Telegram delivery. Existing third-party skills are not
modified. No repository digest, Google Tasks, or scheduled notifications.

## Shared configuration and orchestration

Each skill uses the active workspace configuration, without embedding personal
identifiers or credentials:

| File | Observable effect |
| --- | --- |
| `IDENTITY.md` | Use the configured assistant identity in the output. |
| `SOUL.md` | Friendly Italian, concrete explanations, verified facts distinguished from assumptions. |
| `USER.md` | Connect learning and planning to the user's actual AI engineering/project goals; resolve ambiguous timezone settings explicitly. |
| `AGENTS.md` | STOP -> ASK -> WAIT -> ACT; no speculative actions or disclosures. |
| `TOOLS.md` | Use configured service routes and confirmed destinations, not hardcoded accounts or guessed tools. |

The OpenClaw agent orchestrates these procedures. Skills are not autonomous
processes and do not call one another as tools. A user can run each independently.
The planning skill can offer the Telegram digest procedure after producing a plan,
but sending still requires approval of the message and recipient.

## 1. AI Learning Log (`ai-learning-log`)

### What user need does it address, and when is it used?

Turn real learning notes into a useful knowledge entry for the user's AI
engineering journey. Trigger on requests to record learning, summarize a study
session, or clarify a remaining learning question.

### What workflow and output are required?

Read applicable workspace context, separate what the user actually learned from
explanations supplied by the assistant, then produce an Italian entry with:
learning points, application to current goals, an open question, a clearly
labelled explanation, and a small next experiment. Explain skill orchestration
when that is the user's actual question. Present in chat; optional Google Docs
storage requires its own content and destination approval.

### What are the boundaries and acceptance criteria?

Do not invent achievements, dates, or personal context. No automatic storage or
external writes. Test with the user's real learning about building skills and
uncertainty about orchestration. The output must distinguish the agent's
orchestration role from skill instructions and show the five-file personalization.

## 2. Weekly Plan (`weekly-plan`)

### What user need does it address, and when is it used?

Translate remaining project work into a feasible operational plan, recorded in
Google Docs, with real deep-work time blocks in Google Calendar. Support a
single week or an explicitly agreed multi-week window.

### What workflow and output are required?

Collect goals, effort, order/dependencies, exact availability, planning window,
and an explicit timezone. Calculate total effort and flag inconsistent constraints
before proceeding. Preview a document and dated sessions; inspect the live Zapier
schemas, verify destinations and Calendar availability, then request approval.
Create the Google Doc and detailed Calendar events only within that approval.
Read back the document and events and report IDs/links, duration totals, and any
partial failures. Offer, but do not automatically send, a Telegram digest.

### What are the boundaries and acceptance criteria?

No invented deadlines, work slots, deliverables, attendees, default timezone, or
reminders. A project sequence is not proof of a technical dependency. Do not
overwrite existing documents or events. Search for duplicates and overlaps before
writes; stop on uncertain write results rather than retrying blindly. No Google
Tasks or scheduler changes.

Real test: three projects at four hours each, ordered backend, database, RAG.
Six two-hour sessions on the agreed Tuesdays/Thursdays across three weeks,
18:00-20:00 in Europe/Rome. Verify 12 hours, correct dates/timezone, and actual
Google Docs and Calendar output after approval.

## 3. Plan Digest via Telegram (`plan-digest-telegram`)

### What user need does it address, and when is it used?

Give the user an actionable private Telegram summary of an approved operational
plan or its execution status. Trigger on requests to send a plan, recap, or
project progress notification via Telegram.

### What workflow and output are required?

Consume the agreed plan and verified service results from the current conversation,
or read an explicitly identified document. Produce a concise Italian recap with
project order, dates, workload, next action, and verified links when available.
Use the configured assistant identity and goals, and the native OpenClaw Telegram
message tool. Preview the exact message and confirm the private recipient before
sending. Report the actual send result/message ID.

### What are the boundaries and acceptance criteria?

No repository reads, ClawLink installation, unsolicited delivery, scheduled
alerts, secrets, or invented completion claims. Do not send to a group or infer
the recipient from the sender allowlist. Send only the approved content to the
confirmed private chat. A timeout is not proof of failure; do not resend without
clarification. Test with the user's real project plan and verify a Telegram
delivery result, not only a dry run.

## Implementation and verification

- Place each skill in the OpenClaw workspace at `skills/<name>/SKILL.md` with
  matching YAML name and a useful trigger description.
- Keep the five configuration files authoritative and preserve existing edits.
- Verify all three appear as ready, model-visible OpenClaw skills.
- Exercise every skill with real user input, checking exact output requirements.
- Verify at least one external service result; the agreed end-to-end goal includes
  the plan document, six Calendar blocks, and Telegram delivery.
- Keep private test payloads and service receipts out of committed skill files.
- Commit this design before creating skill implementations.

## Delivery verification

- This three-skill design was committed as `9f49741` before implementation.
- All three skills were discovered as ready, model-visible workspace skills.
- Real-input agent tests used the user's learning question and approved project
  time allocation, not placeholder prompts.
- The operational Google Doc was read back and matched the approved content;
  its destination folder was verified.
- Six unique Calendar events were read back: 12 hours total, four per project,
  with approved dates, private visibility, and no reminders.
- The approved private Telegram recap returned a successful non-dry-run
  delivery receipt. Private payloads and receipts are not committed here.
- Seven focused tests pass:
  `node --test .openclaw/workspace/skills/weekly-plan/scripts/check-plan.test.mjs`
  from the main repository root.
- Two consecutive serial `openclaw doctor --non-interactive` runs completed
  without health errors after an earlier three-second health probe timeout.
  The gateway also passed its separate connectivity probe. The transient
  timeout's root cause was not established; no gateway patch was applied.
  Load the configured environment in the same shell before running doctor,
  and do not publish the environment file or its values.
- Delivery tracks the five configuration files and three skills as ordinary
  files under `.openclaw/workspace/`, replacing the previous gitlink. The local
  nested Git metadata is preserved but is not part of the delivery.
- No new external API or OAuth connection was added for these skills. The
  existing Zapier connection had been re-authenticated during earlier repair.
- Delivery commits are local until publication is explicitly approved.
