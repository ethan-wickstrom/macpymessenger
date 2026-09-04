.. meta::
   :description lang=en:
      Understand when to use macpymessenger for local Python and agent-driven
      iMessage sending on macOS and when to choose another messaging tool.

About macpymessenger
====================

macpymessenger is a small Python library and command-line tool for sending text
through the Messages app on a Mac you control. One validated immutable
``SendRequest`` crosses one replaceable ``MessageTransport``. The built-in
transport encodes private values, streams AppleScript through standard input,
and invokes fixed ``/usr/bin/osascript -`` arguments.

Choose it when
--------------

- your automation, developer tool, or agent already runs on a Mac;
- the signed-in Messages account can reach each recipient;
- you want a typed Python API with no runtime dependencies;
- you want one request model across Python, the CLI, transports, and tests;
- you want structured request, delivery, transport, and bulk outcomes;
- you want reusable messages built with Python 3.14 t-strings; or
- you want to replace the delivery effect without replacing client coordination.

Choose another tool when
------------------------

- your code runs on Linux, Windows, or a hosted server without a Mac;
- you need a supported business messaging gateway, delivery receipts, or scale;
- you need attachments, chat history, message reading, or contact lookup; or
- you cannot grant the Python launcher permission to control Messages.

What is supported
-----------------

The stable client sends text to one or several phone numbers or Messages email
addresses. It can validate and pass prebuilt requests unchanged, delay one send,
render in-memory t-string templates, retain typed sequential bulk failures, emit
standard Python logging records, and report local blockers without side effects.

``IMessageClient()`` uses ``AppleScriptTransport``. Tests and alternate local
integrations can inject ``MessageTransport``. Request validation raises
structured input errors. Delivery failures raise ``MessageSendError`` with
``recipient`` and ``reason`` fields.

The command line accepts one closed JSON request on standard input. It can
validate without creating a client through ``send --dry-run`` and returns one
versioned JSON envelope for agents and scripts.

What success means
------------------

A successful Python send or real CLI send means the local AppleScript transport
completed. It is not a delivery receipt from the recipient's device. A failed or
uncertain send must not be retried automatically because the package has no
idempotency key and a retry may create a duplicate message.

What is not supported
---------------------

macpymessenger does not expose methods for attachments, chat history, contact
lookup, message reading, remote gateways, account management, delivery receipts,
or MCP. The stable API contains only capabilities the package implements.

Next step
---------

Read :doc:`installation`, run :doc:`guides/environment-diagnostics`, then choose
:doc:`guides/sending-messages` or :doc:`guides/command-line`.
