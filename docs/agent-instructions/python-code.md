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

- Keep script-path resolution in `Configuration`.
- Keep one-message delivery in `MessageDelivery`.
- Keep client composition, template convenience, and bulk classification in
  `IMessageClient`.
- Keep t-string storage and rendering in `TemplateManager`.
- Keep subprocess execution in `SubprocessCommandRunner`.
- Keep local readiness checks and their result model in `diagnostics`.
- Raise named exceptions from `exceptions.py`; do not add ad hoc error strings as
  caller contracts.

## Keep effects at the edge

- Build subprocess argv as a sequence. Never use a shell or interpolate command
  strings.
- Inject command execution in tests. Never run real AppleScript in automated
  checks.
- Emit logs through a named logger. Never attach application handlers, set
  levels, select formats, or create files.
- Keep diagnostics read-only. A check must not open Messages, trigger permission
  prompts, or send text.

## Keep templates strict

- Define template factories as callables that return Python 3.14 t-strings.
- Render to plain `str` values.
- Require each interpolated result to be a string.
- Reject duplicate identifiers and unknown identifiers with typed errors.
