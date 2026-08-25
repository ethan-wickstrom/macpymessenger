Troubleshooting
===============

Start with the error message, then use the matching section below.

The first send fails or macOS asks for permission
-------------------------------------------------

The first send may prompt you to allow your terminal, editor, or Python launcher
to control Messages. Approve the prompt. You can review access in **System
Settings > Privacy & Security > Automation**.

If no prompt appears, run a send again from the same application that will run
your program. Automation access belongs to that application, so permission for
Terminal may not apply to an editor or service.

``MessageSendError``
--------------------

Check these items in order:

#. Open Messages and confirm that your account is signed in.
#. Send a message to the same recipient by hand in Messages.
#. Confirm that the application running Python can control Messages.
#. Run the smallest example from :doc:`sending-messages`.

The exception wraps command execution and Messages delivery failures. Its cause
may contain more detail when you inspect a traceback.

``ScriptNotFoundError``
-----------------------

``Configuration`` could not find or read the AppleScript. Use
``Configuration()`` to select the bundled script. If you supply
``send_script_path``, confirm that it points to a readable file.

``InvalidDelayTypeError`` or ``NegativeDelayError``
---------------------------------------------------

Use a whole number of seconds that is zero or greater. Booleans, floats, and
strings are not accepted.

``TemplateTypeError``
---------------------

Confirm that the factory returns a t-string, not a normal string. Then confirm
that every value inside ``{...}`` is already a string.

``TemplateNotFoundError`` or ``TemplateAlreadyExistsError``
-----------------------------------------------------------

Template identifiers are case-sensitive and live only in the current
``TemplateManager``. Create an identifier once. Use ``update_template()`` to
replace it.

No log file appears
-------------------

File logging is opt-in. Pass ``FileLoggingConfiguration()`` when you create the
client. For a custom path, create the parent directory first.

Unsupported features
--------------------

``send_with_attachment()`` and ``get_chat_history()`` are placeholders. They
always raise ``NotImplementedError``. Text delivery is the supported sending
path.
