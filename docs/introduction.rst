Introduction
============

**macpymessenger sends iMessages from Python scripts on macOS.**

The library provides a type-safe interface to the Messages app through AppleScript, with template rendering powered by Python 3.14 t-strings. Send text messages to phone numbers or email addresses with explicit error handling and no hidden state.

Why use macpymessenger
----------------------

**Simple API.** Send a message in three lines of code. Define templates as callables that return t-strings.

**Explicit error handling.** All errors raise typed exceptions, including `TemplateTypeError` for non-string interpolation values.

**Testable design.** Dependency injection isolates subprocess calls from business logic. Write fast tests without executing AppleScript.

**Validated configuration.** The `Configuration` class checks that the AppleScript file exists and is readable at initialization, not at send time.

**Comprehensive type hints.** Every function includes type annotations. The codebase passes `mypy` strict mode.

What you can build
------------------

**Automated notifications.** Send alerts or reminders to users via iMessage when events occur in your application.

**Personalized campaigns.** Use templates to send customized messages to multiple recipients with variable substitution.

**Business process integration.** Trigger iMessages from workflows, approval processes, or monitoring systems.

**Custom applications.** Build tools that leverage iMessage for communication without requiring third-party APIs.

Next steps
----------

**Read the installation guide** to install macpymessenger with `uv` or `pip`.

**Follow the usage guide** to send your first message and learn about templates.

**Explore the configuration options** to customize logging and AppleScript paths.