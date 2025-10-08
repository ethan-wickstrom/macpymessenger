Installation
============

**macpymessenger requires macOS and Python 3.14 or newer.**

The library is published on PyPI. Install with `uv` or `pip`.

Install with uv (recommended)
------------------------------

**uv provides faster installs and reproducible environments.**

.. code-block:: bash

   uv pip install macpymessenger

This command downloads the latest release from PyPI and installs it in the current environment.

Install with pip
----------------

.. code-block:: bash

   pip install macpymessenger

Upgrade to the latest version
------------------------------

**Use the upgrade flag to get the newest release:**

.. code-block:: bash

   uv pip install --upgrade macpymessenger

Or with pip:

.. code-block:: bash

   pip install --upgrade macpymessenger

Verify the installation
------------------------

**Import the library to confirm installation succeeded:**

.. code-block:: bash

   python -c "from macpymessenger import Configuration; print(Configuration())"

This command checks that Python can locate the package and that the bundled AppleScript is present.

**Check the installed version:**

.. code-block:: bash

   pip show macpymessenger

Troubleshooting installation
-----------------------------

**Python version is too old.** macpymessenger requires Python 3.14 or newer. Check your version with `python --version`.

**Custom AppleScript path fails.** If you provide a custom script path to `Configuration`, ensure the file exists and is readable.

**Installation fails with uv.** Run `uv pip install --verbose macpymessenger` to see detailed error messages.
