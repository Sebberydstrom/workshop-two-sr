## Parent

`docs/prd/repo-visualizer.md`

## What to build

Handle the non-happy paths end-to-end: invalid/malformed URLs, nonexistent or private repos,
and repos whose primary language has no extractor (i.e. anything other than Python for now).
The backend returns clear, distinguishable error/status responses for each case, and the
frontend surfaces a clear message to the user instead of a broken or blank state. This also
exercises the "extractor not found" path of the `LanguageExtractor` selection logic introduced
in slice 2, confirming it degrades to the language-breakdown-only view rather than failing.

## Acceptance criteria

- [ ] Invalid/malformed repo URL submission shows a clear frontend error, without a backend crash
- [ ] Nonexistent or private repo submission shows a clear "not found / not accessible" frontend message
- [ ] A repo whose primary language isn't Python still shows the language breakdown, with a clear "deep analysis not supported for this language yet" message instead of a class diagram
- [ ] Backend returns distinguishable error responses (status codes/error bodies) for each of the above cases

## Blocked by

- `docs/issues/repo-visualizer/01-core-pipeline-language-breakdown.md`
