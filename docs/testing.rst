Testing
=======

**macpymessenger includes a comprehensive test suite with static analysis.**

The project uses `pytest` for tests, `ruff` for linting, and `ty` for type checking.

Run tests with pytest
---------------------

**Install dependencies first:**

.. code-block:: bash

   uv sync

**Run the test suite:**

.. code-block:: bash

   uv run pytest

**`uv sync` installs all dependencies from `pyproject.toml` into an isolated environment.** `uv run` executes commands within that environment.

Run linting and type checking
------------------------------

**Check code style with ruff:**

.. code-block:: bash

   uv run ruff check

**Check types with ty:**

.. code-block:: bash

   uv run ty check

**Both tools enforce code quality standards.** Fix any issues before committing.

Understand test results
-----------------------

**Passing tests:**

- `pytest` prints a summary with green dots and "passed" counts
- `ruff` and `ty` exit with status code 0 and no output

**Failing tests:**

- `pytest` shows tracebacks with assertion details for quick debugging
- `ruff` and `ty` print error messages with file paths and line numbers

**Fix failures before committing code.**

Write custom tests
------------------

**Add new test files to the `tests` directory:**

Test files must:

- Follow the naming pattern `test_*.py`
- Import `pytest` fixtures as needed
- Use stubbed subprocess runners to avoid executing AppleScript

**Example test structure:**

.. code-block:: python

   from macpymessenger import IMessageClient, Configuration
   
   def test_send_message_success():
       config = Configuration()
       client = IMessageClient(config)
       # Add assertions here

**Run new tests with `uv run pytest`.** The test suite includes fixtures that demonstrate how to stub the subprocess runner for deterministic behavior.
