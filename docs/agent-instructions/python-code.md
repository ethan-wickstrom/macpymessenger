# Python code guidelines

Use this file when changing `src/macpymessenger/`.

## Keep the public path small

- Target Python 3.14 or newer.
- Preserve `IMessageClient()` as the zero-configuration Python path.
- Preserve `macpymessenger send` as the one-shot agent and shell path.
- Export supported user-facing names from `macpymessenger.__init__`.
- Prefer plain strings, tuples, frozen data classes, and standard library types
  over wrappers or framework-shaped abstractions.
- Add no runtime dependency unless the standard library cannot meet a proven
  requirement.
- Add no placeholder API for work that does not exist.

## Preserve ownership

- Keep the immutable delivery shape in `SendRequest`.
- Parse CLI JSON directly into `SendRequest`; do not add a CLI-only request
  class.
- Keep one-message failure mapping and logging in `MessageDelivery`.
- Keep client composition, template convenience, and bulk classification in
  `IMessageClient`.
- Keep t-string storage and rendering in `TemplateManager`.
- Keep the replaceable effect in `MessageTransport` and the production effect in
  `AppleScriptTransport`.
- Keep side-effect-free blocker checks and their result model in `diagnostics`.
- Keep command parsing, stream routing, and exit codes in `__main__`.
- Keep bundled skill discovery and validation in `agent_skills`.
- Raise named exceptions from `exceptions.py`; do not make message text or child
  exceptions part of caller contracts.

## Keep effects at the edge

- The built-in transport must invoke fixed argv `('/usr/bin/osascript', '-')`.
- Carry encoded private payload through standard input. Do not put recipients or
  message bodies in argv, environment variables, temporary files, output, logs,
  or exception causes.
- Validate untrusted command input before creating `IMessageClient`.
- Inject `MessageTransport` in ordinary tests. A macOS integration test may
  compile rendered AppleScript but must not execute it.
- Emit logs through a named logger. Never attach application handlers, set
  levels, select formats, or create files.
- Keep diagnostics side-effect-free. A check must not open Messages, invoke
  AppleScript, trigger permission prompts, read message data, or send text.

## Keep the command Unix-shaped

- Read private request data from standard input, not command arguments.
- Write machine-readable results to standard output and human diagnostics to
  standard error.
- Keep commands non-interactive and document them through `--help`.
- Keep stable, meaningful exit codes.
- Keep each invocation bounded. Do not add a daemon or shared process state for
  one-shot work.
- Do not retry sends automatically.

## Use Python's template semantics

- Define template factories as callables that return Python 3.14 t-strings.
- Render to plain `str` values.
- Apply the interpolation value's normal conversion and format protocol.
- Treat only `None` as missing context; do not branch on a mapping's truth value.
- Reject duplicate and unknown identifiers with typed errors.
