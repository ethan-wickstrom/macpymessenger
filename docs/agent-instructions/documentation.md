# Documentation guidelines

Use this file for `README.md`, `docs/`, examples, docstrings, package metadata,
Agent Skills, or other user-facing text.

## Use the current public contract

- Start ordinary Python examples with `IMessageClient()`.
- Start agent command examples with `macpymessenger skills get core`.
- Import public clients, request and result types, transports, and exceptions from
  `macpymessenger`.
- Show `send()` returning `None` or raising `MessageSendError`.
- Use `MessageSendError.recipient` and the closed `.reason` values `delivery` and
  `transport` instead of parsing text.
- Show `BulkSendResult.sent` and `.failed`; mention tuple unpacking only as
  compatibility.
- Show `SendRequest` and `MessageTransport` when replacing the delivery effect.
  Never document script-path configuration or command-runner injection.
- Show the CLI accepting one JSON object on standard input. Never add recipient
  or message command flags to an example.
- State the CLI exit codes and that transport completion is not a delivery
  receipt.
- Show template factories as callables that return t-strings, normal Python
  conversion and formatting, and rendering as a plain string.
- Show application-owned standard library logging. Never document
  `FileLoggingConfiguration` or library-created output handlers.
- Do not document unsupported chat history, attachments, contact lookup, remote
  gateway, or account-management capabilities as methods that exist.

## Make examples copy-safe

- Make every code block self-contained unless the surrounding text explicitly
  establishes shared state.
- Use reserved example phone numbers, placeholders, and invented account data.
- State macOS, Python, Messages sign-in, and Automation permission before a real
  send example.
- After `uv add macpymessenger`, invoke the console script with
  `uv run macpymessenger ...`. Use a bare `macpymessenger` command only when the
  surrounding instructions activate the environment or describe an installed
  command generically.
- Explain that doctor status `blocked: false` means no automated blocker was
  found. Preserve and show every `manual` next step.
- Never put real message bodies or private paths in logs, tracebacks, JSON
  examples, process arguments, issue templates, or screenshots.
- Never imply that a failed send is safe to retry automatically.

## Keep discovery surfaces in sync

A public contract change may require updates to:

- `README.md` for package and repository visitors;
- the owning task guide and API page;
- `docs/index.rst` navigation and metadata;
- `docs/llms.txt` for retrieval;
- `.agents/skills/macpymessenger/SKILL.md` for repository discovery;
- `src/macpymessenger/skills/core/SKILL.md` for installed workflow behavior;
- `pyproject.toml` when search or package metadata changes; and
- `CHANGELOG.md` for downstream users.

Keep the repository skill thin. The full workflow belongs in the installed
package so instructions and command behavior share a version.

Use descriptive page titles, filenames, and meta descriptions. Link every public
page from a toctree or mark deliberate compatibility pages as orphaned.

Build with:

```bash
uv run --locked sphinx-build -n -T -W --keep-going docs docs/_build/html
```
