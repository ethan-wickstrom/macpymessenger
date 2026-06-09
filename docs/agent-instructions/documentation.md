# Documentation guidelines

Use this file when changing `README.md`, `docs/`, examples, or user-facing behavior.

## Keep user-facing behavior accurate

- Show `send()` as raising `MessageSendError` on delivery failure.
- Show template factories as callables that return t-strings.
- Show template context as required when the callable requires arguments.
- Avoid Jinja2 examples for current behavior.
- Keep code examples self-contained and dependency-minimal.

## Use consistent terminology

- Use the same term for the same domain concept across code and docs.
- Allow established technical terms such as API, CI, PR, HTML, PyPI, and Sphinx.
- Use specific terms instead of vague labels such as manager, handler, data, item, object, service, status, type, or process unless the project domain uses that term precisely.

## Maintain Sphinx documentation

- Update the README or `.rst` page that owns changed user-facing behavior.
- Add or update `.rst` pages in `docs/`.
- Include new `.rst` pages in `docs/index.rst`.
- Build documentation with `uv run sphinx-build docs docs/_build/html`.

For public documentation information architecture changes, see
[suggested-docs-structure.md](suggested-docs-structure.md).
