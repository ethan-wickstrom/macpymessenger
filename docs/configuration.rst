.. meta::
   :description lang=en:
      Use macpymessenger with its bundled AppleScript or provide a custom send
      script through explicit Python configuration.

Configuration
=============

Most programs need no configuration. ``IMessageClient()`` uses the AppleScript
bundled in the installed package:

.. code-block:: python

   from macpymessenger import IMessageClient

   client = IMessageClient()

Use ``Configuration`` only when you maintain a custom AppleScript path or need
to inspect the resolved bundled path:

.. code-block:: python

   from pathlib import Path

   from macpymessenger import Configuration, IMessageClient

   configuration = Configuration(Path("scripts/sendMessage.scpt"))
   client = IMessageClient(configuration)

``Configuration`` checks that the script exists and is readable before a send.
See :doc:`api/configuration` for its API, :doc:`guides/environment-diagnostics`
for installation checks, and :doc:`guides/troubleshooting` for failures.
