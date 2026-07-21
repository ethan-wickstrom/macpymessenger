# Lint the parity suite before committing it

The parity baseline was committed before running `ruff`/`ty` on it, so five
style findings (import placement, unescaped regex `match=` patterns, an
unused stub argument) had to be fixed after the freeze. The fixes changed
no assertion or captured behavior — only comment/format-level structure —
and the suite was re-run against both the incumbent capture semantics and
the rebuilt code. Lesson: run the full lint/type gate on characterization
tests before declaring them frozen, so the frozen artifact never needs
touching at all.
