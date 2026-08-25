.. meta::
   :description lang=en:
      Understand when to use macpymessenger for local Python iMessage sending on
      macOS and when to choose another messaging tool.

About macpymessenger
====================

macpymessenger is a small Python library for sending text through the Messages
app on a Mac you control. Python passes a prepared argument list to
``osascript``; the bundled AppleScript asks Messages to send the text.

Choose it when
--------------

- your automation, developer tool, or agent already runs on a Mac;
- the signed-in Messages account can reach each recipient;
- you want a typed Python API with no runtime dependencies;
- you want explicit delivery, delay, configuration, and template failures; or
- you want reusable messages built with Python 3.14 t-strings.

Choose another tool when
------------------------

- your code runs on Linux, Windows, or a hosted server without a Mac;
- you need a supported business messaging gateway, delivery receipts, or scale;
- you need attachments, chat history, message reading, or contact lookup; or
- you cannot grant the Python launcher permission to control Messages.

What is supported
-----------------

The stable client sends text to one or several phone numbers or iMessage email
addresses. It can delay one send, render in-memory t-string templates, classify
bulk outcomes, emit standard Python logging records, and report local readiness
without side effects.

``IMessageClient()`` uses the bundled AppleScript. Delivery failures raise
``MessageSendError`` with structured ``recipient`` and ``reason`` fields.

What is not supported
---------------------

macpymessenger does not expose methods for attachments, chat history, contact
lookup, message reading, a remote gateway, or MCP. The stable API contains only
capabilities the package implements.

Next step
---------

Read :doc:`installation`, run :doc:`guides/environment-diagnostics`, then follow
:doc:`guides/sending-messages`.
