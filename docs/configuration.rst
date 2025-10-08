Configuration
=============

macpymessenger provides a :class:`~macpymessenger.configuration.Configuration` class that allows you to customize the AppleScript path used by the library. In this section, we outline how the configuration discovers the packaged script, how it validates readability, and the logging defaults applied by the client.

Customizing Script Paths
------------------------

By default, :class:`~macpymessenger.configuration.Configuration` resolves the bundled AppleScript located at ``osascript/sendMessage.scpt`` inside the package. You can point to a different script by instantiating the configuration with an explicit path:

.. code-block:: python

   from pathlib import Path
   from macpymessenger import Configuration

   config = Configuration(send_script_path=Path("/path/to/custom/sendMessage.scpt"))

Validation and Error Handling
-----------------------------

During initialization the configuration normalizes the provided path and guarantees that the AppleScript both exists and is readable before it is stored. The private :meth:`~macpymessenger.configuration.Configuration._determine_script_path` helper checks:

* the path exists on disk;
* the process can open the file in binary mode, surfacing permission issues immediately.

If either check fails a :class:`~macpymessenger.exceptions.ScriptNotFoundError` is raised, keeping runtime execution of ``osascript`` free of surprises.

Logging Defaults
----------------

Instances of :class:`~macpymessenger.client.IMessageClient` rely on the handlers already configured on the provided ``logger``. To persist events to disk you can opt in by instantiating the client with ``enable_file_logging=True``, which attaches a ``macpymessenger.log`` :class:`logging.FileHandler` when one is not present. Supplying a pre-configured logger remains the recommended approach when you need custom destinations or formatting.
