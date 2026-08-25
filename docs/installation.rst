Install and prepare your Mac
============================

Check the requirements
----------------------

You need:

- macOS;
- Python 3.14 or newer; and
- an Apple account signed in to the Messages app.

The package may install on another operating system, but it cannot send there.
It controls the local Messages app through AppleScript.

Install the package
-------------------

Use uv in a project:

.. code-block:: bash

   uv add macpymessenger

Or use pip in an active virtual environment:

.. code-block:: bash

   python -m pip install macpymessenger

Check the installation
----------------------

.. code-block:: bash

   python -c "import macpymessenger; print(macpymessenger.__name__)"

This confirms that Python can import the package. It does not send a message.

Prepare Messages
----------------

#. Open Messages.
#. Sign in and send a message by hand.
#. Run the quick-start example in :doc:`guides/sending-messages`.
#. If macOS asks whether your terminal or Python can control Messages, allow it.

You can review this access in **System Settings > Privacy & Security >
Automation**. Permission belongs to the application that launches Python. For
example, Terminal and an editor may need separate permission.

Next step
---------

Follow :doc:`guides/sending-messages` to send a message and handle failures. If
setup does not work, use :doc:`guides/troubleshooting`.
