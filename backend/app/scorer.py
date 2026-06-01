from __future__ import annotations

from typing import Literal

from app.models import (
    AxisScore,
    IntakeRequest,
    ProblemType,
    Recommendation,
    TimeBudget,
)

LeadQualification = Literal["low", "medium", "high"]


def _axis(
    axis: str, score: float, label: str, rationale: str
) -> AxisScore:
    return AxisScore(
        axis=axis, score=round(max(0.0, min(1.0, score)), 2), label=label, rationale=rationale
    )


def score_axes(req: IntakeRequest, class_id: str) -> list[AxisScore]:
    n = req.variable_count
    size_score = 0.2
    if 200 <= n <= 50_000:
        size_score = 0.85
    elif 50 <= n < 200:
        size_score = 0.55
    elif n < 50:
        size_score = 0.15
    elif n > 50_000:
        size_score = 0.45

    structure_score = 0.4
    if req.has_qubo_structure is True or class_id in (
        "tsp",
        "scheduling",
        "portfolio",
        "feature_selection",
    ):
        structure_score = 0.88
    elif req.constraint_density == "sparse":
        structure_score = 0.72
    elif req.constraint_density == "dense":
        structure_score = 0.35

    nisq_score = 0.75 if req.nisq_tolerance else 0.35
    if class_id == "simulation":
        nisq_score = 0.25

    hardware_score = 0.7
    if class_id in ("ml_training", "simulation"):
        hardware_score = 0.2
    if req.time_budget == TimeBudget.seconds and n > 5000:
        hardware_score = 0.4

    exactness_penalty = 0.9 if req.needs_exact_solution else 0.55
    if req.needs_exact_solution and n > 500:
        exactness_penalty = 0.25

    classical_alternative = 0.85 if n < 80 else 0.5
    if req.problem_type == ProblemType.ml_training:
        classical_alternative = 0.95

    return [
        _axis(
            "problem_size",
            size_score,
            "Problem scale vs. quantum sweet spot",
            f"~{n:,} decision variables — annealing/hybrid often shines in hundreds to tens of thousands for structured QUBOs.",
        ),
        _axis(
            "structure",
            structure_score,
            "QUBO / combinatorial structure",
            "Sparse or explicit binary quadratic structure improves fit for D-Wave annealing and hybrid BQM solvers.",
        ),
        _axis(
            "nisq_readiness",
            nisq_score,
            "Tolerance for heuristic / sample-based answers",
            "Quantum annealing returns samples, not guaranteed global optima — best when good-enough solutions suffice.",
        ),
        _axis(
            "hardware_fit",
            hardware_score,
            "Annealing vs. gate-model fit",
            "Problem class maps to Ocean / Leap workflows vs. gate-model simulation stacks.",
        ),
        _axis(
            "exactness",
            exactness_penalty,
            "Need for provably optimal solutions",
            "Exact MIP/CP solvers on classical hardware remain default when optimality certificates are required.",
        ),
    ]


def recommend(
    req: IntakeRequest, class_id: str, axis_scores: list[AxisScore]
) -> tuple[Recommendation, str, list[str], str, LeadQualification]:
    avg = sum(a.score for a in axis_scores) / len(axis_scores)
    n = req.variable_count

    if class_id in ("ml_training",) or req.problem_type == ProblemType.ml_training:
        return (
            Recommendation.classical,
            "Stay classical — GPU/TPU training stacks are the right tool",
            [
                "Your intake maps to large-scale ML training, where quantum hardware does not replace gradient-based training today.",
                "Classical frameworks (PyTorch, JAX, etc.) plus classical hyperparameter search remain the practical path.",
                "Revisit quantum only for specific combinatorial sub-problems (e.g., feature subset selection) encoded as small QUBOs.",
            ],
            "Conservative default: quantum is not recommended for end-to-end model training.",
            "low",
        )

    if class_id == "simulation" or req.problem_type == ProblemType.simulation:
        return (
            Recommendation.explore_hybrid,
            "Explore gate-model / specialized stacks — not annealing-first",
            [
                "Chemistry and materials simulation often targets gate-model or dedicated classical HPC rather than QUBO annealing.",
                "Partner with a quantum architecture team if Hamiltonian simulation is core to the roadmap.",
                "Use this tool's combinatorial path when you can reformulate a sub-problem as QUBO.",
            ],
            "Simulation problems are routed away from 'use annealing now' recommendations.",
            "medium",
        )

    if n < 50 and not req.has_qubo_structure:
        return (
            Recommendation.classical,
            "Classical solvers will be faster and exact enough",
            [
                f"At ~{n} variables, modern MIP/CP/heuristic classical solvers typically finish in {req.time_budget.value}.",
                "Quantum setup, embedding, and queue latency rarely pay off at this scale.",
                "Document the problem as a benchmark — revisit if variable count grows 10× or structure becomes QUBO-native.",
            ],
            "Rule: under ~50 unstructured variables → classical unless you are explicitly learning Ocean.",
            "low",
        )

    structure = next(a for a in axis_scores if a.axis == "structure").score
    if req.needs_exact_solution and n > 200:
        return (
            Recommendation.hybrid,
            "Hybrid classical + quantum — classical certifies, quantum explores",
            [
                "You need high-quality solutions but also optimality pressure — start with classical MIP/CP baselines.",
                "Use Leap hybrid solvers to search large neighborhoods, then validate winners classically.",
                "Treat quantum output as candidate generation, not the sole source of truth.",
            ],
            "When exactness is required, we never recommend quantum-only.",
            "medium",
        )

    if avg >= 0.72 and structure >= 0.7 and n >= 100:
        return (
            Recommendation.quantum,
            "Strong quantum annealing / hybrid candidate",
            [
                "Encode the problem as a BQM/QUBO and prototype on Leap (hybrid or QPU).",
                "Benchmark against your current classical heuristic — compare time-to-good-solution, not just best value.",
                "Engage D-Wave support with your BQM size and industry vertical for solver selection.",
            ],
            "High scores on structure + scale — still validate samples classically before production.",
            "high",
        )

    if avg >= 0.55 or (structure >= 0.65 and n >= 80):
        return (
            Recommendation.hybrid,
            "Hybrid workflow recommended",
            [
                "Run a classical decomposition (fix obvious variables, preprocess constraints).",
                "Submit the core combinatorial core to a Leap hybrid solver.",
                "Compare sample distributions across runs — track reproducibility for stakeholders.",
            ],
            "Default for 'maybe quantum' cases: hybrid first, not QPU-only.",
            "medium",
        )

    return (
        Recommendation.classical,
        "Start classical — keep quantum as a structured experiment",
        [
            "Build a classical baseline with OR-Tools, Gurobi, or domain heuristics.",
            "If you can write a QUBO, prototype in Ocean with toy instances before scaling.",
            "Re-run this advisor when variable count or QUBO structure changes materially.",
        ],
        "Conservative bias: classical unless quantum advantage signals are clear.",
        "low",
    )
