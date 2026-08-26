# CI and agent integration review

This note records the facts, hypotheses, primary sources, decisions, and verification for PR #56.

## Facts

- PR #53 merged at `a5fa6fb9f5e9293b6658e0c755c5d4354139d1d4` and left the CI formatter gate failing on both Linux and macOS.
- The formatter failure came from merged Python files that were not in Ruff's canonical form. A stale invariant test also referred to the deleted configuration and command-runner design.
- PR #56 repairs those failures and adds an agent-facing command surface on branch `fix/ci-and-agent-cli`.
- The current PR merge run reaches dependency setup, then fails strict Ruff lint in the new CLI and Agent Skill loader.
- The existing `SendRequest` is the authoritative shape for one send. A second CLI-only request model would duplicate knowledge.
- `AppleScriptTransport` already sends the rendered AppleScript through standard input to `/usr/bin/osascript -`; recipient and message text do not enter process arguments.
- The installed command already owns diagnostics and package-version reporting, so the same command is the narrowest place for send and skill workflows.
- macpymessenger has no runtime dependencies and should keep that property unless the standard library cannot meet a proven need.

## Hypotheses

| ID | Hypothesis | Confidence | Evidence or test |
| --- | --- | ---: | --- |
| H1 | The original CI failure is deterministic formatter drift, not an operating-system-specific fault. | 1.00 | Both jobs failed the same Ruff formatter gate; formatting the two reported files repairs that class of failure. |
| H2 | A JSON request on standard input is the smallest safe Unix interface for agent sends. | 0.99 | It reuses `SendRequest`, preserves arbitrary Unicode and line breaks, avoids shell parsing, and keeps private values out of process arguments and temporary files. |
| H3 | A thin repository discovery skill plus CLI-served runtime instructions prevents installed-command and skill-version drift. | 0.99 | Vercel agent-browser uses this split: the stable discovery stub points to skill content bundled with the installed CLI. |
| H4 | Human output plus explicit JSON output is better than JSON-only output. | 0.97 | Shell users get compact text; agents get stable fields and exit codes without parsing prose. |
| H5 | Promoting `skills get core` in top-level help and making bare `skills` list the catalog improves discovery without adding a new subsystem. | 0.94 | agent-browser moved its skills entry point near `Usage:` after agents skipped a buried help section. |
| H6 | A daemon, background service, plugin host, or protocol server would add state and failure modes without helping this one-shot send workflow. | 0.99 | Each operation is a bounded local process call; no session state or expensive startup must persist between commands. |
| H7 | A YAML runtime dependency is unnecessary for one controlled bundled skill. | 0.94 | The package needs only required single-line `name` and `description` fields; repository tests can enforce the supported subset and the public Agent Skills constraints. |
| H8 | Automatic retries are unsafe because a transport failure may occur after Messages accepted the send. | 0.99 | The package has no delivery receipt or idempotency key; retrying can duplicate a message. |

## Primary sources

- Vercel agent-browser repository and command documentation: <https://github.com/vercel-labs/agent-browser>
- Vercel agent-browser runtime skill implementation: <https://github.com/vercel-labs/agent-browser/blob/4ad28489/cli/src/skills.rs>
- Vercel agent-browser discovery skill: <https://github.com/vercel-labs/agent-browser/blob/main/skills/agent-browser/SKILL.md>
- Vercel agent-browser core runtime skill: <https://github.com/vercel-labs/agent-browser/blob/main/skill-data/core/SKILL.md>
- Vercel agent-browser skill-versioning change: <https://github.com/vercel-labs/agent-browser/pull/1225>
- Vercel agent-browser help-discovery change: <https://github.com/vercel-labs/agent-browser/pull/1251>
- Agent Skills format specification: <https://github.com/agentskills/agentskills/blob/main/docs/specification.mdx>
- Agent Skills implementation guide: <https://github.com/agentskills/agentskills/blob/main/docs/client-implementation/adding-skills-support.mdx>

## Decisions

- Add `macpymessenger send`, which accepts exactly one JSON object from standard input.
- Keep the send contract on `SendRequest` and the effect boundary on `IMessageClient` and `MessageTransport`.
- Return stable exit codes: `0` for success, `1` for a send failure, and `2` for invalid input.
- Never echo recipient or message content in command output or library logs.
- Add a spec-shaped discovery skill under `.agents/skills/macpymessenger/`.
- Serve the current workflow from `macpymessenger skills get core` so it always matches the installed package.
- Keep one core skill until another workflow has distinct triggers, steps, and references.
- Do not add a daemon, protocol server, configuration language, runtime YAML package, automatic retries, or agent-specific SDK.

## Verification record

Pending. The completion gate is:

```bash
uv sync --locked
uv run --locked ruff check
uv run --locked ruff format --check
uv run --locked ty check
uv run --locked pytest
uv run --locked sphinx-build -n -T -W --keep-going docs docs/_build/html
uv build
```

The built wheel must also expose the send command, bundled core skill, package version, diagnostics, and private-data-safe JSON output in a clean environment.
