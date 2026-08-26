.. meta::
   :description lang=en:
      Use the macpymessenger command line from shell scripts and AI agents with
      JSON over standard input, stable output, exit codes, and Agent Skills.

Use the command line
====================

The ``macpymessenger`` command provides three bounded workflows:

- ``doctor`` checks the local Mac without sending a message;
- ``send`` sends one user-approved text from one JSON object on standard input;
  and
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

List the available skills with compact text:

.. code-block:: bash

   macpymessenger skills

Use stable JSON when another program consumes the catalog:

.. code-block:: bash

   macpymessenger skills list --json

Check the Mac
-------------

Run the side-effect-free diagnostic before the first send:

.. code-block:: bash

   macpymessenger doctor --json

A ``blocked`` value of ``false`` means no automated blocker was found. It does
not prove that Messages is signed in or that the current launcher has Automation
permission. Follow every check whose status is ``manual``.

Send one message
----------------

``send`` reads exactly one JSON object from standard input. Recipient and
message text do not enter the ``macpymessenger`` process arguments, environment
variables, or temporary files:

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

Unknown fields, duplicate keys, malformed JSON, non-UTF-8 text, and missing or
empty required strings fail before the client or Messages effect is created.

Read the result
---------------

With ``--json``, ``send`` writes one compact object to standard output. It never
echoes the recipient or message.

A successful result has this shape:

.. code-block:: json

   {"ok":true,"tool":"macpymessenger-send","version":"0.3.0"}

A failed send has a generic code and closed reason:

.. code-block:: json

   {
     "error": {"code": "delivery_failed", "reason": "delivery"},
     "ok": false,
     "tool": "macpymessenger-send",
     "version": "0.3.0"
   }

The process exit status is authoritative:

``0``
   The local AppleScript transport completed.

``1``
   Messages rejected the send or the local transport could not run.

``2``
   Standard input was malformed or did not match the closed request shape.

A zero exit status is not a delivery receipt from the recipient's device. Do not
automatically retry a failed or uncertain send because a retry may create a
duplicate message.

Human output
------------

Omit ``--json`` for a short human result:

.. code-block:: text

   Message sent.

Human errors go to standard error. Structured output goes to standard output,
so programs can compose the command with ordinary Unix pipes without parsing
prose.
