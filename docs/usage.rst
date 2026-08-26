.. meta::
   :description lang=en:
      Task guide index for command-line agents, Python sending, diagnostics,
      templates, transports, logging, and troubleshooting on macOS.

Choose a task
=============

Use the smallest guide that answers the current question.

Use a shell script or AI agent
------------------------------

Read :doc:`guides/command-line` for:

- version-matched Agent Skill discovery;
- one closed JSON request on standard input;
- stable machine output and exit codes;
- private-data boundaries; and
- the no-automatic-retry rule.

Check your Mac
--------------

Read :doc:`guides/environment-diagnostics` to inspect macOS,
``/usr/bin/osascript``, Messages, and bundled package data without sending text.
Use its JSON output from scripts and agents.

Send from Python
----------------

Read :doc:`guides/sending-messages` to:

- send one text message;
- delay a send;
- classify several recipients with ``BulkSendResult``; and
- handle delivery, transport, and input failures.

Use templates
-------------

Read :doc:`guides/templates` to create, render, update, list, and delete reusable
Python 3.14 t-string templates with normal Python formatting.

Replace the delivery effect
---------------------------

Read :doc:`api/transport` to inject a ``MessageTransport`` for tests or another
local delivery mechanism. The rest of the client continues to own template
rendering, bulk classification, logging, and public error mapping.

Configure logging
-----------------

Read :doc:`guides/logging` to route generic delivery events through the host
application's Python logging setup. macpymessenger does not create handlers,
choose formats, or write log files itself.

Fix a problem
-------------

Read :doc:`guides/troubleshooting` for Automation permission, Messages account,
transport, installation, delay, command-input, and template failures.

Look up the API
---------------

Read :doc:`modules` when you know what you want to build and need a class,
method, result shape, diagnostic model, transport, or exception reference.
