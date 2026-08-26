.. meta::
   :description lang=en:
      API reference for macpymessenger environment checks, blocker reports,
      manual statuses, and JSON output.

Diagnostics API
===============

The command-line doctor and programmatic API share one immutable data model.
Collection does not invoke AppleScript or control Messages.

.. autofunction:: macpymessenger.diagnostics.diagnose_environment

.. autoclass:: macpymessenger.diagnostics.EnvironmentReport
   :members: blocked, to_dict
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

``EnvironmentReport.blocked`` is true only when an automated check returns
``FAIL``. ``MANUAL`` checks remain unresolved and must not be treated as
successful delivery evidence.
