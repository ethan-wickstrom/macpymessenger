# Security guidelines

Use this file for subprocesses, scripts, diagnostics, logs, recipients,
credentials, paths, or examples.

## Protect private data

- Never commit secrets, account data, real phone numbers, or real email addresses.
- Treat recipient handles in logs and exceptions as private data.
- Redact private home paths and recipient data from doctor output, tracebacks,
  issues, and pull requests before sharing.
- Use reserved example numbers and invented addresses in every fixture and guide.
- Never print message bodies from library logging or diagnostics.

## Keep subprocess execution explicit

- Build argv as a sequence of strings.
- Always keep `shell=False`.
- Let `SubprocessCommandRunner` delegate prepared internal commands directly to
  `subprocess.run`; do not add a second escaping or validation language.
- Keep the send script path resolved by `Configuration` before command execution.
- Never run a real send from an automated test.

## Keep diagnostics read-only

- A doctor check may inspect platform names, executable paths, known app paths,
  and package files.
- A check must not open Messages, run AppleScript, trigger Automation permission,
  inspect private message databases, contact a network service, or change state.
- Report unverifiable account and permission state as `INFO` with a human next
  step. Do not infer success.

## Keep logging application-owned

- The package may add only a `NullHandler`.
- Do not create log files, attach host handlers, set levels, choose formats, or
  define retention.
- Document that delivery records include recipient handles.

## Keep release credentials out of code

- Use GitHub secrets or trusted publishing configuration.
- Never place PyPI tokens in files, commands, examples, commits, or logs.
