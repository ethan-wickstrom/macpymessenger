# AGENTS.md

macpymessenger is a Python 3.14+ library and command-line tool that sends text
through the local macOS Messages app. The package is send-only, has no runtime
dependencies, and must remain testable without a Messages account or permission
to control Messages.

## Start here

Read [the task index](docs/agent-instructions/index.md), then load only the files
that match the work. Use [the project map](docs/agent-instructions/project-map.md)
for data shapes, ownership, and effect flow.

For product use rather than repository work, load the version-matched installed
workflow:

```bash
macpymessenger skills get core
```

## Invariants

- Keep the common Python path at `IMessageClient()` with
  `AppleScriptTransport`.
- Keep public imports at the `macpymessenger` package root.
- Keep one immutable value at the effect boundary:
  `SendRequest(recipient, message, delay_seconds)`.
- Keep delivery replaceable through `MessageTransport`. Automated tests inject a
  transport and never send a real message.
- Keep the agent send path non-interactive: one closed JSON object on standard
  input, structured output on standard output, diagnostics on standard error,
  and stable exit codes.
- Reject malformed JSON, unknown fields, duplicate keys, empty required values,
  invalid delays, and non-UTF-8 text before creating the client.
- Keep private recipient and message values out of process arguments, environment
  variables, temporary files, child output, exception causes, logs, examples,
  issues, and commits. Built-in delivery logs contain generic outcomes only.
- Keep library logging passive. Add no handler except the package `NullHandler`;
  the host application owns levels, formats, destinations, and retention.
- Keep the repository Agent Skill as a discovery stub. Serve the full workflow
  from the installed package so the skill and command contract share a version.
- Keep unsupported capabilities out of the stable client. Do not add placeholder
  methods for chat history, attachments, contact lookup, remote gateways, or
  account management.
- Treat `doctor.blocked == false` as “no automated blocker found,” not “delivery
  proven.” Preserve every manual check.
- Never retry a failed or uncertain send automatically; the package has no
  delivery receipt or idempotency key.
- Update the owning guide, API page, `README.md`, `docs/llms.txt`, bundled skill,
  and `CHANGELOG.md` when a public contract changes.

## Commands

Run commands from the repository root:

```bash
uv sync --locked
uv run --locked ruff check
uv run --locked ruff format --diff
uv run --locked ty check
uv run --locked pytest
uv run --locked sphinx-build -n -T -W --keep-going docs docs/_build/html
uv build
```

The ordinary suite is hermetic on Linux and macOS. The macOS job also compiles a
rendered AppleScript with `osacompile` but does not execute it. The doctor checks
an installed user's machine; a nonzero result is expected when a definite local
blocker exists.

## Task references

- Python code: [python-code.md](docs/agent-instructions/python-code.md)
- Tests: [testing.md](docs/agent-instructions/testing.md)
- Public docs: [documentation.md](docs/agent-instructions/documentation.md)
- Security and private data: [security.md](docs/agent-instructions/security.md)
- Git and releases: [git-release.md](docs/agent-instructions/git-release.md)
