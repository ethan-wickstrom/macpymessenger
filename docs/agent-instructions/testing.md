# Testing guidelines

Use this file when adding or changing tests.

## Keep tests hermetic

- Never execute `osascript`, open Messages, request Automation permission, or
  send a real message.
- Inject `StubRunner` or a focused callable through `command_runner`.
- Use `tmp_path` for custom scripts and filesystem fixtures.
- Monkeypatch platform discovery in diagnostic tests. Do not make the suite
  depend on the runner's operating system.
- Restore logger handlers, levels, and propagation changed by a test.

## Test contracts, not implementation trivia

- Assert public return shapes, exception types and fields, emitted records, argv,
  and exit codes.
- Test one named behavior per test.
- Add edge cases at input boundaries: empty recipient lists, all failures,
  negative or non-integer delays, missing scripts, and non-string interpolation.
- Preserve compatibility only when a test states the supported contract, such as
  tuple unpacking for `BulkSendResult`.

## Run the matching checks

Python behavior or tests:

```bash
uv run --locked ruff check
uv run --locked ruff format --check
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
