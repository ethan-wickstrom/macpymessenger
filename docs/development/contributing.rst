.. meta::
   :description lang=en:
      Set up macpymessenger development with uv, hermetic transport tests,
      strict documentation, installed-artifact checks, and focused changes.

Contribute
==========

A useful contribution changes one public behavior or one authoritative data
shape, proves the change with hermetic tests, and updates the documentation that
owns the contract.

Requirements
------------

Install ``uv`` and use Python 3.14 or newer. Automated work does not require a
Messages account or permission to control Messages. The suite injects transport
doubles and must remain hermetic on Linux and macOS. A macOS-only integration
test compiles AppleScript but never executes it.

Set up the repository
---------------------

.. code-block:: bash

   git clone https://github.com/ethan-wickstrom/macpymessenger.git
   cd macpymessenger
   uv sync --locked
   uv run --locked pytest

Read ``AGENTS.md`` before agent-assisted work. It routes each task to the
smallest relevant instruction set. Read
``docs/agent-instructions/project-map.md`` before changing a data shape,
capability owner, or effect boundary.

Make a focused change
---------------------

#. State the public behavior or data shape that should change.
#. Add a failing behavior or edge-case test before production code when behavior
   changes.
#. Put the implementation at the layer that owns the behavior. Do not coordinate
   one capability through special cases across callers.
#. Keep effects behind ``MessageTransport`` and tests free of real sends.
#. Keep recipients, message bodies, account data, private paths, child output,
   and secrets out of process arguments, environment variables, temporary files,
   logs, tracebacks, examples, issues, and commits.
#. Update the owning guide, API page, ``README.md``, ``docs/llms.txt``, bundled
   Agent Skill, and ``CHANGELOG.md`` when their public contract changes.
#. Run the checks in :doc:`testing`.
#. Use a small Conventional Commit such as
   ``fix: keep message text out of argv``.

Preserve authoritative shapes
-----------------------------

Do not create a second representation for:

- ``SendRequest`` request data or validation;
- ``BulkSendFailure`` and ``BulkSendResult`` outcomes;
- ``EnvironmentCheck`` and ``EnvironmentReport`` diagnostics;
- installed ``AgentSkill`` content; or
- the versioned JSON command envelope.

Unsupported capabilities do not need placeholder methods. Chat history,
attachments, contact lookup, remote gateways, account management, and delivery
receipts remain outside the stable package.

Verify the installed product
----------------------------

Run the complete gate from the repository root:

.. code-block:: bash

   uv sync --locked
   uv run --locked ruff check
   uv run --locked ruff format --diff
   uv run --locked ty check
   uv run --locked pytest
   uv run --locked sphinx-build -n -T -W --keep-going docs docs/_build/html
   uv build

CI installs and verifies both the wheel and source distribution after the source
checks pass. The artifact verifier checks public imports, package data, typing,
request validation, bulk result shape, command help, the versioned JSON envelope,
validation-only sends, diagnostics, and the bundled Agent Skill. A source-tree
success is not enough when the installed artifact differs.

Report a problem
----------------

Open an issue at https://github.com/ethan-wickstrom/macpymessenger/issues. Include
what you expected, what happened, ``uv run macpymessenger doctor --json`` output,
and the smallest reproducer. Remove phone numbers, email addresses, account
details, message text, child output, and private paths before posting logs or
tracebacks.
