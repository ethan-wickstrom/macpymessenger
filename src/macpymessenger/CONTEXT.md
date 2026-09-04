# macpymessenger context

macpymessenger sends text through the local macOS Messages app. The package
combines one validated immutable request, one replaceable transport, optional
t-string rendering, typed public failures, passive logging, and side-effect-free
blocker diagnostics.

## Domain terms

| Term | Meaning |
| ---- | ------- |
| Recipient | A destination accepted by Messages, either a phone number or iMessage email address. |
| Message | The text passed to Messages for delivery. |
| Send request | The validated immutable `SendRequest(recipient, message, delay_seconds)` value crossing the effect boundary. |
| Message transport | The effect owner that sends one `SendRequest` and reports known failures as `MessageSendError`. |
| AppleScript transport | The default transport that streams encoded AppleScript through stdin to fixed `/usr/bin/osascript -` argv and sanitizes low-level failures. |
| Bundled AppleScript | The packaged handler source loaded by `AppleScriptTransport`. |
| Template factory | A callable that returns a Python 3.14 t-string. |
| Template identifier | The caller-supplied key for one template factory. |
| Bulk send failure | The immutable `BulkSendFailure(recipient, reason)` record for one known failure. |
| Bulk send result | The immutable `BulkSendResult(sent, failures)` outcome with derived `failed` and `ok` views. |
| Environment check | One immutable diagnostic with an identifier, status, summary, and optional next step. |
| Environment report | The ordered tuple of checks and derived aggregate blocker state. |
| Delivery failure | A send where AppleScript or Messages returned failure. |
| Transport failure | A send where the operating system could not run the transport. |
| Installation failure | A wheel whose bundled AppleScript cannot be read. |
| Template failure | An invalid factory, missing identifier, or duplicate registration. |

Use these exact terms in code, docs, tests, and changelog entries. Do not use
`phone_number` for a value that may be an email address. Do not use `command`,
`runner`, `configuration`, or `script path` for the public delivery effect.

## Stable capabilities

- `IMessageClient()` sends one text through `AppleScriptTransport`.
- `IMessageClient.send_request()` accepts the same `SendRequest` used by the CLI
  and transports without reconstructing it.
- The client can delay one send, render and send a registered template, and send
  the same message to recipients sequentially in input order.
- `SendRequest` validates recipient, message, and delay before any delivery
  effect and contains no shared mutable state.
- `BulkSendResult` exposes immutable `sent` and detailed `failures`; `failed`
  projects recipient strings and `ok` reports whether `failures` is empty.
- `MessageTransport` keeps the effect replaceable and ordinary tests hermetic.
  Known failures use `MessageSendError` with a closed reason.
- `AppleScriptTransport` keeps recipient and message text out of process argv and
  temporary files, captures child output, and leaves low-level exceptions out of
  public `__cause__` and `__context__` fields.
- `MessageDelivery` resanitizes typed failures and maps legacy
  `CalledProcessError` or `OSError` failures from custom transports.
- `TemplateManager` stores callable t-string factories and renders plain strings
  with normal Python conversion and formatting.
- Python logging stays application-owned; the library emits records only and
  never logs message bodies or raw transport exceptions.
- The doctor reports automated blockers and manual checks without controlling
  Messages or claiming readiness.
- Public failures use the package exception hierarchy and structured fields.
- JSON command output uses one versioned envelope with `schema_version`, `tool`,
  `command`, `version`, `ok`, and either `data` or `error`.

## Stable exclusions

The package does not read messages, expose chat history, resolve contacts, send
attachments, host a remote gateway, or provide an MCP server. Do not reserve
public names for excluded work.

## State and concurrency

- Each client owns its template manager, transport, delivery object, and logger.
- Template storage is mutable but not shared unless a caller explicitly shares a
  `TemplateManager`; callers own synchronization for concurrent mutation.
- Send requests, bulk failures, bulk results, diagnostic checks, and diagnostic
  reports are immutable values.
- Delivery performs sends sequentially. Do not introduce shared mutable
  coordination for bulk delivery.
