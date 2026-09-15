from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(req: AnalyzeRequest) -> AnalyzeResponse:
    try:
        with clone_repo(req.repo_url) as repo_path:
            breakdown = get_language_breakdown(repo_path)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return AnalyzeResponse(repo_url=req.repo_url, language_breakdown=breakdown)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
