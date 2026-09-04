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
rejected private value.

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
rejected the send, or ``"transport"`` when the transport could not run. The raw
transport exception is intentionally not chained because it can contain private
child-process data.

Installation errors
-------------------

.. autoclass:: macpymessenger.ScriptNotFoundError

Template errors
---------------

.. autoclass:: macpymessenger.TemplateError
.. autoclass:: macpymessenger.TemplateTypeError
.. autoclass:: macpymessenger.TemplateNotFoundError
.. autoclass:: macpymessenger.TemplateAlreadyExistsError

Base error
----------

.. autoclass:: macpymessenger.MacPyMessengerError
