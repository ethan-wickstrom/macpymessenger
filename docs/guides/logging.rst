Configure logging
=================

macpymessenger logs successful and failed delivery events. It does not write a
log file unless you ask it to.

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

   file_logging = FileLoggingConfiguration(path=Path("logs/messages.log"))
   client = IMessageClient(Configuration(), file_logging=file_logging)

The parent directory must already exist and be writable. Otherwise, client
creation raises ``ConfigurationError``.

Use your application's logger
------------------------------

.. code-block:: python

   import logging

   logger = logging.getLogger("example.messages")
   client = IMessageClient(Configuration(), logger=logger)

The client keeps your logger's level and handlers. You can also pass both a
logger and ``FileLoggingConfiguration``. The client adds a file handler only if
the logger does not already have one.

Protect recipient information
-----------------------------

Delivery logs include the recipient handle. Choose a protected log location,
limit access, and set a retention policy that fits your application.
