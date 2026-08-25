# AGENTS.md

macpymessenger is a Python 3.14+ library that sends text through the local macOS
Messages app with AppleScript. The package is send-only, has no runtime
dependencies, and must remain testable without macOS or Messages.

## Start here

Read [the task index](docs/agent-instructions/index.md), then load only the files
that match the work. Use [the project map](docs/agent-instructions/project-map.md)
for ownership and data flow.

## Invariants

- Keep the common path at `IMessageClient()` with the bundled send script.
- Keep public imports at the `macpymessenger` package root.
- Keep command execution injectable. Automated tests must never run `osascript`
  or send a real message.
- Keep library logging passive. Add no handler except the package `NullHandler`;
  the host application owns levels, formats, destinations, and retention.
- Keep unsupported capabilities out of the stable client. Do not add placeholder
  methods for chat history, attachments, contact lookup, remote gateways, or MCP.
- Keep examples, fixtures, logs, and commits free of real phone numbers, account
  data, and secrets.
- Update the owning guide, API page, `README.md`, `docs/llms.txt`, and
  `CHANGELOG.md` when a public contract changes.

## Commands

Run commands from the repository root:

```bash
uv sync --locked
uv run --locked ruff check
uv run --locked ruff format --check
uv run --locked ty check
uv run --locked pytest
uv run --locked sphinx-build -n -T -W --keep-going docs docs/_build/html
uv build
```

The test suite is hermetic on Linux and macOS. `macpymessenger doctor` checks an
installed user's machine; a nonzero result is expected on non-macOS systems.

## Task references

- Python code: [python-code.md](docs/agent-instructions/python-code.md)
- Tests: [testing.md](docs/agent-instructions/testing.md)
- Public docs: [documentation.md](docs/agent-instructions/documentation.md)
- Security and private data: [security.md](docs/agent-instructions/security.md)
- Git and releases: [git-release.md](docs/agent-instructions/git-release.md)
