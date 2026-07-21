# Changelog

All notable changes to macpymessenger are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

**The library no longer manages log handlers.** Following the standard library logging contract for libraries, the package installs a `logging.NullHandler` and each module logs to `logging.getLogger(__name__)`. The client never attaches file handlers, sets levels, or chooses formats. Configure standard `logging` in your application to route events, or keep passing a `logger` to `IMessageClient`. See `docs/paradigm.md` for the design verdicts behind this and the other changes below.

**Template rendering returns plain strings.** `TemplateManager.render_template` is the single rendering API.

**`IMessageClient.send` is typed `delay_seconds: int = 0`.** The runtime validation (rejecting `bool`, non-`int`, and negative values with `InvalidDelayTypeError`/`NegativeDelayError`) is unchanged.

**Parity and property suites.** `tests/parity/` records the pre-rebuild behavior as a frozen characterization baseline plus explicitly justified divergences, and `tests/test_properties.py` verifies the foundation invariants with Hypothesis. The rebuild rationale lives in `docs/paradigm.md`, `docs/audit.md`, and `docs/foundation.md`.

### Removed

**`FileLoggingConfiguration` and the `file_logging` client parameter.** Replaced by standard `logging` configuration owned by the application. `ConfigurationError.file_logging_unavailable` is gone with it.

**Experimental stub methods.** `IMessageClient.get_chat_history` and `IMessageClient.send_with_attachment` only ever raised `NotImplementedError` and are removed.

**`RenderedTemplate` and `TemplateManager.compose_template`.** The wrapper added nothing over the rendered string.

**`InvalidCommandError` and the command pre-validation in `SubprocessCommandRunner`.** Commands are built internally and `subprocess.run` rejects invalid argument types itself.

**`TemplateTypeError.unexpected_element`.** `string.templatelib.Template` cannot be subclassed and iterating it yields only `str` and `Interpolation`, so the branch that raised it could never execute.

**Compatibility re-exports of `CommandRunner` and `SubprocessCommandRunner` from `macpymessenger.client`.** Import them from the package root or `macpymessenger.commands`.

### Earlier unreleased changes

**Message delivery extracted to a dedicated module.** All delivery behavior — delay validation, send command construction, command execution, delivery failure mapping, and send logging — now lives in `macpymessenger.delivery.MessageDelivery`. `IMessageClient.send` delegates to `MessageDelivery.deliver` so the client facade stays thin. The delivery class depends on the `CommandRunner` seam (from `macpymessenger.commands`) rather than embedding subprocess concerns in the client. Implements [#36](https://github.com/ethan-wickstrom/macpymessenger/issues/36).

**Command execution moved to a named module.** The `CommandRunner` protocol and `SubprocessCommandRunner` adapter now live in `macpymessenger.commands`. Fixes [#35](https://github.com/ethan-wickstrom/macpymessenger/issues/35).

## [0.3.0] - 2026-06-09

### Added

**Continuous integration workflow.** Pull requests and pushes to `main` now run linting, type checking, tests, documentation, and package builds through GitHub Actions. See `.github/workflows/ci.yml`.

### Changed

**File logging is now opt-in.** `IMessageClient` no longer creates `macpymessenger.log` automatically. Pass `file_logging=FileLoggingConfiguration()` to the constructor or provide a pre-configured logger to persist events.

**Packaging now uses uv's build backend.** The project builds with `uv_build` and uses uv-managed development tooling baselines.

**Template system migrated to t-strings.** The library now requires Python 3.14 and uses callable templates that return t-strings with strict string interpolation checks.

**Experimental methods are now documented.** `IMessageClient.get_chat_history` and `IMessageClient.send_with_attachment` are marked as experimental stubs. Both raise `NotImplementedError` until fully implemented.

### Fixed

**Installable artifacts.** The 0.2.0 wheel and sdist on PyPI shipped no Python modules: the Hatchling sdist `include` list was restricted to the AppleScript file, and the wheel was built from that sdist. Installing 0.2.0 produced an empty namespace package, so `from macpymessenger import Configuration` failed with `ImportError: cannot import name 'Configuration' from 'macpymessenger' (unknown location)`. Artifacts now build with `uv_build` from `src/macpymessenger`, and the publish workflow imports the public API from the built wheel in a clean environment before uploading. Fixes [#33](https://github.com/ethan-wickstrom/macpymessenger/issues/33).

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

**Template-focused documentation.** The README and usage guide center on templates, context dictionaries, and error handling.

**Standardized packaging.** The project uses `pyproject.toml` with Hatchling and `uv` for faster installations and easier audits. See `docs/installation.rst`.

### Removed

**Legacy package layout.** The `i_py_messenger` package name and the promotional example templates were removed. The package is now just `macpymessenger`.
