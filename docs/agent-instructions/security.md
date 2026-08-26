# Security guidelines

Use this file for transports, AppleScript, diagnostics, logs, recipients,
credentials, package data, command input, or examples.

## Protect private data

- Never commit secrets, account data, real phone numbers, real email addresses,
  or real message bodies.
- Treat `MessageSendError.recipient` as private application data.
- Redact private home paths and recipient data from doctor output, tracebacks,
  issues, and pull requests before sharing.
- Use reserved example numbers and invented addresses in every fixture and guide.
- Never put message bodies in library logs, diagnostics, child output, exception
  causes, process arguments, environment variables, or temporary files.

## Keep the agent command boundary closed

- Read one JSON object from standard input. Do not add recipient or message
  command flags.
- Accept only `recipient`, `message`, and optional `delay_seconds`.
- Reject malformed JSON, unknown fields, duplicate keys, empty required strings,
  non-integer or negative delays, and non-UTF-8 text before creating a client.
- Write structured results to standard output and human diagnostics to standard
  error. Never echo recipient or message text.
- Keep exit codes stable: `0` for transport completion, `1` for send or transport
  failure, and `2` for invalid input.
- Never retry a failed or uncertain send automatically. The package has no
  delivery receipt or idempotency key.

## Keep the transport boundary narrow

- Cross the effect boundary with one immutable `SendRequest`.
- Keep production argv fixed at `('/usr/bin/osascript', '-')` and `shell=False`.
- Encode recipient and message text into the AppleScript streamed through
  standard input. Do not add a second shell, escaping language, or file-backed
  payload path.
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
- Built-in delivery records contain generic outcomes only. They must never
  include recipient handles, message bodies, or raw transport exceptions.

## Keep release credentials out of code

- Publish through PyPI Trusted Publishing with a short-lived OIDC identity.
- Keep build code in an unprivileged job and grant `id-token: write` only to the
  publish job that downloads and uploads the built artifact.
- Never place PyPI tokens in files, commands, examples, commits, or logs.
