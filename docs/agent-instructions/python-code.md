# Python code guidelines

Use this file when changing library code under `src/macpymessenger/`.

## Keep the public model explicit

- Target Python 3.14 or newer.
- Use full type hints where behavior crosses a public or module boundary.
- Prefer simple data objects and functions over layered class hierarchies.
- Prefer `dataclass(frozen=True, slots=True)` for immutable value objects.
- Keep effects near the outer layer; keep rendering, validation, and transformation logic deterministic when practical.

## Preserve domain boundaries

- Keep AppleScript path discovery in `Configuration`.
- Keep message orchestration in `IMessageClient`.
- Keep template registration and rendering in `TemplateManager`.
- Raise exception types from `src/macpymessenger/exceptions.py` instead of adding ad hoc errors.
- Name concepts by their domain role, not by temporary implementation details.

## Keep template behavior strict

- Define templates as callables that return Python 3.14 t-strings.
- Use examples like `t"Hello, {name}!"`.
- Preserve `TemplateTypeError` for non-string interpolation values.
- Reject duplicate template identifiers.
