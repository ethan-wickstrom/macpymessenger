.. meta::
   :description lang=en:
      Fix macpymessenger command input, setup, Automation permission, Messages
      delivery, AppleScript transport, delay, template, and logging problems.

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

``macpymessenger send`` exits with status 2
-------------------------------------------

The JSON input is malformed or does not match the closed request shape. Run:

.. code-block:: bash

   macpymessenger send --help

Confirm that standard input contains exactly one object with non-empty string
``recipient`` and ``message`` fields. ``delay_seconds`` is optional and must be
a non-negative integer. Remove unknown fields and duplicate keys. Booleans,
floats, and text that cannot be encoded as UTF-8 are invalid.

With ``--json``, the command returns ``error.code == "invalid_input"`` without
echoing the rejected values. Input errors happen before the client or Messages
effect is created.

``macpymessenger send`` exits with status 1
-------------------------------------------

Read ``error.reason`` from JSON output:

``"delivery"``
   The transport ran, but AppleScript or Messages reported failure.

``"transport"``
   The local AppleScript transport could not run or load its bundled source.

Do not retry automatically. The command has no delivery receipt or idempotency
key, so an uncertain retry can create a duplicate message.

``MessageSendError``
--------------------

Python callers should inspect the structured fields first:

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
Python logging in the host application before sending. Built-in records contain
generic outcomes only. See :doc:`logging`.

Unsupported capability
----------------------

Attachments, chat history, message reading, contact lookup, remote gateways,
delivery receipts, and account management are outside the stable package. There
are no placeholder methods to call.
