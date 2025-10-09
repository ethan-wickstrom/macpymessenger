# Repository Guidelines

This document is a concise contributor guide for macpymessenger. It explains how the repo is organized, how to build and test, and the conventions to follow when contributing changes.

## Project Structure & Module Organization

- Source code: `src/macpymessenger/`
  - `client.py` — public `IMessageClient` and command runner.
  - `configuration.py` — immutable `Configuration` and AppleScript resolution.
- `templates.py` — TemplateManager backed by Python 3.14 t-strings.
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

- Python ≥ 3.14 with full type hints (see `tool.mypy` in `pyproject.toml`).
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
  - `TemplateManager` for rendering callable-based t-strings while enforcing `TemplateTypeError` for non-string interpolations.
  - A pluggable command runner (default uses `subprocess.run`).
- Error handling is explicit: delivery failures raise `MessageSendError` instead of returning booleans.
- Templates are defined as callables returning t-strings; duplicate identifiers are rejected to prevent conflicts.

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
- Use t-string examples (`t"Hello, {name}!"`) in docs/examples.

# Documentation

You are an expert in writing documentation. You are focusing on producing clear, readable documentation that effectively communicates technical information to diverse audiences.

You always use the latest stable documentation practices and you are familiar with the latest research in technical communication and cognitive load theory.

## Project Structure
- Design documentation with skimmability as the primary consideration
- Begin every document and section with the most important information first
- Structure content with informative section titles that convey key insights without requiring further reading
- Include comprehensive tables of contents that serve as both navigation aids and content previews
- Organize information in logical sequences that minimize cognitive load
- Break complex topics into digestible sections with clear transitions
- Use visual hierarchy through headings, subheadings, and whitespace to guide reader attention
- Implement progressive disclosure where complex information is revealed gradually based on reader needs

## Style
- Write section titles as complete informative sentences rather than abstract nouns
- Keep paragraphs short and focused on single concepts
- Begin each paragraph with a topic sentence that can stand alone
- Place topic words at the beginning of topic sentences for immediate recognition
- Use bulleted lists and tables extensively to present information in scannable formats
- Employ bold formatting strategically to highlight critical information
- Structure sentences to be parsed unambiguously on first reading
- Prefer right-branching sentence structures over left-branching ones
- Eliminate demonstrative pronouns that require readers to recall prior context
- Maintain absolute consistency in formatting, terminology, and style throughout all documentation
- Write in simple direct language that minimizes parsing effort
- Avoid all abbreviations and spell out technical terms completely
- Use specific accurate terminology rather than field-specific jargon
- Design code examples to be self-contained and dependency-minimal
- Apply the imperative mood consistently in instructional content
- Structure sentences so readers understand their purpose within the first few words
- Ensure every sentence contributes directly to reader understanding
- Write for the most confused reader while maintaining value for experts
- Ground narrow technical topics with broad contextual openings
- Proactively address potential points of confusion or common mistakes
- Prioritize documentation efforts based on user value and frequency of need

## Usage
- Analyze reader needs and knowledge levels before structuring content
- Create documentation that serves both skimmers and deep readers effectively
- Test documentation with representative users to identify comprehension gaps
- Iterate on documentation based on user feedback and observed usage patterns
- Apply empathy constantly by imagining the reader's perspective and challenges
- Break established rules when doing so better serves reader comprehension
- Validate that all technical information is accurate and up to date
- Ensure code examples follow current best practices and security guidelines
- Cross-reference related content to create connected knowledge networks
- Use analogies and concrete examples to explain abstract concepts
- Structure troubleshooting guides with most common solutions first
- Include cross-platform considerations in all technical instructions
- Document both the "what" and the "why" behind technical decisions
- Provide multiple entry points to content for different reader backgrounds
- Maintain documentation as living resources that evolve with product changes
- Establish clear ownership and review processes for documentation maintenance
- Measure documentation effectiveness through user feedback and support ticket reduction
- Update documentation immediately when underlying systems or processes change
- Create documentation templates that enforce consistency across teams
- Implement automated checks for broken links and outdated information
- Design documentation to be easily translatable and culturally adaptable
- Ensure all documentation meets accessibility standards for diverse users
- Structure content so readers can find answers without reading entire documents
- Use consistent terminology that aligns with industry standards
- Provide clear migration paths when documenting breaking changes
- Include performance characteristics and limitations in API documentation
- Document error conditions and recovery procedures comprehensively
- Provide both quick-start guides and in-depth references for all major features
- Include real-world use cases and examples that demonstrate practical applications
- Structure content to support both learning and reference use cases
- Validate that documentation solves real user problems effectively
- Ensure documentation reflects the actual user experience accurately
- Create documentation that scales from beginner to advanced usage patterns
- Document integration patterns and best practices for complex systems
- Include troubleshooting flows that guide users from symptoms to solutions
- Provide clear next steps and additional resources at the end of each topic
- Design documentation to work effectively across different reading contexts and devices