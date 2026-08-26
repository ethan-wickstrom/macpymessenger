# Testing guidelines

Use this file when adding or changing tests.

## Keep tests hermetic

- Never execute a rendered script, open Messages, request Automation permission,
  or send a real message.
- Inject `StubTransport` or another focused `MessageTransport`.
- The macOS-only compiler test may run `/usr/bin/osacompile`; compilation must
  not execute the script or control Messages.
- Monkeypatch platform, fixed paths, and package-source loading in diagnostic
  tests. Do not make ordinary assertions depend on the current runner.
- Restore logger handlers, levels, and propagation changed by a test.

## Test contracts, not implementation trivia

- Assert public request and result shapes, exception types and fields, emitted
  records, fixed transport argv, stdin source properties, JSON fields, and exit
  codes.
- Assert that raw recipient and message values do not appear in transport argv,
  logs, child output, or exception causes.
- Test one named behavior per test.
- Add edge cases at input boundaries: empty recipient lists, all failures,
  negative or non-integer delays, false-valued mappings, conversion, formatting,
  and missing bundled package data.
- Preserve compatibility only when a test states the supported contract, such as
  tuple unpacking for `BulkSendResult`.

## Run the matching checks

Python behavior or tests:

```bash
uv run --locked ruff check
uv run --locked ruff format --diff
uv run --locked ty check
uv run --locked pytest
```

Public docs or docstrings:

```bash
uv run --locked sphinx-build -n -T -W --keep-going docs docs/_build/html
```

Packaging or exports:

```bash
uv build
```

The root `AGENTS.md` contains the full completion gate.
