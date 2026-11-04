# Skill Design Explained

Discussion guide: **why this task, why this input, why this output format**.
Use it to prepare your own explanation, not as a substitute for understanding.

## 1. AI Learning Log

Implementation: [ai-learning-log](./.openclaw/workspace/skills/ai-learning-log/SKILL.md).

- **Why this task?** Turn recurring study notes into reusable knowledge for my
  AI engineering journey, rather than collecting unstructured summaries.
- **Why this input?** Real learning notes and an unresolved question keep the
  entry grounded. My test covered building skills and understanding orchestration.
- **Why this output?** Five sections separate reported learning, relevance to
  my goals, the open question, Giacomo's explanation, and a proposed experiment.
  This avoids presenting the assistant's explanation as something I already knew.
- **Boundary:** Output stays in chat; optional Docs storage needs approval.

**Short explanation:** "This skill turns my actual learning into a structured
entry, separates knowledge from uncertainty, and suggests a practical next step."

## 2. Weekly Plan

Implementation: [weekly-plan](./.openclaw/workspace/skills/weekly-plan/SKILL.md).

- **Why this task?** Make remaining backend, database, and RAG work feasible
  within my available time instead of maintaining a list of intentions.
- **Why this input?** Projects, effort, order, availability, planning window,
  and timezone prevent invented dates or an overloaded schedule.
- **Real case:** Four hours per project; Tuesday/Thursday sessions, 18:00-20:00,
  Europe/Rome. Backend: November 24/26; database: December 1/3;
  RAG: December 8/10, 2026. We explicitly extended the window to fit all work.
- **Why this output?** Docs preserves the operational plan; Calendar reserves
  actual work time. Verification reports distinguish success from partial failure.
- **Boundary:** Project order is not proof of a technical dependency.
  Reserved hours do not prove completed work. No Google Tasks or scheduled alerts.
- **Evidence:** Document read-back and six verified events: 12 hours total,
  four per project. A deterministic checker validates planning constraints.

**Short explanation:** "I use real effort and availability to build a feasible
plan. Docs explains it, Calendar reserves time, and read-back verifies the result."

## 3. Plan Digest via Telegram

Implementation: [plan-digest-telegram](./.openclaw/workspace/skills/plan-digest-telegram/SKILL.md).

- **Why this task?** Make the agreed plan easy to consult in my private bot chat.
- **Why this input?** The agreed plan and verified receipts prevent invented
  progress or links. The exact message and private recipient need confirmation.
- **Why this output?** Short bullets show project order, dates, local hours,
  workload, document link, reservation status, and one next action.
- **Boundary:** Native OpenClaw Telegram, no repository reads or ClawLink setup.
  No automatic sending, scheduled reminders, or claims that the recipient read it.
- **Evidence:** Successful real delivery receipt, message ID `67`, not a dry run.

**Short explanation:** "This skill communicates verified planning results
concisely through Telegram, after I approve the content and recipient."

## How the Five Configuration Files Affect Behavior

| File | Observable effect |
| --- | --- |
| [IDENTITY.md](./.openclaw/workspace/IDENTITY.md) | Assistant identifies as Giacomo. |
| [SOUL.md](./.openclaw/workspace/SOUL.md) | Friendly Italian, concrete explanations, explicit uncertainty. |
| [USER.md](./.openclaw/workspace/USER.md) | AI engineering/4Geeks goals and confirmed timezone guide personalization. |
| [AGENTS.md](./.openclaw/workspace/AGENTS.md) | STOP -> ASK -> WAIT -> ACT before ambiguous or unauthorized actions. |
| [TOOLS.md](./.openclaw/workspace/TOOLS.md) | Configured integration routes and destination-confirmation rules. |

The skills use active configuration without embedding credentials.
This explanation is English; the configured agent's user-facing language is Italian.

## Orchestration and Separation

**The OpenClaw agent orchestrates the skills.** Skills describe procedures;
they are not autonomous processes or tools callable simply by name.
The agent can follow `weekly-plan`, then use its agreed data and receipts
to follow `plan-digest-telegram`. The handoff does not authorize sending.
Scheduling would require a separately authorized mechanism.

Three separate skills support independent learning, planning, and communication.
Each has clear inputs, outputs, safety boundaries, and reusable instructions.
Seven focused automated tests pass; real-input agent tests also exposed
text inaccuracies, which prompted stronger instructions and deterministic checks.

## Delivery Facts and Practice

- [SKILLS_DESIGN.md](./SKILLS_DESIGN.md) was committed before implementation.
- Docs, Calendar, and Telegram outputs were verified using real personal inputs.
- Existing connections were reused; Zapier was re-authenticated during earlier
  repair, not newly connected for these skills.
- Practice explaining: why six sessions, why Docs plus Calendar, who orchestrates,
  when approval is required, and why reserved time is not completed work.
