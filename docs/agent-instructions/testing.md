# Testing guidelines

Use this file when adding or changing tests.

## Tests must stay hermetic

- Do not execute real AppleScript in tests.
- Use stubbed command runners from shared test support.
- Use `tmp_path` for script files and filesystem fixtures.

## Assertions should cover domain behavior

- Assert on raised and logged behavior when error handling changes.
- Verify command composition through a stub runner rather than through `osascript`.
- Keep tests focused on changed behavior and public contracts.

## Verification scope

- Run `uv run pytest` when behavior or tests change.
- Run `uv run ruff check` and `uv run ty check` when Python code changes.

See the root `AGENTS.md` for the complete command list.
