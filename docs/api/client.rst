.. meta::
   :description lang=en:
      API reference for IMessageClient, prebuilt SendRequest delivery, and
      structured immutable bulk-send outcomes on macOS.

Client API
==========

IMessageClient
--------------

Create ``IMessageClient()`` for the built-in AppleScript transport. Inject
keyword-only collaborators when a test or host application owns the transport,
template store, or logger.

``send()`` is the shortest path. ``send_request()`` accepts the same immutable
``SendRequest`` data shape used by transports and the command line, so callers
do not need to decompose and rebuild validated work.

.. autoclass:: macpymessenger.IMessageClient
   :members: send, send_request, send_template, send_bulk, create_template,
      update_template, delete_template, logger
   :no-private-members:
   :no-special-members:

BulkSendFailure
---------------

Each failed bulk item keeps the recipient and the closed failure reason that a
single ``MessageSendError`` would expose.

.. autoclass:: macpymessenger.BulkSendFailure
   :members:
   :no-private-members:
   :no-special-members:

BulkSendResult
--------------

``send_bulk()`` returns an immutable ``BulkSendResult``. ``sent`` and
``failures`` are the authoritative ordered outcome data. ``failed`` projects
only recipient strings, and ``ok`` is true when ``failures`` is empty:

.. code-block:: python

   from macpymessenger import IMessageClient

   client = IMessageClient()
   recipients = ["+15555550123", "+15555550124"]
   result = client.send_bulk(recipients, "The build is ready.")

   print(result.sent)
   for failure in result.failures:
       print(failure.recipient, failure.reason)

   sent, failed = result

Two-value unpacking yields ``sent`` and the compatibility ``failed`` projection.
A success means the local transport completed; it is not a recipient delivery
receipt. Do not automatically retry failed or uncertain sends.

.. autoclass:: macpymessenger.BulkSendResult
   :members: failed, ok
   :no-private-members:
   :no-special-members:

See :doc:`transport` for ``SendRequest``, ``MessageTransport``, and the built-in
``AppleScriptTransport``.
