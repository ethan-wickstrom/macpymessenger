About macpymessenger
====================

macpymessenger is a small Python library for sending iMessages from a Mac you
control. Your Python program calls AppleScript, and AppleScript asks the local
Messages app to send the text.

Choose it when
--------------

- your automation already runs on a Mac;
- the Messages account on that Mac can reach each recipient;
- you want typed Python errors instead of command status strings; or
- you want reusable messages built with Python 3.14 t-strings.

Choose another tool when
------------------------

- your code runs on Linux, Windows, or a hosted server without a Mac;
- you need a supported business messaging gateway or delivery receipts;
- you need attachments or chat history; or
- you cannot grant the Python launcher permission to control Messages.

What is supported
-----------------

The library sends text to one or several phone numbers or iMessage email
addresses. It can delay a send, render in-memory t-string templates, and emit
operational logs. It uses the bundled AppleScript unless you select another
file.

Delivery failures raise ``MessageSendError``. Invalid delays, configuration
problems, and template problems have their own exception types.

What is not supported
---------------------

The library is not a hosted service and does not work around Messages or macOS
permissions. ``send_with_attachment()`` and ``get_chat_history()`` are
placeholders that always raise ``NotImplementedError``.

Next step
---------

Read :doc:`installation`, then :doc:`guides/sending-messages`.
