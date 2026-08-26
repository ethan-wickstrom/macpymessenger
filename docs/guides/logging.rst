.. meta::
   :description lang=en:
      Configure macpymessenger delivery logs with Python standard library
      logging while keeping handlers, formats, and retention in your app.

Configure logging
=================

macpymessenger emits successful and failed delivery events through Python's
``logging`` package. The library does not set log levels, choose formats, write
files, or attach output handlers. The application owns those choices.

Use standard application logging
--------------------------------

Configure the root logger before creating a client:

.. code-block:: python

   import logging

   from macpymessenger import IMessageClient

   logging.basicConfig(
       filename="macpymessenger.log",
       level=logging.INFO,
       format="%(asctime)s %(name)s %(levelname)s %(message)s",
   )

   client = IMessageClient()

The default client logger is ``macpymessenger.client``. Its records propagate to
handlers configured by the host application. macpymessenger adds only a
``NullHandler`` to its top-level package logger, which prevents output when the
application has not configured logging.

Pass a caller-owned logger
--------------------------

Pass a logger when delivery events belong in a specific application namespace:

.. code-block:: python

   import logging

   from macpymessenger import IMessageClient

   logger = logging.getLogger("example.messages")
   client = IMessageClient(logger=logger)

The client uses the logger unchanged. It does not add handlers, set its level,
or change propagation.

Route only macpymessenger records
---------------------------------

Add a handler to the package namespace and disable propagation when the same
record must not also reach a root handler:

.. code-block:: python

   import logging

   logger = logging.getLogger("macpymessenger")
   logger.setLevel(logging.INFO)
   logger.addHandler(logging.StreamHandler())
   logger.propagate = False

Private data
------------

Built-in delivery records contain generic outcomes. They do not include the
recipient, message body, child-process output, or raw transport exception. A
caller-owned transport or logger can still add private data, so the host
application remains responsible for destinations, access, and retention.
