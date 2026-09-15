## Parent

`docs/prd/repo-visualizer.md`

## What to build

Add real class/module-level UML-style diagram generation for Python repos. Introduce a
`LanguageExtractor` interface and a `pyreverse`-based implementation for Python that turns
source into a graph structure (classes, methods, attributes, relationships). Wire it into the
`/analyze` endpoint: when the repo's primary language is Python, the response includes this
diagram data in addition to the language breakdown from slice 1. The frontend renders the class
diagram (Mermaid class-diagram syntax, or `d3-graphviz` if relationships don't map cleanly to
Mermaid) alongside the existing language-breakdown chart.

## Acceptance criteria

- [ ] `LanguageExtractor` interface defined, with a Python/`pyreverse` implementation
- [ ] Backend selects the Python extractor when the repo's primary language (from the slice 1 breakdown) is Python
- [ ] Extractor output includes classes, methods, attributes, and relationships (inheritance/associations)
- [ ] `/analyze` response includes the class-diagram graph data for Python repos
- [ ] Frontend renders the class diagram as an interactive diagram
- [ ] Demoed successfully against `psf/requests`, showing `Session`, `Request`, `PreparedRequest`, `Response` and their relationships

## Blocked by

- `docs/issues/repo-visualizer/01-core-pipeline-language-breakdown.md`
