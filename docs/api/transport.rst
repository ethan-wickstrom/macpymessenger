.. meta::
   :description lang=en:
      API reference for validated immutable SendRequest values, custom
      MessageTransport implementations, and AppleScriptTransport.

Transport API
=============

SendRequest
-----------

``SendRequest`` is the single value that crosses the delivery effect boundary.
It is frozen and slotted, so a transport cannot observe later caller mutation.
The Python client, command line, custom transports, and tests all use the same
shape.

Construction validates every request field before an effect runs:

- ``recipient`` and ``message`` are non-empty strings that can be encoded as
  UTF-8;
- ``delay_seconds`` is an integer but not a boolean; and
- ``delay_seconds`` is zero or greater.

Use ``IMessageClient.send_request(request)`` to pass a prebuilt request without
reconstructing it.

.. autoclass:: macpymessenger.SendRequest
   :members:
   :no-private-members:
   :no-special-members:

MessageTransport
----------------

A transport owns the effect of sending one request. Tests and alternate local
integrations can implement this protocol without reproducing client
coordination, request validation, template rendering, bulk classification,
logging, or error mapping.

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
   request = SendRequest("+15555550123", "Recorded, not sent.")
   client.send_request(request)

AppleScriptTransport
--------------------

``AppleScriptTransport`` is the production default. It invokes fixed argv
``('/usr/bin/osascript', '-')`` and streams a complete script through standard
input. Recipient and message text are base64-encoded inside that script, so
private values do not enter process arguments or temporary files. Child output
is captured inside the transport and does not cross the public error boundary.

.. autoclass:: macpymessenger.AppleScriptTransport
   :members: send
   :no-private-members:
   :no-special-members:
