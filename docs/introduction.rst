Introduction
============

**macpymessenger sends iMessages from Python on macOS.** It uses AppleScript to talk to the built-in Messages app.

Use it when you want a small Python library, not a hosted messaging service. Your script runs on a Mac. Messages.app sends the iMessage.

What macpymessenger gives you
-----------------------------

**A short sending path.** Create a ``Configuration``. Create an ``IMessageClient``. Call ``send()``.

**Clear errors.** Delivery failures raise ``MessageSendError``. Bad delays raise ``InvalidDelayTypeError`` or ``NegativeDelayError``.

**Real t-string templates.** Templates are callables that return Python 3.14 t-strings, such as ``lambda name: t"Hello, {name}!"``. Jinja2 is not used.

**Safe template rendering.** Every interpolation must resolve to ``str``. If not, macpymessenger raises ``TemplateTypeError``.

**Early configuration checks.** ``Configuration`` checks that the AppleScript file exists and is readable when you create it.

**Testable seams.** The client accepts a custom command runner. Tests can avoid running AppleScript.

When to use it
--------------

**Personal automation.** Send yourself reminders or small alerts from a script.

**Team workflows.** Send iMessage notices from approval flows, monitoring jobs, or local tools.

**Message templates.** Reuse message text while changing names, dates, or short status text.

**Bulk sends.** Send the same message to a list of recipients and collect successes and failures.

Important limits
----------------

**macOS is required.** The library depends on AppleScript and Messages.app.

**Python 3.14 or newer is required.** Templates use Python t-strings.

**Attachments and chat history are not ready.** ``send_with_attachment`` and ``get_chat_history`` are experimental stubs. They always raise ``NotImplementedError``.

Next steps
----------

**Install the package.** Start with the installation guide.

**Send a first message.** Follow the usage guide for sending, templates, bulk sends, and errors.

**Tune configuration.** Read the configuration guide if you need a custom AppleScript path, file logging, or your own logger.
