Installation
============

**macpymessenger requires macOS and Python 3.14 or newer.** It sends through the Messages app by running AppleScript.

Install with uv
---------------

**Use ``uv add`` when you are adding macpymessenger to a project.**

.. code-block:: bash

   uv add macpymessenger

This updates your project environment and records the dependency.

Install with pip
----------------

**Use ``pip`` when you want a standard Python install.**

.. code-block:: bash

   pip install macpymessenger

Verify the install
------------------

**Import the package to check that Python can find it.**

.. code-block:: bash

   python -c "from macpymessenger import Configuration; print(Configuration())"

This also checks that the bundled AppleScript exists and is readable.

Check the installed package metadata if needed:

.. code-block:: bash

   pip show macpymessenger

Common install issues
---------------------

**Python is too old.** Run ``python --version``. You need Python 3.14 or newer.

**The platform is not macOS.** The package can install elsewhere, but sending messages requires macOS, AppleScript, and Messages.app.

**A custom script path fails.** ``Configuration(send_script_path=...)`` checks the file immediately. Make sure the file exists and can be read.

Development setup
-----------------

**Use ``uv sync`` when you are working on this repository.**

.. code-block:: bash

   uv sync

Then run commands inside the environment with ``uv run``.
