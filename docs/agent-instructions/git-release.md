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
