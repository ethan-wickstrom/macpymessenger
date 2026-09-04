.. meta::
   :description lang=en:
      Release macpymessenger with semantic versions, verified distributions,
      short-lived PyPI identity, and installed command smoke tests.

Release process
===============

Releases are maintainer tasks.

Prepare Trusted Publishing once
-------------------------------

Configure a PyPI Trusted Publisher for this repository before the first release:

- owner: ``ethan-wickstrom``;
- repository: ``macpymessenger``;
- workflow: ``python-publish.yml``; and
- environment: ``pypi``.

The workflow requests a short-lived OpenID Connect identity only in the publish
job. It does not use a stored PyPI token. The build job has read-only repository
access and cannot publish.

Release a version
-----------------

#. Confirm that ``CHANGELOG.md`` describes every user-visible addition, change,
   removal, and migration step.
#. Update the version in ``pyproject.toml`` using Semantic Versioning.
#. Update version-specific examples only when the output contract changed.
#. Run every command in :doc:`testing`.
#. Merge only when Linux and macOS CI pass.
#. Tag the verified commit with the exact package version, such as ``v0.4.0``.
#. Publish a GitHub release from that tag.
#. Let the release workflow reject a tag/version mismatch, build the wheel and
   source distribution, and install each artifact in an isolated Python 3.14
   environment.
#. Let ``scripts/verify_installed_package.py`` verify public imports, package
   data, ``py.typed``, the AppleScript source, the console entry point, doctor
   JSON, send input rejection, and the bundled Agent Skill.
#. Let the unprivileged build job upload the verified distributions.
#. Let the separate ``pypi`` environment job download those exact artifacts and
   publish them with its short-lived identity.
#. Install the published version independently and check ``macpymessenger
   --version``, ``macpymessenger doctor --json``, and ``macpymessenger skills get
   core``.

The built distributions are the release units. Passing source-tree tests is
necessary but not enough. Never publish from an uncommitted tree, bypass the
installed-package verifier, rebuild inside the credential-bearing job, or place
credentials in a command, example, commit, or build log.
