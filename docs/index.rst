.. meta::
   :description lang=en:
      Send iMessages from Python on macOS through the built-in Messages app.
      Install macpymessenger, check your Mac, and send typed messages.
   :keywords: Python iMessage, macOS Messages automation, AppleScript, Python 3.14

macpymessenger
==============

Send iMessages from Python on macOS.

macpymessenger is a small, typed library for scripts, local automations,
developer tools, and agents running on a Mac. It controls the built-in Messages
app through AppleScript. It has no runtime dependencies and does not read chat
history, send attachments, expose a remote API, or act as a messaging server.

Quick start
-----------

You need macOS, Python 3.14 or newer, an Apple account signed in to Messages,
and Automation permission for the application that launches Python.

.. code-block:: bash

   uv add macpymessenger
   macpymessenger doctor

Then create one client and reuse it:

.. code-block:: python

   from macpymessenger import IMessageClient, MessageSendError

   client = IMessageClient()

   try:
       client.send("+15555550123", "Hello from Python!")
   except MessageSendError as error:
       print(f"Could not send {error.recipient}: {error}")

The first real send may ask whether Terminal, your editor, or another launcher
can control Messages. Allow access, or review it in **System Settings > Privacy
& Security > Automation**.

Find what you need
------------------

**First send**
   Follow :doc:`installation`, run :doc:`guides/environment-diagnostics`, then
   use :doc:`guides/sending-messages`.

**Reusable messages**
   Read :doc:`guides/templates`.

**A send failed**
   Use :doc:`guides/troubleshooting` and the :doc:`api/exceptions` reference.

**Application logging**
   Read :doc:`guides/logging` before routing recipient handles to a log sink.

**Class, method, or result shape**
   Go to :doc:`modules`.

**Contributing or changing the library**
   Start with :doc:`development/contributing`.

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

   guides/environment-diagnostics
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
   api/diagnostics

.. toctree::
   :maxdepth: 2
   :caption: Development

   development/contributing
   development/testing
   development/release-process

License
-------

macpymessenger uses the Apache-2.0 license.
