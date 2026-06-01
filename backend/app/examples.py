from __future__ import annotations

from app.models import IntakeRequest, WorkedExample


def worked_example(req: IntakeRequest, class_id: str) -> WorkedExample:
    n = req.variable_count
    if class_id == "tsp":
        return WorkedExample(
            title="Routing as QUBO (sketch)",
            formulation_kind="QUBO",
            body=f"""# Variables: x_{{i,j}} ∈ {{0,1}} — edge (i,j) selected (~{n} nodes → O(n²) binaries)

# Objective: minimize tour length
minimize  Σ_{{i,j}} w_{{ij}} x_{{ij}}

# Constraints (penalty or slack):
# - each city entered once, left once
# - subtour elimination (Miller-Tucker-Zemlin or repeated penalties)

# Ocean path:
from dwave.optimization import Model
# ... build model, send to Leap hybrid or QPU sampler
""",
        )
    if class_id == "scheduling":
        return WorkedExample(
            title="Shift assignment BQM (sketch)",
            formulation_kind="BQM",
            body=f"""# x_{{worker, shift}} ∈ {{0,1}} for ~{n} assignment slots

# Minimize: understaffing penalties + preference violations
# Subject to: one shift per worker per day (hard → large penalty)

# Hybrid tip: fix obvious assignments classically, BQM only the bottleneck day/shift block.
""",
        )
    if class_id == "portfolio":
        return WorkedExample(
            title="Cardinality-constrained portfolio (sketch)",
            formulation_kind="QUBO",
            body=f"""# x_i ∈ {{0,1}} — asset i selected (universe size ~{n})

# minimize  x^T Q x   where Q encodes risk + return tradeoff
# penalty: (Σ x_i - K)² for exactly K assets

# Compare Leap hybrid samples vs. classical MIQP on same Q.
""",
        )
    if class_id == "feature_selection":
        return WorkedExample(
            title="Feature subset QUBO (sketch)",
            formulation_kind="QUBO",
            body=f"""# x_j ∈ {{0,1}} — feature j active ({n} features)

# minimize  relevance_loss(x) + λ · |x|_0
# encode |x|_0 via Σ x_j or penalty (Σ x_j - k)²

# Good first quantum POC: small n (<500), sparse correlation structure.
""",
        )
    return WorkedExample(
        title="Generic BQM template",
        formulation_kind="BQM",
        body=f"""# Decision vector x ∈ {{0,1}}^{n}  (your intake: ~{n} vars)

from dimod import BinaryQuadraticModel

bqm = BinaryQuadraticModel("BINARY")
# bqm.add_variable(v, bias)
# bqm.add_interaction(u, v, bias)

# sampler = LeapHybridSampler()  # or EmbeddingComposite + QPU
# sampleset = sampler.sample(bqm, num_reads=100)
""",
    )
