Contribute
==========

Requirements
------------

Install ``uv`` and use Python 3.14 or newer. A Mac is needed for manual delivery
tests, but the automated tests replace AppleScript execution with test doubles.

Set up the repository
---------------------

.. code-block:: bash

   git clone https://github.com/ethan-wickstrom/macpymessenger.git
   cd macpymessenger
   uv sync

Make a focused change
---------------------

#. Add or update tests when behavior changes.
#. Keep examples free of real phone numbers, account details, and secrets.
#. Update user documentation and ``CHANGELOG.md`` for public behavior changes.
#. Run the checks in :doc:`testing`.
#. Use a Conventional Commit such as ``docs: improve the getting-started guide``.

Report a problem
----------------

Open an issue at https://github.com/ethan-wickstrom/macpymessenger/issues. Include
what you expected, what happened, your macOS and Python versions, and the
smallest example that reproduces the problem. Remove phone numbers and other
private information from logs and tracebacks.
