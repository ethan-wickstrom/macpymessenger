macpymessenger
==============

Send iMessages from Python on macOS.

macpymessenger runs AppleScript against the Messages app on the same Mac as your
Python program. Use it for local tools and automations where you control the Mac.
It is not a hosted service or a cross-platform messaging gateway.

Quick start
-----------

You need macOS, Python 3.14 or newer, and an account signed in to Messages.

.. code-block:: bash

   uv add macpymessenger

.. code-block:: python

   from macpymessenger import Configuration, IMessageClient
   from macpymessenger.exceptions import MessageSendError

   client = IMessageClient(Configuration())

   try:
       client.send("+15555550123", "Hello from Python!")
   except MessageSendError as error:
       print(f"Could not send the message: {error}")

The first send may ask for permission to control Messages. See
:doc:`guides/troubleshooting` if the send fails.

Find what you need
------------------

**New user**
   Start with :doc:`installation`, then follow :doc:`guides/sending-messages`.

**Building reusable messages**
   Read :doc:`guides/templates`.

**A send failed**
   Use :doc:`guides/troubleshooting` and the :doc:`api/exceptions` reference.

**Looking for a class or method**
   Go to :doc:`modules`.

**Contributing**
   Set up the repository with :doc:`development/contributing`.

.. toctree::
   :maxdepth: 2
   :caption: Get started

   introduction
   installation
   usage
   configuration

.. toctree::
   :maxdepth: 2
   :caption: Guides

   guides/sending-messages
   guides/templates
   guides/logging
   guides/troubleshooting

.. toctree::
   :maxdepth: 2
   :caption: API reference

   modules
   api/client
   api/configuration
   api/templates
   api/exceptions

.. toctree::
   :maxdepth: 2
   :caption: Development

   development/contributing
   testing
   development/testing
   development/release-process

License
-------

macpymessenger uses the Apache-2.0 license.
