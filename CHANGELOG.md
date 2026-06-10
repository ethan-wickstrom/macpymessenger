# Changelog

All notable changes to macpymessenger are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

<!-- Add changes here after each significant change -->

## [0.3.0] - 2026-06-09

### Added

**Continuous integration workflow.** Pull requests and pushes to `main` now run linting, type checking, tests, documentation, and package builds through GitHub Actions. See `.github/workflows/ci.yml`.

### Changed

**File logging is now opt-in.** `IMessageClient` no longer creates `macpymessenger.log` automatically. Pass `file_logging=FileLoggingConfiguration()` to the constructor or provide a pre-configured logger to persist events.

**Packaging now uses uv's build backend.** The project builds with `uv_build` and uses uv-managed development tooling baselines.

**Template system migrated to t-strings.** The library now requires Python 3.14 and uses callable templates that return t-strings with strict string interpolation checks.

**Experimental methods are now documented.** `IMessageClient.get_chat_history` and `IMessageClient.send_with_attachment` are marked as experimental stubs. Both raise `NotImplementedError` until fully implemented.

### Fixed

**Template rendering honors t-string conversions and format specs.** Interpolations such as `t"{name!r}"` or `t"{name:>10}"` now apply their conversion and format spec instead of silently ignoring them. Interpolation values must still be strings.

**The bundled send script now honors `delay_seconds`.** Previously the AppleScript ignored the delay argument that `IMessageClient.send` passed to it. The script now waits the requested number of seconds before sending.

**Delivery failures now raise `MessageSendError`.** The bundled send script previously caught AppleScript errors and returned an `"Error: …"` string with a zero exit code, so Python treated every send as successful. Errors now propagate, `osascript` exits non-zero, and `IMessageClient.send` raises `MessageSendError` as documented.

### Removed

**Stale Jinja2 example templates.** The unused `templates/` directory and `.env.template` file were removed. Templates are callables that return t-strings; see `docs/usage.rst`.

**Unused `DuplicateTemplateIdentifierError` exception.** File-based template loading no longer exists, so the exception was unreachable. Use `TemplateAlreadyExistsError` for duplicate registrations.

## [0.2.0] - 2025-10-07

### Added

**Discoverable public API.** All primary classes (`Configuration`, `IMessageClient`, `TemplateManager`) are importable from the package root: `from macpymessenger import ...`. See `docs/index.rst`.

**Jinja2-powered templates.** The `TemplateManager` previously relied on Jinja2 with ready-to-use examples (`welcome`, `reminder`, `thank_you`). Historical details are retained for context.

**Complete Sphinx documentation.** Guides cover installation, usage, configuration, testing, and module overviews. See `docs/index.rst`, `docs/installation.rst`, and `docs/usage.rst`.

**Maintained changelog.** Each release includes upgrade notes for downstream consumers.

### Changed

**Explicit error handling.** `IMessageClient.send` raises `MessageSendError` on delivery failures instead of returning boolean values. See `docs/usage.rst` for error handling examples.

**Template-focused documentation.** The README and usage guide emphasize templated messaging, context dictionaries, and failure handling best practices.

**Standardized packaging.** The project uses `pyproject.toml` with Hatchling and `uv` for faster installations and easier audits. See `docs/installation.rst`.

### Removed

**Legacy package layout.** The `i_py_messenger` package name and verbose promotional templates were removed in favor of the streamlined `macpymessenger` API.
