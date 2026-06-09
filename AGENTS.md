# Agent instructions

macpymessenger is a Python 3.14+ library for sending macOS iMessages through AppleScript with t-string templates and explicit error handling.

## Essentials

- Use `uv` for Python environment management and tool execution.
- Keep examples, fixtures, and commits free of secrets and real phone numbers.
- When public behavior changes, update `docs/usage.rst`, `docs/modules.rst`, and `CHANGELOG.md`.

## Commands

- Create or refresh the environment: `uv sync`
- Lint: `uv run ruff check`
- Type check: `uv run ty check`
- Run tests: `uv run pytest`
- Build the package: `uv build`
- Build documentation: `uv run sphinx-build docs docs/_build/html`

`pytest`, `ruff`, `ty`, and `sphinx` are development dependencies.

## Task guidance

Start with the [agent instruction index](docs/agent-instructions/index.md), then read only
the task-specific files it routes you to.

## Agent skills

### Issue tracker

Issues live in GitHub Issues for `ethan-wickstrom/macpymessenger`. See `docs/agents/issue-tracker.md`.

### Triage labels

Use the default Matt Pocock triage label vocabulary. See `docs/agents/triage-labels.md`.

### Domain docs

Use a multi-context domain documentation layout rooted at `CONTEXT-MAP.md`. See `docs/agents/domain.md`.
