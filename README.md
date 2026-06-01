# Quantum Fit Advisor

Open-source prototype for the **D-Wave "Should I Use Quantum?"** concept from the internship design brief: a guided intake wizard that classifies optimization problems, scores quantum fit on five axes, and returns a **conservative** classical / hybrid / quantum recommendation with rationale, worked QUBO/BQM sketches, and D-Wave documentation links.

## Why this exists

Most engineers do not need a lecture on qubits — they need a clear answer to whether annealing or Leap hybrid solvers are worth exploring for *their* combinatorial problem. This tool lowers the expertise barrier while **defaulting to classical** when scale or structure does not justify quantum.

## Run locally

**API** (port 8001):

```bash
cd dwave-quantum-fit-advisor/backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8001
```

**UI** (port 5174):

```bash
cd dwave-quantum-fit-advisor/frontend
npm install
npm run dev
```

Open http://127.0.0.1:5174

## API

- `GET /api/health` — liveness
- `GET /api/taxonomy` — problem class metadata
- `POST /api/analyze` — full recommendation payload from intake JSON

## Design choices

| Area | Approach |
|------|----------|
| Classification | Problem-type wizard + keyword boosts in free text |
| Scoring | Transparent 5-axis rules (size, structure, NISQ tolerance, hardware fit, exactness) |
| Recommendation | Conservative bias; quantum only when structure + scale align |
| Examples | Problem-class-specific QUBO/BQM pseudocode |
| Resources | Curated links into D-Wave docs (Ocean, Leap, examples) |
| Lead signal | `low` / `medium` / `high` for sales-adjacent funnel experiments |

## Not affiliated

Prototype for portfolio / outreach. Not an official D-Wave product.
