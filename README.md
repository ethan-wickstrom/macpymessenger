# macpymessenger

**macpymessenger** is a Python library for sending iMessages on macOS through AppleScript.

The library provides a type-safe, testable interface for message automation with clear error handling and no hidden state.

## What macpymessenger provides

**Validated configuration.** The `Configuration` class checks that the packaged AppleScript exists and is readable before any messages are sent.

**Template management.** The `TemplateManager` stores callables that return Python 3.14 t-strings. Template rendering enforces that every interpolated value is a `str`, delivering strict type safety.

**Isolated subprocess execution.** The `IMessageClient` uses dependency injection to separate subprocess calls from business logic, making tests straightforward.

**Explicit error handling.** All errors raise typed exceptions. No boolean return values or hidden failures.

**Experimental APIs for future features.** Methods for chat history retrieval and attachment sending are defined but raise `NotImplementedError` until they are fully implemented.

## Installation

**macpymessenger requires Python 3.10 or newer and runs only on macOS.**

Install from PyPI with `uv` (recommended) or `pip`:

```bash
uv pip install macpymessenger
```

Or with `pip`:

```bash
pip install macpymessenger
```

## Quick start

Send a message in three lines:

```python
from macpymessenger import Configuration, IMessageClient

configuration = Configuration()
client = IMessageClient(configuration)
client.send("+15555555555", "Hello from macpymessenger!")
```

**Use templates for reusable messages:**

```python
from string.templatelib import Template

client.create_template(
    "welcome",
    lambda name: t"Hello, {name}! Welcome aboard."
)
client.send_template("+15555555555", "welcome", {"name": "Ada"})
```

Templates are defined as callables that return t-strings. The manager validates that all interpolated values are strings before rendering.

## Experimental features

**Two methods are defined but not yet implemented:**

- `IMessageClient.get_chat_history` — for retrieving message history
- `IMessageClient.send_with_attachment` — for sending files with messages

Both methods raise `NotImplementedError` with an "Experimental" prefix when called.

These methods exist to stabilize the API signature before the features ship in a future release. Do not call them in production code.

## Configuration

**By default, macpymessenger uses the bundled AppleScript.**

You can provide a custom script path if needed:

```python
from pathlib import Path
from macpymessenger import Configuration

configuration = Configuration(send_script_path=Path("/path/to/custom/sendMessage.scpt"))
```

**Configuration validates the script at initialization.** If the AppleScript file is missing or unreadable, `Configuration` raises `ScriptNotFoundError` immediately.

**Enable file logging if needed:**

```python
client = IMessageClient(configuration, enable_file_logging=True)
```

This creates a `macpymessenger.log` file in the current directory. See the [configuration guide](docs/configuration.rst) for details.

## Development

**macpymessenger uses `uv` for dependency management.**

Install dependencies:

```bash
uv sync
```

Run linters and tests:

```bash
uv run ruff check    # lint
uv run mypy          # type checking
uv run pytest        # tests
```

All commands run in an isolated environment defined by `pyproject.toml`.

## License

macpymessenger is available under the [Apache 2.0 license](LICENSE).
