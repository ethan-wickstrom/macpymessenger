# Issue tracker: GitHub

Issues and PRDs for this repo live in GitHub Issues for `ethan-wickstrom/macpymessenger`. Use the `gh` CLI for issue operations.

## Conventions

- Create an issue: `gh issue create --repo ethan-wickstrom/macpymessenger --title "..." --body "..."`
- Read an issue: `gh issue view <number> --repo ethan-wickstrom/macpymessenger --comments`
- List issues: `gh issue list --repo ethan-wickstrom/macpymessenger --state open --json number,title,body,labels,comments`
- Comment on an issue: `gh issue comment <number> --repo ethan-wickstrom/macpymessenger --body "..."`
- Apply or remove labels: `gh issue edit <number> --repo ethan-wickstrom/macpymessenger --add-label "..."` / `--remove-label "..."`
- Close an issue: `gh issue close <number> --repo ethan-wickstrom/macpymessenger --comment "..."`

Pass `--repo ethan-wickstrom/macpymessenger` so commands work even outside a checkout
with a configured GitHub remote.

## When a skill says "publish to the issue tracker"

Create a GitHub issue in `ethan-wickstrom/macpymessenger`.

## When a skill says "fetch the relevant ticket"

Run `gh issue view <number> --repo ethan-wickstrom/macpymessenger --comments`.
