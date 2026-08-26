.. meta::
   :description lang=en:
      Public API map for macpymessenger clients, immutable send requests,
      transports, bulk results, t-string templates, diagnostics, and errors.

API reference
=============

Most programs need only ``IMessageClient`` and one or more specific exceptions.
The supported public API is available from ``macpymessenger``:

.. code-block:: python

   from macpymessenger import IMessageClient, MessageSendError

   client = IMessageClient()

Choose a reference page
-----------------------

- :doc:`api/client` — sending, templates, named bulk results, and logging.
- :doc:`api/transport` — immutable send requests and effect replacement.
- :doc:`api/templates` — t-string registration and Python formatting.
- :doc:`api/exceptions` — reachable failures and structured delivery errors.
- :doc:`api/diagnostics` — side-effect-free blocker and manual-check reports.

Supported scope
---------------

macpymessenger sends text through the local Messages app. Attachments, chat
history, message reading, contact lookup, a remote gateway, and an MCP server are
not part of the package. Unsupported capabilities do not occupy placeholder
methods on the stable client.
