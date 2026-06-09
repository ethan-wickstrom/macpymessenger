# Domain docs

How the engineering skills should consume this repo's domain documentation when exploring the codebase.

## Layout

This repo uses a multi-context domain documentation layout.

- `CONTEXT-MAP.md` at the repo root points to the relevant context docs.
- `docs/adr/` holds repo-wide architecture decisions.
- Context-specific `CONTEXT.md` files and `docs/adr/` directories may live near the code they describe.

If these files do not exist yet, proceed silently. Producer skills such as `grill-with-docs` create them lazily when terms or decisions are resolved.

## Before exploring, read these

- Read `CONTEXT-MAP.md` first when it exists.
- Read each context `CONTEXT.md` relevant to the task.
- Read ADRs that touch the area you're about to work in.

## Use glossary vocabulary

When output names a domain concept in an issue title, refactor proposal, hypothesis, or test name, use the term defined in the relevant `CONTEXT.md`.

If the concept is missing, do not invent a smooth abstraction. Note the gap for `grill-with-docs`.

## Flag ADR conflicts

If output contradicts an existing ADR, surface it explicitly rather than silently overriding.
