# Changelog

All notable changes to macpymessenger are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

**Side-effect-free environment diagnostics.** `macpymessenger doctor` checks
macOS, `osascript`, Messages.app, and the bundled send script without opening
Messages or sending text. `macpymessenger doctor --json` returns stable check
identifiers, statuses, summaries, repair steps, package version, aggregate
readiness, and meaningful exit codes for scripts and agents. The same immutable
`EnvironmentCheck` and `EnvironmentReport` data model is available from
`macpymessenger.diagnostics`.

**Named bulk-send results.** `send_bulk()` now returns
`BulkSendResult(sent, failed)`. Named fields replace positional guesswork while
existing `sent, failed = result` unpacking remains valid.

**One package-root API.** Common clients, result types, command runners,
configuration, exceptions, and `__version__` are importable from
`macpymessenger`.

**Agent and search discovery.** The hosted docs now publish canonical URLs,
page descriptions, OpenSearch metadata, and `llms.txt`. Package metadata uses
specific Python, macOS, Messages, AppleScript, automation, typing, and chat
search terms. `AGENTS.md` routes coding agents through current data shapes,
ownership boundaries, invariants, and exact verification commands.

### Changed

**The common send path needs no configuration object.** `IMessageClient()` now
uses the bundled AppleScript. Pass `Configuration` only for a custom script or
explicit inspection.

**The public domain term is `recipient`.** `send()`, `send_template()`, and
`send_bulk()` now name phone numbers and Messages email addresses accurately as
`recipient` or `recipients`. Callers that used the old `phone_number=` or
`phone_numbers=` keyword must rename that keyword. Positional calls are
unchanged.

**Bulk results contain immutable tuples.** `BulkSendResult.sent` and `.failed`
are tuples, not shared mutable lists. Callers that mutate the old lists should
copy the desired field first, such as `list(result.failed)`.

**Logging follows the standard library contract.** The package installs a
`NullHandler` and emits through named loggers. macpymessenger no longer creates
files, attaches application handlers, sets levels, or chooses formats. Configure
logging in the host application:

```python
import logging

logging.basicConfig(filename="messages.log", level=logging.INFO)
```

**Delivery errors expose data.** `MessageSendError.recipient` identifies the
failed handle. `MessageSendError.reason` is `"delivery"` when AppleScript or
Messages fails and `"command"` when the operating system cannot start the
command.

**Templates render directly to strings.** `TemplateManager.render_template()` is
the complete rendering contract. `IMessageClient.send_template()` sends that
string without an intermediate wrapper.

**Message delivery has one owner.** Delay validation, argv construction, command
execution, failure mapping, and delivery logging live in
`macpymessenger.delivery.MessageDelivery`. `IMessageClient` remains the thin
public facade. Implements [#36](https://github.com/ethan-wickstrom/macpymessenger/issues/36).

**Command execution has one adapter.** `CommandRunner` and
`SubprocessCommandRunner` live in `macpymessenger.commands` and remain available
from the package root. The production adapter delegates prepared argv directly
to `subprocess.run(..., check=True, shell=False)`. Fixes
[#35](https://github.com/ethan-wickstrom/macpymessenger/issues/35).

**Documentation is task-first and requirement-first.** The README and Sphinx
site now lead from requirements to diagnostics to the first send. Focused guides
cover sending, templates, application logging, diagnostics, troubleshooting,
API reference, contribution, testing, and release work. Examples are
self-contained and use the supported package-root imports.

**Development and release checks are artifact-first.** CI uses the locked uv
environment, lint and format checks, type checks, hermetic tests, strict Sphinx
builds, package builds, and clean-wheel smoke tests on Linux and macOS. The
installed wheel must expose bundled data, the public API, the console entry
point, and valid doctor JSON before release.

### Removed

**Library-owned file logging.** `FileLoggingConfiguration` and the
`file_logging=` client parameter are removed. Applications own logging output.

**Unimplemented stable-client methods.** `get_chat_history()` and
`send_with_attachment()` are removed. Unsupported capabilities no longer occupy
public names that always raise `NotImplementedError`.

**Template wrapper machinery.** `RenderedTemplate` and
`TemplateManager.compose_template()` are removed. Rendering returns `str`.

**Redundant command validation.** `InvalidCommandError` is removed. Commands are
built inside the package and the subprocess boundary already rejects invalid
argument types.

**Finished compatibility exports.** `macpymessenger.client` no longer advertises
command-runner names. Import them from `macpymessenger` or
`macpymessenger.commands`.

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
