.. meta::
   :description lang=en:
      Release macpymessenger with semantic versions, changelog updates, strict
      CI, and clean installed-wheel smoke tests before PyPI publication.

Release process
===============

Releases are maintainer tasks.

#. Confirm that ``CHANGELOG.md`` describes every user-visible addition, change,
   removal, and migration step.
#. Update the version in ``pyproject.toml`` using Semantic Versioning.
#. Update version-specific examples only when the output contract changed.
#. Run every command in :doc:`testing`.
#. Merge only when Linux and macOS CI pass.
#. Tag the verified commit with a version such as ``v0.4.0``.
#. Publish a GitHub release from that tag.
#. Let the release workflow build the wheel and source distribution, install the
   wheel in a clean Python 3.14 environment, verify package data and public
   imports, run the console entry point, and then upload to PyPI.
#. Install the published version independently and check ``macpymessenger
   --version`` and ``macpymessenger doctor --json``.

The built wheel is the release unit. Passing source-tree tests is necessary but
not enough. Never publish from an uncommitted tree, bypass the clean-wheel smoke
test, or place credentials in a command, example, commit, or build log.
