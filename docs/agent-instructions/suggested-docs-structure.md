# Suggested docs structure

Use this as a future information architecture target for the public Sphinx documentation.

```text
docs/
|-- index.rst
|-- introduction.rst
|-- installation.rst
|-- usage.rst
|-- configuration.rst
|-- testing.rst
|-- modules.rst
|-- guides/
|   |-- sending-messages.rst
|   |-- templates.rst
|   |-- logging.rst
|   `-- troubleshooting.rst
|-- api/
|   |-- client.rst
|   |-- configuration.rst
|   |-- templates.rst
|   `-- exceptions.rst
|-- development/
|   |-- contributing.rst
|   |-- testing.rst
|   `-- release-process.rst
`-- agent-instructions/
    |-- index.md
    |-- project-map.md
    |-- python-code.md
    |-- testing.md
    |-- documentation.md
    |-- git-release.md
    |-- security.md
    `-- suggested-docs-structure.md
```

## Why this structure helps

- Top-level pages stay useful for first-time readers.
- `guides/` holds task-oriented user workflows.
- `api/` holds reference material for public modules and classes.
- `development/` holds contributor-facing process documentation.
- `agent-instructions/` keeps agent behavior separate from user documentation.
