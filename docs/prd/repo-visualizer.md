## Problem Statement

Developers want a quick, visual understanding of an unfamiliar public GitHub repository's
structure — what classes/modules exist and how they relate — without reading through every
file. GitHub itself only shows a coarse language bar and a flat file tree; it doesn't show
code-level structure like classes, methods, and relationships.

## Solution

A locally-run tool with a Python backend and a browser frontend. The user pastes a public
GitHub repo URL. The backend fetches the repo, and for Python codebases, generates a
UML-style class diagram (classes, methods, attributes, relationships) using `pyreverse`. For
any repo regardless of language, it also produces a language/file breakdown as a fallback
overview. The frontend renders both as interactive diagrams.

The analysis layer is designed so that Python (via `pyreverse`) is the first of potentially
several pluggable per-language extractors, without needing to change the API contract or
frontend rendering.

## User Stories

1. As a developer, I want to paste a public GitHub repo URL, so that I can visualize its structure without cloning and reading it manually.
2. As a developer, I want to see a class diagram of a Python repo's classes, methods, attributes, and relationships, so that I understand its object-oriented structure at a glance.
3. As a developer, I want to see a language/file breakdown of any repo, so that I get a useful overview even when the repo isn't in a supported language for deep analysis.
4. As a developer, I want a clear message when a repo's primary language isn't supported for deep analysis yet, so that I know why I'm only seeing the fallback overview.
5. As a developer, I want the diagram to be pannable/zoomable, so that I can explore larger diagrams without them becoming unreadable.
6. As a developer, I want to see file and class names in the diagram, so that I can map the visualization back to the actual source.
7. As a developer, I want the tool to run entirely on my local machine, so that I don't need to deploy anything or grant access to a hosted service.
8. As a developer, I want the backend and frontend to be separate services communicating over an API, so that either can be modified or replaced independently.
9. As a maintainer of this tool, I want the language-analysis step to be a pluggable interface, so that adding support for a new language (e.g. Java, Kotlin) doesn't require reworking the backend or frontend.
10. As a developer, I want a reasonable error message if the repo URL is invalid, private, or doesn't exist, so that I understand what went wrong.
11. As a developer, I want to see the language/file breakdown as a chart (e.g. pie chart), so that I can quickly gauge the repo's composition.

## Implementation Decisions

- **Backend**: Python + FastAPI. Exposes an API (e.g. `POST /analyze` with a repo URL) that returns structured JSON describing the diagram(s) to render.
- **Repo fetching**: Uses the GitHub API (public, unauthenticated where possible) to fetch repo contents. Falls back to a shallow `git clone` into a temp directory if needed for running `pyreverse` (which needs local source files, not just API metadata).
- **Language/file breakdown**: Shells out to `scc` on the fetched repo to get per-language line/file counts as JSON, transformed into a chart-ready structure.
- **Python class diagram**: Shells out to `pyreverse` on the fetched Python source, producing `.dot` output, which the backend parses/transforms into either Mermaid class-diagram syntax or a JSON graph structure (nodes = classes, edges = relationships) for the frontend to render.
- **Language-extractor interface**: A common internal interface (e.g. `LanguageExtractor.extract(repo_path) -> DiagramGraph`) that the Python/`pyreverse` extractor implements. The API layer picks an extractor based on detected primary language (from the `scc` breakdown) and returns a "not supported" state if no extractor matches, rather than hardcoding Python-specific logic into the API/response layer.
- **Frontend**: Static HTML/JS (no build step), using Mermaid.js (or `d3-graphviz` if Mermaid's class-diagram syntax proves too limiting for relationships) to render the class diagram, and a simple chart library or Mermaid pie chart for the language breakdown. Fetches from the FastAPI backend over `localhost`.
- **Local-only**: No deployment/hosting concerns. Backend runs via `uvicorn` locally; frontend is served as static files (e.g. via FastAPI's static file serving or a simple dev server).
- **Temp repo storage**: Cloned/fetched repos are stored in a temp directory and cleaned up after analysis (or reused if the same URL is re-analyzed within a session — implementation detail, not user-facing).

## Testing Decisions

- Good tests here verify observable behavior: given a repo path with known Python classes, the extractor produces the expected graph structure (nodes/edges) — not that it calls `pyreverse` with specific flags.
- **Modules to test**:
  - The Python `LanguageExtractor` implementation (`pyreverse` output → graph structure), using a small fixture Python package with known classes/relationships checked into the test suite (avoids network calls to a real repo in tests).
  - The `scc` output → language-breakdown transformation, using fixture JSON output from `scc`.
  - The extractor-selection logic (given a language breakdown, pick the right extractor or return "unsupported").
- API-level tests (FastAPI `TestClient`) for the `/analyze` endpoint covering: valid Python repo, unsupported-language repo, invalid/nonexistent repo URL.
- No prior art for tests in this repo yet — this is the first feature built here.

## Out of Scope

- Support for languages other than Python for deep class-diagram analysis (Java, Kotlin, JavaScript, etc.) — the extractor interface is designed to allow this later, but no additional extractors are built in this PRD.
- Private repo support / GitHub authentication.
- Hosting/deployment — local-only for now.
- Diagram editing or exporting (e.g. to image/PDF) beyond on-screen viewing.
- Caching/persistence of analyzed repos across restarts.
- Function-level call graphs (as opposed to class/module-level structure).

## Further Notes

- Demo/test target repo for development: [`psf/requests`](https://github.com/psf/requests) — moderate size, clear OOP structure (`Session`, `Request`, `PreparedRequest`, `Response`), well-known.
- `pyreverse` ships with `pylint`, so `pylint` becomes a backend dependency.
- `scc` (https://github.com/boyter/scc) is a standalone Go binary; the backend needs it available on `PATH` (documented as a prerequisite, not vendored).
