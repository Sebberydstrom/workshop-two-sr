## das systeme

## Quickstart

1. Open this repo in Claude Code (or VS Code with the Claude extension).
2. Describe what you want to build and run `/grill-me` to work through the plan.
3. In the same session, run `/to-prd` to generate a PRD under `docs/prd/`.
4. In the same session, run `/to-issues` to break the PRD into tickets under `docs/issues/`.
5. For each ticket, start a new session, implement the ticket, review the diff, then commit and push.
6. Keep `CHANGELOG.md` up to date as tickets are completed (see `CLAUDE.md` for the workflow rules).

## Running the Repo Visualizer app

Prerequisites (one-time):

- Python 3.10+ and `git` on `PATH`.
- [`scc`](https://github.com/boyter/scc) on `PATH` (used for the language breakdown). No package
  manager install needed — download a release binary, e.g.:
  ```
  curl -sL -o scc.tar.gz https://github.com/boyter/scc/releases/latest/download/scc_Linux_x86_64.tar.gz
  tar xzf scc.tar.gz && mkdir -p ~/.local/bin && mv scc ~/.local/bin/
  ```
  (use the `_Darwin_` or `_Windows_` asset instead on macOS/Windows).
- `pyreverse` (installed automatically via `backend/requirements.txt`, it ships with `pylint`).

Install backend dependencies (once, or after `requirements.txt` changes):

```
cd backend
pip install -r requirements.txt
```

Start the backend (from `backend/`):

```
python3 -m uvicorn app.main:app --reload --port 8000
```

Start the frontend (from `frontend/`, in a second terminal):

```
python3 -m http.server 5173
```

Then open `http://localhost:5173` in a browser.

### Testing it

- **Happy path**: paste `https://github.com/psf/requests` and click Analyze. Expect a language
  pie chart (mostly Python) and a class diagram showing `Session`, `Response`,
  `PreparedRequest`, `HTTPAdapter`, etc. with their relationships.
- **Unsupported language**: paste `https://github.com/mermaid-js/mermaid` (TypeScript). Expect
  the language breakdown to render, but the class-diagram panel to show a
  "not supported for this language yet" message instead of erroring.
- **Malformed URL**: paste `not-a-url`. Expect a clear inline error, no blank/broken page.
- **Nonexistent/private repo**: paste a URL to a repo that doesn't exist, e.g.
  `https://github.com/<your-username>/definitely-not-a-real-repo`. Expect a clear
  "not found" error, not a raw stack trace.
- You can also hit the backend directly, e.g.:
  ```
  curl -X POST http://localhost:8000/analyze \
    -H "Content-Type: application/json" \
    -d '{"repo_url": "https://github.com/psf/requests"}'
  ```
  and check `http://localhost:8000/health` returns `{"status": "ok"}`.
