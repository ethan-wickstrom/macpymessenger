# Project map

Use this file when a task requires repository navigation, architecture context, or package ownership boundaries.

## Repository areas

- Library code lives under `src/macpymessenger/`.
- Tests live under `tests/`.
- Public Sphinx documentation lives under `docs/`.
- Example template text assets live under `templates/`; runtime templates are callable t-strings.

Use `fd` or `rg` to confirm current file names before editing.

## Capability map

- The public client facade sends messages, sends rendered templates, classifies bulk sends, and owns operational logging.
- Configuration resolves and validates the AppleScript send script before delivery.
- Template management registers callable t-string factories, renders templates, and rejects invalid interpolation values.
- Command execution is adapter-backed so tests can verify command composition without running `osascript`.
- The error model separates delivery, configuration, command, and template failures through typed exceptions.

## Composition model

```text
Caller
`-- public client facade
    |-- configuration
    |-- template rendering
    `-- command execution adapter
```

Keep behavior near the capability that owns it. Cross capability boundaries through the
public client facade, configuration object, template manager, or command runner seam.
