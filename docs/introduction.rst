Introduction
============

macpymessenger sends iMessages from Python on macOS. It uses AppleScript to talk
to the built-in Messages app.

Use it when you want a small Python library, not a hosted messaging service. Your
script runs on a Mac, and Messages.app sends the iMessage.

What you get
------------

The sending path is short: create a ``Configuration``, create an
``IMessageClient``, call ``send()``. Delivery failures raise ``MessageSendError``,
and bad delays raise ``InvalidDelayTypeError`` or ``NegativeDelayError``.

Templates are callables that return Python 3.14 t-strings, such as
``lambda name: t"Hello, {name}!"``. Jinja2 is not used. Every interpolation must
resolve to ``str``. Anything else raises ``TemplateTypeError``.

``Configuration`` checks that the AppleScript file exists and is readable when
you create it, so path problems surface before the first send. The client also
accepts a custom command runner, which lets tests skip AppleScript.

When to use it
--------------

Sending yourself reminders from a script. Sending notices from approval flows,
monitoring jobs, or local tools. Reusing message text where only names, dates,
or status text change. Sending one message to many recipients and collecting
successes and failures.

Limits
------

macOS is required. The library depends on AppleScript and Messages.app, so the
package can install elsewhere but cannot send from there.

Python 3.14 or newer is required, because templates use t-strings.

``send_with_attachment`` and ``get_chat_history`` are stubs that always raise
``NotImplementedError``.

Next steps
----------

Install the package, then follow the usage guide to send a first message. Read
the configuration guide if you need a custom AppleScript path, file logging, or
your own logger.
