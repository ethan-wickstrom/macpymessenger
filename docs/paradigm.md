# Paradigm: verdicts for macpymessenger

This document records the phase-0 requirements, the option space researched,
and the per-component design verdicts. It froze at the end of phase 2.
Changing it afterward requires a note in `docs/notes/` recording what was
learned that invalidates the frozen version.

## Requirements

What the application actually is: a Python library, published on PyPI, that
lets a script running on a signed-in macOS machine send an iMessage text to a
recipient handle, with optional named message templates. Constraints:

- **Platform** (stated, `pyproject.toml`): macOS only, Python >= 3.14, zero
  runtime dependencies.
- **Scale** (assumed): single process, one machine, human-scale send volume
  (at most a few messages per second; Messages.app itself is the bottleneck).
  Sensitivity: if bulk campaign volume were a requirement, the synchronous
  `osascript`-per-message design would flip toward a queue and a persistent
  scripting session. Nothing in the repository, issues, or README suggests
  that requirement, so the verdicts below assume human-scale volume.
- **Durability/consistency** (assumed): none. A failed send raises; the
  caller decides what to retry. No state survives the process except
  Messages.app's own database.
- **Callers** (stated, `docs/usage.rst`): Python developers writing scripts
  and small automations. They need typed errors, not status flags.
- **Operational** (stated, `AGENTS.md`, CI workflow): tests, lint, and type
  checks must run on Linux CI where Messages.app does not exist, so real
  AppleScript execution must be substitutable.
- **Receiving messages** (stated by omission): not a requirement.
  `get_chat_history` has never been implemented and no issue tracks it with
  a design.

## Option space for the send boundary

How real projects send iMessages from macOS, with the conditions under which
each is right:

