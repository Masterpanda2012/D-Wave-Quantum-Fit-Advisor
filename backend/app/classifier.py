from __future__ import annotations

import json
from pathlib import Path

from app.models import IntakeRequest, ProblemType

_TAXONOMY_PATH = Path(__file__).resolve().parent.parent / "data" / "problem_taxonomy.json"

_TYPE_TO_CLASS: dict[ProblemType, tuple[str, str, float]] = {
    ProblemType.routing: ("tsp", "Traveling salesperson / routing", 0.92),
    ProblemType.scheduling: ("scheduling", "Job / shift scheduling", 0.9),
    ProblemType.portfolio: ("portfolio", "Portfolio / asset selection", 0.88),
    ProblemType.feature_selection: (
        "feature_selection",
        "Feature / subset selection (ML prep)",
        0.86,
    ),
    ProblemType.simulation: ("simulation", "Physics / chemistry simulation", 0.85),
    ProblemType.ml_training: ("ml_training", "Large-scale ML training", 0.9),
    ProblemType.general: ("general_optimization", "General constrained optimization", 0.65),
}

_KEYWORD_BOOSTS: list[tuple[str, str, str, float]] = [
    ("tsp", "routing", "Traveling salesperson / routing", 0.15),
    ("scheduling", "schedule", "Job / shift scheduling", 0.12),
    ("portfolio", "portfolio", "Portfolio / asset selection", 0.12),
    ("feature_selection", "feature", "Feature / subset selection (ML prep)", 0.1),
]


def _load_taxonomy() -> dict:
    with _TAXONOMY_PATH.open(encoding="utf-8") as f:
        return json.load(f)


def classify(req: IntakeRequest) -> tuple[str, str, float]:
    """Return (class_id, label, confidence)."""
    class_id, label, conf = _TYPE_TO_CLASS[req.problem_type]
    text = f"{req.problem_description} {req.current_approach}".lower()

    for cid, keyword, blabel, boost in _KEYWORD_BOOSTS:
        if keyword in text and cid != class_id:
            class_id, label = cid, blabel
            conf = min(0.95, conf + boost)
            break
        if keyword in text:
            conf = min(0.98, conf + boost * 0.5)

    if req.has_qubo_structure is True and class_id == "general_optimization":
        conf = min(0.9, conf + 0.1)

    if "qubo" in text or "ising" in text or "binary quadratic" in text:
        if class_id == "general_optimization":
            class_id, label = "feature_selection", "QUBO-structured combinatorial problem"
        conf = min(0.97, conf + 0.08)

    return class_id, label, round(conf, 2)
