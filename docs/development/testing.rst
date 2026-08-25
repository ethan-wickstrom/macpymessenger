Test and check changes
======================

Run all commands from the repository root.

.. code-block:: bash

   uv sync
   uv run ruff check
   uv run ty check
   uv run pytest
   uv build
   uv run sphinx-build -W docs docs/_build/html

What each check covers
----------------------

``ruff check``
   Finds style errors and common bugs.

``ty check``
   Checks types in ``src/`` and ``tests/``.

``pytest``
   Runs the test suite. Tests use command-runner doubles and do not send real
   messages.

``uv build``
   Creates the wheel and source distribution in ``dist/``.

``sphinx-build -W``
   Builds the documentation and treats warnings as errors.

Test delivery code safely
-------------------------

Inject a command runner instead of invoking AppleScript:

.. code-block:: python

   from collections.abc import Sequence

   from macpymessenger import Configuration, IMessageClient

   commands: list[Sequence[str]] = []

   def record_command(command: Sequence[str]) -> None:
       commands.append(command)

   client = IMessageClient(Configuration(), command_runner=record_command)
   client.send("+15555550123", "Hello")

   assert commands[0][-3:] == ["+15555550123", "Hello", "0"]
