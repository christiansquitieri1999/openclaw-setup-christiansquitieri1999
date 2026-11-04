# TOOLS.md - Local Notes

Local integration routes and destination candidates for Chris's OpenClaw setup.
Configured destinations are not authorization to write; confirm targets first.

## Zapier (via mcporter)

Server: `zapier` in `config/mcporter.json` (MCP over HTTP). Auth is OAuth with Zapier; re-run `mcporter auth zapier --no-browser` if it reports `auth required`.

Read-only health check: `mcporter list zapier --no-oauth --timeout 20000`

### Connected services

- **Google Calendar** (Zapier app 1.16.0): Connected in Zapier dashboard
  - Default calendar: micheleinfo789@gmail.com
  - Calendar timezone: Europe/Madrid. Plan in the user's confirmed Europe/Rome timezone with explicit timestamp offsets; do not change calendar settings automatically.
- **Google Docs** (Zapier app 1.11.2): Connected in Zapier dashboard
  - Default Drive folder: 1YtbGjLtpfrrzVhfJqaQaqHh3Bi4nHCMe

### Telegram

- Use the native OpenClaw Telegram channel, account `default`, bot `@giacomo_o_bot`.
- Confirm the private chat from trusted delivery context or ask the user; never infer a recipient from an allowlist.
- Use the native `message` tool, or inspect `openclaw message send --help` for the CLI route. No ClawLink installation is needed for this channel.
- Show the exact message and confirm its recipient before sending. Verify the returned message ID.
- Scheduled notifications are not authorized by a request for a one-time recap.

### Sign-off

- Assistant recaps identify Giacomo, as configured in `IDENTITY.md`.
- No signature on Chris's behalf has been specified. Ask before signing a message as Chris.

### Rules

- Before any write (create, update, send), confirm the exact target: calendar, folder, recipient.
- Use `inspect_zapier_actions` before `execute_zapier_*`.
- If the target is ambiguous, list candidates and ask. Do not guess.

## Related

- [Agent workspace](/concepts/agent-workspace)
