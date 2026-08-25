.. meta::
   :description lang=en:
      Install macpymessenger on macOS, check Messages and AppleScript readiness,
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
can run there, but message delivery requires macOS, Messages, and ``osascript``.

Install the package
-------------------

Use uv in a project:

.. code-block:: bash

   uv add macpymessenger

Or use pip in an active virtual environment:

.. code-block:: bash

   python -m pip install macpymessenger

Check the installed wheel
-------------------------

Run the package diagnostic:

.. code-block:: bash

   macpymessenger doctor

This checks local requirements without opening Messages or sending a message.
Use ``macpymessenger doctor --json`` when a script or agent needs structured
output. See :doc:`guides/environment-diagnostics` for the result contract.

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

Follow :doc:`guides/sending-messages`. If the diagnostic passes but delivery
fails, use :doc:`guides/troubleshooting`.
