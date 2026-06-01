# Quantum Fit Advisor

**Quantum Fit Advisor** (working name) is an open-source prototype for the D-Wave **“Should I Use Quantum?”** idea from the internship design brief. It is a **FastAPI** backend plus a **React** wizard that helps engineers who are not quantum specialists answer one question: *for this optimization problem, should I start with classical solvers, a hybrid Leap workflow, or a structured quantum POC?*

The README is the full product explanation (outreach emails stay short and link here).

## The gap it tries to fill

Public quantum content often explains *how* to run a sampler. The blocker for adoption is usually *whether* quantum is the right tool for **this** problem at **this** scale. Teams still spend time on problems that were always classical wins, or jump to quantum without a QUBO formulation or baseline.

This prototype is a **self-serve first pass**: qualify the problem in domain terms, surface tradeoffs on five inspectable axes, and point to a concrete next step—classical baseline, hybrid Leap workflow, or a small quantum experiment—**without** replacing D-Wave solutions architects or Ocean documentation.

## What you get

After a short wizard, the app returns a single results view with:

| Capability | Description |
|------------|-------------|
| **Four-step intake wizard** | Problem type → scale & time budget → constraints & structure → review, then analyze. |
| **Problem classification** | Maps input to classes aligned with common Ocean examples: routing (TSP/VRP), scheduling, portfolio, feature selection, simulation, ML training, general optimization. Optional free-text boosts confidence via keywords (e.g. QUBO, Ising). |
| **5-axis fit model** | Transparent scores (0–100%) with rationale: problem size, QUBO/combinatorial structure, tolerance for sample-based answers, annealing vs gate-model fit, need for provably optimal solutions. |
| **Conservative recommendation** | **Classical**, **hybrid**, **quantum**, or **explore hybrid** (e.g. simulation-heavy problems), with plain-English paragraphs explaining why. |
| **Rules-first engine** | Deterministic logic first: e.g. under ~50 unstructured variables → classical; exact optimality required at scale → hybrid, not quantum-only; ML training at scale → classical. |
| **Worked QUBO/BQM sketches** | Problem-class-specific pseudocode so the output is actionable for someone opening Ocean. |
| **D-Wave resource links** | Curated docs/examples (TSP, portfolio, BQM overview, Leap hybrid, Ocean install) matched to the detected class. |
| **Priority tier** | `low` / `medium` / `high` signal for funnel-style experiments (which intakes might warrant a solutions conversation). |

## How it works (flow)

```
Intake wizard → classify problem → score 5 axes → recommend (classical | hybrid | quantum)
              → rationale + next steps + QUBO sketch + doc links
```

## Run locally

You need **two terminals**: API on port **8001**, UI on port **5174** (Vite proxies `/api` to the backend).

### Prerequisites

- Python 3.10+
- Node.js 18+

### Terminal 1 — API

From the repository root:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8001
```

Health check: http://127.0.0.1:8001/api/health

### Terminal 2 — UI

From the repository root:

```bash
cd frontend
npm install
npm run dev
```

Open **http://127.0.0.1:5174** and walk through the wizard. Click **Get recommendation** on the review step.

### Try these scenarios

Use these to sanity-check conservative behavior:

| Scenario | Suggested inputs | Expected direction |
|----------|------------------|-------------------|
| **Routing / VRP** | Problem type: Routing; ~250–500 variables; sparse constraints; sample-based OK | Hybrid or **quantum**, with notes on QUBO formulation |
| **Small unstructured problem** | General optimization; **&lt;50** variables; no QUBO checkbox | **Classical** — setup/queue rarely pays off |
| **ML training** | Problem type: ML training; large variable count | **Classical** — directs to GPU/TPU stacks |
| **Needs exact optimum** | Any combinatorial type; **&gt;200** variables; “provably optimal” checked | **Hybrid** — classical validation, not quantum-only |

## API

| Endpoint | Description |
|----------|-------------|
| `GET /api/health` | Liveness |
| `GET /api/taxonomy` | Problem class metadata (`backend/data/problem_taxonomy.json`) |
| `POST /api/analyze` | Full recommendation JSON from intake body (see `backend/app/models.py` → `IntakeRequest`) |

Example analyze payload (minimal):

```json
{
  "industry": "logistics",
  "problem_type": "routing",
  "problem_description": "120 stops with time windows",
  "variable_count": 400,
  "constraint_density": "sparse",
  "needs_exact_solution": false,
  "has_qubo_structure": null,
  "current_approach": "OR-Tools heuristic",
  "time_budget": "minutes",
  "nisq_tolerance": true
}
```

## Project layout

```
backend/
  app/           # classifier, scorer, examples, resources, FastAPI routes
  data/          # taxonomy + D-Wave doc link catalog
frontend/
  src/App.tsx    # wizard + results UI
```

## Design choices

| Area | Approach |
|------|----------|
| Classification | Wizard problem type + keyword boosts in description / current approach |
| Scoring | Transparent 5-axis rules—not a black-box LLM score |
| Recommendation | **Conservative bias**; quantum only when structure and scale align |
| Examples | Problem-class-specific QUBO/BQM pseudocode in the response |
| Resources | Static curated list in `backend/data/dwave_resources.json` |
| LLM | Not required; entire path is rules-based for reproducible demos |

## Outreach

A short, spam-safe email template lives in [`OUTREACH_EMAIL.md`](OUTREACH_EMAIL.md). Point recipients to this README for run steps and feature detail.

## Not affiliated

Student/portfolio prototype inspired by D-Wave’s adoption narrative. **Not** an official D-Wave product or endorsement.
