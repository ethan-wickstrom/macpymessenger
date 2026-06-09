macpymessenger Documentation
============================

**macpymessenger sends iMessages from Python on macOS.** It uses AppleScript, the Messages app, and Python 3.14 t-string templates.

It is built for scripts that should be easy to read and easy to test. The public API is small. Errors are explicit. Configuration is checked before a message is sent.

Start here
----------

**Install the package.** Use ``uv add macpymessenger`` or ``pip install macpymessenger``.

**Send one message.** Create ``Configuration`` and ``IMessageClient``, then call ``send()``.

.. code-block:: python

   from macpymessenger import Configuration, IMessageClient

   client = IMessageClient(Configuration())
   client.send("+15555555555", "Hello from macpymessenger!")

``send()`` returns ``None`` when delivery succeeds. It raises ``MessageSendError`` when delivery fails.

What is in these docs
---------------------

**Introduction.** Learn what the library does and where it fits.

**Installation.** Install with ``uv`` or ``pip`` and confirm your environment.

**Usage.** Send messages, use t-string templates, handle errors, and send in bulk.

**Configuration.** Use the bundled AppleScript, set a custom path, and configure logging.

**Testing.** Run the development checks for this repository.

**Modules.** See the public classes and how the package is organized.

Explore the documentation
-------------------------

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   introduction
   installation
   usage
   configuration
   testing
   modules

Get help and contribute
-----------------------

**Report bugs and request features on GitHub.** Open an issue at https://github.com/ethan-wickstrom/macpymessenger/issues

**Send pull requests for focused changes.** Keep examples free of real phone numbers and secrets.

License
-------

macpymessenger is licensed under Apache-2.0.

See the `LICENSE file <https://github.com/ethan-wickstrom/macpymessenger/blob/main/LICENSE>`_ for details.

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
