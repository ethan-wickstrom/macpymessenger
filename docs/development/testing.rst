.. meta::
   :description lang=en:
      Run macpymessenger lint, format, type, test, documentation, package, CLI,
      Agent Skill, and private-data-safe transport checks locally.

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
   Checks public and internal types in ``src/``, ``tests/``, and ``scripts/``.

``pytest``
   Runs hermetic behavior tests with warnings treated as errors. Tests inject
   ``MessageTransport`` doubles and never send real messages. On macOS, one
   integration test compiles a rendered script with ``/usr/bin/osacompile``
   without executing it.

``sphinx-build -n -T -W --keep-going``
   Resolves references, prints full tracebacks, treats warnings as errors, and
   reports all documentation failures in one run.

``uv build``
   Creates the wheel and source distribution in ``dist/``. CI installs each
   artifact in an isolated environment and runs
   ``scripts/verify_installed_package.py``.

What the installed-package verifier covers
-------------------------------------------

The verifier checks:

- public imports and distribution version metadata;
- ``py.typed``, bundled AppleScript source, and the bundled core Agent Skill;
- the console entry point, top-level help, and ``send --help``;
- doctor JSON and blocker semantics;
- human and JSON skill discovery;
- invalid send rejection, exit status ``2``, and private-data-safe output; and
- the default client, request, bulk-result, and template-manager shapes.

Run the verifier against a local wheel after ``uv build``:

.. code-block:: bash

   wheel="$(find dist -name '*.whl' -print -quit)"
   uv run --isolated --no-project --python 3.14 --with "$wheel" \
     python -P scripts/verify_installed_package.py

Use ``-P`` so the repository cannot shadow the installed distribution.

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

Test command input safely
-------------------------

Replace ``sys.stdin`` with ``io.StringIO`` and inject a client backed by a
``MessageTransport`` double. Invalid input tests should replace
``IMessageClient`` with a function that raises if called; this proves rejection
happens before the effect boundary.

Test diagnostics safely
-----------------------

Monkeypatch platform discovery, fixed executable paths, Messages paths, and the
bundled-source loader. Do not make diagnostic tests depend on the current
runner, open Messages, invoke AppleScript, or trigger a permission prompt.
