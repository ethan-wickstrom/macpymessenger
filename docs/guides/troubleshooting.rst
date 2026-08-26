.. meta::
   :description lang=en:
      Fix macpymessenger setup, Automation permission, Messages delivery,
      AppleScript transport, delay, template, and logging problems on macOS.

Troubleshooting
===============

Start with a side-effect-free report. In a uv project:

.. code-block:: bash

   uv run macpymessenger doctor

Fix every ``FAIL`` result and complete every ``MANUAL`` next step, then use the
matching section below.

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
   The transport ran, but AppleScript or Messages reported failure. Open
   Messages, confirm sign-in, send to the same recipient by hand, then check
   Automation permission.

``error.reason == "transport"``
   The operating system could not run the transport. Run the doctor and confirm
   that ``/usr/bin/osascript`` is available.

The raw child-process exception is intentionally not chained. It can contain
private transport data and is not part of the public recovery contract.

``ScriptNotFoundError``
-----------------------

The AppleScript source bundled in the installed wheel is missing or unreadable.
Reinstall macpymessenger from a complete wheel. Custom delivery behavior belongs
behind ``MessageTransport`` rather than a script-path override; see
:doc:`../api/transport`.

``InvalidDelayTypeError`` or ``NegativeDelayError``
---------------------------------------------------

Use a whole number of seconds that is zero or greater. Booleans, floats, and
strings are not accepted.

``TemplateTypeError``
---------------------

Confirm the factory returns a Python 3.14 t-string, not a normal string.
Interpolated values otherwise use Python's normal conversion and format
protocols. A ``TypeError`` or ``ValueError`` from formatting belongs to the
value or format specification itself.

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
