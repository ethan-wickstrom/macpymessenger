---
name: core
description: Send text through the local macOS Messages app with the macpymessenger CLI. Use only when the user explicitly asks an agent to send an iMessage or check macpymessenger readiness.
license: Apache-2.0
compatibility: Requires macOS, Python 3.14 or newer, Messages sign-in, Automation access, and the macpymessenger CLI.
---

# macpymessenger core

Use this skill only when the user explicitly asks the agent to send a text through Messages or inspect macpymessenger readiness. Never infer a recipient, message, or permission to send from surrounding context.

## Check the Mac

Run the side-effect-free diagnostic first:

```bash
macpymessenger doctor --json
```

Read `blocked` and every check. Stop when `blocked` is `true`. A `manual` check means the CLI did not prove that Messages is signed in or that the current launcher has Automation access. Follow the reported `next_step`; do not treat a zero exit status as proof of delivery readiness.

## Send one message

Pass one JSON object through standard input. Never put the recipient or message in command arguments, shell history, environment variables, or temporary files.

```bash
cat <<'JSON' | macpymessenger send --json
{"recipient":"<recipient>","message":"<message>","delay_seconds":0}
JSON
```

The input fields are:

- `recipient`: required string containing a phone number or Messages email address supplied by the user.
- `message`: required string containing the exact text approved by the user.
- `delay_seconds`: optional non-negative integer; defaults to `0`.

No other fields are accepted.

## Read the result

The command writes one JSON object to standard output and uses stable exit codes:

- `0`: the AppleScript transport completed successfully.
- `1`: Messages rejected the send or the local transport could not run.
- `2`: the JSON input was malformed or did not match the input shape.

A successful process exit means the local transport completed; it is not a delivery receipt from the recipient's device.

Do not retry a failed or uncertain send automatically. A retry can create a duplicate message. Report the generic error code and ask the user to decide whether to retry.

## Boundaries

macpymessenger sends text only. Do not claim support for attachments, chat history, message reading, contact lookup, delivery receipts, remote sending, or account management.

Before finishing, confirm that command output contains no recipient or message text and report the exit code and generic result only.
