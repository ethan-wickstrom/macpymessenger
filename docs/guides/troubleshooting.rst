.. meta::
   :description lang=en:
      Fix macpymessenger setup, Automation permission, Messages delivery,
      AppleScript, delay, template, and logging problems on macOS.

Troubleshooting
===============

Start with a side-effect-free report:

.. code-block:: bash

   macpymessenger doctor

Fix every ``FAIL`` result, follow each ``INFO`` next step, then use the matching
section below.

The first send fails or macOS asks for permission
-------------------------------------------------

The first send may prompt you to allow Terminal, an editor, an agent host, or
another launcher to control Messages. Approve the prompt. Review access in
**System Settings > Privacy & Security > Automation**.

Automation access belongs to the launching application. Permission granted to
Terminal does not grant permission to an editor, background service, or agent
host. Reproduce the send from the same launcher that will run the program.

``MessageSendError``
--------------------

Inspect the structured fields first:

``error.recipient``
   The phone number or email address that failed.

``error.reason == "delivery"``
   ``osascript`` started, but AppleScript or Messages returned failure. Open
   Messages, confirm sign-in, send to the same recipient by hand, then check
   Automation permission.

``error.reason == "command"``
   The operating system could not start ``osascript``. Run the doctor, inspect
   ``PATH``, and confirm the configured send script is readable.

The original exception remains available as ``error.__cause__`` in a traceback.

``ScriptNotFoundError``
-----------------------

The bundled or custom AppleScript is missing or unreadable. Reinstall the wheel
when the bundled script check fails. When using a custom path, confirm it names a
readable file:

.. code-block:: python

   from macpymessenger import Configuration, IMessageClient

   client = IMessageClient(Configuration("scripts/sendMessage.scpt"))

``InvalidDelayTypeError`` or ``NegativeDelayError``
---------------------------------------------------

Use a whole number of seconds that is zero or greater. Booleans, floats, and
strings are not accepted.

``TemplateTypeError``
---------------------

Confirm the factory returns a Python 3.14 t-string, not a normal string. Then
confirm that every interpolated result is already a string. Convert inside the
expression when conversion is intentional, such as ``t"{str(count)}"``.

``TemplateNotFoundError`` or ``TemplateAlreadyExistsError``
-----------------------------------------------------------

Template identifiers are case-sensitive and live in the current
``TemplateManager``. Create an identifier once. Use ``update_template()`` to
replace its factory.

No delivery logs appear
-----------------------

macpymessenger does not configure output handlers or log levels. Configure
Python logging in the host application before sending. See :doc:`logging`.

Unsupported capability
----------------------

Attachments, chat history, message reading, contact lookup, remote gateways, and
MCP are outside the stable package. There are no placeholder methods to call.
