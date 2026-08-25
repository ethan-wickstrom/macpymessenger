# macpymessenger

Send an iMessage from Python on your Mac.

macpymessenger uses the Messages app and AppleScript. It has no runtime
dependencies. It supports Python 3.14 t-string templates and raises typed errors
that your code can handle.

> **Before you start:** You need macOS, Python 3.14 or newer, and an account
> signed in to Messages. macpymessenger is not a hosted messaging service and
> cannot send from Linux or Windows.

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
can reach. The first send may prompt you to let your terminal or Python control
Messages. Allow access in **System Settings > Privacy & Security > Automation**.

`send()` returns `None` after a successful send. It raises `MessageSendError`
if AppleScript cannot run or Messages cannot send the message.

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

Template values must be strings. macpymessenger does not use Jinja2 or template
files.

### Send to several recipients

```python
recipients = ["+15555550123", "+15555550124"]
sent, failed = client.send_bulk(recipients, "The build is ready.")
```

`send_bulk()` returns the recipients that succeeded and the recipients that
failed. It does not raise `MessageSendError` for an individual failed send.

## Learn more

- [Install and prepare your Mac](docs/installation.rst)
- [Choose a task guide](docs/usage.rst)
- [Troubleshoot a failed send](docs/guides/troubleshooting.rst)
- [Browse the public API](docs/modules.rst)
- [Set up a development environment](docs/development/contributing.rst)
- [Read the changelog](CHANGELOG.md)

## Project status

The project is alpha software. Text messages, t-string templates, delayed sends,
and bulk sends are supported. Attachments and chat history are not implemented.

macpymessenger is licensed under [Apache-2.0](LICENSE). It is maintained by
[Ethan Wickstrom](https://github.com/ethan-wickstrom) and started as a fork of
[Rolstenhouse/py-iMessage](https://github.com/Rolstenhouse/py-iMessage).
