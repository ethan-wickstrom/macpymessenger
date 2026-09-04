# Contributing to macpymessenger

A useful contribution changes one public behavior or one authoritative data
shape, proves the change with hermetic tests, and updates the documentation that
owns the contract.

## Set up

You need [uv](https://docs.astral.sh/uv/) and Python 3.14 or newer:

```bash
git clone https://github.com/ethan-wickstrom/macpymessenger.git
cd macpymessenger
uv sync --locked
uv run --locked pytest
```

The ordinary suite does not need a Messages account, Automation permission, or
a Mac. Tests inject `MessageTransport` doubles. A macOS-only test compiles the
rendered AppleScript but never executes it.

Read [AGENTS.md](AGENTS.md) before agent-assisted work and use the
[project map](docs/agent-instructions/project-map.md) before changing data shapes
or ownership.

## Make one coherent change

1. Define the public behavior or data shape first.
2. Add a failing behavior or edge-case test when behavior changes.
3. Implement the smallest change at the layer that owns the behavior.
4. Keep effects behind `MessageTransport`; never perform a real send in an
   automated test.
5. Update the owning guide, API page, README, `docs/llms.txt`, bundled Agent
   Skill, and changelog when their contract changes.
6. Commit one coherent abstraction or correction at a time with Conventional
   Commit messages.

Do not create a second representation for `SendRequest`, bulk outcomes,
diagnostic checks, Agent Skills, or the JSON command envelope. Do not add
placeholder methods for excluded capabilities.

## Protect private data

Use invented recipients and messages in tests and examples. Keep real phone
numbers, email addresses, message bodies, account details, private paths, raw
child output, and secrets out of process arguments, environment variables,
temporary files, logs, tracebacks, fixtures, issues, pull requests, and commits.

## Verify

Run the complete local gate from the repository root:

```bash
uv sync --locked
uv run --locked ruff check
uv run --locked ruff format --diff
uv run --locked ty check
uv run --locked pytest
uv run --locked sphinx-build -n -T -W --keep-going docs docs/_build/html
uv build
```

CI runs the same checks on Linux and macOS, then installs and verifies both the
wheel and source distribution. A change is not complete when only source-tree
tests pass.

## Report a problem

Open a GitHub issue with the expected result, actual result, smallest reproducer,
and sanitized `uv run macpymessenger doctor --json` output. Remove private data
before posting logs or tracebacks.

[Read the full contribution guide](https://macpymessenger.readthedocs.io/en/latest/development/contributing.html)
explains repository conventions, testing, and release gates.
