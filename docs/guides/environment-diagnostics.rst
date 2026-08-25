.. meta::
   :description lang=en:
      Check macOS, Messages, AppleScript, and package readiness before sending
      an iMessage from Python with macpymessenger doctor.

Check your environment
======================

Run the doctor before the first send or when setup fails:

.. code-block:: bash

   macpymessenger doctor

The command is read-only. It does not open Messages, run AppleScript, request
Automation access, or send a message.

What the doctor checks
----------------------

The doctor can verify:

- the operating system is macOS;
- ``osascript`` is available;
- the Messages app exists in a standard location; and
- the AppleScript bundled in the installed wheel exists and is readable.

Automation permission and Messages account sign-in require the Messages app, so
the doctor reports those as manual checks instead of claiming to know their
state.

Read the result
---------------

Each check has one of three statuses:

``PASS``
   The local requirement is present.

``FAIL``
   A required local capability is missing. The command exits with status ``1``.

``INFO``
   The command cannot verify the state without causing a side effect. Follow the
   printed next step.

The command exits with status ``0`` when no required local check fails.

Use JSON from scripts and agents
--------------------------------

Request stable machine-readable output:

.. code-block:: bash

   macpymessenger doctor --json

The payload includes the package version, aggregate readiness, stable check
identifiers, statuses, summaries, and repair steps. Agents should use the JSON
fields rather than parse the human-readable output.

.. code-block:: json

   {
     "checks": [
       {
         "fix": null,
         "id": "platform",
         "status": "pass",
         "summary": "macOS detected."
       }
     ],
     "ready": true,
     "tool": "macpymessenger-doctor",
     "version": "0.3.0"
   }

A ready report proves only that the checks above passed. The first real send may
still prompt the launching application for Automation permission. See
:doc:`troubleshooting` for that flow.
