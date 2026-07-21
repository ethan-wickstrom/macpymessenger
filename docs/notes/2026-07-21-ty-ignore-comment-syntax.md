# ty needs `# ty: ignore[rule]`, not `# type: ignore[rule]`

`ty` does not honor rule-coded `# type: ignore[...]` comments carrying its
own rule names (for example `invalid-argument-type`); use
`# ty: ignore[rule]` for targeted suppressions in tests that deliberately
pass ill-typed values across the public boundary. This repo enables
`unused-ignore-comment = "error"`, so stale suppressions fail the check.
