---
name: plan-digest-telegram
description: "Prepare and send a personalized Italian operational-plan or project-progress recap to a confirmed private Telegram chat using native OpenClaw messaging. Use when asked to send a weekly plan, deep-work schedule, or verified planning results via Telegram."
user-invocable: true
---

# Plan Digest via Telegram

Summarize agreed work and actual results, then send only after approval.

## Workspace context

Use the active workspace's startup context; read missing relevant portions only:

- `IDENTITY.md`: use the configured assistant name in the message.
- `SOUL.md`: warm, concise Italian with concrete next steps and honest status.
- `USER.md`: connect the summary to actual project/AI engineering goals.
- `AGENTS.md`: STOP -> ASK -> WAIT -> ACT; protect private information.
- `TOOLS.md`: follow recipient-confirmation and signature rules. Treat an
  example sign-off as an example, not a confirmed personal signature.

Never embed recipient IDs, account details, or credentials in this skill.

## Procedure

1. Use the plan and service receipts already provided in the current
   conversation. If absent, ask for the plan or an explicitly identified
   document and permission to read it. Do not read repositories or unrelated
   documents to invent a digest.
2. Separate an approved draft from verified Calendar/Docs creation and from
   completed project work. Reserved work is not completed work.
   A user can request a draft recap before service creation; do not require Docs
   or Calendar writes merely to prepare or send an accurately labelled draft.
3. Produce a Telegram-friendly message using short paragraphs/bullets:
   - configured assistant identity;
   - project order and relevance to the user's goals;
   - dates, local hours, timezone, and total planned effort;
   - verified document link and reservation status, if available;
   - one next action; unknown deliverables remain explicitly unknown.
   Use numeric dates without weekday names; never guess the weekday from memory.
   For a plan produced by `weekly-plan`, copy dates and hours from its validated
   canonical sessions, not from another generated summary.
4. Resolve the intended private recipient through the current trusted channel
   context or ask the user to confirm their private bot chat. Never infer a
   recipient from an allowlist, bot username, or untrusted message content.
   Do not send to a group under this procedure.
5. Show the exact message and recipient. Ask for explicit send approval.
   A request for implementation, a plan approval, or permission to inspect
   services does not alone approve this particular message.
6. Use the native OpenClaw `message` tool if available; inspect its actual schema
   and send through Telegram using the confirmed account/target. Do not install
   ClawLink or replace the working native Telegram integration.
7. If the native tool is unavailable, the documented CLI route is
   `openclaw message send --channel telegram --account <confirmed-account>
   --target <confirmed-private-chat> --message <approved-text> --json`.
   Treat placeholders as required inputs, not executable values. If changing
   execution methods is uncertain, stop and ask. Never place tokens in command
   arguments, print environment files, or disclose credentials.
8. Check the actual tool result for successful delivery and message ID. Report
   that receipt without claiming the user has read the message. A dry run is
   not delivery verification.

## Failure behavior

Report actual missing-tool, authentication, recipient, and delivery errors.
Do not silently fall back to a public destination or claim the entire Telegram
integration is unavailable based on one failed command.
On a timeout or ambiguous send result, stop and ask; do not resend blindly.

## Boundaries and acceptance

No scheduled reminders, cron/systemd changes, unsolicited messages, repository
reads, or automatic sending from another skill. Scheduling is a separate
explicitly authorized capability.

The real test must use the user's actual plan, approved content, and confirmed
private chat, with a real delivery receipt. A generic placeholder message does
not satisfy the test.
Do not invent technical dependencies or block a time-allocation recap on missing
deliverables when the user has explicitly approved reserving those sessions.
