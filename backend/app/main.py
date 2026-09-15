from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.extractors.registry import get_extractor
from app.language_breakdown import get_language_breakdown
from app.repo_fetch import clone_repo

app = FastAPI(title="Repo Visualizer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnalyzeRequest(BaseModel):
    repo_url: str


class AnalyzeResponse(BaseModel):
    repo_url: str
    language_breakdown: list[dict]
    primary_language: str | None
    class_diagram: str | None
    class_diagram_supported: bool
    class_diagram_error: str | None = None


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(req: AnalyzeRequest) -> AnalyzeResponse:
    try:
        with clone_repo(req.repo_url) as repo_path:
            breakdown = get_language_breakdown(repo_path)
            primary_language = breakdown[0]["language"] if breakdown else None

            class_diagram = None
            class_diagram_error = None
            extractor = get_extractor(primary_language) if primary_language else None

            if extractor is not None:
                try:
                    class_diagram = extractor.extract(repo_path)
                except (ValueError, RuntimeError) as exc:
                    class_diagram_error = str(exc)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return AnalyzeResponse(
        repo_url=req.repo_url,
        language_breakdown=breakdown,
        primary_language=primary_language,
        class_diagram=class_diagram,
        class_diagram_supported=extractor is not None,
        class_diagram_error=class_diagram_error,
    )


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
