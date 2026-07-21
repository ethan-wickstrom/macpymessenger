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

Route log events
----------------

The library emits events to ``logging.getLogger("macpymessenger...")`` behind
a ``NullHandler`` and never attaches handlers, sets levels, or chooses
formats. Configure standard :mod:`logging` in your application to see them.

.. code-block:: python

   import logging

   logging.basicConfig(
       filename="macpymessenger.log",
       level=logging.INFO,
       format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
   )

Pass your own logger
--------------------

Use a custom logger when your app already owns logging.

.. code-block:: python

   import logging
   from macpymessenger import Configuration, IMessageClient

   logger = logging.getLogger("my_app.messages")

   client = IMessageClient(Configuration(), logger=logger)

The client emits its events to the logger you pass and does not modify it.
