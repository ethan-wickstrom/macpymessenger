.. meta::
   :description lang=en:
      Send one or many iMessages from Python on macOS, validate immutable send
      requests, and handle typed delivery and bulk outcomes.

Send messages from Python
=========================

Create one client and reuse it. ``IMessageClient()`` owns the built-in
``AppleScriptTransport``. Shell scripts and agents should use
:doc:`command-line` instead of generating Python glue.

Send one message
----------------

.. code-block:: python

   from macpymessenger import IMessageClient, MessageSendError

   client = IMessageClient()

   try:
       client.send("+15555550123", "The report is ready.")
   except MessageSendError as error:
       print(f"Send failed for {error.recipient}: {error.reason}")

The recipient can be a phone number or email address that Messages recognizes.
``send()`` returns ``None`` after the local transport completes. This result is
not a delivery receipt from the recipient's device.

A failed send raises ``MessageSendError``. The exception exposes the private
``recipient`` for application logic and a closed ``reason`` value:

``"delivery"``
   AppleScript ran, but the script or Messages reported failure.

``"transport"``
   The operating system could not run the transport.

The exception message, traceback cause, and built-in logs omit the recipient,
message body, and child-process output.

Build and reuse a request
-------------------------

``SendRequest`` is the single validated value that crosses the delivery effect
boundary. Build one when a program validates or queues work before it owns a
client:

.. code-block:: python

   from macpymessenger import IMessageClient, SendRequest

   request = SendRequest(
       recipient="+15555550123",
       message="The report is ready.",
       delay_seconds=30,
   )

   client = IMessageClient()
   client.send_request(request)

``send_request()`` passes the same immutable request object to the transport.
``send()`` is the convenience form; it constructs ``SendRequest`` and delegates
to ``send_request()``.

Creating a request validates all three fields before an effect can run:

- ``recipient`` and ``message`` must be non-empty strings that can be encoded as
  UTF-8;
- ``delay_seconds`` must be an integer, not a boolean; and
- ``delay_seconds`` must be zero or greater.

Invalid text raises ``InvalidSendTextError`` with ``field`` set to
``"recipient"`` or ``"message"`` and ``reason`` set to ``"type"``, ``"empty"``,
or ``"encoding"``. Invalid delays raise ``InvalidDelayTypeError`` or
``NegativeDelayError``.

Delay a send
------------

Set ``delay_seconds`` to a non-negative integer:

.. code-block:: python

   client.send("+15555550123", "One-minute reminder.", delay_seconds=60)

The delay runs inside AppleScript immediately before Messages receives the send
request. It does not create a durable scheduled message. If the process or
Messages stops first, the message is not sent.

Send to several recipients
---------------------------

``send_bulk()`` snapshots the input iterable, sends sequentially in input order,
and retains each typed failure:

.. code-block:: python

   recipients = ["+15555550123", "+15555550124", "+15555550125"]
   result = client.send_bulk(recipients, "The report is ready.")

   if result.ok:
       print("Every local send request completed.")

   for failure in result.failures:
       print(f"{failure.recipient}: {failure.reason}")

``result.sent`` contains successful recipient strings. ``result.failures``
contains immutable ``BulkSendFailure(recipient, reason)`` values. The derived
``result.failed`` property returns only failed recipient strings for simpler
callers. Existing two-value unpacking also remains available:

.. code-block:: python

   sent, failed = client.send_bulk(recipients, "The report is ready.")

A bulk result preserves known local outcomes, not delivery receipts. Do not
automatically retry a failed or uncertain send; a retry may create a duplicate
message. Ask a person or apply an application-specific policy with that risk
made explicit.

``send_bulk()`` catches ``MessageSendError`` for each recipient. Request
validation errors and other exceptions still stop the operation. Bulk sends do
not accept a delay.

Handle errors at the right boundary
-----------------------------------

Catch the narrowest error that the program can act on:

.. code-block:: python

   from macpymessenger import (
       InvalidDelayTypeError,
       InvalidSendTextError,
       MessageSendError,
       NegativeDelayError,
   )

   try:
       client.send("+15555550123", "Hello!", delay_seconds=10)
   except (InvalidSendTextError, InvalidDelayTypeError, NegativeDelayError):
       raise  # Correct the request before retrying.
   except MessageSendError as error:
       print(f"Local send failed: {error.reason}")

For setup and permission failures, run :doc:`environment-diagnostics`, then use
:doc:`troubleshooting`.

Understand the private-data boundary
------------------------------------

The built-in transport carries recipient and message text in encoded AppleScript
sent through standard input. Private values do not enter process arguments,
environment variables, or temporary files. Built-in delivery logs contain only
generic outcomes.
