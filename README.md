# macpymessenger

[![PyPI](https://img.shields.io/pypi/v/macpymessenger.svg)](https://pypi.org/project/macpymessenger/)
[![Python](https://img.shields.io/pypi/pyversions/macpymessenger.svg)](https://pypi.org/project/macpymessenger/)
[![CI](https://github.com/ethan-wickstrom/macpymessenger/actions/workflows/ci.yml/badge.svg)](https://github.com/ethan-wickstrom/macpymessenger/actions/workflows/ci.yml)
[![Documentation](https://readthedocs.org/projects/macpymessenger/badge/?version=latest)](https://macpymessenger.readthedocs.io/en/latest/)

Send iMessages from Python on macOS with the built-in Messages app.

macpymessenger is a small, typed library for local scripts, automations,
developer tools, and agents. It uses AppleScript to control Messages on the Mac
that runs your Python program. It has no runtime dependencies, supports Python
3.14 t-string templates, and raises explicit errors that callers can handle.

> **Before you start:** You need macOS, Python 3.14 or newer, an Apple account
> signed in to Messages, and Automation permission for the application that
> launches Python. The first send may ask to let Terminal, your editor, or
> another launcher control Messages. Allow access, or review it in **System
> Settings > Privacy & Security > Automation**. macpymessenger is not a hosted
> service and cannot send from Linux or Windows.

## Install

```bash
uv add macpymessenger
```

You can also use `pip install macpymessenger`.

Check local requirements without sending a message:

```bash
macpymessenger doctor
```

Use `macpymessenger doctor --json` from scripts and agents.

## Send your first message

```python
from macpymessenger import IMessageClient, MessageSendError

client = IMessageClient()

try:
    client.send("+15555550123", "Hello from Python!")
except MessageSendError as error:
    print(f"Could not send to {error.recipient}: {error}")
```

Replace the example number with a phone number or email address that Messages
can reach. `send()` returns `None` after the AppleScript command succeeds. It
raises `MessageSendError` when the command cannot start or Messages reports a
failure. The error exposes `recipient` and `reason` fields.

## Common tasks

### Send later

```python
client.send("+15555550123", "This sends in one minute.", delay_seconds=60)
```

The delay must be a non-negative integer.

### Reuse a message template

Templates are functions that return Python 3.14 t-strings:

```python
client.create_template("welcome", lambda name: t"Hello, {name}!")
client.send_template(
    "+15555550123",
    "welcome",
    {"name": "Ada"},
)
```

Every interpolated result must be a string. Context values may use other types
when the template converts them before interpolation or uses them only for
control flow. macpymessenger does not use Jinja2 or template files.

### Send to several recipients

```python
recipients = ["+15555550123", "+15555550124"]
result = client.send_bulk(recipients, "The build is ready.")

print(result.sent)
print(result.failed)
```

`send_bulk()` sends in input order and returns `BulkSendResult(sent, failed)`.
Existing tuple unpacking remains valid: `sent, failed = result`.

### Use application logging

macpymessenger emits through Python logging but does not add output handlers,
set levels, choose formats, or create log files:

```python
import logging

logging.basicConfig(filename="messages.log", level=logging.INFO)
client = IMessageClient()
```

Delivery logs include recipient handles. The host application owns access and
retention policy.

## Scope

Use macpymessenger when code running on your Mac needs to send text through your
existing Messages account. The package deliberately does not read chat history,
send attachments, resolve contacts, expose a remote API, run a messaging server,
or provide an MCP server. A narrow surface keeps installation, testing, and
failure handling predictable.

## Documentation

- [Install and prepare your Mac](https://macpymessenger.readthedocs.io/en/latest/installation.html)
- [Check your environment](https://macpymessenger.readthedocs.io/en/latest/guides/environment-diagnostics.html)
- [Send messages](https://macpymessenger.readthedocs.io/en/latest/guides/sending-messages.html)
- [Use t-string templates](https://macpymessenger.readthedocs.io/en/latest/guides/templates.html)
- [Configure logging](https://macpymessenger.readthedocs.io/en/latest/guides/logging.html)
- [Troubleshoot a failed send](https://macpymessenger.readthedocs.io/en/latest/guides/troubleshooting.html)
- [Browse the public API](https://macpymessenger.readthedocs.io/en/latest/modules.html)
- [Contribute](https://macpymessenger.readthedocs.io/en/latest/development/contributing.html)
- [Read the changelog](https://github.com/ethan-wickstrom/macpymessenger/blob/main/CHANGELOG.md)

## Project status

macpymessenger is alpha software. Text messages, t-string templates, delayed
sends, bulk sends, typed errors, and read-only environment diagnostics are
supported.

macpymessenger is licensed under [Apache-2.0](https://github.com/ethan-wickstrom/macpymessenger/blob/main/LICENSE).
It is maintained by [Ethan Wickstrom](https://github.com/ethan-wickstrom) and
started as a fork of [Rolstenhouse/py-iMessage](https://github.com/Rolstenhouse/py-iMessage).
