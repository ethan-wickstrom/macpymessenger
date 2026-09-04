.. meta::
   :description lang=en:
      Send text through the local macOS Messages app from typed Python, shell
      scripts, or AI agents with validated requests and structured outcomes.

macpymessenger
==============

macpymessenger sends text through the built-in Messages app on a Mac you control.
It provides a typed Python API, a validation-safe command line, version-matched
Agent Skills, Python 3.14 t-string templates, structured failures, passive
logging, and side-effect-free environment diagnostics. The package has no
runtime dependencies.

You need macOS, Python 3.14 or newer, an Apple account signed in to Messages,
and Automation permission for the application that launches Python. The first
real send may ask Terminal, an editor, or an agent host for permission to control
Messages.

Install and inspect the Mac
---------------------------

Add the package to a uv project and run the side-effect-free doctor:

.. code-block:: bash

   uv add macpymessenger
   uv run macpymessenger doctor

The doctor reports definite blockers and manual checks. A clean result means no
automated blocker was found; it does not prove Messages sign-in, Automation
permission, or recipient delivery.

Send from Python
----------------

.. code-block:: python

   from macpymessenger import IMessageClient, MessageSendError

   client = IMessageClient()

   try:
       client.send("+15555550123", "Hello from Python!")
   except MessageSendError as error:
       print(f"Local send failed: {error.reason}")

``send()`` returns after the local transport completes. This result is not a
delivery receipt from the recipient's device. Build a validated immutable
``SendRequest`` and call ``send_request()`` when another layer creates or queues
work before it owns the client.

Use the command from an agent
-----------------------------

Load the instructions bundled with the installed package:

.. code-block:: bash

   uv run macpymessenger skills get core

Validate one closed request without creating a client or sending:

.. code-block:: bash

   cat <<'JSON' | uv run macpymessenger send --dry-run --json
   {"recipient":"<recipient>","message":"<message>","delay_seconds":0}
   JSON

Every JSON command uses one versioned envelope. A dry run returns
``data.outcome == "validated"``. A real-send success returns
``data.outcome == "transport_completed"``, not proof of recipient delivery.
Failed or uncertain sends must not be retried automatically because a retry may
create a duplicate message.

Understand the boundary
-----------------------

The built-in transport invokes fixed ``/usr/bin/osascript -`` arguments and
streams encoded AppleScript through standard input. Recipient and message text
do not enter process arguments, environment variables, or temporary files. Raw
child output does not cross the public error boundary.

The package deliberately does not read chat history, send attachments, resolve
contacts, expose a remote API, manage a Messages account, provide delivery
receipts, or run an MCP server.

Start with a task
-----------------

.. toctree::
   :maxdepth: 2
   :caption: Start here

   introduction
   installation
   usage

.. toctree::
   :maxdepth: 2
   :caption: Guides

   guides/command-line
   guides/environment-diagnostics
   guides/sending-messages
   guides/templates
   guides/logging
   guides/troubleshooting

.. toctree::
   :maxdepth: 2
   :caption: API reference

   modules
   api/client
   api/transport
   api/templates
   api/exceptions
   api/diagnostics

.. toctree::
   :maxdepth: 2
   :caption: Project

   development/contributing
   development/testing
   development/release-process

Search and agent indexes
------------------------

- :download:`llms.txt <llms.txt>` — curated task, guide, API, and repository
  links for agents and retrieval systems.
- ``searchindex.js`` — Sphinx search data in the built documentation.
