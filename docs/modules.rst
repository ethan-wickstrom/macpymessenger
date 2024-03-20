Modules
=======

macpymessenger is organized into several modules, each responsible for a specific set of functionalities. In this section, we'll provide an overview of the main modules and their purposes.

imessage_client.py
------------------

The `imessage_client.py` module contains the `IMessageClient` class, which is the main entry point for interacting with the macpymessenger library. This module provides methods for sending messages, managing templates, and performing other iMessage-related operations.

configuration.py
----------------

The `configuration.py` module defines the `Configuration` class, which handles the configuration settings for macpymessenger. It allows you to customize various options, such as script paths and logging behavior.

message_template.py
-------------------

The `message_template.py` module provides the `MessageTemplate` class, which represents a reusable message template. It encapsulates the template ID and content, allowing you to create, update, and delete templates easily.

template_manager.py
-------------------

The `template_manager.py` module contains the `TemplateManager` class, which is responsible for managing message templates. It provides methods for creating, retrieving, updating, and deleting templates, as well as handling template storage and retrieval.

exceptions.py
-------------

The `exceptions.py` module defines custom exception classes used by macpymessenger. These exceptions are raised when specific error conditions occur, such as when a message fails to send or when a template is not found.

utils.py
--------

The `utils.py` module contains utility functions and helper classes used throughout the macpymessenger library. These utilities provide common functionality, such as string formatting, file handling, and logging setup.

tests/
------

The `tests/` directory contains the test suite for macpymessenger. It includes various test modules and test cases to ensure the functionality and reliability of the library. The tests cover different aspects of macpymessenger, such as sending messages, managing templates, and handling error scenarios.

Each module plays a specific role in the overall functionality of macpymessenger. By understanding the purpose and responsibilities of each module, you can effectively navigate and utilize the library in your projects.

For detailed information on the classes, methods, and functions provided by each module, please refer to the API reference documentation.