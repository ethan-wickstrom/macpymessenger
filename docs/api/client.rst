.. meta::
   :description lang=en:
      API reference for sending iMessages from Python with IMessageClient and
      immutable BulkSendResult values on macOS.

Client API
==========

IMessageClient
--------------

Create ``IMessageClient()`` for the built-in AppleScript transport. Inject
keyword-only collaborators when a test or host application owns the transport,
template store, or logger.

.. autoclass:: macpymessenger.IMessageClient
   :members: send, send_template, send_bulk, create_template, update_template, delete_template, logger
   :no-private-members:
   :no-special-members:

BulkSendResult
--------------

``send_bulk()`` returns immutable ``BulkSendResult(sent, failed)`` tuples. The
named fields are the primary interface, and tuple unpacking remains valid:

.. code-block:: python

   from macpymessenger import IMessageClient

   client = IMessageClient()
   recipients = ["+15555550123", "+15555550124"]
   result = client.send_bulk(recipients, "The build is ready.")

   print(result.sent)
   print(result.failed)

   sent, failed = result

.. autoclass:: macpymessenger.BulkSendResult
   :no-private-members:
   :no-special-members:

See :doc:`transport` for ``SendRequest``, ``MessageTransport``, and the built-in
``AppleScriptTransport``.
