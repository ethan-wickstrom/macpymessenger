# Documentation guidelines

Use this file for `README.md`, `docs/`, examples, docstrings, package metadata, or
other user-facing text.

## Use the current public contract

- Start ordinary examples with `IMessageClient()`.
- Import public clients, result types, and exceptions from `macpymessenger`.
- Show `send()` returning `None` or raising `MessageSendError`.
- Use `MessageSendError.recipient` and `.reason` instead of parsing text.
- Show `BulkSendResult.sent` and `.failed`; mention tuple unpacking only as
  compatibility.
- Show template factories as callables that return t-strings and rendering as a
  plain string.
- Show application-owned standard library logging. Never document
  `FileLoggingConfiguration` or library-created handlers.
- Do not document unsupported chat history, attachments, contact lookup, remote
  gateway, or MCP capabilities as methods that exist.

## Make examples copy-safe

- Make every code block self-contained unless the surrounding text explicitly
  establishes shared state.
- Use reserved example phone numbers and invented account data.
- State macOS, Python, Messages sign-in, and Automation permission before a real
  send example.
- Use `macpymessenger doctor` for side-effect-free setup checks and
  `macpymessenger doctor --json` for scripts and agents.

## Keep discovery surfaces in sync

A public contract change may require updates to:

- `README.md` for package and repository visitors;
- the owning task guide and API page;
- `docs/index.rst` navigation and metadata;
- `docs/llms.txt` for agent retrieval;
- `pyproject.toml` when search or package metadata changes; and
- `CHANGELOG.md` for downstream users.

Use descriptive page titles, filenames, and meta descriptions. Link every public
page from a toctree or mark deliberate compatibility pages as orphaned.

Build with:

```bash
uv run --locked sphinx-build -n -T -W --keep-going docs docs/_build/html
```
