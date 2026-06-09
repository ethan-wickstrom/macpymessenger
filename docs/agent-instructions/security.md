# Security guidelines

Use this file when a task touches subprocess execution, user input, paths, credentials, phone numbers, or examples.

## Protect user data

- Never commit secrets.
- Never commit real phone numbers.
- Use fixtures, placeholders, or environment variables for examples.

## Keep subprocess execution explicit

- Avoid `shell=True`.
- Use argument lists for subprocess calls.
- Validate paths before use.
- Prefer the existing `SubprocessCommandRunner` behavior unless the task specifically changes command execution.

## Keep configuration predictable

- Let `Configuration` validate the AppleScript path.
- Prefer the bundled AppleScript unless tests require a custom path.
- Raise `ScriptNotFoundError` for missing or unreadable scripts.
