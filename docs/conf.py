"""Sphinx configuration for macpymessenger."""

from __future__ import annotations

import os
import sys
import tomllib
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_PATH))

with (PROJECT_ROOT / "pyproject.toml").open("rb") as pyproject_stream:
    project_metadata = tomllib.load(pyproject_stream)["project"]

project = project_metadata["name"]
release = project_metadata["version"]
version = release

author_names = [record["name"] for record in project_metadata.get("authors", [])]
author = ", ".join(author_names)
copyright = f"2024-2026, {author}"  # noqa: A001

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3.14/", None),
}

autosummary_generate = True
autodoc_default_options = {
    "members": True,
    "show-inheritance": True,
}
autodoc_member_order = "bysource"
autodoc_type_aliases = {
    "MessageFailureReason": "macpymessenger.MessageFailureReason",
}
autodoc_typehints = "description"

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
language = "en"
root_doc = "index"
templates_path: list[str] = []

html_theme = "alabaster"
html_title = "macpymessenger: send iMessages from Python on macOS"
html_short_title = "macpymessenger"
html_baseurl = os.environ.get(
    "READTHEDOCS_CANONICAL_URL",
    "https://macpymessenger.readthedocs.io/en/latest/",
)
html_use_opensearch = "https://macpymessenger.readthedocs.io/en/latest"
html_extra_path = ["llms.txt"]
html_static_path: list[str] = []
html_theme_options = {
    "description": "Send iMessages from Python on macOS.",
    "github_button": True,
    "github_repo": "macpymessenger",
    "github_user": "ethan-wickstrom",
}
htmlhelp_basename = project

napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = False
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
