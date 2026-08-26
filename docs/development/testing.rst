.. meta::
   :description lang=en:
      Run macpymessenger lint, format, type, test, documentation, package, and
      private-data-safe transport checks locally.

Test and check changes
======================

Run all commands from the repository root:

.. code-block:: bash

   uv sync --locked
   uv run --locked ruff check
   uv run --locked ruff format --diff
   uv run --locked ty check
   uv run --locked pytest
   uv run --locked sphinx-build -n -T -W --keep-going docs docs/_build/html
   uv build

What each check covers
----------------------

``uv sync --locked``
   Recreates the declared environment and fails when ``uv.lock`` is stale.

``ruff check`` and ``ruff format --diff``
   Find bugs, enforce imports and style, reject unformatted files, and print the
   exact formatter patch when a file differs.

``ty check``
   Checks public and internal types in ``src/`` and ``tests/``.

``pytest``
   Runs hermetic behavior tests. Tests inject ``MessageTransport`` doubles and
   never send real messages. On macOS, one integration test compiles a rendered
   script with ``/usr/bin/osacompile`` without executing it.

``sphinx-build -n -T -W --keep-going``
   Resolves references, prints full tracebacks, treats warnings as errors, and
   reports all documentation failures in one run.

``uv build``
   Creates the wheel and source distribution in ``dist/``. CI then installs the
   wheel in a clean environment and checks public imports, ``py.typed``, bundled
   AppleScript source, the console entry point, and doctor JSON.

Test delivery code safely
-------------------------

Inject a transport that records immutable requests:

.. code-block:: python

   from macpymessenger import IMessageClient, SendRequest


   class RecordingTransport:
       def __init__(self) -> None:
           self.requests: list[SendRequest] = []

       def send(self, request: SendRequest) -> None:
           self.requests.append(request)


   transport = RecordingTransport()
   client = IMessageClient(transport=transport)
   client.send("+15555550123", "Hello")

   assert transport.requests == [SendRequest("+15555550123", "Hello")]

Test diagnostics safely
-----------------------

Monkeypatch platform discovery, fixed executable paths, Messages paths, and the
bundled-source loader. Do not make diagnostic tests depend on the current
runner, open Messages, invoke AppleScript, or trigger a permission prompt.
