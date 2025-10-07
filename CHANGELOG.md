# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

<!-- note: add changes here after each major change -->

## [0.2.0] - 2025-10-07
### Added
- A refreshed macpymessenger package with a discoverable public API (`Configuration`, `IMessageClient`, `TemplateManager`, etc.), making new integrations as simple as `from macpymessenger import ...` (see `docs/index.rst`).
- Richer template management powered by Jinja2 plus ready-to-use examples (`welcome`, `reminder`, `thank_you`), helping teams send personalised messages quickly (`docs/usage.rst`).
- Full Sphinx docs covering installation, usage, configuration, testing, and module overviews so readers can get from setup to production without guesswork (`docs/index.rst`, `docs/installation.rst`, `docs/usage.rst`).
- A maintained changelog and release automation, giving downstream consumers predictable upgrade notes.

### Changed
- `IMessageClient.send` surfaces delivery errors via `MessageSendError`, encouraging explicit error handling as demonstrated in the updated usage guide (`docs/usage.rst`).
- The README and docs now emphasise templated messaging, context dictionaries, and best practices for handling failures, reducing the time to a reliable rollout.
- Installation is standardised on `pyproject.toml` + Hatchling with `uv`-backed publishing, so wheels install faster and are easier for DevOps teams to audit (`docs/installation.rst`).

### Removed
- The legacy `i_py_messenger` package layout and verbose promotional templates were retired in favour of the streamlined examples and modern API described above.
