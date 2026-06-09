# Git and release guidelines

Use this file when preparing commits, pull requests, changelog entries, or releases.

## Commits use Conventional Commits

- Use prefixes such as `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`, and `ci:`.
- Use an optional scope when it adds useful context.
- Example: `feat(client): raise MessageSendError on failures`.

## Pull requests should stay short and structured

- Explain why the change exists.
- Summarize how the change works.
- Link related issues such as `Closes #123`.
- Include checks run and results.
- Include documentation and changelog updates when behavior changes.

## Releases are maintainer tasks

- Update `CHANGELOG.md` with user-visible changes.
- Link to relevant documentation when helpful.
- Bump `pyproject.toml` using Semantic Versioning.
- Ensure CI is green.
- Tag releases with a version such as `v0.2.0`.
- Publish through the GitHub workflow.
