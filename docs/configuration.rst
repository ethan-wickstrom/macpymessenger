Configuration
=============

**The `Configuration` class validates the AppleScript path and provides logging options.**

By default, the configuration uses the bundled AppleScript. You can customize the script path and logging behavior.

Use a custom AppleScript path
------------------------------

**By default, macpymessenger uses the bundled AppleScript at `osascript/sendMessage.scpt`.**

Provide a custom path if needed:

.. code-block:: python

   from pathlib import Path
   from macpymessenger import Configuration

   config = Configuration(send_script_path=Path("/path/to/custom/sendMessage.scpt"))

**The configuration validates the path at initialization.** If the file does not exist or is not readable, `Configuration` raises `ScriptNotFoundError`.

How validation works
--------------------

**The configuration validates the AppleScript at initialization, not at send time.**

Validation checks:

1. **File exists.** The path points to an existing file on disk.
2. **File is readable.** The process can open the file in binary mode.

**Validation raises `ScriptNotFoundError` if either check fails.** This keeps runtime execution of `osascript` predictable.

Enable file logging
-------------------

**By default, `IMessageClient` logs to the console only.**

Enable file logging to persist events to disk:

.. code-block:: python

   from macpymessenger import Configuration, IMessageClient

   config = Configuration()
   client = IMessageClient(config, enable_file_logging=True)

**This creates a `macpymessenger.log` file in the current directory.**

Provide a custom logger
------------------------

**Pass a pre-configured logger for custom destinations or formatting:**

.. code-block:: python

   import logging
   from macpymessenger import Configuration, IMessageClient

   logger = logging.getLogger("my_app")
   logger.setLevel(logging.DEBUG)
   # Add custom handlers here

   config = Configuration()
   client = IMessageClient(config, logger=logger)

**The client uses the logger's existing handlers.** It does not add or remove handlers automatically.
