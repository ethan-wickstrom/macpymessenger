# Project map

Use this file for repository navigation, ownership, and data flow.

## Repository areas

- `src/macpymessenger/` contains the installed library, command line, and bundled
  Agent Skill.
- `.agents/skills/macpymessenger/` contains only the repository discovery stub.
- `tests/` contains hermetic behavior tests and shared transport doubles.
- `docs/` contains the public Sphinx site, `llms.txt`, and review notes.
- `.github/workflows/` contains package, documentation, test, and release gates.
- `pyproject.toml` is the package, tool, and public metadata source of truth.

Use `fd` or `rg --files` to confirm current paths before editing.

## Core data shapes

- `SendRequest(recipient, message, delay_seconds)` is the validated frozen,
  slotted value that crosses the delivery effect boundary. It owns recipient,
  message, and delay validation.
- The CLI parses its closed JSON input directly into `SendRequest`; it does not
  define a second send-request model.
- `BulkSendFailure(recipient, reason)` retains the closed failure reason for one
  bulk item.
- `BulkSendResult(sent, failures)` is immutable. `failures` is authoritative;
  `failed` projects recipient strings, `ok` derives aggregate success, and
  iteration preserves two-value `sent, failed` unpacking.
- The JSON envelope owns `schema_version`, `tool`, `command`, `version`, `ok`,
  and one command-specific `data` or `error` object.
- `EnvironmentReport(checks)` owns aggregate blocker state. `checks` is an
  ordered tuple of immutable `EnvironmentCheck` values.
- `EnvironmentCheck(identifier, status, summary, next_step)` is the stable
  diagnostic record used by human and JSON output.
- `AgentSkill(name, description, content)` is an immutable view of one skill
  bundled with the installed package.

Do not introduce a second representation for any of these concepts.

## Capability ownership

- `IMessageClient` composes collaborators, exposes the stable send surface,
  renders registered templates, and classifies sequential bulk outcomes.
- `IMessageClient.send()` constructs one `SendRequest`; `send_request()` passes a
  prebuilt request unchanged.
- `MessageDelivery` crosses `MessageTransport`, rebuilds typed and legacy
  low-level custom-transport failures after their handlers end, and emits only
  generic delivery events.
- `MessageTransport` is the only replaceable delivery effect. Known failures use
  `MessageSendError` with a closed `delivery` or `transport` reason.
- `AppleScriptTransport` loads the bundled handler source, encodes private
  values, runs fixed `/usr/bin/osascript -` argv with script input on standard
  input, and maps child-process or operating-system failures to context-free
  public errors.
- `TemplateManager` stores callable t-string factories and renders plain strings
  through Python's normal conversion and format protocols.
- `diagnostics` performs side-effect-free local checks and owns the doctor model.
- `agent_skills` loads and verifies version-matched package skill resources.
- `__main__` owns command parsing, closed JSON object structure, the versioned
  output envelope, output routing, and exit codes. It delegates request-value
  validation to `SendRequest` and domain work to the client.
- `exceptions` contains only failures that reachable public behavior can raise.

## Data flow

```text
Python caller
`-- IMessageClient
    |-- TemplateManager (only for templated sends)
    |-- send(...) -> SendRequest
    `-- send_request(SendRequest)
        `-- MessageDelivery
            `-- MessageTransport
                `-- AppleScriptTransport (default)

Agent or shell caller
`-- macpymessenger skills get core
`-- macpymessenger doctor --json
`-- JSON stdin
    `-- macpymessenger send [--dry-run] --json
        `-- SendRequest
            |-- validation-only result (--dry-run)
            `-- IMessageClient.send_request (real send)

Doctor CLI
`-- diagnose_environment
    `-- EnvironmentReport[EnvironmentCheck, ...]
```

## State and concurrency

- Each client owns its transport, template manager, logger, and delivery object.
- `SendRequest`, `BulkSendFailure`, `BulkSendResult`, `EnvironmentCheck`,
  `EnvironmentReport`, and `AgentSkill` are immutable and may cross task
  boundaries.
- `TemplateManager` is mutable and not safe for unsynchronized concurrent
  mutation. Share it only when the host owns synchronization.
- `send_bulk()` is intentionally sequential and preserves input order.
- Each command invocation is one bounded process. Do not add shared daemon state
  for one-shot send, validation, diagnostic, or skill-read operations.

Keep behavior with its owner. Do not spread a capability across callers through
special-case coordination.
