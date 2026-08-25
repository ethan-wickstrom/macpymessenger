Exceptions
==========

All library-defined errors inherit from ``MacPyMessengerError``. Catch a
specific error when your program can recover from it. Catch
``MacPyMessengerError`` only at an application boundary where one response is
right for every library error.

Delivery errors
---------------

.. autoclass:: macpymessenger.exceptions.MessageSendError
.. autoclass:: macpymessenger.exceptions.InvalidDelayTypeError
.. autoclass:: macpymessenger.exceptions.NegativeDelayError
.. autoclass:: macpymessenger.exceptions.InvalidCommandError

Configuration errors
--------------------

.. autoclass:: macpymessenger.exceptions.ConfigurationError
.. autoclass:: macpymessenger.exceptions.ScriptNotFoundError

Template errors
---------------

.. autoclass:: macpymessenger.exceptions.TemplateError
.. autoclass:: macpymessenger.exceptions.TemplateTypeError
.. autoclass:: macpymessenger.exceptions.TemplateNotFoundError
.. autoclass:: macpymessenger.exceptions.TemplateAlreadyExistsError

Base error
----------

.. autoclass:: macpymessenger.exceptions.MacPyMessengerError
