Modules
=======

macpymessenger is organized into several modules, each responsible for a specific set of functionalities. In this section, we'll provide an overview of the main modules and their purposes.

client.py
---------

The :mod:`client` module exposes the public messaging interface via :class:`macpymessenger.IMessageClient`. It wraps AppleScript execution, handles logging, surfaces delivery failures through :class:`macpymessenger.exceptions.MessageSendError`, and provides helpers such as :class:`macpymessenger.SubprocessCommandRunner` for command execution.

configuration.py
----------------

The :mod:`configuration` module defines :class:`macpymessenger.Configuration`, which discovers the bundled AppleScript files, validates the configuration, and lets you customize script locations and logging behavior.

exceptions.py
-------------

The :mod:`exceptions` module defines the error hierarchy for the package, including :class:`macpymessenger.exceptions.MessageSendError` for delivery issues, :class:`macpymessenger.exceptions.TemplateError` for template problems, and :class:`macpymessenger.exceptions.ConfigurationError` for configuration validation.

templates.py
------------

The :mod:`templates` module manages reusable message templates. It provides :class:`macpymessenger.TemplateManager` for CRUD operations, :class:`macpymessenger.TemplateDefinition` for describing templates, and :class:`macpymessenger.RenderedTemplate` for working with the rendered content. Templates are rendered with Jinja2, so standard Jinja syntax and features are available.

__init__.py
-----------

The package root re-exports the primary public interfaces through ``__all__`` so that ``from macpymessenger import ...`` surfaces the classes listed above. Refer to :mod:`macpymessenger.__init__` for the authoritative list of supported entry points.

osascript/
----------

The ``osascript`` directory contains the AppleScript files invoked by :class:`macpymessenger.IMessageClient`. The scripts implement the low-level interaction with the Messages app and are resolved automatically by :class:`macpymessenger.Configuration`.

Each module plays a specific role in the overall functionality of macpymessenger. By understanding the purpose and responsibilities of each module, you can effectively navigate and utilize the library in your projects.

For detailed information on the classes, methods, and functions provided by each module, please refer to the API reference documentation.
