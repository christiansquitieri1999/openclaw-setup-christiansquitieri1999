---
name: ai-learning-log
description: "Create a personalized Italian learning log from real study notes. Use when the user asks to record learning, summarize an AI engineering or project study session, or clarify an open question about skills and agent orchestration."
user-invocable: true
---

# AI Learning Log

Turn the user's real learning into an actionable knowledge entry, not a generic
summary or an invented achievement.

## Workspace context

Use the active workspace's five configuration files from startup context. Read
only missing relevant context; do not reread files already supplied:

- `IDENTITY.md`: introduce or sign the entry using the assistant's configured name.
- `SOUL.md`: friendly, concrete Italian; distinguish facts from explanations.
- `USER.md`: connect the entry to the user's actual project and learning goals.
- `AGENTS.md`: apply STOP -> ASK -> WAIT -> ACT and privacy boundaries.
- `TOOLS.md`: consult the configured Docs route only if storage is requested.

Do not copy personal identifiers, credentials, or destination IDs into this skill.
If required configuration is missing or ambiguous, ask instead of inventing it.

## Procedure

1. Collect actual learning notes and an open question. A short note is sufficient;
   do not demand artificial bullet counts. Ask for missing facts needed to
   interpret the notes. A date is optional: omit it unless known or confirmed.
   Quote the user's short note verbatim before organizing it. Do not turn details
   from the assistant's explanation into claims that the user learned them.
2. Preserve what the user claims to have learned. Do not upgrade it to mastery
   or claim that an experiment was completed.
3. Write the entry in this order:
   - **Cosa ho imparato**: faithful, structured learning points.
   - **Per il mio percorso**: a specific connection to goals from `USER.md`.
   - **Dubbio aperto**: the user's question, without pretending it is resolved.
   - **Spiegazione di <configured assistant name>**: a grounded explanation,
     explicitly separate from the user's reported learning.
   - **Prossimo esperimento**: one small, concrete exercise; label it as proposed.
4. If the question concerns skill interaction, explain that the agent selects
   and follows skill procedures and invokes exposed tools. Skills are not
   autonomous processes or callable tools merely because they have names.
   Handoffs can pass an agreed plan or document ID between procedures in the
   conversation; scheduling requires a separately configured scheduler.
   Say explicitly that the OpenClaw agent is the orchestrator: it selects
   relevant procedures and runs their steps/tools. Do not imply that a separate
   skill orchestration engine is required. Use only these installed procedures
   as examples: `weekly-plan` and `plan-digest-telegram`; do not introduce an
   unverified integration such as Notion.
5. Present the entry in chat. Offer optional storage, but do not store it, send
   it, modify memory, or install tools merely because this skill was invoked.
6. For the orchestration question, propose this bounded experiment only:
   ask `weekly-plan` for a chat-only draft, then ask `plan-digest-telegram`
   for a chat-only recap of that draft, with no send. Explain that the agent
   carries the same dates and total hours into the second procedure.
   Do not propose another integration, skill, memory write, or subagent API.
   Do not claim that the current scheduler is configured or absent without
   verification; describe scheduling only as a separately authorized capability.

## Optional Google Docs storage

Only after the user asks to store the entry:

1. Follow the Zapier route and target-confirmation rules in `TOOLS.md`.
2. From the configured workspace, use `mcporter list zapier --no-oauth --timeout
   20000` to discover tools. Inspect enabled Google Docs actions and their live
   schemas with `inspect_zapier_actions` before execution.
3. Preview the exact entry and confirm whether to create a new document in the
   configured folder or append to an identified existing document. Do not treat
   a configured folder as permission to write.
4. Search for an existing intended entry before creating/appending. If a write
   result is uncertain, stop and ask; do not blindly repeat it.
5. Execute the approved action and retrieve the document content to verify the
   entry. Report the verified link/ID or the actual error.

## Acceptance

The output includes the user's actual learning and question, a visibly
personalized explanation, and one proposed experiment. It does not claim that
draft text has been saved or that another skill ran unless there is evidence.
Before returning, check names against workspace context; omit a repository name
if irrelevant rather than paraphrasing it inaccurately.
Avoid invented YAML fields such as `support_files` and do not present optional
headings as OpenClaw-required syntax. The installed skill's frontmatter and
resource files are the concrete example.
