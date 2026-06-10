Modules
=======

**macpymessenger keeps its public API small.** Most users can import what they need from the package root.

Public API exports
------------------

**These classes are available from ``macpymessenger``.**

.. code-block:: python

   from macpymessenger import (
       Configuration,
       FileLoggingConfiguration,
       IMessageClient,
       RenderedTemplate,
       SubprocessCommandRunner,
       TemplateManager,
   )

Custom exceptions are available from ``macpymessenger.exceptions``.

client module
-------------

**The client module sends messages and connects the other pieces.**

Key classes:

- ``IMessageClient`` sends messages, sends templates, manages templates, and sends bulk messages.
- ``FileLoggingConfiguration`` opts in to file logging. The default path is ``macpymessenger.log`` in the current working directory.
- ``SubprocessCommandRunner`` runs ``osascript`` with ``subprocess.run(..., shell=False)``.

``IMessageClient.send(phone_number, message, delay_seconds=0)`` returns ``None`` on success. It raises ``MessageSendError`` when delivery fails. The bundled AppleScript honors ``delay_seconds`` and reports delivery errors through a non-zero ``osascript`` exit code.

configuration module
--------------------

**The configuration module defines ``Configuration``.**

``Configuration(send_script_path=None)`` uses the bundled AppleScript by default. If you pass a path, it uses that path instead.

The path is checked during initialization. The file must exist and be readable. If not, ``Configuration`` raises ``ScriptNotFoundError``.

templates module
----------------

**The templates module stores and renders t-string templates.**

Key classes:

- ``TemplateManager`` stores callables that return Python 3.14 t-strings.
- ``RenderedTemplate`` contains a template identifier and rendered message content.

Common methods:

- ``create_template(identifier, factory)`` stores a new template.
- ``update_template(identifier, factory)`` replaces an existing template.
- ``delete_template(identifier)`` removes an existing template.
- ``render_template(identifier, context=None)`` returns the rendered string.
- ``compose_template(identifier, context=None)`` returns ``RenderedTemplate``.
- ``list_templates()`` returns a shallow copy of registered factories.

Template factories receive context values as keyword arguments. Every interpolation must resolve to ``str``. Non-string values raise ``TemplateTypeError``. Conversions (``!s``, ``!r``, ``!a``) and format specs are applied after the type check.

Template errors
---------------

**Template errors tell you whether storage or rendering failed.**

- ``TemplateNotFoundError`` means the identifier does not exist.
- ``TemplateAlreadyExistsError`` means the identifier already exists.
- ``TemplateTypeError`` means the factory did not return a t-string, or an interpolation was not a string.

exceptions module
-----------------

**The exceptions module defines the project error hierarchy.**

Common exceptions include:

- ``MessageSendError`` for failed delivery or command execution.
- ``InvalidDelayTypeError`` for a delay that is not an ``int``.
- ``NegativeDelayError`` for a delay below zero.
- ``ScriptNotFoundError`` for a missing or unreadable AppleScript.
- ``ConfigurationError`` for configuration failures, including unavailable file logging.

Experimental methods
--------------------

**Two client methods are present but not implemented.**

- ``get_chat_history`` always raises ``NotImplementedError``.
- ``send_with_attachment`` always raises ``NotImplementedError``.

They exist to reserve the API shape for future work. Do not call them in production code.

AppleScript resource
--------------------

**The package includes the AppleScript used for sending.** ``Configuration`` finds it automatically.

You only need to think about the script path when you pass ``send_script_path`` yourself.
