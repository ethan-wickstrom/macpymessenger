.. meta::
   :description lang=en:
      Public API map for macpymessenger clients, bulk send results, Python
      t-string templates, diagnostics, configuration, and typed errors.

API reference
=============

Most programs need only ``IMessageClient`` and one or more specific exceptions.
The supported public API is available from ``macpymessenger``:

.. code-block:: python

   from macpymessenger import IMessageClient, MessageSendError

   client = IMessageClient()

Choose a reference page
-----------------------

- :doc:`api/client` — sending, named bulk results, logging, and test injection.
- :doc:`api/configuration` — custom AppleScript paths for advanced callers.
- :doc:`api/templates` — t-string registration and string rendering.
- :doc:`api/exceptions` — reachable failures and structured delivery errors.
- :doc:`api/diagnostics` — read-only environment checks and report data.

Supported scope
---------------

macpymessenger sends text through the local Messages app. Attachments, chat
history, message reading, contact lookup, a remote gateway, and an MCP server are
not part of the package. Unsupported capabilities do not occupy placeholder
methods on the stable client.
