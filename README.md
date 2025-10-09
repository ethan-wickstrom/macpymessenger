# macpymessenger

A Python library for sending iMessages on macOS through AppleScript with template support and explicit error handling.

## Features

- Send iMessages to phone numbers or email addresses from Python scripts
- Create and manage message templates with Python 3.14 t-strings
- Send bulk messages to multiple recipients
- Type-safe interface with comprehensive error handling
- Configurable logging options
- macOS-only solution that works with the built-in Messages app

## Installation

macpymessenger requires Python 3.14 or newer and runs only on macOS.

Install from PyPI with `uv` (recommended):

```bash
uv add macpymessenger
```

Or with `pip`:

```bash
pip install macpymessenger
```

## Usage Examples

### Send a simple message

```python
from macpymessenger import Configuration, IMessageClient

configuration = Configuration()
client = IMessageClient(configuration)
client.send("+15555555555", "Hello from macpymessenger!")
```

### Using templates

```python
from string.templatelib import Template

# Create a template
client.create_template(
    "welcome",
    lambda name: t"Hello, {name}! Welcome aboard."
)

# Send a message using the template
client.send_template("+15555555555", "welcome", {"name": "Ada"})
```

### Send bulk messages

```python
numbers = ["+15551234567", "+15557654321", "+15558765432"]
successful, failed = client.send_bulk(numbers, "Reminder: Meeting at 10 AM.")

print(f"Successfully sent to: {successful}")
print(f"Failed to send to: {failed}")
```

## Configuration Options

### Custom AppleScript path

By default, macpymessenger uses the bundled AppleScript. You can provide a custom script path:

```python
from pathlib import Path
from macpymessenger import Configuration

configuration = Configuration(send_script_path=Path("/path/to/custom/sendMessage.scpt"))
client = IMessageClient(configuration)
```

### Enable file logging

```python
client = IMessageClient(configuration, enable_file_logging=True)
```

This creates a `macpymessenger.log` file in the current directory.

### Custom logger

```python
import logging
from macpymessenger import Configuration, IMessageClient

logger = logging.getLogger("my_app")
logger.setLevel(logging.DEBUG)
# Add custom handlers here

configuration = Configuration()
client = IMessageClient(configuration, logger=logger)
```

## Contribution Guidelines

We welcome contributions! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and ensure they follow the project's code style
4. Run tests and linting: `uv run pytest`, `uv run ruff check`, `uv run ty check`
5. Commit your changes with clear, descriptive messages
6. Push to your fork and submit a pull request

Please ensure your code follows the existing style and conventions. See the AGENTS.md file for detailed contribution guidelines.

## Testing Instructions

Install dependencies:

```bash
uv sync
```

Run the test suite:

```bash
uv run pytest
```

Run linting and type checking:

```bash
uv run ruff check    # lint
uv run ty check      # type checking
```

## License

macpymessenger is available under the [Apache 2.0 license](LICENSE).

## Acknowledgements/Credits

Created and maintained by [Ethan Wickstrom](https://github.com/ethan-wickstrom).

macpymessenger was originally forked from [Rolstenhouse/py-iMessage](https://github.com/Rolstenhouse/py-iMessage). I would like to express our gratitude to the developers of the libraries and tools used in this project, as well as the open-source community for their contributions.

This project uses AppleScript to interact with macOS's Messages application and Python 3.14's t-string feature for template rendering.

For more detailed documentation, see the [docs](docs/) directory.
