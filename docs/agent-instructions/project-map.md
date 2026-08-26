# Project map

Use this file for repository navigation, ownership, and data flow.

## Repository areas

- `src/macpymessenger/` contains the installed library and diagnostic CLI.
- `tests/` contains hermetic behavior tests and shared transport doubles.
- `docs/` contains the public Sphinx site, `llms.txt`, and review notes.
- `.github/workflows/` contains package, documentation, test, and release gates.
- `pyproject.toml` is the package, tool, and public metadata source of truth.

Use `fd` or `rg --files` to confirm current paths before editing.

## Core data shapes

- `SendRequest(recipient, message, delay_seconds)` is the frozen, slotted value
  that crosses the delivery effect boundary. It owns delay validation.
- `BulkSendResult(sent, failed)` is a named tuple. Named fields are the primary
  interface; tuple unpacking preserves compatibility.
- `EnvironmentReport(checks)` owns aggregate blocker state. `checks` is an
  ordered tuple of immutable `EnvironmentCheck` values.
- `EnvironmentCheck(identifier, status, summary, next_step)` is the stable
  diagnostic record used by human and JSON output.

Do not introduce a second representation for any of these concepts.

## Capability ownership

- `IMessageClient` composes collaborators, exposes the stable send surface,
  renders registered templates, and classifies sequential bulk outcomes.
- `MessageDelivery` creates one `SendRequest`, crosses `MessageTransport`, maps
  transport-specific exceptions, and emits delivery events.
- `MessageTransport` is the only replaceable delivery effect.
- `AppleScriptTransport` loads the bundled handler source, encodes private
  values, and runs fixed `/usr/bin/osascript -` argv with script input on stdin.
- `TemplateManager` stores callable t-string factories and renders plain strings
  through Python's normal conversion and format protocols.
- `diagnostics` performs side-effect-free local checks and owns the doctor model.
- `exceptions` contains only failures that reachable public behavior can raise.

## Data flow

```text
Caller
`-- IMessageClient
    |-- TemplateManager (only for templated sends)
    `-- MessageDelivery
        `-- SendRequest
            `-- MessageTransport
                `-- AppleScriptTransport (default)

Doctor CLI
`-- diagnose_environment
    `-- EnvironmentReport[EnvironmentCheck, ...]
```

## State and concurrency

- Each client owns its transport, template manager, logger, and delivery object.
- `SendRequest`, `BulkSendResult`, `EnvironmentCheck`, and `EnvironmentReport`
  are immutable and may cross task boundaries.
- `TemplateManager` is mutable and not safe for unsynchronized concurrent
  mutation. Share it only when the host owns synchronization.
- `send_bulk()` is intentionally sequential and preserves input order.

Keep behavior with its owner. Do not spread a capability across callers through
special-case coordination.
