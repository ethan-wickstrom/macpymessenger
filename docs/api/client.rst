Client API
==========

IMessageClient
--------------

.. autoclass:: macpymessenger.IMessageClient
   :members: send, send_template, send_bulk, create_template, update_template, delete_template, logger, get_chat_history, send_with_attachment
   :no-private-members:
   :no-special-members:

FileLoggingConfiguration
------------------------

.. autoclass:: macpymessenger.FileLoggingConfiguration
   :members:
   :no-private-members:
   :no-special-members:

Command runners
---------------

Pass a ``CommandRunner`` when you need to observe commands in tests or replace
subprocess execution. Production clients use ``SubprocessCommandRunner`` by
default.

.. autoclass:: macpymessenger.commands.CommandRunner
   :members:
   :no-private-members:
   :no-special-members:

.. autoclass:: macpymessenger.commands.SubprocessCommandRunner
   :members:
   :no-private-members:
   :no-special-members:
