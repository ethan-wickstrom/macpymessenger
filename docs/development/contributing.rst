.. meta::
   :description lang=en:
      Set up macpymessenger development with uv, hermetic transport tests,
      strict docs, and focused contribution rules.

Contribute
==========

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

Read ``AGENTS.md`` before agent-assisted work. It routes each task to the
smallest relevant instruction set and project map.

Make a focused change
---------------------

#. Start from the public behavior or data shape that should change.
#. Add a failing behavior test before production code when behavior changes.
#. Keep effects behind ``MessageTransport`` and tests free of real sends.
#. Keep recipients, message bodies, account data, private paths, and secrets out
   of process arguments, files, logs, tracebacks, examples, and commits.
#. Update the owning guide, API page, ``README.md``, ``docs/llms.txt``, and
   ``CHANGELOG.md`` when their public contract changes.
#. Run the checks in :doc:`testing`.
#. Use a small Conventional Commit such as ``fix: keep message text out of argv``.

Report a problem
----------------

Open an issue at https://github.com/ethan-wickstrom/macpymessenger/issues. Include
what you expected, what happened, ``uv run macpymessenger doctor --json`` output,
and the smallest reproducer. Remove phone numbers, email addresses, account
details, message text, and private paths before posting logs or tracebacks.
