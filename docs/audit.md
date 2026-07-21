# Audit of the incumbent implementation

Phase-1 findings: every duplicated concept, ad hoc special case, and place
where subsystems disagree, with the single underlying concept each one
hides. Line references are to the tree at commit `327762d`.

## 1. Two subsystems disagree about who owns logging

`client.py` mutates logger levels, attaches `FileHandler`s, and defines
`FileLoggingConfiguration`; `delivery.py` treats the logger as an opaque
sink it writes events to. The second is the correct concept: a library
emits events, the application decides where they go (Python logging HOWTO,
"adding handlers other than NullHandler to a library's loggers is
forbidden" in spirit). The client's handler management is a symptom of a
wrong verdict-level decision (library-managed log destinations), not sloppy
code — see `docs/paradigm.md` § Logging. It also drags in a special-cased
exception factory (`ConfigurationError.file_logging_unavailable`) and 130
lines of tests for behavior the logging framework already owns. Reference
comparison: neither mautrix-imessage nor bluebubbles-server configures log
destinations inside its send module; both write to an injected logger.

## 2. Validation duplicated at an internal seam

`SubprocessCommandRunner.__call__` re-validates that the command is a
sequence of strings (`commands.py:31-35`, `InvalidCommandError`). The
command is constructed two frames up by `MessageDelivery._build_command`,
which by type can only produce `list[str]`; `subprocess.run` raises
`TypeError` for anything else. The underlying concept: validation belongs at
system boundaries (caller input, filesystem), and the runner is not one.

## 3. The same signature declared three times

`IMessageClient.send` carries two `@overload`s that differ only in typing
`delay_seconds` as `int` versus `object` (`client.py:135-141`). The `object`
overload exists to admit invalid input that `_validate_delay` then rejects
at runtime. One signature (`delay_seconds: int = 0`) plus the runtime
boundary check expresses the same contract without lying to the type
checker twice.

## 4. A rendering result wrapped only to be unwrapped

`compose_template` wraps `render_template`'s string in `RenderedTemplate`
(`templates.py:86-97`); the only internal consumer, `send_template`,
immediately reads `.content` and discards the identifier it already had.
The underlying concept: rendering produces a string.

## 5. API surface that only refuses to run

`get_chat_history` and `send_with_attachment` (`client.py:172-244`) are 70
lines of docstring documenting behavior that does not exist, plus tests
asserting the docstrings mention "Experimental". The underlying concept:
the public API is the set of things the library can do.

## 6. Import machinery working around the type checker

`client.py:19-25` imports `Template` and `Configuration` via
`import_module` at runtime while type-checking them through `TYPE_CHECKING`
— a hand-rolled duplicate of a plain `from .configuration import
Configuration`, apparently to satisfy a lint rule (`TC001`) that has a
standard suppression. Plain imports express the dependency honestly.

## 7. Compatibility re-exports from a finished migration

`client.py` still re-exports `CommandRunner` and `SubprocessCommandRunner`
after their extraction to `commands.py` (issue #35). The migration is done;
the shim now creates two import paths for the same names.

## What is *not* wrong

- The `osascript`-with-argv boundary, the `CommandRunner` seam, frozen
  `Configuration` with fail-fast script resolution, t-string templates,
  typed exception hierarchy with message-owning factories, delay validation
  at the public boundary, and the `send_bulk` partition — all match the
  paradigm verdicts and survive on merit (see `docs/paradigm.md`).
- The AppleScript itself: propagates delivery errors as non-zero exit,
  passes recipient/body via argv, honors the delay argument.
