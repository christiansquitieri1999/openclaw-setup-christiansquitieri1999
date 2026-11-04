---
name: weekly-plan
description: "Build a personalized operational project plan for one or more weeks, save an approved Google Doc, and reserve verified deep-work blocks in Google Calendar via Zapier. Use for weekly planning, remaining projects, effort allocation, and Calendar time blocking."
user-invocable: true
---

# Weekly Plan

Create a feasible plan first; write to services only after approval.
Accept an explicitly agreed multi-week window despite the skill's short name.

## Workspace context

Use these active workspace files from startup context, reading missing relevant
context only:

- `IDENTITY.md`: identify the planner using the configured assistant name.
- `SOUL.md`: friendly Italian, concrete explanations, verified facts separated
  from proposals and uncertainty.
- `USER.md`: use actual project/learning goals to explain priorities. Confirm
  timezone if ambiguous; a fixed UTC offset is not an IANA timezone.
- `AGENTS.md`: STOP -> ASK -> WAIT -> ACT; respect privacy and write boundaries.
- `TOOLS.md`: use configured Zapier routes, calendar/folder candidates and
  target-confirmation rules. Do not embed their private values in this skill.

## Inputs and feasibility

1. Collect project names, remaining work, effort, priority/order, actual
   dependencies, deadline/window, available dates/hours, and timezone.
   Do not require invented deliverables: when only time allocation is known,
   label detailed work goals as not yet specified.
2. Distinguish project ordering from technical dependency. Ask only if missing
   details affect the requested plan or an action's scope.
3. Calculate effort per project, total hours, session durations, and available
   capacity. Use explicit dates and an agreed IANA timezone for dated events.
4. If constraints conflict, show the conflict and choices, then wait. Never
   silently extend the window, shorten effort, split blocks, or add availability.
5. Draft a plan with:
   - configured planner identity and a connection to the user's goals;
   - agreed window, timezone, project order, and total effort;
   - session table: project, date, local start/end, duration, known work goal;
   - unknown deliverables and next action, explicitly labelled;
   - separate document, Calendar, and optional Telegram status.
6. Validate the agreed plan using
   `node skills/weekly-plan/scripts/check-plan.mjs <plan-json-path>` from the
   workspace. The JSON has `title`, `timezone`, `startDate`, `endDate`,
   `projects: [{name, hours}]`, and `sessions: [{project, start, end}]`.
   Timestamps require seconds and an explicit UTC offset. Use the agreed values,
   not dates inferred from project order. The checker verifies dates against
   the timezone, effort, window, chronological order, and overlaps. Use its
   canonical sessions for previews and writes; stop on validation errors.
   Before returning, remove draft mistakes or contradictory earlier tables.

## Live service preflight

Run `mcporter` from the active workspace containing `config/mcporter.json`.
An unknown server from another working directory is not proof of broken auth.

1. Discover tools with `mcporter list zapier --no-oauth --timeout 20000`.
2. Use `inspect_zapier_actions` to discover the enabled Google Docs/Calendar
   apps, actions, live parameter schemas, and dynamic choices. Do not guess
   `selected_api`, action names, parameter keys, or connection IDs.
   CLI calls use `mcporter call zapier.<tool> --args '<JSON>' --output json`.
3. Confirm exact Docs account/folder and Calendar destination from `TOOLS.md`.
   Inspect available choices when needed; do not switch accounts automatically.
4. Inspect Calendar read actions and check conflicts across the requested
   sessions, including recurring events and pagination where applicable.
   A truncated or failed search is not evidence of availability.
5. Search for the intended document and events before creating them. Compare
   title, destination, start/end, timezone, and contents; an ambiguous match
   requires clarification. Do not update or duplicate an existing object.
6. Preview the complete document content and every event's exact fields.
   Use detailed event creation with explicit offset-aware timestamps; avoid
   natural-language Quick Add parsing. Do not add attendees, recurrence,
   reminders, or scheduled Telegram alerts without separate authorization.
   State when Calendar defaults might still apply.
7. Ask for approval of the exact content, destinations, and writes. Approval
   to design or inspect is not approval to create service objects.

## Approved execution and verification

1. Create the approved Google Doc using the live action schema. Verify returned
   ID/link and retrieve content before claiming storage succeeded. If folder
   placement cannot be verified, report it as unverified and stop that claim.
2. Create only the approved, non-conflicting Calendar sessions. Include the
   verified document link in event descriptions if previewed and approved.
3. Retrieve each created event by ID; compare project, start/end, timezone,
   duration, destination, and verified link against the approved plan.
   Use the exported `checkCalendarEvent` helper in `scripts/check-plan.mjs`
   to validate read-back fields against the approved session and payload.
   Google Calendar can omit `transparency` when it has the documented default
   `opaque` (busy); do not misinterpret omission as a failed creation or resend.
   Reference: https://developers.google.com/workspace/calendar/api/v3/reference/events
4. Report the document and each session as `verified`, `failed`, `unverified`,
   or `not attempted`, with links/IDs for verified objects and the actual errors.
   Never call the whole operation successful if only part succeeded.
5. On a timeout or uncertain write, stop affected writes and ask before any
   retry or alternative method. Preserve receipts; do not delete successful
   objects as an unapproved rollback.
6. Offer to follow `../plan-digest-telegram/SKILL.md` with the agreed plan and
   verification results. This is an agent procedure handoff, not a tool call
   named after a skill. Sending requires its own content/recipient approval.

## Boundaries and acceptance

No Google Tasks, repository access, scheduler changes, or silent writes.
No secrets in messages, documents, logs, or committed files.

Check exact total hours, per-project effort, dates, local times, agreed window,
and project order. A dry run or CLI exit code alone does not verify Docs content,
folder placement, or Calendar reservations.
Do not invent a reason for the user's project order or require unspecified
deliverables as a prerequisite for reserving explicitly approved work time.
Do not claim separate study projects are components of the OpenClaw architecture.
Connect the value of planning to the user's goals without inventing project scope.
