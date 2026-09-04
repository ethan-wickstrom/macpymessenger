.. meta::
   :description lang=en:
      Exception reference for macpymessenger request validation, delivery,
      transport, delay, installation, and Python t-string template failures.

Exceptions
==========

All public exceptions are importable from ``macpymessenger``. Catch the
narrowest error your program can act on. Catch ``MacPyMessengerError`` only at
an application boundary where one response is correct for every library
failure.

Request validation
------------------

.. autotype:: macpymessenger.SendTextField
.. autotype:: macpymessenger.SendTextValidationReason

.. autoclass:: macpymessenger.InvalidSendTextError
   :members:

``InvalidSendTextError.field`` is ``"recipient"`` or ``"message"``.
``InvalidSendTextError.reason`` is ``"type"``, ``"empty"``, or ``"encoding"``.
The exception message identifies the field and rule but never includes the
rejected private value. An encoding failure also discards the underlying
``UnicodeEncodeError`` after validation, so its private ``object`` value is not
reachable through ``__cause__`` or ``__context__``.

.. autoclass:: macpymessenger.InvalidDelayTypeError
.. autoclass:: macpymessenger.NegativeDelayError

Delivery errors
---------------

.. autotype:: macpymessenger.MessageFailureReason

``MessageFailureReason`` is the closed set of machine-readable send-failure
reasons: ``"delivery"`` and ``"transport"``.

.. autoclass:: macpymessenger.MessageSendError
   :members:

``MessageSendError.recipient`` identifies the failed Messages handle.
``MessageSendError.reason`` is ``"delivery"`` when AppleScript or Messages
rejected the send, or ``"transport"`` when the transport could not run. Raw
child-process and operating-system exceptions can contain private data, so the
built-in transport and client expose neither exception through ``__cause__`` or
``__context__``.

Installation errors
-------------------

.. autoclass:: macpymessenger.ScriptNotFoundError

``ScriptNotFoundError`` reports a generic reinstall action. The filesystem or
Unicode exception that prevented package-data loading is not retained as
``__cause__`` or ``__context__`` because it may include a private installation
path or content.

Template errors
---------------

.. autoclass:: macpymessenger.TemplateError
.. autoclass:: macpymessenger.TemplateTypeError
.. autoclass:: macpymessenger.TemplateNotFoundError
.. autoclass:: macpymessenger.TemplateAlreadyExistsError

Base error
----------

.. autoclass:: macpymessenger.MacPyMessengerError
