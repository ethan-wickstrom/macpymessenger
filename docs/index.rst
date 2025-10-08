macpymessenger Documentation
============================

**macpymessenger** is a Python library for sending iMessages on macOS through AppleScript.

The library provides a type-safe, testable interface with explicit error handling and no hidden state.

What macpymessenger does
-------------------------

**Sends text messages.** The `IMessageClient` sends iMessages to phone numbers or email addresses using AppleScript and explicit subprocess control.

**Manages message templates.** The `TemplateManager` stores callables that return t-strings. Rendering is validated so that every interpolated value is a string.

**Validates configuration upfront.** The `Configuration` class checks that the AppleScript file exists and is readable before any messages are sent.

**Isolates subprocess calls.** Dependency injection separates subprocess execution from business logic, making tests straightforward.

**Uses comprehensive static analysis.** The codebase includes type hints for all functions and is validated with `mypy` and `ruff`.

Send your first message
-----------------------

**Install macpymessenger:**

.. code-block:: bash

   uv pip install macpymessenger

**Import the required classes:**

.. code-block:: python

   from macpymessenger import IMessageClient, Configuration

**Create a configuration and client:**

.. code-block:: python

   configuration = Configuration()
   client = IMessageClient(configuration)

**Send a message:**

.. code-block:: python

   client.send("+15555555555", "Hello from macpymessenger!")

The `send` method raises `MessageSendError` if delivery fails.

Explore the documentation
--------------------------

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

**Report issues or request features** on GitHub: https://github.com/ethan-wickstrom/macpymessenger

**Submit pull requests** with bug fixes or new features. See the repository for contribution guidelines.

**Ask questions** by opening a GitHub issue with the "question" label.

License information
-------------------

macpymessenger is licensed under the Apache License 2.0.

See the `LICENSE file <https://github.com/ethan-wickstrom/macpymessenger/blob/main/LICENSE>`_ for details.

Indices and Tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
