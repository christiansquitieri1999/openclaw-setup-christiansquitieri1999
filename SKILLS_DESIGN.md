# Skills Design

This document records the design for each skill before implementation or changes.

## Telegram Messaging (`telegram-messaging`)

### 1. What user need does the skill address, and when should it be used?

It helps users interact with Telegram through their connected bot: inspect bot and chat information, read updates, send or manage messages, handle media, and perform supported chat operations. Use it when a user asks to perform or troubleshoot a Telegram bot workflow.

### 2. What workflow should it follow, and what result should it provide?

First verify the Telegram integration and discover its live tool catalog; use that catalog as the source of truth rather than assuming a tool is available. For unfamiliar actions, inspect the tool guidance and schema. Prefer read operations to resolve ambiguity, then perform the requested operation and report the actual result or error clearly.

### 3. What safety boundaries and failure behavior are required?

Never ask the user to disclose a bot token in chat. Require explicit user confirmation before any write operation, and preview the action when supported. Do not guess chat IDs, permissions, or available tools. If the integration is missing or a call fails, explain the observed error and give the appropriate connection or permission troubleshooting steps; do not claim success without a successful tool result.
