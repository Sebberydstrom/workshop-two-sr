## Parent

`docs/prd/repo-visualizer.md`

## What to build

End-to-end path: the user enters a public GitHub repo URL in the frontend, the backend fetches
the repo, runs `scc` to produce a language/file breakdown, and the frontend renders that
breakdown as a chart. This establishes the FastAPI backend, the `/analyze` endpoint contract,
the repo-fetching mechanism (GitHub API + shallow clone to a temp directory), and the static
frontend shell that all later slices build on.

## Acceptance criteria

- [ ] Frontend has a form to submit a public GitHub repo URL, calling the backend `/analyze` endpoint
- [ ] Backend fetches the repo (via GitHub API and/or shallow `git clone` into a temp dir) given a URL
- [ ] Backend runs `scc` on the fetched repo and returns a language/file breakdown as JSON
- [ ] Frontend renders the language breakdown as a chart (e.g. Mermaid pie chart)
- [ ] Fetched repo is cleaned up from the temp directory after analysis
- [ ] Demoed successfully against `psf/requests`

## Blocked by

None - can start immediately
