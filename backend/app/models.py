from __future__ import annotations

from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


class ProblemType(str, Enum):
    routing = "routing"
    scheduling = "scheduling"
    portfolio = "portfolio"
    feature_selection = "feature_selection"
    simulation = "simulation"
    ml_training = "ml_training"
    general = "general"


class IndustryVertical(str, Enum):
    logistics = "logistics"
    finance = "finance"
    manufacturing = "manufacturing"
    life_sciences = "life_sciences"
    energy = "energy"
    other = "other"


class TimeBudget(str, Enum):
    seconds = "seconds"
    minutes = "minutes"
    hours = "hours"
    days = "days"


class IntakeRequest(BaseModel):
    industry: IndustryVertical = IndustryVertical.other
    problem_type: ProblemType = ProblemType.general
    problem_description: str = Field(default="", max_length=4000)
    variable_count: int = Field(ge=1, le=10_000_000, default=100)
    constraint_density: Literal["sparse", "medium", "dense"] = "medium"
    needs_exact_solution: bool = False
    has_qubo_structure: bool | None = None
    current_approach: str = Field(default="", max_length=2000)
    time_budget: TimeBudget = TimeBudget.minutes
    nisq_tolerance: bool = True


class AxisScore(BaseModel):
    axis: str
    score: float = Field(ge=0, le=1)
    label: str
    rationale: str


class Recommendation(str, Enum):
    classical = "classical"
    hybrid = "hybrid"
    quantum = "quantum"
    explore_hybrid = "explore_hybrid"


class WorkedExample(BaseModel):
    title: str
    formulation_kind: str
    body: str


class ResourceLink(BaseModel):
    title: str
    url: str
    kind: str


class AnalyzeResponse(BaseModel):
    problem_class_id: str
    problem_class_label: str
    classifier_confidence: float
    recommendation: Recommendation
    recommendation_headline: str
    rationale_paragraphs: list[str]
    axis_scores: list[AxisScore]
    conservative_note: str
    next_steps: list[str]
    worked_example: WorkedExample
    resources: list[ResourceLink]
    lead_qualification: Literal["low", "medium", "high"]
