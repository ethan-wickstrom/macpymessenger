# Cleanup candidates

Use this file when deciding whether a proposed agent instruction belongs in active guidance.

The instructions below should stay out of the root `AGENTS.md`. Some may belong in focused task files; others should be deleted entirely.

## Redundant with normal agent behavior

- "You are an expert in writing documentation."
- "You always use the latest stable documentation practices."
- "Apply empathy constantly by imagining the reader's perspective and challenges."
- "Break established rules when doing so better serves reader comprehension."

## Too vague to be directly actionable

- "Ensure every sentence contributes directly to reader understanding."
- "Create documentation that scales from beginner to advanced usage patterns."
- "Validate that documentation solves real user problems effectively."
- "Design documentation to work effectively across different reading contexts and devices."
- "Use analogies and concrete examples to explain abstract concepts."
- "Keep code easy to skim."

## Too broad for the root AGENTS.md

- "Test documentation with representative users to identify comprehension gaps."
- "Measure documentation effectiveness through user feedback and support ticket reduction."
- "Establish clear ownership and review processes for documentation maintenance."
- "Create documentation templates that enforce consistency across teams."
- "Implement automated checks for broken links and outdated information."
- "Design documentation to be easily translatable and culturally adaptable."

## Better kept as task-specific guidance

- Architecture boundaries belong in `project-map.md` and `python-code.md`.
- Detailed documentation style rules belong in `documentation.md`.
- Commit and release details belong in `git-release.md`.
- Test fixture and subprocess stubbing rules belong in `testing.md`.
- Security rules belong in `security.md`.
