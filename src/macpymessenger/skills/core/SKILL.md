---
name: core
description: Use this skill when the user explicitly asks an agent to send an iMessage through the local macOS Messages app or inspect macpymessenger readiness.
license: Apache-2.0
compatibility: Requires macOS, Python 3.14 or newer, Messages sign-in, Automation access, and the macpymessenger CLI.
---

# macpymessenger core

Use this skill only when the user explicitly asks the agent to send text through
Messages or inspect macpymessenger readiness. Never infer a recipient, message,
or permission to send from surrounding context.

## Check the Mac

Run the side-effect-free diagnostic first:

```bash
macpymessenger doctor --json
```

Require `schema_version` to be `1`, `tool` to be `"macpymessenger"`, and
`command` to be `"doctor"`. Read `data.blocked` and every item in `data.checks`.
Stop when `data.blocked` is `true`. A `manual` check means the CLI did not prove
that Messages is signed in or that the current launcher has Automation access.
Follow the reported `next_step`; do not treat `ok: true` or exit status `0` as
proof of delivery readiness.

## Build one request

Keep recipient and message text out of process arguments, environment variables,
and temporary files. Feed exactly one JSON object through standard input:

```json
{"recipient":"<recipient>","message":"<message>","delay_seconds":0}
```

The input fields are:

- `recipient`: required non-empty string containing a phone number or Messages
  email address supplied by the user.
- `message`: required non-empty string containing the exact text approved by the
  user.
- `delay_seconds`: optional non-negative integer; defaults to `0`.

No other fields or duplicate keys are accepted. Text must be valid UTF-8.

## Validate without sending

Validate the exact closed request before a real send when the workflow benefits
from a separate parse check:

```bash
cat <<'JSON' | macpymessenger send --dry-run --json
{"recipient":"<recipient>","message":"<message>","delay_seconds":0}
JSON
```

A valid result has `command: "send"`, `ok: true`, and
`data.outcome: "validated"`. Dry run does not construct a client, load the
AppleScript transport, inspect Messages sign-in, request Automation permission,
or send text. It consumes standard input, so provide the approved request again
for a real send. Do not save private request data to a temporary file or
environment variable to reuse it.

## Send one message

Send only after the user has approved the exact recipient and message:

```bash
cat <<'JSON' | macpymessenger send --json
{"recipient":"<recipient>","message":"<message>","delay_seconds":0}
JSON
```

## Read the result

The command writes one JSON object to standard output. Require these envelope
fields before reading command-specific data:

- `schema_version`: `1`.
- `tool`: `"macpymessenger"`.
- `command`: `"send"`.
- `version`: the installed package version.
- `ok`: the command outcome.

The process exit status is authoritative:

- `0`: the request validated in dry-run mode or the AppleScript transport
  completed in send mode.
- `1`: Messages rejected the send or the local transport could not run.
- `2`: the JSON input was malformed or did not match the closed request shape.

A real-send success has `data.outcome: "transport_completed"`. This means the
local transport completed; it is not a delivery receipt from the recipient's
device.

A failure includes a generic `error.code`, may include `error.reason`, and sets
`error.retryable` to `false`. Do not retry a failed or uncertain send
automatically. A retry can create a duplicate message. Report the generic result
and let the user decide whether to make another send request.

## Boundaries

macpymessenger sends text only. Do not claim support for attachments, chat
history, message reading, contact lookup, delivery receipts, remote sending, or
account management.

Before finishing, confirm that command output contains no recipient or message
text. Report the exit code and generic result only.
