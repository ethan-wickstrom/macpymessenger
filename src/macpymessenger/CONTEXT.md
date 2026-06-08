# macpymessenger context

macpymessenger sends macOS iMessages from Python by composing a validated send script, template rendering, and explicit command execution.

## Domain terms

| Term | Meaning |
| ---- | ------- |
| Recipient handle | The destination accepted by Messages.app, usually a phone number or iMessage email address. |
| Message body | The text content passed to Messages.app for delivery. |
| Send script | The AppleScript entry point invoked through `osascript` to send a message. |
| Bundled send script | The packaged send script used when callers do not configure a custom script path. |
| Script path | The filesystem path to the send script after configuration resolves it. |
| Template factory | A callable that returns a Python 3.14 t-string template for a message body. |
| Template identifier | The caller-supplied name used to register, update, render, or delete a template factory. |
| Rendered template | A template identifier paired with the rendered message body produced from a template factory. |
| Command runner | The adapter that executes an argument list for a command. Tests replace it to avoid real AppleScript execution. |
| Delivery failure | A failed message send caused by Messages.app or `osascript` execution. |
| Configuration failure | A setup failure that prevents reliable delivery, such as an unreadable send script or unavailable file logging. |

## Stable capabilities

- The public client facade exposes message sending, template-backed sending, template management, bulk send classification, and logging configuration.
- Configuration resolves the send script before delivery starts.
- Template management enforces t-string template factories and string-only interpolation values.
- Command execution stays replaceable so tests can verify behavior without invoking real AppleScript.
- Public failures should use the project exception hierarchy rather than ad hoc exception types.

## Naming guidance

- Prefer `recipient handle` when behavior accepts either phone numbers or iMessage email addresses.
- Prefer `message body` for user-authored send text.
- Prefer `send script` for the AppleScript entry point and `script path` for the resolved filesystem path.
- Prefer `command runner` for the execution adapter seam.
- Use `delivery failure`, `configuration failure`, and `template failure` for error categories.
