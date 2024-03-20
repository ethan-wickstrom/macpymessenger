Configuration
=============

macpymessenger provides a `Configuration` class that allows you to customize various settings and paths used by the library. In this section, we'll explore the available configuration options.

Customizing Script Paths
------------------------

By default, macpymessenger uses the following paths for AppleScript files:

- `send_script_path`: `osascript/sendMessage.scpt`

You can modify these paths by creating an instance of the `Configuration` class and setting the desired paths:

.. code-block:: python

   from macpymessenger import Configuration

   config = Configuration(send_script_path="path/to/custom/sendMessage.scpt")

Make sure to provide the correct paths to your custom AppleScript files.