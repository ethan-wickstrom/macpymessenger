Testing
=======

**macpymessenger uses uv for development commands.** The project checks tests, lint, types, builds, and documentation.

Set up the environment
----------------------

**Install the development dependencies first.**

.. code-block:: bash

   uv sync

``uv sync`` creates or updates the local environment from the project files.

Run tests
---------

**Use pytest for the test suite.**

.. code-block:: bash

   uv run pytest

The tests use stubs for command execution where possible. They do not need to send real iMessages.

Run lint and type checks
------------------------

**Use ruff for linting.**

.. code-block:: bash

   uv run ruff check

**Use ty for type checking.**

.. code-block:: bash

   uv run ty check

Both commands should exit with status code 0 before you open a pull request.

Build the package
-----------------

**Use uv to build the distribution files.**

.. code-block:: bash

   uv build

This checks that the package can be built from the current source tree.

Build the documentation
-----------------------

**Use Sphinx to build the HTML documentation.**

.. code-block:: bash

   uv run sphinx-build docs docs/_build/html

When you are checking for warnings, add ``-W`` so warnings fail the build.

Understand failures
-------------------

**pytest failures show the failing assertion and traceback.** Start with the first failure.

**ruff failures show file paths and rule codes.** Fix the reported line, then run the command again.

**ty failures show type mismatches.** Keep public examples aligned with the typed API.

**Sphinx failures often point to invalid reStructuredText.** Check heading underlines, code-block directives, and inline markup.

Write tests for changes
-----------------------

**Add tests under ``tests/`` when behavior changes.** Test files use the ``test_*.py`` naming pattern.

For message sending behavior, prefer a stub command runner. That keeps tests fast and avoids AppleScript.

.. code-block:: python

   from macpymessenger import Configuration, IMessageClient

   def test_send_message_success(stub_command_runner):
       client = IMessageClient(Configuration(), command_runner=stub_command_runner)
       client.send("+15555555555", "Hello")

Run new tests with ``uv run pytest``.
