# Changelog

All notable changes to macpymessenger are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

<!-- Add changes here after each significant change -->

### Changed

**File logging is now opt-in.** `IMessageClient` no longer creates `macpymessenger.log` automatically. Pass `enable_file_logging=True` to the constructor or provide a pre-configured logger to persist events.

**Template system migrated to t-strings.** The library now requires Python 3.14 and uses callable templates that return t-strings with strict string interpolation checks.

**Experimental methods are now documented.** `IMessageClient.get_chat_history` and `IMessageClient.send_with_attachment` are marked as experimental stubs. Both raise `NotImplementedError` until fully implemented.

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
