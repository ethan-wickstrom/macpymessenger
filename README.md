# macpymessenger

[![PyPI](https://img.shields.io/pypi/v/macpymessenger.svg)](https://pypi.org/project/macpymessenger/)
[![Python](https://img.shields.io/pypi/pyversions/macpymessenger.svg)](https://pypi.org/project/macpymessenger/)
[![CI](https://github.com/ethan-wickstrom/macpymessenger/actions/workflows/ci.yml/badge.svg)](https://github.com/ethan-wickstrom/macpymessenger/actions/workflows/ci.yml)
[![Documentation](https://readthedocs.org/projects/macpymessenger/badge/?version=latest)](https://macpymessenger.readthedocs.io/en/latest/)

Send iMessages from Python on macOS through the built-in Messages app.

macpymessenger is a typed, dependency-free library for local scripts,
automations, developer tools, and agents. It sends text through one immutable
request model, supports Python 3.14 t-string templates, and exposes failures as
data instead of command output.

> **Before you start:** You need macOS, Python 3.14 or newer, an Apple account
> signed in to Messages, and Automation permission for the application that
> launches Python. The first send may ask to let Terminal, your editor, or
> another launcher control Messages. Allow access, or review it in **System
> Settings > Privacy & Security > Automation**. macpymessenger is not a hosted
> service and cannot send from Linux or Windows.

## Install and check the Mac

Add macpymessenger to a uv project, then run its side-effect-free doctor through
the project environment:

```bash
uv add macpymessenger
uv run macpymessenger doctor
```

With an active virtual environment, use pip and the installed command directly:

```bash
python -m pip install macpymessenger
macpymessenger doctor
```

The doctor reports definite blockers and manual checks. It does not open
Messages, request permission, read message data, run AppleScript, or send text.
Use `--json` for stable script and agent output.

## Send your first message

```python
from macpymessenger import IMessageClient, MessageSendError

client = IMessageClient()

try:
    client.send("+15555550123", "Hello from Python!")
except MessageSendError as error:
    print(f"Could not send to {error.recipient}: {error}")
```

The recipient may be a phone number or email address that Messages recognizes.
`send()` returns `None` after the AppleScript transport succeeds. A failure
raises `MessageSendError` with `recipient` and a closed `reason` value:
`"delivery"` or `"transport"`.

## Common tasks

### Send later

```python
client.send("+15555550123", "This sends in one minute.", delay_seconds=60)
```

The delay must be a non-negative integer.

### Reuse a message template

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

### Send to several recipients

```python
recipients = ["+15555550123", "+15555550124"]
result = client.send_bulk(recipients, "The build is ready.")

print(result.sent)
print(result.failed)
```

`send_bulk()` sends sequentially in input order and returns the immutable
`BulkSendResult(sent, failed)`. Tuple unpacking also works:
`sent, failed = result`.

### Replace the delivery effect

Inject a `MessageTransport` for tests or another local delivery mechanism. The
transport receives one immutable `SendRequest`:

```python
from macpymessenger import IMessageClient, SendRequest


class RecordingTransport:
    def __init__(self) -> None:
        self.requests: list[SendRequest] = []

    def send(self, request: SendRequest) -> None:
        self.requests.append(request)


transport = RecordingTransport()
client = IMessageClient(transport=transport)
client.send("+15555550123", "Recorded, not sent.")
```

### Use application logging

macpymessenger emits through Python logging but never adds output handlers, sets
levels, chooses formats, or creates files:

```python
import logging

logging.basicConfig(filename="messages.log", level=logging.INFO)
client = IMessageClient()
```

Delivery logs may include recipient handles but never message bodies. The host
application owns destinations, access, and retention.

## Private-data boundary

The built-in transport invokes fixed argv `('/usr/bin/osascript', '-')` and
streams encoded AppleScript through stdin. Recipient and message text do not
enter process arguments or temporary files. Transport exceptions and child
output do not cross the public error boundary.

## Scope

Use macpymessenger when code running on your Mac needs to send text through your
existing Messages account. The package deliberately does not read chat history,
send attachments, resolve contacts, expose a remote API, run a messaging server,
or provide an MCP server.

## Documentation

- [Install and prepare your Mac](https://macpymessenger.readthedocs.io/en/latest/installation.html)
- [Check your environment](https://macpymessenger.readthedocs.io/en/latest/guides/environment-diagnostics.html)
- [Send messages](https://macpymessenger.readthedocs.io/en/latest/guides/sending-messages.html)
- [Use t-string templates](https://macpymessenger.readthedocs.io/en/latest/guides/templates.html)
- [Use a custom transport](https://macpymessenger.readthedocs.io/en/latest/api/transport.html)
- [Configure logging](https://macpymessenger.readthedocs.io/en/latest/guides/logging.html)
- [Troubleshoot a failed send](https://macpymessenger.readthedocs.io/en/latest/guides/troubleshooting.html)
- [Browse the public API](https://macpymessenger.readthedocs.io/en/latest/modules.html)
- [Contribute](https://macpymessenger.readthedocs.io/en/latest/development/contributing.html)
- [Read the changelog](https://github.com/ethan-wickstrom/macpymessenger/blob/main/CHANGELOG.md)

## Project status

macpymessenger is alpha software. Text messages, t-string templates, delayed
sends, sequential bulk sends, typed errors, custom transports, and read-only
environment diagnostics are supported.

macpymessenger is licensed under [Apache-2.0](https://github.com/ethan-wickstrom/macpymessenger/blob/main/LICENSE).
It is maintained by [Ethan Wickstrom](https://github.com/ethan-wickstrom) and
started as a fork of [Rolstenhouse/py-iMessage](https://github.com/Rolstenhouse/py-iMessage).
