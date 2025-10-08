# Repository Guidelines

This document is a concise contributor guide for macpymessenger. It explains how the repo is organized, how to build and test, and the conventions to follow when contributing changes.

## Project Structure & Module Organization

- Source code: `src/macpymessenger/`
  - `client.py` — public `IMessageClient` and command runner.
  - `configuration.py` — immutable `Configuration` and AppleScript resolution.
  - `templates.py` — Jinja2-backed `TemplateManager` and template models.
  - `exceptions.py` — error hierarchy (e.g., `MessageSendError`).
  - `osascript/` — packaged AppleScript (`sendMessage.scpt`).
- Tests: `tests/` (pytest-based unit tests).
- Documentation: `docs/` (Sphinx; usage, installation, modules, etc.).
- Examples/templates: `templates/` (sample text templates, loaded optionally).
- Packaging: `pyproject.toml` (Hatchling) and `uv.lock` (reproducible tooling).

## Build, Test, and Development Commands

Use Astral's uv for a fast, reproducible workflow.

- Create/refresh environment: `uv sync`
- Lint: `uv run ruff check`
- Type check: `uv run mypy`
- Run tests: `uv run pytest`
- Build sdist/wheel: `uvx --from build pyproject-build`
- Build docs (HTML): `uv run sphinx-build docs docs/_build/html`

## Coding Style & Naming Conventions

- Python ≥ 3.10 with full type hints (see `tool.mypy` in `pyproject.toml`).
- Linting via Ruff (line length 100). Keep code formatted accordingly.
- Naming: modules and functions `snake_case`, classes `CamelCase`, constants `UPPER_SNAKE_CASE`.
- Prefer dataclasses with `slots=True` where appropriate and explicit immutability where used.
- Logging: use a module logger; avoid duplicate handlers. No print statements in library code.
- Exceptions: raise types from `src/macpymessenger/exceptions.py` (e.g., `MessageSendError`, `TemplateNotFoundError`).

## Testing Guidelines

- Framework: pytest. Test files live under `tests/` and follow `test_*.py` naming.
- Do not invoke real AppleScript in tests. Use stubbed runners (see `tests/test_imessage_client.py`).
- Use temporary paths (`tmp_path`) for script files and fixtures.
- Validate error handling with `pytest.raises(...)` and assert on logged/raised behavior.

## Commit & Pull Request Guidelines

- Follow Conventional Commits:
  - `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`, `ci:` (optional scope allowed).
  - Example: `feat(client): raise MessageSendError on failures`.
- PRs should include:
  - Clear description of the change and rationale.
  - Linked issues (e.g., “Closes #123”).
  - Evidence the change passes checks: lint, type check, tests, and (if relevant) docs build.
  - Updates to `docs/` and `CHANGELOG.md` (Unreleased section) when user-visible behavior changes.

## Security & Configuration Tips

- Never commit secrets or real phone numbers. Use fixtures or environment variables locally.
- `Configuration` validates the AppleScript path; prefer defaults unless testing custom paths.
- Avoid shell=True for subprocess calls; use argument lists and validated input (see `SubprocessCommandRunner`).

## Architecture Overview

- `IMessageClient` orchestrates sending by composing:
  - `Configuration` for script discovery and validation.
  - `TemplateManager` for rendering Jinja2 templates.
  - A pluggable command runner (default uses `subprocess.run`).
- Error handling is explicit: delivery failures raise `MessageSendError` instead of returning booleans.
- Templates use Jinja2 syntax (`{{ name }}`); duplicate identifiers are rejected to prevent conflicts.

## Docs Authoring

- Sphinx + Napoleon. Add or update `.rst` pages in `docs/` and include them in `docs/index.rst`.
- Keep examples accurate to the code (e.g., `send()` raises on failure; template context is required).
- Build locally: `uv run sphinx-build docs docs/_build/html`.

## Release Process (maintainers)

- Update `CHANGELOG.md` (benefits-focused, link to relevant docs sections where helpful).
- Bump the version in `pyproject.toml` using SemVer.
- Ensure CI is green; tag the release (e.g., `v0.2.0`) and publish via the GitHub workflow.

## Agent-Specific Instructions (for AI assistants)

- Make surgical, minimal changes that align with existing style and architecture.
- When modifying public behavior, update `docs/usage.rst`, `docs/modules.rst`, and `CHANGELOG.md`.
- Prefer raising defined exceptions over introducing new ad-hoc error types.
- Keep tests fast and hermetic; stub subprocess calls instead of executing AppleScript.
- Use Jinja2 `{{ ... }}` in docs/examples; avoid `{...}` placeholders.

