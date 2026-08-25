Configuration
=============

Use ``Configuration()`` for the bundled AppleScript. Most users do not need any
other setup.

.. code-block:: python

   from macpymessenger import Configuration, IMessageClient

   client = IMessageClient(Configuration())

For a custom AppleScript path, see :doc:`api/configuration`. For application and
file logs, see :doc:`guides/logging`. For setup failures, see
:doc:`guides/troubleshooting`.
