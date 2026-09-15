# Changelog

All notable changes to this project are documented in this file.

## Unreleased

- Set up the `grill-me` → `to-prd` → `to-issues` skill chain under `.claude/skills/`.
- Added `CLAUDE.md` with project context and workflow rules.
- Added `docs/prd/repo-visualizer.md` and its issue breakdown under `docs/issues/repo-visualizer/`.
- Implemented ticket 01: core pipeline. FastAPI backend (`backend/`) that clones a public
  GitHub repo, runs `scc` for a language/file breakdown, and exposes it via `POST /analyze`.
  Static frontend (`frontend/index.html`) submits a repo URL and renders the breakdown as a
  Mermaid pie chart plus a table. Verified end-to-end against `psf/requests`.
- Implemented ticket 02: Python class diagram. Added a `LanguageExtractor` interface
  (`backend/app/extractors/`) with a `pyreverse`-based Python implementation that emits a
  Mermaid `classDiagram` directly (classes, attributes, methods, inheritance/composition).
  `/analyze` now includes `class_diagram` for Python repos and a `class_diagram_supported`
  flag otherwise; frontend renders the diagram or a "not supported" message. Verified against
  `psf/requests` (correct classes/relationships) and `mermaid-js/mermaid` (correctly falls
  back to unsupported for TypeScript).
- Implemented ticket 03: error handling. Backend now pre-checks repo existence via the GitHub
  API before cloning, returning a distinct 404 (`RepoNotFoundError`) for nonexistent/private
  repos, 400 for malformed URLs, and 500 for internal failures, each with a clear message.
  Disabled git credential prompts/helpers during clone so failures don't leak confusing
  auth-related git output. Frontend already surfaces `detail` from any non-2xx response.
  Unsupported-language handling was already covered by ticket 02. Verified all paths
  (malformed URL → 400, nonexistent repo → 404, TypeScript repo → unsupported flag,
  Python repo → 200 with diagram).
