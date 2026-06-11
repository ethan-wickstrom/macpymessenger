# macpymessenger

macpymessenger sends iMessages from Python on macOS.

It talks to the built-in Messages app through AppleScript, and adds Python 3.14 t-string templates and typed errors.

## Features

- Send iMessages to phone numbers or email addresses from Python.
- Use Python 3.14 t-strings for message templates.
- Send the same message to many recipients.
- Delay a send with `delay_seconds`.
- Handle delivery, delay, template, and configuration errors explicitly.
- Opt in to file logging when you want a local log file.

## Requirements

macpymessenger requires macOS and Python 3.14 or newer.

It uses AppleScript, so it is not a cross-platform messaging gateway. It sends through the Messages app on the Mac that runs your script.

## Installation

Add macpymessenger to a project with `uv`:

```bash
uv add macpymessenger
```

Or with `pip`:

```bash
pip install macpymessenger
```

## Quick start

```python
from macpymessenger import Configuration, IMessageClient
from macpymessenger.exceptions import MessageSendError

client = IMessageClient(Configuration())

try:
    client.send("+15555555555", "Hello from macpymessenger!")
except MessageSendError as error:
    print(f"Delivery failed: {error}")
```

`send()` returns `None` on success and raises `MessageSendError` when delivery fails.

You can also wait before sending:

```python
client.send("+15555555555", "I will arrive soon.", delay_seconds=60)
```

`delay_seconds` must be a non-negative `int`.

## Templates

Templates are Python callables that return Python 3.14 t-strings. Jinja2 is not used, and there is no `templates/` directory.

```python
client.create_template(
    "welcome",
    lambda name: t"Hello, {name}! Welcome aboard.",
)

client.send_template("+15555555555", "welcome", {"name": "Ada"})
```

Every interpolation must resolve to a `str`, or rendering raises `TemplateTypeError`.

## Bulk sending

```python
numbers = ["+15555555555", "+15555555556", "+15555555557"]
successful, failed = client.send_bulk(numbers, "Reminder: meeting at 10 AM.")

print(f"Sent: {successful}")
print(f"Failed: {failed}")
```

`send_bulk()` returns two lists: successful recipients and failed recipients.

## Configuration and logging

macpymessenger uses the bundled AppleScript by default. To use your own:

```python
from pathlib import Path
from macpymessenger import Configuration, IMessageClient

configuration = Configuration(send_script_path=Path("/path/to/custom/sendMessage.scpt"))
client = IMessageClient(configuration)
```

`Configuration` checks at creation that the script exists and is readable, and raises `ScriptNotFoundError` if not.

File logging is opt-in:

```python
from macpymessenger import Configuration, FileLoggingConfiguration, IMessageClient

client = IMessageClient(Configuration(), file_logging=FileLoggingConfiguration())
```

This writes `macpymessenger.log` in the current working directory. You can also pass your own `logging.Logger` to `IMessageClient`.

## Public API

These classes are importable from the package root:

```python
from macpymessenger import (
    Configuration,
    FileLoggingConfiguration,
    IMessageClient,
    RenderedTemplate,
    SubprocessCommandRunner,
    TemplateManager,
)
```

Custom exceptions live in `macpymessenger.exceptions`.

## Development

Install development dependencies:

```bash
uv sync
```

Run the checks:

```bash
uv run ruff check
uv run ty check
uv run pytest
uv build
uv run sphinx-build docs docs/_build/html
```

## License

macpymessenger is available under the [Apache-2.0 license](LICENSE).

## Credits

Created and maintained by [Ethan Wickstrom](https://github.com/ethan-wickstrom).

macpymessenger started as a fork of [Rolstenhouse/py-iMessage](https://github.com/Rolstenhouse/py-iMessage).

For more detail, see the [docs](docs/) directory.
