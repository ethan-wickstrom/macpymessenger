# Foundation: core primitives and derivations

Written in phase 2, within the verdicts of `docs/paradigm.md`. Every module
in `src/macpymessenger/` must be derivable from the primitives below with no
special cases; a component needing a special case the core cannot express
means the core is wrong and must be revised here first.

## Core primitives

1. **Send command** — the value `["osascript", script_path, recipient,
   body, str(delay)]`. Everything the library does to a message ends in this
   list. Arguments travel as argv, never interpolated into script source, so
   no escaping machinery exists anywhere.
2. **Command runner** — a callable `(Sequence[str]) -> None` that raises
   `subprocess.CalledProcessError` on non-zero exit and `OSError` when the
   process cannot start. The production runner is a thin `subprocess.run`
   call; tests substitute it. This is the only process boundary.
3. **Resolved configuration** — a frozen value holding the send script
   path, validated once at construction (exists, readable). After
   construction, no code re-checks the filesystem.
4. **Template factory** — a caller-supplied callable returning a PEP 750
   `Template`; rendering flattens it to `str`, enforcing string-only
   interpolation values and applying conversions and format specs.
5. **Typed failure** — every failure crossing the public boundary is a
   `MacPyMessengerError` subclass whose message is owned by the exception
   type (constructor or named factory), never composed at the raise site.

## Boundary rule

Runtime validation exists exactly where data enters the system: caller
arguments (`delay_seconds`, template identifiers, factory return values)
and the filesystem (script path). Internal seams (delivery → runner) trust
their types; the runner performs no argument validation because it only
ever receives the send command primitive.

## Logging rule

Events are emitted through the logger injected into `MessageDelivery`,
which defaults to the client module's logger
(`logging.getLogger("macpymessenger.client")`). The package `__init__`
installs a `NullHandler`. The library never attaches other handlers, sets
levels, or chooses formats. `IMessageClient` accepts an optional `logger`
for callers who want events routed to their own logger object.

## Derivations

- `configuration.Configuration` — primitive 3, plus `ScriptNotFoundError`
  (primitive 5) for the filesystem boundary.
- `commands.CommandRunner` / `commands.SubprocessCommandRunner` —
  primitive 2. No validation, no logging, no mapping: exceptions propagate
  raw for delivery to interpret.
- `templates.TemplateManager` — primitive 4 keyed by identifier, with
  `TemplateNotFoundError` / `TemplateAlreadyExistsError` /
  `TemplateTypeError` (primitive 5) at the caller boundary. Rendering
  returns `str` — there is no rendered-value wrapper type.
- `delivery.MessageDelivery` — validates the delay (boundary rule), builds
  the send command (primitive 1), executes it through the runner
  (primitive 2), maps `CalledProcessError`/`OSError` to `MessageSendError`
  (primitive 5), and logs the outcome (logging rule).
- `client.IMessageClient` — composition only: wires configuration, template
  manager, runner, and logger into a `MessageDelivery`, and expresses
  `send`, `send_template` (render then send), template CRUD (delegation),
  and `send_bulk` (partition recipients by `MessageSendError`). The client
  contains no behavior of its own beyond composition.
- `exceptions` — primitive 5's catalogue. Exception types exist only for
  failures that can occur: `InvalidCommandError` and the file-logging
  `ConfigurationError` factory have no producers and therefore do not
  exist.

## Rejected alternatives

- **Single-module layout**: defensible at this size, rejected because each
  primitive already has an independent test surface and the split costs
  nothing (paradigm § Module layout).
- **Returning a result object from `send`**: the contract is
  raise-or-`None`; a result type would duplicate the exception channel.
- **Async runner**: no requirement; `osascript` sends are serialized by
  Messages.app anyway.
- **Validating the command inside the runner**: violates the boundary rule;
  the command is an internal value.

## Verified properties

Checked by the suites in this repository (run on every CI push):

- Parity: `tests/parity/test_baseline.py` (frozen) proves the surviving
  surface behaves identically to commit `327762d`;
  `tests/parity/test_divergences.py` pins every intentional difference.
- Correctness properties: `tests/test_properties.py` exercises the
  invariants with randomized inputs — command shape round-trips arbitrary
  recipient/body text unchanged (no escaping layer to corrupt it),
  rendering equals Python's own f-string semantics for string values, delay
  validation accepts exactly the non-negative non-bool ints, and
  `send_bulk` partitions losslessly.
- Types: `uv run ty check`; lint: `uv run ruff check`.

With phase 2 complete, `docs/paradigm.md` and the parity baseline are
frozen; later changes require a `docs/notes/` entry recording what
invalidated them.
