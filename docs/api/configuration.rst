.. meta::
   :description lang=en:
      API reference for resolving the bundled macpymessenger AppleScript or
      validating a custom send script path.

Configuration API
=================

Ordinary callers use ``IMessageClient()`` and do not construct configuration.
Use ``Configuration`` when you need a custom script or want to inspect the
resolved bundled path.

.. autoclass:: macpymessenger.Configuration
   :members:
   :no-private-members:
   :no-special-members:

``Configuration()`` resolves the AppleScript bundled in the wheel. Passing a
``Path`` or string validates that custom file immediately. A missing or unreadable
file raises ``ScriptNotFoundError`` before delivery begins.
