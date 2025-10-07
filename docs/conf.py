"""Sphinx configuration for macpymessenger documentation."""

from __future__ import annotations

import importlib
import sys
import warnings
from pathlib import Path

import tomllib

# Ensure the project source is importable when building the docs.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

with (PROJECT_ROOT / "pyproject.toml").open("rb") as pyproject_stream:
    _pyproject = tomllib.load(pyproject_stream).get("project", {})

project = _pyproject.get("name", "macpymessenger")
release = _pyproject.get("version", "0.0.0")
version = release

_authors = [author_record.get("name") for author_record in _pyproject.get("authors", [])]
author = ", ".join(name for name in _authors if name) or "Unknown"

if sys.version_info >= (3, 10):
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

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.autosummary',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

master_doc = 'index'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']

# -- Options for autodoc extension -------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#configuration

autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'private-members': True,
    'special-members': '__init__',
    'inherited-members': True,
    'show-inheritance': True,
}

autodoc_mock_imports = [
    'dotenv',
    'pytest',
]

# -- Options for autosummary extension ---------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/autosummary.html#configuration

autosummary_generate = True

# -- Options for viewcode extension ------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/viewcode.html#configuration

viewcode_import = True

# -- Options for HTMLHelp output ---------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-htmlhelp-output

htmlhelp_basename = project

# -- Options for Napoleon extension ------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html#configuration

napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = True
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
