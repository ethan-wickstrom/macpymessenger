# macpymessenger

Send iMessages from Python on macOS with the built-in Messages app.

macpymessenger is a small, typed Python library for local iMessage automation. It
uses AppleScript to control Messages on the Mac that runs your Python program,
has no runtime dependencies, supports Python 3.14 t-string templates, and raises
explicit errors that callers can handle.

> **Before you start:** You need macOS, Python 3.14 or newer, an Apple account
> signed in to Messages, and Automation permission for the application that
> launches Python. On the first send, macOS may ask to let Terminal, your editor,
> or another launcher control Messages. Allow access, or review it in **System
> Settings > Privacy & Security > Automation**. macpymessenger is not a hosted
> messaging service and cannot send from Linux or Windows.

## Install

```bash
uv add macpymessenger
```

You can also use `pip install macpymessenger`.

## Send your first message

```python
from macpymessenger import Configuration, IMessageClient
from macpymessenger.exceptions import MessageSendError

client = IMessageClient(Configuration())

try:
    client.send("+15555550123", "Hello from Python!")
except MessageSendError as error:
    print(f"Could not send the message: {error}")
```

Replace the example number with a phone number or email address that Messages
can reach. `send()` returns `None` after the AppleScript command succeeds. It
raises `MessageSendError` when AppleScript cannot run or Messages reports a
failure.

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

Every interpolated result must be a string. Context values can use other types
when the template converts them or uses them without interpolation. macpymessenger
does not use Jinja2 or template files.

### Send to several recipients

```python
recipients = ["+15555550123", "+15555550124"]
sent, failed = client.send_bulk(recipients, "The build is ready.")
```

`send_bulk()` sends one recipient at a time and returns the recipients that
succeeded and failed. It does not raise `MessageSendError` for an individual
failed send.

## What macpymessenger is for

Use macpymessenger when a Python script, local automation, developer tool, or
agent running on your Mac needs to send an iMessage through your existing
Messages account. The package deliberately stays narrow: it sends text messages
and does not expose chat history, attachments, a remote API, or a messaging
server.

## Documentation

- [Install and prepare your Mac](https://macpymessenger.readthedocs.io/en/latest/installation.html)
- [Send messages](https://macpymessenger.readthedocs.io/en/latest/guides/sending-messages.html)
- [Use t-string templates](https://macpymessenger.readthedocs.io/en/latest/guides/templates.html)
- [Configure logging](https://macpymessenger.readthedocs.io/en/latest/guides/logging.html)
- [Troubleshoot a failed send](https://macpymessenger.readthedocs.io/en/latest/guides/troubleshooting.html)
- [Browse the public API](https://macpymessenger.readthedocs.io/en/latest/modules.html)
- [Contribute](https://macpymessenger.readthedocs.io/en/latest/development/contributing.html)
- [Read the changelog](https://github.com/ethan-wickstrom/macpymessenger/blob/main/CHANGELOG.md)

## Project status

macpymessenger is alpha software. Text messages, t-string templates, delayed
sends, and bulk sends are supported. Attachments and chat history are not
implemented.

macpymessenger is licensed under [Apache-2.0](https://github.com/ethan-wickstrom/macpymessenger/blob/main/LICENSE).
It is maintained by [Ethan Wickstrom](https://github.com/ethan-wickstrom) and
started as a fork of [Rolstenhouse/py-iMessage](https://github.com/Rolstenhouse/py-iMessage).
