# Python code guidelines

Use this file when changing `src/macpymessenger/`.

## Keep the public path small

- Target Python 3.14 or newer.
- Preserve `IMessageClient()` as the zero-configuration common path.
- Export supported user-facing names from `macpymessenger.__init__`.
- Prefer plain strings, tuples, frozen data classes, and standard library types
  over wrappers or framework-shaped abstractions.
- Add no runtime dependency unless the standard library cannot meet a proven
  requirement.
- Add no placeholder API for work that does not exist.

## Preserve ownership

- Keep the immutable delivery shape in `SendRequest`.
- Keep one-message failure mapping and logging in `MessageDelivery`.
- Keep client composition, template convenience, and bulk classification in
  `IMessageClient`.
- Keep t-string storage and rendering in `TemplateManager`.
- Keep the replaceable effect in `MessageTransport` and the production effect in
  `AppleScriptTransport`.
- Keep side-effect-free blocker checks and their result model in `diagnostics`.
- Raise named exceptions from `exceptions.py`; do not make message text or child
  exceptions part of caller contracts.

## Keep effects at the edge

- The built-in transport must invoke fixed argv `('/usr/bin/osascript', '-')`.
- Carry encoded private payload through stdin. Do not put recipients or message
  bodies in argv, environment variables, temporary files, output, logs, or
  exception causes.
- Inject `MessageTransport` in ordinary tests. A macOS integration test may
  compile rendered AppleScript but must not execute it.
- Emit logs through a named logger. Never attach application handlers, set
  levels, select formats, or create files.
- Keep diagnostics side-effect-free. A check must not open Messages, invoke
  AppleScript, trigger permission prompts, read message data, or send text.

## Use Python's template semantics

- Define template factories as callables that return Python 3.14 t-strings.
- Render to plain `str` values.
- Apply the interpolation value's normal conversion and format protocol.
- Treat only `None` as missing context; do not branch on a mapping's truth value.
- Reject duplicate and unknown identifiers with typed errors.
