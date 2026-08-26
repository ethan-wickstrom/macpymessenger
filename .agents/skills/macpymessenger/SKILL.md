---
name: macpymessenger
description: Send a user-approved text through the local macOS Messages app or inspect macpymessenger readiness. Use when the user explicitly asks an agent to send an iMessage with macpymessenger.
license: Apache-2.0
compatibility: Requires an installed macpymessenger CLI on macOS.
---

# macpymessenger

This file is a discovery stub. Load the workflow content from the installed CLI before using macpymessenger:

```bash
macpymessenger skills get core
```

Inside a uv project where macpymessenger is a project dependency, use:

```bash
uv run macpymessenger skills get core
```

The CLI serves instructions bundled with the installed package, so the workflow and command contract stay on the same version.
