Configuration
=============

``Configuration`` tells the client which AppleScript to run and checks that the
script can be used.

Use the bundled AppleScript
---------------------------

The default configuration uses the AppleScript packaged with macpymessenger.

.. code-block:: python

   from macpymessenger import Configuration, IMessageClient

   client = IMessageClient(Configuration())

This is the right choice for most users.

Use a custom AppleScript path
-----------------------------

Pass ``send_script_path`` when you need your own script.

.. code-block:: python

   from pathlib import Path
   from macpymessenger import Configuration, IMessageClient

   config = Configuration(send_script_path=Path("/path/to/custom/sendMessage.scpt"))
   client = IMessageClient(config)

``Configuration`` validates the path during initialization. If the file is missing or unreadable, it raises ``ScriptNotFoundError``.

Enable file logging
-------------------

File logging is off by default. Turn it on to write client events to disk.

.. code-block:: python

   from macpymessenger import Configuration, FileLoggingConfiguration, IMessageClient

   client = IMessageClient(Configuration(), file_logging=FileLoggingConfiguration())

This writes ``macpymessenger.log`` in the current working directory.

Choose a log file path
----------------------

Pass a path to ``FileLoggingConfiguration`` for a different file.

.. code-block:: python

   from pathlib import Path
   from macpymessenger import Configuration, FileLoggingConfiguration, IMessageClient

   logging_config = FileLoggingConfiguration(path=Path("logs/messages.log"))
   client = IMessageClient(Configuration(), file_logging=logging_config)

If the file handler cannot be created, the client raises ``ConfigurationError``.

Pass your own logger
--------------------

Use a custom logger when your app already owns logging.

.. code-block:: python

   import logging
   from macpymessenger import Configuration, IMessageClient

   logger = logging.getLogger("my_app.messages")
   logger.setLevel(logging.INFO)

   client = IMessageClient(Configuration(), logger=logger)

The client uses the logger you pass and does not remove your handlers.

Combine custom logging options
------------------------------

You can pass both ``logger`` and ``file_logging``. If the logger does not already have a file handler, the client adds one.

.. code-block:: python

   import logging
   from macpymessenger import Configuration, FileLoggingConfiguration, IMessageClient

   logger = logging.getLogger("my_app.messages")

   client = IMessageClient(
       Configuration(),
       logger=logger,
       file_logging=FileLoggingConfiguration(),
   )
