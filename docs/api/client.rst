.. meta::
   :description lang=en:
      API reference for sending iMessages from Python with IMessageClient,
      BulkSendResult, and injectable command runners on macOS.

Client API
==========

IMessageClient
--------------

Create ``IMessageClient()`` to use the bundled AppleScript. Pass collaborators
only when you need a custom script, template store, test runner, or logger.

.. autoclass:: macpymessenger.IMessageClient
   :members: send, send_template, send_bulk, create_template, update_template, delete_template, logger
   :no-private-members:
   :no-special-members:

BulkSendResult
--------------

``send_bulk()`` returns ``BulkSendResult(sent, failed)``. The named fields make
call sites clear, while tuple unpacking remains valid:

.. code-block:: python

   result = client.send_bulk(recipients, "The build is ready.")
   print(result.sent)
   print(result.failed)

   sent, failed = result

.. autoclass:: macpymessenger.BulkSendResult
   :no-private-members:
   :no-special-members:

Command runners
---------------

Pass a ``CommandRunner`` when a test or host application needs to observe or
replace command execution. Production clients use ``SubprocessCommandRunner``
by default. Automated tests should inject a runner and must not invoke
``osascript``.

.. autoclass:: macpymessenger.CommandRunner
   :members:
   :no-private-members:
   :no-special-members:

.. autoclass:: macpymessenger.SubprocessCommandRunner
   :members:
   :no-private-members:
   :no-special-members:
