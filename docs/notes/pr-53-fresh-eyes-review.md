# PR 53 fresh-eyes review

This file records the audit scope, testable hypotheses, evidence, and final
outcomes for the post-implementation review of PR #53. It is a review record,
not public API documentation.

## Scope

- Compare the pull-request head with merge base
  `327762d2d053df48734af4dd4d271fdac967570a`.
- Trace public calls through templates, delivery, subprocess execution, logging,
  diagnostics, packaging, documentation, and release gates.
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
| H1 | The package claims inline typing without shipping the PEP 561 marker required by installed type checkers. | 0.00 | `src/macpymessenger/py.typed` exists and the installed-package test passes. | Disproved |
| H2 | The doctor reports “ready” even though account sign-in and Automation permission remain unknown. | 0.99 | `ready` ignores `INFO`; the CLI prints “Ready for a first send”; Apple makes Automation a user-controlled per-app permission. | Reproduced |
| H3 | A relative custom AppleScript path can pass validation and later fail after the process changes directory. | 0.99 | The focused test reproduced the relative path after construction. | Reproduced; abstraction selected for deletion |
| H4 | `context or {}` can discard a valid custom mapping whose truth value is false. | 0.99 | A false-valued non-empty mapping reaches the factory as an empty dictionary. | Reproduced |
| H5 | Some docs or agent guidance still conflict with current behavior. | 0.95 | The client API example uses undefined names; the changelog links delivery work to issue #36 instead of #37; uv installation examples invoke project scripts without `uv run`. | Confirmed, audit continuing |
| H6 | Raw command failures can expose private message text through child output, logging, and traceback chaining. | 0.99 | The focused failure test captures the full argv, including message body, in both the logged traceback and chained exception. | Reproduced |
| H7 | The known system executable should not be resolved through caller-controlled `PATH`. | 0.99 | Apple documents `/usr/bin/osascript`; the focused test found the bare command name. | Reproduced |
| H8 | The release workflow keeps a long-lived token and runs build code in the same credential-bearing job. | 0.95 | PyPI recommends Trusted Publishing and a separate, least-privileged publish job that only retrieves and uploads artifacts. | Confirmed |
| H9 | String-only interpolation is an unnecessary restriction that blocks normal numeric formatting and duplicates work already done by Python's format protocol. | 0.99 | Focused integer, conversion, and numeric-format tests all fail before Python's normal format protocol runs. | Reproduced |
| H10 | Doctor output can reveal a private home path. | 0.99 | The focused test found the full installed script path in the successful check summary. | Reproduced |
| H11 | Current CI never compiles the bundled AppleScript against the current macOS Messages dictionary. | 0.90 | All delivery tests inject a runner; a new macOS-only compiler test now defines the required gate. | Test added |
| H12 | Some public fields are more weakly typed than their closed domain. | 0.90 | `MessageSendError.reason` is unrestricted `str` although only two values are produced. | Confirmed |
| H13 | The documented uv quick start cannot invoke the installed console script as written without activating the environment. | 0.99 | uv documents `uv run <command>` as the project-script invocation path; README and Sphinx use a bare command after `uv add`. | Confirmed |
| H14 | Recipient and message text in process argv remain visible to process inspection for the full delay interval. | 0.99 | `MessageDelivery` constructs argv as executable, script, recipient, message, delay. | Confirmed; root abstraction selected for deletion |

## Competing designs

1. Patch the existing command runner with output capture, absolute paths, and
   exception suppression. This fixes terminal and traceback leaks but leaves
   private recipient and message values in process argv.
2. Move payloads into temporary files. This removes argv exposure but adds file
   lifecycle, permissions, cleanup, crash recovery, and race concerns.
3. Replace the generic command runner and script-path configuration with one
   domain transport. The transport accepts an immutable `SendRequest`, encodes
   private values into AppleScript source carried through stdin, and invokes
   fixed argv `('/usr/bin/osascript', '-')`.

Design 3 wins. It removes two shallow public abstractions, preserves option value
through a custom `MessageTransport`, keeps private data out of argv and the
filesystem, and gives tests one stable request shape.

## Review log

- The audit started from the merge-base diff rather than the final commit alone.
- Repository shell access could not resolve GitHub, so code is being read from
  exact branch Git objects and behavior is being verified through GitHub Actions
  and focused reproductions.
- Primary sources reviewed so far: the Python typing specification, Python 3.14
  `string.templatelib` and `pathlib` documentation, Apple Automation and
  AppleScript documentation, the `osascript` manual, uv documentation, Ruff
  formatter documentation, and PyPI Trusted Publishing guidance.
- The confirmed RED run reached all 62 tests after lint, formatting, and type
  checks passed: 14 tests failed for the intended missing behaviors and 48
  existing tests passed.
