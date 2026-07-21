Modules
=======

The public API is small. Most users can import everything they need from the
package root.

Public API exports
------------------

These classes are available from ``macpymessenger``.

.. code-block:: python

   from macpymessenger import (
       CommandRunner,
       Configuration,
       IMessageClient,
       SubprocessCommandRunner,
       TemplateManager,
   )

Custom exceptions are available from ``macpymessenger.exceptions``.

client module
-------------

The client module sends messages and connects the other pieces.

Key class:

- ``IMessageClient`` sends messages, sends templates, manages templates, and sends bulk messages.

``IMessageClient.send(phone_number, message, delay_seconds=0)`` returns ``None``
on success and raises ``MessageSendError`` when delivery fails. The bundled AppleScript honors ``delay_seconds`` and reports delivery errors through a non-zero ``osascript`` exit code.

commands module
---------------

The commands module owns command execution.

Key classes:

- ``CommandRunner`` is the protocol for injectable command runners.
- ``SubprocessCommandRunner`` runs ``osascript`` with ``subprocess.run(..., shell=False)``.

Both classes are also exported from the package root.

delivery module
---------------

The delivery module owns the full message delivery behavior surface.

Key class:

- ``MessageDelivery`` validates the send delay, constructs the ``osascript``
  command, executes it through the ``CommandRunner`` seam, maps subprocess
  and OS failures to typed ``MessageSendError`` variants, and logs the
  outcome.

``IMessageClient.send`` delegates to ``MessageDelivery.deliver`` so the
client facade stays thin while all delivery concerns are co-located and
independently testable.

configuration module
--------------------

The configuration module defines ``Configuration``.

``Configuration(send_script_path=None)`` uses the bundled AppleScript by
default. The path is checked at initialization; a missing or unreadable file
raises ``ScriptNotFoundError``.

templates module
----------------

The templates module stores and renders t-string templates.

Key class:

- ``TemplateManager`` stores callables that return Python 3.14 t-strings.

Common methods:

- ``create_template(identifier, factory)`` stores a new template.
- ``update_template(identifier, factory)`` replaces an existing template.
- ``delete_template(identifier)`` removes an existing template.
- ``render_template(identifier, context=None)`` returns the rendered string.
- ``list_templates()`` returns a shallow copy of registered factories.

Template factories receive context values as keyword arguments. Non-string
interpolations raise ``TemplateTypeError``. Conversions (``!s``, ``!r``,
``!a``) and format specs are applied after the type check.

Template errors
---------------

Template errors tell you whether storage or rendering failed.

- ``TemplateNotFoundError`` means the identifier does not exist.
- ``TemplateAlreadyExistsError`` means the identifier already exists.
- ``TemplateTypeError`` means the factory did not return a t-string, or an interpolation was not a string.

exceptions module
-----------------

The exceptions module defines the project error hierarchy.

Common exceptions include:

- ``MessageSendError`` for failed delivery or command execution.
- ``InvalidDelayTypeError`` for a delay that is not an ``int``.
- ``NegativeDelayError`` for a delay below zero.
- ``ScriptNotFoundError`` for a missing or unreadable AppleScript.
- ``ConfigurationError`` is the base class for configuration failures.

AppleScript resource
--------------------

The package bundles the AppleScript used for sending, and ``Configuration``
finds it automatically. The path matters only when you pass
``send_script_path`` yourself.
