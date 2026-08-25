.. meta::
   :description lang=en:
      Send one or many iMessages from Python on macOS, delay delivery, and handle
      typed macpymessenger errors and bulk results.

Send messages
=============

Create one client and reuse it for each send. The default constructor uses the
AppleScript bundled in the package.

Send one message
----------------

.. code-block:: python

   from macpymessenger import IMessageClient, MessageSendError

   client = IMessageClient()

   try:
       client.send("+15555550123", "The report is ready.")
   except MessageSendError as error:
       print(f"Could not send to {error.recipient}: {error}")

The recipient can be a phone number or email address that Messages recognizes.
``send()`` returns ``None`` when the AppleScript command succeeds. It raises
``MessageSendError`` when the command cannot start or Messages reports failure.
The exception exposes ``recipient`` and ``reason`` fields, so callers do not need
to parse its text.

Delay a send
------------

Set ``delay_seconds`` to a non-negative integer:

.. code-block:: python

   client.send("+15555550123", "One-minute reminder.", delay_seconds=60)

The bundled AppleScript waits before sending. A value below zero raises
``NegativeDelayError``. A non-integer value, including ``True``, raises
``InvalidDelayTypeError``.

Send to several recipients
---------------------------

.. code-block:: python

   recipients = ["+15555550123", "+15555550124", "+15555550125"]
   result = client.send_bulk(recipients, "The report is ready.")

   for recipient in result.failed:
       print(f"Retry later: {recipient}")

``send_bulk()`` sends in input order, catches ``MessageSendError`` for each
recipient, and returns ``BulkSendResult(sent, failed)``. The named fields make
result handling explicit. Existing tuple unpacking also works:

.. code-block:: python

   sent, failed = client.send_bulk(recipients, "The report is ready.")

Errors other than ``MessageSendError`` still propagate. Bulk sends do not accept
a delay.

Handle errors at the right boundary
-----------------------------------

Catch the narrowest error that your program can act on:

.. code-block:: python

   from macpymessenger import (
       InvalidDelayTypeError,
       MessageSendError,
       NegativeDelayError,
   )

   try:
       client.send("+15555550123", "Hello!", delay_seconds=10)
   except (InvalidDelayTypeError, NegativeDelayError):
       raise  # Fix the input or caller.
   except MessageSendError as error:
       print(f"Try {error.recipient} again later: {error.reason}")

For setup and permission failures, run :doc:`environment-diagnostics`, then use
:doc:`troubleshooting`.
