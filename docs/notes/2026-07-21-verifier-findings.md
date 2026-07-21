# Independent verification caught a vacuous divergence pin and a doc/code mismatch

A fresh-context verifier (seeing only paradigm, foundation, parity suite,
and code) found: (1) the logger-level divergence test pinned
`macpymessenger.delivery`, a logger the incumbent never mutated, so it
would have passed on the old code too — the real divergence is on
`macpymessenger.client`; (2) the foundation's logging rule said "each
module logs to `logging.getLogger(__name__)`" while delivery actually
emits through the injected client logger; (3) `TemplateTypeError.unexpected_element`
guarded an unreachable branch (`Template` is not subclassable); (4) the
runner's `text=True` was a no-op. All four were fixed. Lesson: divergence
tests must be shown to FAIL against the incumbent before they count as
pins, and construction-context confidence about "what the old code did"
loses to a verifier reading the old code fresh.
