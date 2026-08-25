# macpymessenger context

macpymessenger sends text through the local macOS Messages app. The package
combines a resolved AppleScript, optional t-string rendering, one delivery
boundary, typed failures, and read-only environment diagnostics.

## Domain terms

| Term | Meaning |
| ---- | ------- |
| Recipient | A destination accepted by Messages, either a phone number or iMessage email address. |
| Message | The text passed to Messages for delivery. |
| Send script | The AppleScript entry point invoked through `osascript`. |
| Bundled send script | The packaged script selected by `IMessageClient()` and `Configuration()`. |
| Script path | The resolved filesystem path to a bundled or custom send script. |
| Template factory | A callable that returns a Python 3.14 t-string. |
| Template identifier | The caller-supplied key for one template factory. |
| Command runner | The injectable adapter that executes prepared argv. |
| Bulk send result | The immutable `BulkSendResult(sent, failed)` classification. |
| Environment check | One immutable diagnostic with an identifier, status, summary, and optional fix. |
| Environment report | The ordered tuple of checks and derived aggregate readiness. |
| Delivery failure | A send where AppleScript or Messages returned failure. |
| Command failure | A send where the operating system could not start `osascript`. |
| Configuration failure | A missing or unreadable send script. |
| Template failure | An invalid factory, interpolation, identifier, or registration. |

Use these exact terms in code, docs, tests, and changelog entries. Do not use
`phone_number` for a value that may be an email address. Do not use `rendered
template` for a plain message string.

## Stable capabilities

- `IMessageClient()` sends one message with the bundled script.
- The client can delay one send, render and send a registered template, and send
  the same message to recipients in order.
- `BulkSendResult` exposes immutable `sent` and `failed` recipient tuples.
- `Configuration` resolves and validates bundled or custom script paths.
- `TemplateManager` stores callable t-string factories and renders plain strings.
- `CommandRunner` keeps subprocess execution replaceable and tests hermetic.
- Python logging stays application-owned; the library emits records only.
- The doctor reports local readiness without opening Messages or sending text.
- Public failures use the package exception hierarchy and structured fields.

## Stable exclusions

The package does not read messages, expose chat history, resolve contacts, send
attachments, host a remote gateway, or provide an MCP server. Do not reserve
public names for excluded work.

## State and concurrency

- Clients own their template manager, command runner, configuration, and logger.
- Template storage is mutable but not shared unless a caller explicitly shares a
  `TemplateManager`.
- Configuration, diagnostic checks, diagnostic reports, and bulk results are
  immutable values.
- Delivery uses local variables and performs sends sequentially. Do not introduce
  shared mutable coordination for bulk delivery.
