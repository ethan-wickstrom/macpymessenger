.. meta::
   :description lang=en:
      Check macOS, Messages, AppleScript, and package blockers before sending an
      iMessage with the macpymessenger doctor command.

Check your environment
======================

Run the doctor before the first send or when setup fails. In a uv project:

.. code-block:: bash

   uv run macpymessenger doctor

With an active virtual environment:

.. code-block:: bash

   macpymessenger doctor

The command is side-effect-free. It does not open Messages, invoke AppleScript,
request Automation access, read message data, or send text.

What the doctor checks
----------------------

The doctor can verify:

- the operating system is macOS;
- ``/usr/bin/osascript`` is executable;
- the Messages app exists in a standard location; and
- the AppleScript source bundled in the installed wheel is readable.

Automation permission and Messages account sign-in cannot be observed without
crossing the Messages effect boundary. The doctor reports those as manual checks
instead of claiming that the Mac is ready.

Read the result
---------------

Each check has one of three statuses:

``OK``
   The automated check passed.

``FAIL``
   A definite local blocker was found. The command exits with status ``1``.

``MANUAL``
   The state cannot be checked without a side effect. Complete the printed next
   step before sending.

The command exits with status ``0`` when no automated check fails. A zero exit
code means **no detectable blocker**, not **delivery is proven to work**.

Use JSON from scripts and agents
--------------------------------

Request stable machine-readable output:

.. code-block:: bash

   uv run macpymessenger doctor --json

Doctor output uses the versioned envelope shared by every JSON command. The
``data`` object contains aggregate blocker state, stable check identifiers,
statuses, summaries, and next steps:

.. code-block:: json

   {
     "command": "doctor",
     "data": {
       "blocked": false,
       "checks": [
         {
           "identifier": "platform",
           "next_step": null,
           "status": "ok",
           "summary": "macOS detected."
         },
         {
           "identifier": "automation",
           "next_step": "Run one send, then check System Settings > Privacy & Security > Automation.",
           "status": "manual",
           "summary": "Automation permission cannot be checked without sending an Apple event."
         }
       ]
     },
     "ok": true,
     "schema_version": 1,
     "tool": "macpymessenger",
     "version": "0.3.0"
   }

``ok`` is the inverse of ``data.blocked``. Neither field means that Messages
sign-in, Automation permission, or recipient delivery was verified. Show every
``manual`` check to a person or carry out its ``next_step`` before attempting a
send.

See :doc:`command-line` for the shared envelope and exit-code contract.
