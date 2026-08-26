# Security guidelines

Use this file for transports, AppleScript, diagnostics, logs, recipients,
credentials, package data, or examples.

## Protect private data

- Never commit secrets, account data, real phone numbers, real email addresses,
  or real message bodies.
- Treat recipient handles in logs and exceptions as private data.
- Redact private home paths and recipient data from doctor output, tracebacks,
  issues, and pull requests before sharing.
- Use reserved example numbers and invented addresses in every fixture and guide.
- Never put message bodies in library logs, diagnostics, child output, exception
  causes, process arguments, environment variables, or temporary files.

## Keep the transport boundary narrow

- Cross the effect boundary with one immutable `SendRequest`.
- Keep production argv fixed at `('/usr/bin/osascript', '-')` and `shell=False`.
- Encode recipient and message text into the AppleScript streamed through stdin.
  Do not add a second shell, escaping language, or file-backed payload path.
- Capture child stdout and stderr inside `AppleScriptTransport`.
- Map transport exceptions to `MessageSendError` without chaining the raw cause.
- Inject a `MessageTransport` in ordinary tests. Never run a real send from an
  automated test.

## Keep diagnostics side-effect-free

- A doctor check may inspect the platform, fixed executable and app paths, and
  bundled package data.
- A check must not open Messages, invoke AppleScript, trigger Automation
  permission, inspect private message databases, contact a network service, or
  change state.
- Report unverifiable account and permission state as `MANUAL` with a next step.
  Do not infer readiness.

## Keep logging application-owned

- The package may add only a `NullHandler`.
- Do not create log files, attach host handlers, set levels, choose formats, or
  define retention.
- Delivery records may include recipient handles but must never include message
  bodies or raw transport exceptions.

## Keep release credentials out of code

- Publish through PyPI Trusted Publishing with a short-lived OIDC identity.
- Keep build code in an unprivileged job and grant `id-token: write` only to the
  publish job that downloads and uploads the built artifact.
- Never place PyPI tokens in files, commands, examples, commits, or logs.
