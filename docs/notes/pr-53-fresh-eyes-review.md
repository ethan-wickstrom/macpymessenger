# PR 53 fresh-eyes review

This file records the audit scope, testable hypotheses, evidence, and final
outcomes for the post-implementation review of PR #53. It is a review record,
not public API documentation.

## Scope

- Compare the pull-request head with merge base
  `327762d2d053df48734af4dd4d271fdac967570a`.
- Trace public calls through configuration, templates, delivery, subprocess
  execution, logging, diagnostics, packaging, documentation, and release gates.
- Prefer deletion and smaller data shapes over adding coordination or options.
- Verify both the source tree and the installed wheel.

## Initial facts

- The pull request changes more than 50 files and introduces or changes public
  API, diagnostics, packaging, CI, Sphinx output, PyPI metadata, and agent
  guidance.
- The final pre-review CI run passed 58 tests and all source, docs, build, and
  installed-wheel checks on Linux and macOS.
- Passing tests prove the asserted behavior, not that every new assumption is
  sound or every supported integration is represented.

## Hypothesis tree

| ID | Hypothesis | Confidence | Evidence | Status |
| --- | --- | ---: | --- | --- |
| H1 | The package claims inline typing without shipping the PEP 561 marker required by installed type checkers. | 0.99 | The typing specification requires `py.typed`; the package tree and wheel smoke test omit it. | Test pending |
| H2 | The doctor reports “ready” even though account sign-in and Automation permission remain unknown. | 0.99 | `ready` ignores `INFO`; the CLI prints “Ready for a first send”; Apple makes Automation a user-controlled per-app permission. | Test pending |
| H3 | A relative custom AppleScript path can pass validation and later fail after the process changes directory. | 0.99 | `Configuration` stores the relative path and `MessageDelivery` resolves it only when spawning. | Test pending |
| H4 | `context or {}` can discard a valid custom mapping whose truth value is false. | 0.99 | `render_template` branches on truthiness instead of presence. | Test pending |
| H5 | Some docs or agent guidance still conflict with current behavior. | 0.90 | The client API example uses undefined names; the changelog links delivery work to issue #36 instead of #37; more surfaces remain under review. | Confirmed, audit continuing |
| H6 | Raw command failures can expose private message text through child output, logging, and traceback chaining. | 0.99 | `osascript` inherits stdout/stderr; the script returns `Success`; `logger.exception` and `raise ... from error` retain `CalledProcessError.cmd`, which contains the message argv. | Test pending |
| H7 | The known system executable should not be resolved through caller-controlled `PATH`. | 0.98 | Apple documents `osascript` at `/usr/bin/osascript`; both execution and diagnostics currently depend on `PATH`. | Test pending |
| H8 | The release workflow keeps a long-lived token and runs build code in the same credential-bearing job. | 0.95 | PyPI recommends Trusted Publishing and a separate, least-privileged publish job that only retrieves and uploads artifacts. | Confirmed |
| H9 | String-only interpolation is an unnecessary restriction that blocks normal numeric formatting and duplicates work already done by Python's format protocol. | 0.90 | Python's t-string reference processor applies conversion and `format()` to arbitrary interpolation values; macpymessenger rejects them before either step. | Design challenge pending |
| H10 | Doctor output can reveal a private home path. | 0.99 | Success and failure summaries include the absolute installed send-script path despite the repository redaction rule. | Test pending |
| H11 | Current CI never compiles the bundled AppleScript against the current macOS Messages dictionary. | 0.85 | The macOS job uses macOS 26 but all tests inject runners; `osacompile` can check the script without executing it. | Gate pending |
| H12 | Some public fields are more weakly typed than their closed domain. | 0.65 | `MessageSendError.reason` is annotated as unrestricted `str` although only `delivery` and `command` are valid. | Review pending |

## Review log

- The audit started from the merge-base diff rather than the final commit alone.
- Repository shell access could not resolve GitHub, so code is being read from
  exact branch Git objects and behavior is being verified through GitHub Actions
  and focused reproductions.
- Primary sources reviewed so far: the Python typing specification, Python 3.14
  `string.templatelib` and `pathlib` documentation, Apple Automation and
  AppleScript documentation, uv build-backend documentation, and PyPI Trusted
  Publishing guidance.
