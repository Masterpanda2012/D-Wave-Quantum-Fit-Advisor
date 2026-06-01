from __future__ import annotations

import json
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.classifier import classify
from app.examples import worked_example
from app.models import AnalyzeResponse, IntakeRequest
from app.resources import links_for_class
from app.scorer import recommend, score_axes

app = FastAPI(title="Quantum Fit Advisor", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

_TAXONOMY_PATH = Path(__file__).resolve().parent.parent / "data" / "problem_taxonomy.json"


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/taxonomy")
def taxonomy() -> dict:
    with _TAXONOMY_PATH.open(encoding="utf-8") as f:
        return json.load(f)


@app.post("/api/analyze", response_model=AnalyzeResponse)
def analyze(body: IntakeRequest) -> AnalyzeResponse:
    class_id, label, conf = classify(body)
    axes = score_axes(body, class_id)
    rec, headline, paragraphs, conservative, lead = recommend(body, class_id, axes)

    next_steps = [
        "Document classical baseline runtime and solution quality.",
        "Draft BQM/QUBO formulation for the combinatorial core only.",
        "Prototype on Leap with small instance before production scale.",
    ]
    if rec.value in ("quantum", "hybrid", "explore_hybrid"):
        next_steps.append("Book a D-Wave technical review with BQM stats (vars, density, max degree).")

    return AnalyzeResponse(
        problem_class_id=class_id,
        problem_class_label=label,
        classifier_confidence=conf,
        recommendation=rec,
        recommendation_headline=headline,
        rationale_paragraphs=paragraphs,
        axis_scores=axes,
        conservative_note=conservative,
        next_steps=next_steps,
        worked_example=worked_example(body, class_id),
        resources=links_for_class(class_id),
        lead_qualification=lead,
    )
