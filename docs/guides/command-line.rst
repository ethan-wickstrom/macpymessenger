.. meta::
   :description lang=en:
      Use the macpymessenger command line from shell scripts and AI agents with
      validation-only sends, versioned JSON, stable exit codes, and Agent Skills.

Use the command line
====================

The ``macpymessenger`` command provides three bounded workflows:

- ``doctor`` checks local prerequisites without sending a message;
- ``send`` validates or executes one user-approved text request from JSON on
  standard input; and
- ``skills`` lists or loads instructions bundled with the installed package.

Run ``macpymessenger --help`` for the current command surface. Inside a uv
project, prefix each command with ``uv run``.

Load the installed Agent Skill
------------------------------

Agents should start with:

.. code-block:: bash

   macpymessenger skills get core

The command prints the core ``SKILL.md`` bundled with the installed wheel. The
instructions therefore describe the same command version that the agent will
run. A repository may contain a small discovery skill that points to this
command, but the installed package remains the workflow source of truth.

List available skills with compact text:

.. code-block:: bash

   macpymessenger skills

Use versioned JSON when another program consumes the catalog:

.. code-block:: bash

   macpymessenger skills list --json

Check the Mac
-------------

Run the side-effect-free diagnostic before the first send:

.. code-block:: bash

   macpymessenger doctor --json

A ``data.blocked`` value of ``false`` means no automated blocker was found. It
does not prove that Messages is signed in or that the current launcher has
Automation permission. Follow every check whose status is ``manual``.

Build one closed request
------------------------

``send`` reads exactly one JSON object from standard input. Recipient and
message text do not enter process arguments, environment variables, or temporary
files:

.. code-block:: bash

   cat <<'JSON' | macpymessenger send --json
   {"recipient":"<recipient>","message":"<message>","delay_seconds":0}
   JSON

The object accepts only these fields:

``recipient``
   Required non-empty string. Use the phone number or Messages email address
   supplied by the user.

``message``
   Required non-empty string. Preserve the exact user-approved text.

``delay_seconds``
   Optional non-negative integer. The default is ``0``. Booleans and numbers
   with a fractional part are invalid.

Unknown fields, duplicate keys, malformed JSON, text that cannot be encoded as
UTF-8, and missing or empty required strings fail before the client or Messages
effect is created. The CLI constructs the same immutable ``SendRequest`` used by
the Python API and transport boundary; it does not maintain a second request
model.

Validate without sending
------------------------

Use ``--dry-run`` to validate the closed JSON request without constructing an
``IMessageClient``, loading the AppleScript transport, or sending a message:

.. code-block:: bash

   cat <<'JSON' | macpymessenger send --dry-run --json
   {"recipient":"<recipient>","message":"<message>","delay_seconds":0}
   JSON

A valid dry run returns exit status ``0`` and ``data.outcome`` set to
``"validated"``. Dry-run validation does not check macOS, Messages sign-in, or
Automation permission. Run ``doctor --json`` for detectable environment
blockers and complete its manual checks.

A dry run consumes standard input. Supply the approved request again for the
real send. Do not persist private request data in a temporary file or environment
variable merely to reuse it.

Read the versioned JSON envelope
--------------------------------

Every command that supports ``--json`` uses the same top-level envelope:

``schema_version``
   Integer version of the machine contract. This release uses ``1``.

``tool``
   Always ``"macpymessenger"``.

``command``
   Stable command identifier: ``"send"``, ``"doctor"``, or ``"skills.list"``.

``version``
   Installed package version.

``ok``
   Boolean command outcome. For ``doctor``, true means no automated blocker was
   found, not that delivery is proven.

``data`` or ``error``
   Successful commands and diagnostics return ``data``. Failed commands return
   ``error`` with a stable ``code``. Send errors also expose ``retryable: false``
   because automatic retries may duplicate a message.

A validated dry run has this shape:

.. code-block:: json

   {
     "command": "send",
     "data": {"outcome": "validated"},
     "ok": true,
     "schema_version": 1,
     "tool": "macpymessenger",
     "version": "0.3.0"
   }

A completed local transport has the same envelope with
``data.outcome`` set to ``"transport_completed"``. This outcome is not a
delivery receipt from the recipient's device.

A failed send has a generic code and closed reason:

.. code-block:: json

   {
     "command": "send",
     "error": {
       "code": "delivery_failed",
       "reason": "delivery",
       "retryable": false
     },
     "ok": false,
     "schema_version": 1,
     "tool": "macpymessenger",
     "version": "0.3.0"
   }

The command never echoes the recipient or message in structured output.

Use exit status as the process result
-------------------------------------

``0``
   The request was valid in dry-run mode, or the local AppleScript transport
   completed in send mode.

``1``
   Messages rejected the send, the local transport could not run, or ``doctor``
   found a definite blocker.

``2``
   Standard input was malformed or did not match the closed request shape.

Do not automatically retry a failed or uncertain send. The package has no
idempotency key or recipient delivery receipt, so a retry may create a duplicate
message.

Human output
------------

Omit ``--json`` for short human output. A successful real send says:

.. code-block:: text

   Send request completed. Delivery is not confirmed.

A successful dry run says:

.. code-block:: text

   Request is valid. No message was sent.

Human errors go to standard error. Structured output goes to standard output,
so programs can compose the command with ordinary Unix pipes without parsing
prose.
