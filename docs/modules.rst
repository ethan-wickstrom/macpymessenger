API reference
=============

Most programs need only ``Configuration`` and ``IMessageClient``. Import both
from ``macpymessenger``. Import typed errors from
``macpymessenger.exceptions``.

.. code-block:: python

   from macpymessenger import Configuration, IMessageClient
   from macpymessenger.exceptions import MessageSendError

Choose a reference page
-----------------------

- :doc:`api/client` — sending, bulk sends, logging, and dependency injection.
- :doc:`api/configuration` — bundled and custom AppleScript paths.
- :doc:`api/templates` — t-string registration and rendering.
- :doc:`api/exceptions` — the error hierarchy and when each error occurs.

Package exports
---------------

The package root exports ``CommandRunner``, ``Configuration``,
``FileLoggingConfiguration``, ``IMessageClient``, ``RenderedTemplate``,
``SubprocessCommandRunner``, and ``TemplateManager``.

Attachments and chat history are not supported. Their placeholder methods raise
``NotImplementedError``.
