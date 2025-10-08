"""Sphinx configuration for macpymessenger documentation.

This configuration file defines settings for building HTML documentation with Sphinx.
The configuration reads project metadata from pyproject.toml and imports the package
to extract the public API.
"""

from __future__ import annotations

import importlib
import sys
import warnings
from pathlib import Path

import tomllib

# Add the project source to sys.path so Sphinx can import macpymessenger.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

# Load project metadata from pyproject.toml.
with (PROJECT_ROOT / "pyproject.toml").open("rb") as pyproject_stream:
    _pyproject = tomllib.load(pyproject_stream).get("project", {})

# Extract project name, version, and authors from metadata.
project = _pyproject.get("name", "macpymessenger")
release = _pyproject.get("version", "0.0.0")
version = release

_authors = [author_record.get("name") for author_record in _pyproject.get("authors", [])]
author = ", ".join(name for name in _authors if name) or "Unknown"

# Import the package to extract the public API from __all__.
# This enables Sphinx to document only the classes and functions we export.
if sys.version_info >= (3, 14):
    try:
        _module = importlib.import_module(project)
    except Exception as import_error:  # pragma: no cover - defensive for older doc builders
        warnings.warn(
            f"Unable to import project package '{project}' while configuring docs: {import_error}",
            RuntimeWarning,
        )
        public_api: tuple[str, ...] = ()
    else:
        public_api = tuple(sorted(getattr(_module, "__all__", ())))
else:  # pragma: no cover - executed only on unsupported interpreters
    warnings.warn(
        "Skipping project import because the docs builder is running on Python < 3.10.",
        RuntimeWarning,
    )
    public_api = ()

copyright_year = "2025"
copyright = f"{copyright_year}, {author}"

# -- General Sphinx configuration --------------------------------------------

# Sphinx extensions provide additional documentation features.
extensions = [
    "sphinx.ext.autodoc",  # Generate docs from docstrings
    "sphinx.ext.viewcode",  # Add links to source code
    "sphinx.ext.napoleon",  # Support Google-style docstrings
    "sphinx.ext.autosummary",  # Generate summary tables
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

master_doc = "index"

# -- HTML output configuration -----------------------------------------------

html_theme = "alabaster"
html_static_path = ["_static"]

# -- autodoc extension configuration -----------------------------------------
# Controls how API documentation is generated from docstrings.

autodoc_default_options = {
    "members": True,  # Document all members
    "undoc-members": True,  # Include members without docstrings
    "private-members": True,  # Include private members
    "special-members": "__init__",  # Include __init__ method
    "inherited-members": True,  # Include inherited members
    "show-inheritance": True,  # Show base classes
}

# Mock these imports when building docs (they are not needed at doc build time).
autodoc_mock_imports = [
    "dotenv",
    "pytest",
]

# -- autosummary extension configuration -------------------------------------

autosummary_generate = True  # Automatically generate stub files

# -- viewcode extension configuration ----------------------------------------

viewcode_import = True  # Import modules for source links

# -- HTMLHelp output configuration -------------------------------------------

htmlhelp_basename = project

# -- Napoleon extension configuration ----------------------------------------
# Napoleon parses Google-style and NumPy-style docstrings.

napoleon_google_docstring = True  # Parse Google-style docstrings
napoleon_numpy_docstring = False  # Do not parse NumPy-style docstrings
napoleon_include_init_with_doc = True  # Include __init__ docstrings
napoleon_include_private_with_doc = True  # Include private member docstrings
napoleon_include_special_with_doc = True  # Include special member docstrings
napoleon_use_admonition_for_examples = False  # Use plain blocks for examples
napoleon_use_admonition_for_notes = False  # Use plain blocks for notes
napoleon_use_admonition_for_references = False  # Use plain blocks for references
napoleon_use_ivar = False  # Do not use :ivar: for attributes
napoleon_use_param = True  # Use :param: for parameters
napoleon_use_rtype = True  # Use :rtype: for return types
