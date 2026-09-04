# macpymessenger

[![PyPI](https://img.shields.io/pypi/v/macpymessenger.svg)](https://pypi.org/project/macpymessenger/)
[![Python](https://img.shields.io/pypi/pyversions/macpymessenger.svg)](https://pypi.org/project/macpymessenger/)
[![CI](https://github.com/ethan-wickstrom/macpymessenger/actions/workflows/ci.yml/badge.svg)](https://github.com/ethan-wickstrom/macpymessenger/actions/workflows/ci.yml)
[![Documentation](https://readthedocs.org/projects/macpymessenger/badge/?version=latest)](https://macpymessenger.readthedocs.io/en/latest/)

Send text through the built-in macOS Messages app from Python, shell scripts, or
local AI agents.

macpymessenger is typed, dependency-free, local, and send-only. One validated
immutable `SendRequest` crosses one replaceable `MessageTransport`. The built-in
transport keeps recipient and message text out of process arguments and
temporary files. Public failures expose closed reason fields instead of raw
AppleScript output.

> **Requirements:** macOS, Python 3.14 or newer, an Apple account signed in to
> Messages, and Automation permission for the application that launches Python.
> The first real send may prompt Terminal, an editor, or an agent host to control
> Messages. macpymessenger is not a hosted service and cannot send from Linux or
> Windows.

## First send from Python

Install the package and check detectable local blockers:

```bash
uv add macpymessenger
uv run macpymessenger doctor
```

Then create one client and reuse it:

```python
from macpymessenger import IMessageClient, MessageSendError

client = IMessageClient()

try:
    client.send("+15555550123", "Hello from Python!")
except MessageSendError as error:
    print(f"Local send failed: {error.reason}")
```

`send()` returns `None` after the local AppleScript transport completes. This
result is not a delivery receipt from the recipient's device. A failed send
raises `MessageSendError` with `recipient` and a closed `reason` value:
`"delivery"` or `"transport"`.

The doctor is side-effect-free. It does not open Messages, run AppleScript,
request permission, read message data, or send text. A clean doctor result means
no automated blocker was found; complete every manual check before sending.

Using pip instead of uv:

```bash
python -m pip install macpymessenger
macpymessenger doctor
```

## Build a request once

`SendRequest` is the single request model used by the Python client, CLI, and
transport boundary:

```python
from macpymessenger import IMessageClient, SendRequest

request = SendRequest(
    recipient="+15555550123",
    message="The report is ready.",
    delay_seconds=30,
)

client = IMessageClient()
client.send_request(request)
```

Construction rejects empty, non-string, or non-UTF-8 recipient and message
values, non-integer delays including booleans, and negative delays before any
delivery effect can run. `send()` is the convenience form; it builds one
`SendRequest` and delegates to `send_request()`.

## Use the command from a script or agent

Load instructions from the installed package before an agent uses the command:

```bash
macpymessenger skills get core
```

Run diagnostics with machine-readable output:

```bash
macpymessenger doctor --json
```

Validate one closed request without constructing a client or sending:

```bash
cat <<'JSON' | macpymessenger send --dry-run --json
{"recipient":"<recipient>","message":"<message>","delay_seconds":0}
JSON
```

A valid dry run returns `data.outcome: "validated"`. Dry run checks request data
only; it does not replace doctor checks, user approval, or Messages permission.

Send the exact user-approved request:

```bash
cat <<'JSON' | macpymessenger send --json
{"recipient":"<recipient>","message":"<message>","delay_seconds":0}
JSON
```

Every JSON command uses one versioned envelope with `schema_version`, `tool`,
`command`, `version`, `ok`, and either `data` or `error`. A successful real send
returns `data.outcome: "transport_completed"`; delivery is not confirmed. Send
failures include `error.retryable: false`. Do not automatically retry a failed
or uncertain send because a retry may duplicate the message.

`send` accepts no unknown fields or duplicate keys. Invalid input exits with
status `2` before the client exists. Send or transport failure exits with status
`1`. Validation or local transport completion exits with status `0`. Structured
output never echoes recipient or message text.

Read the [complete command contract](https://macpymessenger.readthedocs.io/en/latest/guides/command-line.html).

## Send to several recipients

```python
recipients = ["+15555550123", "+15555550124"]
result = client.send_bulk(recipients, "The build is ready.")

print(result.sent)
for failure in result.failures:
    print(failure.recipient, failure.reason)
```

`send_bulk()` snapshots the iterable and sends sequentially in input order.
`result.failures` contains immutable `BulkSendFailure(recipient, reason)` values.
`result.failed` projects only failed recipient strings, `result.ok` reports
whether every local send completed, and `sent, failed = result` remains valid.
Bulk outcomes are not delivery receipts. Do not automatically retry failed or
uncertain items.

## Reuse a t-string template

Templates are functions that return Python 3.14 t-strings. Interpolations use
normal Python conversion and formatting:

```python
client.create_template(
    "build-result",
    lambda project, duration: t"{project} finished in {duration:.1f}s",
)
client.send_template(
    "+15555550123",
    "build-result",
    {"project": "Example", "duration": 3.25},
)
```

macpymessenger does not use Jinja2 or template files.

## Replace the delivery effect

Inject a `MessageTransport` for tests or another local delivery mechanism. The
transport receives the exact immutable request:

```python
from macpymessenger import IMessageClient, SendRequest


class RecordingTransport:
    def __init__(self) -> None:
        self.requests: list[SendRequest] = []

    def send(self, request: SendRequest) -> None:
        self.requests.append(request)


transport = RecordingTransport()
client = IMessageClient(transport=transport)
request = SendRequest("+15555550123", "Recorded, not sent.")
client.send_request(request)
assert transport.requests[0] is request
```

A transport should raise `MessageSendError` for a known delivery or transport
failure. `IMessageClient` sanitizes typed failures before exposing them and still
maps `CalledProcessError` or `OSError` from older custom transports. Ordinary
automated tests should inject a transport and never invoke Messages or
AppleScript.

## Logging and private data

macpymessenger emits generic records through Python logging but does not add
output handlers, set levels, choose formats, or create files. The host
application owns logging destinations, access, and retention.

The built-in transport invokes fixed argv `('/usr/bin/osascript', '-')` and
streams encoded AppleScript through standard input. Recipient and message text
do not enter process arguments, environment variables, or temporary files.
Child output and raw transport exceptions do not cross the public error
boundary. Public encoding, script-loading, delivery, and transport failures
contain neither the raw exception as `__cause__` nor as `__context__`.

## Deliberate scope

Use macpymessenger when code running on a Mac needs to send text through the
existing Messages account. The package does not read chat history, send
attachments, resolve contacts, expose a remote API, run a messaging server,
provide delivery receipts, manage accounts, or provide an MCP server.

## Documentation

- [Installation](https://macpymessenger.readthedocs.io/en/latest/installation.html)
- [Environment diagnostics](https://macpymessenger.readthedocs.io/en/latest/guides/environment-diagnostics.html)
- [Command line and Agent Skill](https://macpymessenger.readthedocs.io/en/latest/guides/command-line.html)
- [Python sending guide](https://macpymessenger.readthedocs.io/en/latest/guides/sending-messages.html)
- [Templates](https://macpymessenger.readthedocs.io/en/latest/guides/templates.html)
- [Custom transports](https://macpymessenger.readthedocs.io/en/latest/api/transport.html)
- [Errors](https://macpymessenger.readthedocs.io/en/latest/api/exceptions.html)
- [Troubleshooting](https://macpymessenger.readthedocs.io/en/latest/guides/troubleshooting.html)
- [Public API](https://macpymessenger.readthedocs.io/en/latest/modules.html)
- [Contributing](CONTRIBUTING.md)
- [Changelog](CHANGELOG.md)

## Project status

macpymessenger is alpha software. Text sends, validated immutable requests,
t-string templates, delays, structured sequential bulk outcomes, typed errors,
custom transports, passive diagnostics, a validation-safe command line, and
version-matched Agent Skills are supported.

macpymessenger is licensed under [Apache-2.0](LICENSE). It is maintained by
[Ethan Wickstrom](https://github.com/ethan-wickstrom) and started as a fork of
[Rolstenhouse/py-iMessage](https://github.com/Rolstenhouse/py-iMessage).
