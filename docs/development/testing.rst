.. meta::
   :description lang=en:
      Run macpymessenger lint, format, type, test, documentation, package, and
      safe command-runner checks locally.

Test and check changes
======================

Run all commands from the repository root:

.. code-block:: bash

   uv sync --locked
   uv run --locked ruff check
   uv run --locked ruff format --check
   uv run --locked ty check
   uv run --locked pytest
   uv run --locked sphinx-build -n -T -W --keep-going docs docs/_build/html
   uv build

What each check covers
----------------------

``uv sync --locked``
   Recreates the declared environment and fails when ``uv.lock`` is stale.

``ruff check`` and ``ruff format --check``
   Find bugs, enforce imports and style, and reject unformatted files.

``ty check``
   Checks public and internal types in ``src/`` and ``tests/``.

``pytest``
   Runs hermetic behavior tests. Tests replace command execution and do not send
   real messages.

``sphinx-build -n -T -W --keep-going``
   Resolves references, prints full tracebacks, treats warnings as errors, and
   reports all documentation failures in one run.

``uv build``
   Creates the wheel and source distribution in ``dist/``. CI then installs the
   wheel in a clean environment and checks package imports, bundled data, the
   console entry point, and doctor JSON.

Test delivery code safely
-------------------------

Inject a command runner instead of invoking AppleScript:

.. code-block:: python

   from collections.abc import Sequence

   from macpymessenger import IMessageClient

   commands: list[tuple[str, ...]] = []

   def record_command(command: Sequence[str]) -> None:
       commands.append(tuple(command))

   client = IMessageClient(command_runner=record_command)
   client.send("+15555550123", "Hello")

   assert commands[0][-3:] == ("+15555550123", "Hello", "0")

Test diagnostics safely
-----------------------

Monkeypatch platform discovery, executable lookup, and Messages paths. Do not
make diagnostic tests depend on the current runner, open Messages, or trigger a
permission prompt.
