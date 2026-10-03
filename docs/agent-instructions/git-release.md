# Git and release guidelines

Use this file for commits, pull requests, changelog entries, or releases.

## Commits

- Use Conventional Commit prefixes such as `feat:`, `fix:`, `docs:`,
  `refactor:`, `test:`, `build:`, and `ci:`.
- Keep each commit to one coherent behavior, data shape, scaffold, or document.
- State the outcome, not the editing activity. Prefer `feat: add environment
  diagnostics` over `chore: update files`.
- Never commit credentials, private recipients, generated build output, or real
  message text.

## Pull requests

- Lead with the developer or maintainer problem solved.
- Describe public additions, changes, removals, and migration steps separately.
- Link related issues.
- Report exact verification commands and hosted CI outcomes.
- Update `README.md`, owning docs, `docs/llms.txt`, package metadata, agent
  instructions, and `CHANGELOG.md` when their contract changes.

## Releases

- Treat the wheel as the release unit, not the source checkout.
- Use Semantic Versioning in `pyproject.toml`; pre-1.0 breaking changes require a
  minor-version release.
- Complete the full root `AGENTS.md` gate and require Linux and macOS CI.
- Tag only the verified commit.
- Let the release workflow build, clean-install, import, inspect bundled data,
  run the console entry point, and publish.
- Independently install the published artifact and check `macpymessenger
  --version` plus `macpymessenger doctor --json`.

## Local version preflight

Before choosing a release tag, save a fresh public PyPI JSON snapshot and run:

```bash
curl --fail --silent --show-error https://pypi.org/pypi/macpymessenger/json -o /tmp/macpymessenger-pypi.json
uv run --locked python scripts/check_release_version.py --published-metadata /tmp/macpymessenger-pypi.json
```

The check is offline and rejects a version already present in that snapshot,
even when its release file list is empty. It is intentionally separate from
ordinary development CI: an Unreleased checkout may retain the current version.
Exit 0 only means the version is absent from the supplied snapshot, not that
release gates passed. Refresh the snapshot immediately before a release review.
Keep the README and installation guide explicit about development source installs
until their examples are available in a published release. At release preparation,
replace the source pin with the chosen published version requirement after its
artifact has been independently verified. Never publish a development build as
an already published version.
