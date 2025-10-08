Modules
=======

**macpymessenger is organized into focused modules, each with a specific responsibility.**

This guide provides an overview of each module and its key classes.

client module — Send messages and manage templates
---------------------------------------------------

**The `client` module provides the main public interface.**

Key classes:

- **`IMessageClient`** — sends messages, manages templates, and handles errors
- **`SubprocessCommandRunner`** — executes AppleScript via subprocess

**The client wraps AppleScript execution and surfaces delivery failures through `MessageSendError`.**

configuration module — Validate AppleScript paths
--------------------------------------------------

**The `configuration` module defines the `Configuration` class.**

The `Configuration` class:

- Discovers the bundled AppleScript at `osascript/sendMessage.scpt`
- Validates that the script exists and is readable
- Allows custom script paths
- Provides logging configuration options

exceptions module — Define the error hierarchy
-----------------------------------------------

**The `exceptions` module defines all custom exceptions.**

Key exceptions:

- **`MessageSendError`** — raised when message delivery fails
- **`TemplateError`** — raised for template rendering or management issues
- **`TemplateNotFoundError`** — raised when a requested template does not exist
- **`DuplicateTemplateIdentifierError`** — raised when loading templates with duplicate identifiers
- **`ConfigurationError`** — raised for configuration validation failures
- **`ScriptNotFoundError`** — raised when the AppleScript file is missing or unreadable

templates module — Manage and render message templates
-------------------------------------------------------

**The `templates` module provides template management with Python 3.14 t-strings.**

Key classes:

- **`TemplateManager`** — stores callables that return t-strings, renders them, and enforces that all interpolations resolve to `str`
- **`RenderedTemplate`** — contains the rendered message after processing a t-string
- **`TemplateTypeError`** — raised when a template interpolation resolves to a non-string value

**Templates use callables instead of Jinja2 strings.** Each callable receives keyword arguments and returns a t-string. The manager raises `TemplateTypeError` if any interpolation is not a string.

Package root — Public API exports
----------------------------------

**The package root re-exports all public classes through `__all__`.**

Import from the package root:

.. code-block:: python

   from macpymessenger import IMessageClient, Configuration, TemplateManager
   from macpymessenger.exceptions import MessageSendError

**All primary classes are available at the top level.** You do not need to import from submodules.

osascript directory — AppleScript implementation
-------------------------------------------------

**The `osascript` directory contains the AppleScript that interacts with Messages.app.**

The bundled script:

- **`sendMessage.scpt`** — sends a text message to a recipient

**The `Configuration` class resolves the script path automatically.** You do not need to reference this directory unless you are providing a custom script.

Module architecture
-------------------

**Each module has a focused responsibility:**

- `client` — orchestrates message sending and template management
- `configuration` — validates AppleScript paths and provides logging options
- `exceptions` — defines the error hierarchy for explicit error handling
- `templates` — manages template storage and t-string rendering

**Understanding the module structure helps you navigate the codebase and extend functionality.**
