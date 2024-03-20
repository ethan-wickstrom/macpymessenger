Welcome to macpymessenger's Documentation!
==========================================

**macpymessenger** is a Python library that provides a simple and intuitive interface for sending iMessages on macOS. It allows you to send text messages programmatically using the Messages app on your Mac.

With macpymessenger, you can easily integrate iMessage functionality into your Python projects, automate messaging tasks, and build powerful applications that leverage the capabilities of iMessage.

Key Features
------------

- 🚀 Send text messages with ease
- 📝 Create and manage message templates
- 🔌 Seamless integration with the Messages app on macOS
- 📂 Customizable configuration options
- 🧪 Comprehensive test suite for ensuring reliability

Getting Started
---------------

To get started with macpymessenger, follow these steps:

1. Install macpymessenger using pip:

   .. code-block:: bash

      pip install macpymessenger

2. Import the necessary classes in your Python script:

   .. code-block:: python

      from macpymessenger import IMessageClient, Configuration

3. Create an instance of the `Configuration` class and customize the settings if needed.

4. Initialize the `IMessageClient` with the configuration:

   .. code-block:: python

      config = Configuration()
      client = IMessageClient(config)

5. Start sending iMessages using the `send` method:

   .. code-block:: python

      phone_number = "1234567890"
      message = "Hello, this is a test message sent using macpymessenger!"
      success = client.send(phone_number, message)

For more detailed information and examples, please refer to the following sections of the documentation:

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

For additional support or inquiries, you can reach out to the maintainer:

- Email: e.t.wickstrom@wustl.edu
- GitHub: `@ethan-wickstrom <https://github.com/ethan-wickstrom>`_

License
-------

macpymessenger is licensed under the Apache License 2.0. See the `LICENSE <https://github.com/ethan-wickstrom/macpymessenger/blob/main/LICENSE>`_ file for more information.

Indices and Tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`