1. **AppleScript via `osascript`, driving Messages.app.** Right when the
   machine is interactive, SIP stays on, and only sending is needed. Wrong
   when you need delivery receipts, incoming messages, or headless
   operation.
   - [mautrix-imessage `imessage/mac/send.go`](https://github.com/mautrix/imessage/blob/master/imessage/mac/send.go)
     (production Matrix bridge, "normal Mac" mode): pipes the script to
     `osascript -` on stdin and passes recipient and body as **argv**, never
     interpolated into the script source. What the design made easy: safe
     sending with no injection surface. What they bolted on: a retry ladder
     for AppleScript error `-1728` (chat-id lookup failures) with two
     fallback scripts, and debug-info collection for that error. What they
     regretted: sending via AppleScript gives no message GUID back, so the
     bridge matches sent messages by polling `chat.db` — a cost this library
     does not pay because it promises nothing after the send.
   - [BlueBubbles server `fileSystem/index.ts`](https://github.com/BlueBubblesApp/bluebubbles-server/blob/master/packages/server/src/server/fileSystem/index.ts):
     builds `osascript -e <part> -e <part>` through a shell
     (`execShellCommand`), which forced them to maintain string-escaping
     machinery for message bodies. That is the special case argv-passing
     avoids.
   - Conditions that would flip this verdict: needing read receipts, typing
     indicators, or inbound messages (mautrix's Barcelona/IMCore mode, SIP
     off) — an explicit non-requirement here.
2. **Private frameworks (IMCore / Barcelona).** Right for full-fidelity
   bridges willing to disable SIP and chase every macOS release. Wrong for a
   zero-dependency library targeting stock machines. mautrix-imessage
   documents this mode as requiring SIP and AMFI disabled; the Barcelona
   project itself is unmaintained since 2023. Rejected.
3. **Writing to `~/Library/Messages/chat.db`.** Not a send mechanism at all:
   inserting rows does not transmit anything. Used by read-side tools
   (imessage-exporter, BlueBubbles' receive path). Rejected for sending;
   would only become relevant if receiving became a requirement.
4. **Shortcuts CLI (`shortcuts run`).** Requires a user-installed Shortcut,
   which cannot be bundled in a wheel; no real library-shaped project ships
   this as its primary path. Rejected: the deployment unit does not fit a
   pip-installable package.
5. **PyObjC / ScriptingBridge.** Adds a heavyweight dependency for the same
   Apple Events the bundled script already sends, and would make the test
   seam harder (CI has no AppleEvent bus). No production send-focused
   codebase found that prefers it over `osascript`. Rejected.

**Verdict (high confidence): keep the bundled compiled AppleScript invoked
as `osascript <script> <recipient> <body> <delay>` with arguments passed as
argv.** Deciding conditions: send-only scope, SIP-on stock macOS, zero
runtime dependencies. Revisit if receiving or delivery receipts become
requirements. The incumbent survives because it matches what the two
production reference codebases converged on, minus the escaping machinery
BlueBubbles needed and the retry ladder mautrix needed for chat-id sends
(this library sends to a buddy handle directly, which is mautrix's own final
fallback for the `-1728` failure).

## Per-component verdicts

### Subprocess execution: stdlib `subprocess.run`, no wrapper library

`subprocess.run(command, check=True, shell=False)` is the wheel; both
reference codebases use their stdlib equivalent (`exec.Command`,
`child_process`). No third-party process library earns a dependency here.
**Keep. High confidence.** Flip condition: needing async sends, which is not
a requirement.

The `CommandRunner` protocol seam stays because the Linux CI requirement
makes execution substitutability a hard constraint (measured: this repo's CI
runs on `ubuntu-latest`). The runner's homemade argument validation
(`InvalidCommandError`) does **not** stay: commands are built internally by
`MessageDelivery._build_command`, which can only produce `list[str]`, and
`subprocess.run` itself raises `TypeError` for invalid argument types.
Validating internal invariants at an internal seam is shallow machinery
duplicating a framework guarantee.

### Templates: PEP 750 t-strings via `string.templatelib`, no template engine

The library's stated identity (`pyproject.toml` keywords, `AGENTS.md`)
includes t-string templates, and Python 3.14 ships `Template`,
`Interpolation`, and `convert` natively. Jinja2 would be the alternative for
untrusted or file-loaded templates; templates here are trusted Python
callables written by the caller, so an engine dependency removes nothing.
**Keep t-strings. High confidence** — the platform is the dependency.
Flip condition: file-based or user-supplied template sources.

`RenderedTemplate`/`compose_template` are a shallow wrapper: the only
consumer (`IMessageClient.send_template`) immediately unwraps `.content`.
Removed; `render_template` returning `str` is the whole contract.

### Logging: stdlib contract, no handler management

The Python logging HOWTO is explicit: a library must not add handlers other
than `NullHandler`, and must not set levels; configuration belongs to the
application. The incumbent client attaches `FileHandler`s, formats them,
mutates logger levels, and defines `FileLoggingConfiguration` plus a
`ConfigurationError.file_logging_unavailable` factory to carry the failure
mode that machinery creates. That is homemade machinery overlapping the
logging framework itself. **Verdict (high confidence): the library logs to
`logging.getLogger(__name__)` per module, installs a package-level
`NullHandler`, and owns no handlers, levels, or formats.** Callers who want
a log file write the three standard lines of `logging` configuration.
Flip condition: none identified; this is the framework's own contract.

### Experimental stub methods: removed

`get_chat_history` and `send_with_attachment` have only ever raised
`NotImplementedError`. An API whose only behavior is refusing to run is not
a capability, and reserving names is not a requirement any caller can cite.
`docs/usage.rst` itself instructs callers not to call them. **Removed.
High confidence.** Flip condition: an implementation exists (attachments
would reuse the existing boundary: mautrix's `sendFileBuddy` script shows
the shape).

### Configuration: frozen dataclass, fail-fast script resolution

Validating the script path at construction is boundary validation of caller
input and keeps the failure close to the mistake. **Keep. High confidence.**

### Delay validation: keep at the public boundary, drop the fake overloads

`delay_seconds` crosses the public boundary and is forwarded to AppleScript,
so the int/bool/negative checks stay. The two `@overload` declarations on
`IMessageClient.send` (one `int`, one `object`, otherwise identical) exist
only to type-launder invalid input and cancel each other out; the signature
is `delay_seconds: int = 0` with runtime validation retained. **High
confidence.**

### Module layout

`configuration` / `templates` / `commands` / `delivery` / `client` /
`exceptions` each own one concept with a real seam between them; the client
compatibility re-exports of `CommandRunner`/`SubprocessCommandRunner` were a
migration shim and are removed (canonical homes: package root and
`macpymessenger.commands`). **Keep the layout. Medium confidence** — a
single-module library would also be defensible at this size; the split
survives because each module's tests are independent and the cost of the
split is near zero. Cheapest-to-change tiebreak favors keeping it.

## Migration verdict

**Incremental replacement in place, behind the existing public interface,
gated by a characterization (parity) suite. Not a rebuild from zero.**
Deciding conditions, all measured in this repository: the code is ~700
source lines, a full test suite (55 tests) passes, components are already
separable, and the public surface is small enough to characterize
exhaustively. A from-zero rebuild would carry cutover risk (losing behavior
nobody wrote down) while removing nothing the incremental path cannot
remove. Behavior is preserved by `tests/parity/test_baseline.py`, captured
against the incumbent before any change and never edited afterward; every
intentional divergence is recorded in `tests/parity/test_divergences.py`
with the old behavior and the justifying requirement.

## What was searched and what would have changed the verdicts

Searched: programmatic iMessage sending approaches (AppleScript/osascript,
Shortcuts, IMCore/Barcelona, chat.db), and the send paths of
mautrix-imessage (Go, production bridge) and bluebubbles-server (TypeScript,
production server), read at file level; the GitHub topic space of
Python+AppleScript senders (py-imessage, imessage-cli and a dozen smaller
ones — all `osascript` wrappers, none with a safer boundary than argv
passing). Stopping rule hit: every additional sender examined used the same
boundary this library already has; no source suggested a different verdict
for a send-only, SIP-on, zero-dependency library. What would have changed
the verdicts: evidence that argv passing to `osascript` is unreliable for
message bodies (none found; mautrix uses it in production), a maintained
supported Apple API for sending (none exists), or a requirement to receive
messages (explicitly absent).
