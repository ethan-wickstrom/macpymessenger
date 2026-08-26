.. meta::
   :description lang=en:
      API reference for macpymessenger SendRequest, MessageTransport, and the
      private-data-safe AppleScriptTransport.

Transport API
=============

SendRequest
-----------

``SendRequest`` is the single value that crosses the delivery effect boundary.
It is frozen and slotted, so a transport cannot observe later caller mutation.
Creating a request validates ``delay_seconds``.

.. autoclass:: macpymessenger.SendRequest
   :members:
   :no-private-members:
   :no-special-members:

MessageTransport
----------------

A transport owns the effect of sending one request. Tests and alternate local
integrations can implement this protocol without reproducing client
coordination, template rendering, bulk classification, logging, or error
mapping.

.. autoclass:: macpymessenger.MessageTransport
   :members: send
   :no-private-members:
   :no-special-members:

.. code-block:: python

   from macpymessenger import IMessageClient, SendRequest


   class RecordingTransport:
       def __init__(self) -> None:
           self.requests: list[SendRequest] = []

       def send(self, request: SendRequest) -> None:
           self.requests.append(request)


   transport = RecordingTransport()
   client = IMessageClient(transport=transport)
   client.send("+15555550123", "Recorded, not sent.")

AppleScriptTransport
--------------------

``AppleScriptTransport`` is the production default. It invokes fixed argv
``('/usr/bin/osascript', '-')`` and streams a complete script through stdin.
Recipient and message text are base64-encoded inside that script, so private
values do not enter process arguments or temporary files. Child output is
captured inside the transport.

.. autoclass:: macpymessenger.AppleScriptTransport
   :members: send
   :no-private-members:
   :no-special-members:
