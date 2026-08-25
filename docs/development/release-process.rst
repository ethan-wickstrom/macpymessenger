Release process
===============

Releases are maintainer tasks.

#. Confirm that ``CHANGELOG.md`` describes user-visible changes.
#. Update the version in ``pyproject.toml`` using Semantic Versioning.
#. Run every command in :doc:`testing`.
#. Merge only when continuous integration passes.
#. Tag the commit with a version such as ``v0.4.0``.
#. Publish through the GitHub release workflow.
#. Check the installed wheel in a clean environment.

Do not publish from an uncommitted working tree. Never place credentials in a
command, example, commit, or build log.
