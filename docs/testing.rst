Testing
=======

macpymessenger ships with a focused automated test suite. The recommended workflow uses `uv` to provision tooling.

Running the Tests
-----------------

.. code-block:: bash

   uv sync
   uv run pytest

``uv sync`` installs both runtime and development dependencies declared in ``pyproject.toml`` into an isolated environment. ``uv run`` executes the requested command within that environment.

Static Analysis and Linting
---------------------------

.. code-block:: bash

   uv run ruff check
   uv run mypy

These commands enforce style and type constraints so regressions are caught early.

Interpreting Results
--------------------

- A passing run prints ``OK`` from ``pytest``.
- Failures include tracebacks with explicit assertions for quick diagnosis.
- Ruff and mypy exit with non-zero status codes when issues are detected; inspect their output for remediation guidance.

Custom Tests
------------

Add new ``test_*.py`` files under ``tests/`` and run ``uv run pytest`` again to execute them. The fixtures in the test suite demonstrate how to stub the subprocess runner for deterministic behaviour.
