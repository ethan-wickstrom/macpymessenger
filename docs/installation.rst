.. meta::
   :description lang=en:
      Install macpymessenger on macOS, check Messages and AppleScript blockers,
      and prepare Automation permission for Python iMessage sending.

Install and prepare your Mac
============================

Check the requirements
----------------------

You need:

- macOS;
- Python 3.14 or newer;
- the built-in Messages app; and
- an Apple account signed in to Messages.

The wheel can be imported on another operating system so tests and type checks
can run there, but message delivery requires macOS, Messages, and
``/usr/bin/osascript``.

Install with uv
---------------

Add the package to a project, then run its command through the project
environment:

.. code-block:: bash

   uv add macpymessenger
   uv run macpymessenger doctor

Use ``uv run macpymessenger doctor --json`` when a script or agent needs
structured output.

Install with pip
----------------

Inside an active virtual environment:

.. code-block:: bash

   python -m pip install macpymessenger
   macpymessenger doctor

Understand the doctor result
----------------------------

The doctor checks definite local blockers without opening Messages, invoking
AppleScript, requesting permission, reading message data, or sending text. A
zero exit code means no automated blocker was found. It does not prove that the
Messages account is signed in or that the current launcher has Automation
permission; complete every ``MANUAL`` check before the first send.

See :doc:`guides/environment-diagnostics` for the text, JSON, and exit-code
contract.

Prepare Messages
----------------

#. Open Messages.
#. Sign in and send a message by hand.
#. Run the first-send example in :doc:`guides/sending-messages`.
#. If macOS asks whether the launching application can control Messages, allow it.

You can review access in **System Settings > Privacy & Security > Automation**.
Permission belongs to the application that launches Python, so Terminal, an
editor, a launcher, and an agent host may each need separate approval.

Next step
---------

Follow :doc:`guides/sending-messages`. If no automated blocker is found but
delivery fails, use :doc:`guides/troubleshooting`.
