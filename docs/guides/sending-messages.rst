Send messages
=============

Create one client and reuse it for each send.

Send one message
----------------

.. code-block:: python

   from macpymessenger import Configuration, IMessageClient
   from macpymessenger.exceptions import MessageSendError

   client = IMessageClient(Configuration())

   try:
       client.send("+15555550123", "The report is ready.")
   except MessageSendError as error:
       print(f"Could not send the message: {error}")

The recipient can be a phone number or email address that Messages recognizes.
``send()`` returns ``None`` when the command succeeds. It raises
``MessageSendError`` when AppleScript cannot run or Messages reports a failure.

Delay a send
------------

Set ``delay_seconds`` to a non-negative integer:

.. code-block:: python

   client.send("+15555550123", "One-minute reminder.", delay_seconds=60)

The AppleScript waits before it sends. A value below zero raises
``NegativeDelayError``. A non-integer value, including ``True``, raises
``InvalidDelayTypeError``.

Send to several recipients
---------------------------

.. code-block:: python

   recipients = ["+15555550123", "+15555550124", "+15555550125"]
   sent, failed = client.send_bulk(recipients, "The report is ready.")

   for recipient in failed:
       print(f"Retry later: {recipient}")

``send_bulk()`` sends to recipients one at a time. It catches
``MessageSendError`` for each recipient and returns ``(sent, failed)``. Other
errors are not added to ``failed`` and still propagate. Bulk sends do not accept
a delay.

Handle errors at the right boundary
-----------------------------------

Catch the narrowest error that your program can act on:

.. code-block:: python

   from macpymessenger.exceptions import (
       InvalidDelayTypeError,
       MessageSendError,
       NegativeDelayError,
   )

   try:
       client.send("+15555550123", "Hello!", delay_seconds=10)
   except (InvalidDelayTypeError, NegativeDelayError):
       raise  # This is a programming or input error.
   except MessageSendError as error:
       print(f"Try again later: {error}")

For setup and permission failures, see :doc:`troubleshooting`.
