macpymessenger documentation
============================

macpymessenger sends iMessages from Python on macOS. It uses AppleScript, the
Messages app, and Python 3.14 t-string templates.

It is built for scripts that should be easy to read and test. The public
API is small, errors are explicit, and configuration is checked before a message
is sent.

Start here
----------

Install with ``uv add macpymessenger`` or ``pip install macpymessenger``, then
create a ``Configuration`` and an ``IMessageClient`` and call ``send()``:

.. code-block:: python

   from macpymessenger import Configuration, IMessageClient

   client = IMessageClient(Configuration())
   client.send("+15555555555", "Hello from macpymessenger!")

``send()`` returns ``None`` when delivery succeeds. It raises
``MessageSendError`` when delivery fails.

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

Report bugs and request features at
https://github.com/ethan-wickstrom/macpymessenger/issues. Pull requests for
focused changes are welcome. Keep examples free of real phone numbers and
secrets.

License
-------

macpymessenger is licensed under Apache-2.0. See the `LICENSE file
<https://github.com/ethan-wickstrom/macpymessenger/blob/main/LICENSE>`_ for
details.

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
