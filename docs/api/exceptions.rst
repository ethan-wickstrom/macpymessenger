.. meta::
   :description lang=en:
      Exception reference for macpymessenger delivery, delay, configuration,
      and Python t-string template failures.

Exceptions
==========

All public exceptions are importable from ``macpymessenger``. Catch the narrowest
error your program can act on. Catch ``MacPyMessengerError`` only at an
application boundary where one response is correct for every library failure.

Delivery errors
---------------

.. autoclass:: macpymessenger.MessageSendError
   :members:

``MessageSendError.recipient`` identifies the failed Messages handle.
``MessageSendError.reason`` is ``"delivery"`` when ``osascript`` ran but failed,
or ``"command"`` when the operating system could not start the command.

.. autoclass:: macpymessenger.InvalidDelayTypeError
.. autoclass:: macpymessenger.NegativeDelayError

Configuration errors
--------------------

.. autoclass:: macpymessenger.ConfigurationError
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
