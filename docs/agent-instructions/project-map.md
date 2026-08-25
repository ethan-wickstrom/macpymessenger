# Project map

Use this file for repository navigation, ownership, and data flow.

## Repository areas

- `src/macpymessenger/` contains the installed library and diagnostic CLI.
- `tests/` contains hermetic behavior tests and shared command-runner doubles.
- `docs/` contains the public Sphinx site and `llms.txt`.
- `.github/workflows/` contains package, documentation, test, and release gates.
- `pyproject.toml` is the package, tool, and public metadata source of truth.

Use `fd` or `rg --files` to confirm current paths before editing.

## Core data shapes

- `BulkSendResult(sent, failed)` is a named tuple. Named fields are the primary
  interface; tuple unpacking preserves compatibility.
- `EnvironmentReport(checks)` owns aggregate readiness. `checks` is an ordered
  tuple of immutable `EnvironmentCheck` values.
- `EnvironmentCheck(identifier, status, summary, fix)` is the stable diagnostic
  record used by human and JSON output.
- `Configuration(send_script_path)` is an immutable resolved script path. Most
  callers never construct it because `IMessageClient()` owns the default.

Do not introduce a second representation for any of these concepts.

## Capability ownership

- `IMessageClient` composes collaborators, exposes the stable send surface,
  renders registered templates, and classifies bulk outcomes.
- `MessageDelivery` validates delay, builds one `osascript` argv sequence, runs
  it through `CommandRunner`, maps failures, and emits delivery events.
- `Configuration` resolves and checks bundled or custom script paths.
- `TemplateManager` stores callable t-string factories and renders plain strings.
- `diagnostics` performs read-only local checks and owns the doctor report model.
- `SubprocessCommandRunner` is the single production subprocess adapter.
- `exceptions` contains only failures that reachable public behavior can raise.

## Data flow

```text
Caller
`-- IMessageClient
    |-- TemplateManager (only for templated sends)
    `-- MessageDelivery
        |-- Configuration
        `-- CommandRunner

Doctor CLI
`-- diagnose_environment
    `-- EnvironmentReport[EnvironmentCheck, ...]
```

Keep behavior with its owner. Do not spread a capability across callers through
special-case coordination.
