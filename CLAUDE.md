# Project Context

This repository is the workspace for a prompt-engineering workshop. The workflow follows a
skill chain to go from an idea to shippable, reviewed code:

1. `/grill-me` — interview the user about what to build until there's a shared understanding of the plan.
2. `/to-prd` — synthesize the conversation into a PRD saved under `docs/prd/`.
3. `/to-issues` — break the PRD into independently-implementable, vertical-slice issues saved under `docs/issues/<feature-name>/`.
4. Each issue is then implemented in its own session, reviewed, and pushed to GitHub as a separate commit.

Skills used in this workflow live in `.claude/skills/` (`grill-me`, `to-prd`, `to-issues`).

## Workflow rules

- After completing and committing the work for a ticket (an issue file under `docs/issues/`), update `CHANGELOG.md` with an entry describing what was done, under an "Unreleased" section (or today's date if the user asks to cut a release).
- Do not modify a PRD or issue file when implementing it — treat those as the spec.
