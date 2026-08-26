# Changelog

All notable changes to macpymessenger are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

**One immutable delivery request.** `SendRequest(recipient, message,
delay_seconds)` is the frozen, slotted value that crosses the delivery effect
boundary. It rejects booleans, non-integer delays, and negative delays before an
effect runs.

**One replaceable delivery effect.** `MessageTransport.send(request)` is the
public extension and test seam. `AppleScriptTransport` is the production default.
Tests can record requests without reproducing client coordination, templates,
bulk classification, logging, or error mapping.

**Private-data-safe AppleScript transport.** The built-in transport invokes fixed
argv `('/usr/bin/osascript', '-')`, base64-encodes recipient and message text into
the rendered script, and streams that script through stdin. Private values no
longer enter process arguments or temporary files. Child output remains inside
the transport.

**Side-effect-free environment diagnostics.** `macpymessenger doctor` checks
macOS, `/usr/bin/osascript`, Messages.app, and bundled AppleScript source without
opening Messages, invoking AppleScript, requesting Automation access, reading
message data, or sending text. JSON output exposes `blocked`, stable
`identifier`, `status`, `summary`, and `next_step` fields. Unverifiable account
and permission state is `manual`, not success.

**Named bulk-send results.** `send_bulk()` returns immutable
`BulkSendResult(sent, failed)` tuples. Named fields replace positional guesswork;
`sent, failed = result` unpacking remains valid.

**Agent and search discovery.** The hosted docs publish canonical URLs, page
metadata, OpenSearch metadata, Python 3.14 intersphinx links, and a curated
`llms.txt`. `AGENTS.md` routes agents through current data shapes, ownership,
private-data rules, and exact verification commands.

### Changed

**The common path is `IMessageClient()`.** The client owns an
`AppleScriptTransport` by default. Optional `transport`, `template_manager`, and
`logger` collaborators are keyword-only.

**The public domain term is `recipient`.** `send()`, `send_template()`, and
`send_bulk()` use `recipient` or `recipients` because Messages accepts both phone
numbers and email addresses. Positional send calls are unchanged; callers using
`phone_number=` or `phone_numbers=` must rename those keywords.

**Delivery errors expose a closed reason.** `MessageSendError.recipient`
identifies the failed handle. `reason` is `"delivery"` when AppleScript or
Messages rejects a send and `"transport"` when the transport cannot run. Raw
transport exceptions are not chained because they can contain private child
process data.

**T-string interpolation uses Python semantics.** Template values use normal
conversion and `format()` behavior. Integers, floats, and domain values with
`__format__` support can be interpolated directly. Only `None` means no context;
a false-valued mapping is preserved.

**Logging follows the standard library contract.** The package installs a
`NullHandler` and emits through named loggers. It never creates files, attaches
application handlers, sets levels, chooses formats, logs message bodies, or logs
raw transport exceptions. Host applications own destinations, access, and
retention.

**Diagnostics report blockers, not readiness.** `EnvironmentReport.ready` is
replaced by `blocked`. `PASS`/`INFO` output becomes `OK`/`MANUAL`. A zero doctor
exit code means no automated blocker was found; it does not prove that Messages
is signed in or that Automation permission has been granted.

**Development and release checks are artifact-first.** CI uses a locked uv
environment, lint and formatter diffs, type checks, hermetic tests, strict Sphinx
builds, package builds, clean-wheel smoke tests, and macOS AppleScript compilation.
The release path uses a separately built artifact and PyPI Trusted Publishing.

### Fixed

**Private send data no longer leaks through process inspection or failures.** The
old argv shape included recipient, full message text, and delay for the lifetime
of the `osascript` process. Failed sends also copied the raw command into logs and
traceback causes. Fixed argv, stdin transport, captured child output, plain error
logging, and `raise ... from None` close those paths.

**Doctor output no longer exposes an installed home path.** The bundled-source
check reports a generic result rather than the full package filesystem path.

**uv quick-start commands now run in the project environment.** Documentation
uses `uv run macpymessenger ...` after `uv add macpymessenger` instead of assuming
the project environment is activated.

**Documentation examples are independently copyable.** API and logging examples
include their own imports and state. The package-logger example disables
propagation when it installs its own handler, avoiding duplicate root output.

### Removed

**Script-path configuration.** `Configuration`, `ConfigurationError`, and custom
AppleScript path handling are removed. A custom effect now implements
`MessageTransport`, which preserves extensibility without a filesystem-shaped
public API.

**Generic command execution.** `CommandRunner`, `SubprocessCommandRunner`, and
`macpymessenger.commands` are removed. The package has one production effect, so
a generic argv adapter added indirection while forcing private data into the
wrong shape.

**Library-owned file logging.** `FileLoggingConfiguration` and the
`file_logging=` client parameter are removed. Applications own logging output.

**Unimplemented client methods.** `get_chat_history()` and
`send_with_attachment()` are removed. Unsupported capabilities no longer occupy
public names that always raise `NotImplementedError`.

**Template wrapper machinery.** `RenderedTemplate` and
`TemplateManager.compose_template()` are removed. Rendering returns `str`.

**String-only interpolation failures.** `TemplateTypeError` now covers only a
factory that fails to return a t-string template. Normal formatting errors come
from Python's conversion or format protocol.

### Migration

- Replace `IMessageClient(Configuration())` with `IMessageClient()`.
- Replace custom script paths or `command_runner=` with a `MessageTransport` and
  pass it as `IMessageClient(transport=...)`.
- Rename `phone_number=` to `recipient=` and `phone_numbers=` to `recipients=`.
- Read bulk outcomes through `result.sent` and `result.failed`; copy with
  `list(result.failed)` before mutation.
- Replace `error.reason == "command"` with `error.reason == "transport"`.
- Replace `compose_template(...).content` with `render_template(...)`.
- Replace doctor JSON `ready`, `id`, and `fix` with `blocked`, `identifier`, and
  `next_step`; handle the `manual` status explicitly.
- Configure logging in the application with `logging.basicConfig(...)` or a
  caller-owned logger.

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
