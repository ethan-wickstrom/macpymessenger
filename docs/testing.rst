Testing
=======

Development commands run through uv. The checks cover tests, lint, types,
builds, and documentation.

Set up the environment
----------------------

Install the development dependencies first.

.. code-block:: bash

   uv sync

``uv sync`` creates or updates the local environment from the project files.

Run tests
---------

.. code-block:: bash

   uv run pytest

The tests stub command execution and send no real iMessages.

Run lint and type checks
------------------------

.. code-block:: bash

   uv run ruff check
   uv run ty check

Both should exit 0 before you open a pull request.

Build the package
-----------------

.. code-block:: bash

   uv build

This checks that the package builds from the source tree.

Build the documentation
-----------------------

.. code-block:: bash

   uv run sphinx-build docs docs/_build/html

Add ``-W`` to make warnings fail the build.

Understand failures
-------------------

pytest shows the failing assertion and traceback; start with the first failure.
ruff reports file paths and rule codes, and ty reports type mismatches. Sphinx
failures usually mean invalid reStructuredText: check heading underlines,
code-block directives, and inline markup.

Write tests for changes
-----------------------

Add tests under ``tests/`` when behavior changes. Test files use the ``test_*.py`` naming pattern.

For sending behavior, use a stub command runner; it keeps tests fast and avoids
AppleScript.

.. code-block:: python

   from macpymessenger import Configuration, IMessageClient

   def test_send_message_success(stub_command_runner):
       client = IMessageClient(Configuration(), command_runner=stub_command_runner)
       client.send("+15555555555", "Hello")
