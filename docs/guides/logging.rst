Configure logging
=================

macpymessenger emits successful and failed delivery events through Python's
``logging`` system. It does not create a log file unless you ask it to.
Delivery records include the recipient handle.

Write the default log file
--------------------------

.. code-block:: python

   from macpymessenger import (
       Configuration,
       FileLoggingConfiguration,
       IMessageClient,
   )

   client = IMessageClient(
       Configuration(),
       file_logging=FileLoggingConfiguration(),
   )

This writes ``macpymessenger.log`` in the current working directory.

Choose a path
-------------

.. code-block:: python

   from pathlib import Path

   from macpymessenger import (
       Configuration,
       FileLoggingConfiguration,
       IMessageClient,
   )

   file_logging = FileLoggingConfiguration(path=Path("logs/messages.log"))
   client = IMessageClient(Configuration(), file_logging=file_logging)

The parent directory must already exist and be writable. Otherwise, client
creation raises ``ConfigurationError``.

Use your application's logger
------------------------------

.. code-block:: python

   import logging

   from macpymessenger import Configuration, IMessageClient

   logger = logging.getLogger("example.messages")
   client = IMessageClient(Configuration(), logger=logger)

The client keeps your logger's level and handlers. You can also pass both a
logger and ``FileLoggingConfiguration``. The client adds a file handler only if
the logger does not already have one.

Understand the default logger
-----------------------------

If you do not pass a logger, the client uses the ``macpymessenger.client``
logger. When that logger has no handlers and no explicit level, the client sets
its level to ``INFO``. Records can then propagate to a root handler configured
by your application. File logging is opt-in; logging itself is not guaranteed
to be silent.

Protect recipient information
-----------------------------

Delivery logs include the recipient handle. Choose protected log destinations,
limit access, and set a retention policy that fits your application. If your
application configures root logging, account for propagated macpymessenger
records there too.
