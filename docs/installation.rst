Installation
============

macpymessenger ships on PyPI and can be installed with either Astral's `uv` (recommended) or standard tooling.

Prerequisites
-------------

- macOS with Python 3.10 or newer.
- `uv` 0.4+ for reproducible project environments (optional but recommended).

Installing with uv
------------------

.. code-block:: bash

   uv pip install macpymessenger

This command downloads the latest release and isolates it inside uv's managed environment cache.

Installing with pip
-------------------

.. code-block:: bash

   pip install macpymessenger

Upgrading macpymessenger
------------------------

To upgrade to the newest version:

.. code-block:: bash

   uv pip install --upgrade macpymessenger

Verification
------------

Confirm the installation succeeded by importing the library:

.. code-block:: bash

   python -c "import macpymessenger; print(macpymessenger.__version__)"

Troubleshooting
---------------

- Ensure the underlying AppleScript file exists if you provide a custom path.
- Verify that your Python interpreter meets the minimum version requirement.
- Use ``uv pip --verbose`` for additional diagnostics when installing with uv.
