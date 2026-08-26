# Agent instruction index

Choose the smallest instruction set that covers the current task. Root
`AGENTS.md` always applies; load the files below only when relevant.

## Task routing

- [Project map](project-map.md) for data shapes, repository navigation,
  ownership, and effect flow.
- [Python code guidelines](python-code.md) for library code, public API,
  diagnostics, or subprocess changes.
- [Testing guidelines](testing.md) for behavior tests, fixtures, doubles, and
  completion evidence.
- [Documentation guidelines](documentation.md) for README, Sphinx, examples,
  package metadata, `llms.txt`, or user-facing behavior.
- [Security guidelines](security.md) for recipients, message content, logs,
  subprocesses, scripts, paths, diagnostics, or credentials.
- [Git and release guidelines](git-release.md) for commits, pull requests,
  changelog entries, versions, artifacts, or publishing.

Do not load unrelated instruction files merely because they exist. The code,
current tests, public docs, and changelog outrank stale historical notes.
