.. meta::
   :description lang=en:
      API reference for macpymessenger environment checks, structured doctor
      reports, statuses, and JSON output.

Diagnostics API
===============

The command-line doctor and programmatic API share one data model. Collection is
read-only and does not run AppleScript.

.. autofunction:: macpymessenger.diagnostics.diagnose_environment

.. autoclass:: macpymessenger.diagnostics.EnvironmentReport
   :members: ready, to_dict
   :no-private-members:
   :no-special-members:

.. autoclass:: macpymessenger.diagnostics.EnvironmentCheck
   :members: to_dict
   :no-private-members:
   :no-special-members:

.. autoclass:: macpymessenger.diagnostics.CheckStatus
   :members:
   :no-private-members:
   :no-special-members:
