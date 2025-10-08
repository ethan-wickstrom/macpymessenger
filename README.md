# macpymessenger

macpymessenger is a modern, strongly typed Python toolkit for orchestrating macOS iMessage automation through AppleScript. The library focuses on clear composition, predictable data flow, and modular design so that message sending, template management, and configuration remain easy to reason about and extend.

## Features

- Deterministic `Configuration` that validates the packaged AppleScript before use.
- Composable `TemplateManager` powered by Jinja2 with in-memory storage for safe inheritance and inclusion.
- Dependency-injected `IMessageClient` that isolates subprocess execution for straightforward testing.
- Type-driven API surface with explicit error handling and no hidden global state.

## Installation

macpymessenger is published on PyPI. You can install it with [Astral's `uv`](https://docs.astral.sh/uv/) (recommended) or with `pip`.

```bash
uv pip install macpymessenger
# or
pip install macpymessenger
```

The package targets Python 3.10 and newer.

## Quick start

```python
from macpymessenger import Configuration, IMessageClient, TemplateManager

configuration = Configuration()
client = IMessageClient(configuration)

client.create_template("welcome", "Hello, {{ name }}! Welcome aboard.")
client.send_template("+15555555555", "welcome", {"name": "Ada"})
```

Templates are stored in-memory and rendered via Jinja2. They support inheritance and inclusion without touching the filesystem unless you opt into loading a directory of templates.

## Configuration

```python
from pathlib import Path
from macpymessenger import Configuration

configuration = Configuration(Path("/path/to/custom/sendMessage.scpt"))
```

`Configuration` will raise `ScriptNotFoundError` if the AppleScript is missing, keeping runtime failures obvious. The [configuration guide](docs/configuration.rst) explains the readability validation in more detail and covers how to opt into the optional ``macpymessenger.log`` handler via ``IMessageClient(enable_file_logging=True)``.

## Development workflow

This repository is now managed with `uv`. The following commands assume you have `uv` installed:

```bash
uv sync              # install dependencies into the local virtual environment
uv run ruff check    # lint the codebase
uv run mypy          # static type analysis
uv run pytest        # run the automated tests
```

Each command runs inside the isolated environment declared in `pyproject.toml`, ensuring reproducible tooling without polluting the global interpreter.

## License

macpymessenger is available under the [Apache 2.0 license](LICENSE).
