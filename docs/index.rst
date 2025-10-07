Welcome to macpymessenger's Documentation!
==========================================

**macpymessenger** is a Python library that provides a clear, type-safe interface for sending iMessages on macOS. It embraces dependency injection and deterministic configuration so that every component can be tested in isolation.

Key Features
------------

- 🚀 Send text messages with explicit subprocess control.
- 📝 Create and manage message templates rendered by Jinja2.
- 🔌 Seamless integration with the Messages app on macOS via packaged AppleScript.
- 📂 Customizable configuration without implicit globals.
- 🧪 Comprehensive tests and static analysis driven by `uv`.

Getting Started
---------------

1. Install macpymessenger using `uv`:

   .. code-block:: bash

      uv pip install macpymessenger

2. Import the necessary classes in your Python script:

   .. code-block:: python

      from macpymessenger import IMessageClient, Configuration

3. Create an instance of the ``Configuration`` class and customise the settings if needed.

4. Initialise the ``IMessageClient`` with the configuration:

   .. code-block:: python

      configuration = Configuration()
      client = IMessageClient(configuration)

5. Send an iMessage using the ``send`` method:

   .. code-block:: python

      phone_number = "+15555555555"
      message = "Hello, this is a test message sent using macpymessenger!"
      client.send(phone_number, message)

For more detailed information and examples, explore the following sections:

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   introduction
   installation
   usage
   configuration
   testing
   modules

Community and Support
---------------------

If you encounter any issues, have questions, or would like to contribute to macpymessenger, please visit our GitHub repository: https://github.com/ethan-wickstrom/macpymessenger

We welcome contributions, bug reports, and feature requests from the community. Feel free to open an issue or submit a pull request on GitHub.

License
-------

macpymessenger is licensed under the Apache License 2.0. See the `LICENSE <https://github.com/ethan-wickstrom/macpymessenger/blob/main/LICENSE>`_ file for more information.

Indices and Tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
