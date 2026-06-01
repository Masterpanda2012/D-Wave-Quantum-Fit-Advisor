# Outreach email — D-Wave Systems

**Subject:** Open-source prototype — “should I use quantum?” intake, fit scoring, and conservative recommendations

---

Hi D-Wave team,

I’m writing to share a small open-source prototype I built in the spirit of how you talk about **lowering the adoption barrier** for quantum optimization — and to spell out the gap it tries to fill for teams who think about **problem qualification, solver selection, and classical baselines** as one loop rather than three disconnected conversations.

## What it is

**Quantum Fit Advisor** (working name) is a **FastAPI** backend plus a **React** wizard UI. The README positions it as a decision companion for engineers who are not quantum specialists: describe an optimization problem in domain terms, and get a **conservative** recommendation — **classical**, **hybrid**, or **quantum** — with plain-English rationale instead of hype.

The app includes:

- A **four-step intake wizard** (problem type, scale, constraints, review) mapped to combinatorial classes you already teach in Ocean examples — routing, scheduling, portfolio, feature selection, and more.
- A **transparent 5-axis fit model** (problem size, QUBO structure, sample tolerance, hardware fit, exactness needs) so the recommendation is inspectable, not a black box.
- A **rules-first recommendation engine** with **conservative bias** — under ~50 unstructured variables it defaults to classical; when exact optimality is required it routes to hybrid, not quantum-only.
- **Worked QUBO/BQM sketches** per problem class so the output is actionable for someone starting in Ocean.
- **Curated D-Wave doc links** (Leap hybrid, BQM concepts, TSP/portfolio examples) matched to the detected class.
- A lightweight **lead-qualification tier** (`low` / `medium` / `high`) for funnel experiments — useful if you want to see which intakes would have been worth a solutions conversation.

## The gap it tries to fill

Public quantum content often answers *how* to run a sampler, but the question that blocks adoption is *whether* quantum is the right tool for this problem at this scale. Sales and solutions teams still spend time on problems that were always classical wins. This prototype is a **self-serve first pass**: qualify the problem, explain the tradeoffs, and point to the right next step — classical baseline, hybrid Leap workflow, or a structured quantum POC — without pretending to replace your solutions architects or Ocean docs.

## How to run it

```bash
# API (port 8001)
cd backend && python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8001

# UI (port 5174)
cd frontend && npm install && npm run dev
# → http://127.0.0.1:5174
```

Try a routing problem at ~250–500 variables with sparse constraints — you should see hybrid or quantum with explicit conservative notes. Try ML training or &lt;50 variables — you should see classical with clear reasoning.

## Repo

https://github.com/Masterpanda2012/D-Wave-Quantum-Fit-Advisor

I’m a student builder exploring how adoption tooling can complement Ocean and Leap, not compete with them. If this is useful, I’d welcome feedback on whether the scoring axes match how your solutions team actually qualifies opportunities — or if you’d point me to someone on the developer-relations or product side who cares about self-serve qualification flows.

Thanks for your time,

Nikhil Avin
