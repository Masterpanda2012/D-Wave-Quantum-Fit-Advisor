import { useState } from "react";

type ProblemType =
  | "routing"
  | "scheduling"
  | "portfolio"
  | "feature_selection"
  | "simulation"
  | "ml_training"
  | "general";

type Industry =
  | "logistics"
  | "finance"
  | "manufacturing"
  | "life_sciences"
  | "energy"
  | "other";

type TimeBudget = "seconds" | "minutes" | "hours" | "days";

type Intake = {
  industry: Industry;
  problem_type: ProblemType;
  problem_description: string;
  variable_count: number;
  constraint_density: "sparse" | "medium" | "dense";
  needs_exact_solution: boolean;
  has_qubo_structure: boolean | null;
  current_approach: string;
  time_budget: TimeBudget;
  nisq_tolerance: boolean;
};

type AxisScore = {
  axis: string;
  score: number;
  label: string;
  rationale: string;
};

type AnalyzeResult = {
  problem_class_id: string;
  problem_class_label: string;
  classifier_confidence: number;
  recommendation: string;
  recommendation_headline: string;
  rationale_paragraphs: string[];
  axis_scores: AxisScore[];
  conservative_note: string;
  next_steps: string[];
  worked_example: { title: string; formulation_kind: string; body: string };
  resources: { title: string; url: string; kind: string }[];
  lead_qualification: string;
};

const STEPS = ["Problem", "Scale", "Constraints", "Review"] as const;

const PROBLEM_TYPES: { id: ProblemType; label: string; hint: string }[] = [
  { id: "routing", label: "Routing / VRP", hint: "TSP, delivery, fleet" },
  { id: "scheduling", label: "Scheduling", hint: "Shifts, jobs, roster" },
  { id: "portfolio", label: "Portfolio", hint: "Selection, allocation" },
  {
    id: "feature_selection",
    label: "Feature selection",
    hint: "ML subset / QUBO",
  },
  { id: "simulation", label: "Simulation", hint: "Physics / chemistry" },
  { id: "ml_training", label: "ML training", hint: "Neural nets at scale" },
  { id: "general", label: "General optimization", hint: "MIP / custom" },
];

const REC_COLORS: Record<string, string> = {
  classical: "var(--classical)",
  hybrid: "var(--hybrid)",
  quantum: "var(--quantum)",
  explore_hybrid: "var(--hybrid)",
};

const DEFAULT_INTAKE: Intake = {
  industry: "logistics",
  problem_type: "routing",
  problem_description: "",
  variable_count: 250,
  constraint_density: "sparse",
  needs_exact_solution: false,
  has_qubo_structure: null,
  current_approach: "",
  time_budget: "minutes",
  nisq_tolerance: true,
};

export default function App() {
  const [step, setStep] = useState(0);
  const [intake, setIntake] = useState<Intake>(DEFAULT_INTAKE);
  const [result, setResult] = useState<AnalyzeResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const patch = (p: Partial<Intake>) => setIntake((i) => ({ ...i, ...p }));

  const analyze = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch("/api/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(intake),
      });
      if (!res.ok) throw new Error(await res.text());
      setResult(await res.json());
    } catch (e) {
      setError(e instanceof Error ? e.message : "Request failed");
    } finally {
      setLoading(false);
    }
  };

  const reset = () => {
    setStep(0);
    setIntake(DEFAULT_INTAKE);
    setResult(null);
    setError(null);
  };

  if (result) {
    const rec = result.recommendation;
    const recColor = REC_COLORS[rec] ?? "var(--text)";

    return (
      <div className="app">
        <header className="masthead">
          <p className="eyebrow">D-Wave-shaped prototype</p>
          <h1>Quantum Fit Advisor</h1>
          <p className="subtitle">Should you use quantum for this problem?</p>
        </header>

        <section
          className="verdict"
          style={{ borderColor: recColor, "--verdict-accent": recColor } as React.CSSProperties}
        >
          <span className="verdict-badge">{rec.replace("_", " ")}</span>
          <h2>{result.recommendation_headline}</h2>
          <p className="class-label">
            Mapped to <strong>{result.problem_class_label}</strong> (
            {(result.classifier_confidence * 100).toFixed(0)}% confidence) · Lead
            tier: <strong>{result.lead_qualification}</strong>
          </p>
        </section>

        <div className="grid-2">
          <section className="card">
            <h3>Rationale</h3>
            {result.rationale_paragraphs.map((p, i) => (
              <p key={i} className="body-text">
                {p}
              </p>
            ))}
            <p className="conservative">{result.conservative_note}</p>
          </section>

          <section className="card">
            <h3>Fit scores (5 axes)</h3>
            <ul className="axis-list">
              {result.axis_scores.map((a) => (
                <li key={a.axis}>
                  <div className="axis-header">
                    <span>{a.label}</span>
                    <span className="mono">{(a.score * 100).toFixed(0)}%</span>
                  </div>
                  <div className="bar-track">
                    <div
                      className="bar-fill"
                      style={{ width: `${a.score * 100}%`, background: recColor }}
                    />
                  </div>
                  <p className="axis-rationale">{a.rationale}</p>
                </li>
              ))}
            </ul>
          </section>
        </div>

        <div className="grid-2">
          <section className="card">
            <h3>Worked example — {result.worked_example.formulation_kind}</h3>
            <p className="example-title">{result.worked_example.title}</p>
            <pre className="code-block">{result.worked_example.body}</pre>
          </section>

          <section className="card">
            <h3>Next steps</h3>
            <ol className="steps-list">
              {result.next_steps.map((s, i) => (
                <li key={i}>{s}</li>
              ))}
            </ol>
            <h3 className="mt">D-Wave resources</h3>
            <ul className="resource-list">
              {result.resources.map((r) => (
                <li key={r.url}>
                  <a href={r.url} target="_blank" rel="noreferrer">
                    {r.title}
                  </a>
                  <span className="tag">{r.kind}</span>
                </li>
              ))}
            </ul>
          </section>
        </div>

        <button type="button" className="btn secondary" onClick={reset}>
          Start over
        </button>
      </div>
    );
  }

  return (
    <div className="app">
      <header className="masthead">
        <p className="eyebrow">D-Wave-shaped prototype</p>
        <h1>Quantum Fit Advisor</h1>
        <p className="subtitle">
          Describe your optimization problem — get a conservative classical /
          hybrid / quantum recommendation in under a minute.
        </p>
      </header>

      <nav className="stepper">
        {STEPS.map((label, i) => (
          <button
            key={label}
            type="button"
            className={`step-pill ${i === step ? "active" : ""} ${i < step ? "done" : ""}`}
            onClick={() => i <= step && setStep(i)}
          >
            {i + 1}. {label}
          </button>
        ))}
      </nav>

      <section className="card wizard">
        {step === 0 && (
          <>
            <h3>What are you optimizing?</h3>
            <label>
              Industry
              <select
                value={intake.industry}
                onChange={(e) => patch({ industry: e.target.value as Industry })}
              >
                <option value="logistics">Logistics</option>
                <option value="finance">Finance</option>
                <option value="manufacturing">Manufacturing</option>
                <option value="life_sciences">Life sciences</option>
                <option value="energy">Energy</option>
                <option value="other">Other</option>
              </select>
            </label>
            <div className="problem-grid">
              {PROBLEM_TYPES.map((pt) => (
                <button
                  key={pt.id}
                  type="button"
                  className={`problem-card ${intake.problem_type === pt.id ? "selected" : ""}`}
                  onClick={() => patch({ problem_type: pt.id })}
                >
                  <strong>{pt.label}</strong>
                  <span>{pt.hint}</span>
                </button>
              ))}
            </div>
            <label>
              Problem description (optional)
              <textarea
                rows={3}
                placeholder="e.g. 120 delivery stops nightly, minimize distance with time windows"
                value={intake.problem_description}
                onChange={(e) => patch({ problem_description: e.target.value })}
              />
            </label>
          </>
        )}

        {step === 1 && (
          <>
            <h3>Scale & time</h3>
            <label>
              Approximate decision variables
              <input
                type="range"
                min={10}
                max={100000}
                step={10}
                value={intake.variable_count}
                onChange={(e) =>
                  patch({ variable_count: Number(e.target.value) })
                }
              />
              <span className="mono">{intake.variable_count.toLocaleString()}</span>
            </label>
            <label>
              Time budget for a solution
              <select
                value={intake.time_budget}
                onChange={(e) =>
                  patch({ time_budget: e.target.value as TimeBudget })
                }
              >
                <option value="seconds">Seconds</option>
                <option value="minutes">Minutes</option>
                <option value="hours">Hours</option>
                <option value="days">Days</option>
              </select>
            </label>
            <label>
              Current approach (optional)
              <textarea
                rows={2}
                placeholder="e.g. OR-Tools VRP heuristic, 8 min runtime"
                value={intake.current_approach}
                onChange={(e) => patch({ current_approach: e.target.value })}
              />
            </label>
          </>
        )}

        {step === 2 && (
          <>
            <h3>Constraints & structure</h3>
            <label>
              Constraint density
              <select
                value={intake.constraint_density}
                onChange={(e) =>
                  patch({
                    constraint_density: e.target
                      .value as Intake["constraint_density"],
                  })
                }
              >
                <option value="sparse">Sparse</option>
                <option value="medium">Medium</option>
                <option value="dense">Dense</option>
              </select>
            </label>
            <label className="checkbox">
              <input
                type="checkbox"
                checked={intake.needs_exact_solution}
                onChange={(e) => patch({ needs_exact_solution: e.target.checked })}
              />
              Need provably optimal / certified solutions
            </label>
            <label className="checkbox">
              <input
                type="checkbox"
                checked={intake.has_qubo_structure === true}
                onChange={(e) =>
                  patch({
                    has_qubo_structure: e.target.checked ? true : null,
                  })
                }
              />
              Problem already expressed as QUBO / BQM
            </label>
            <label className="checkbox">
              <input
                type="checkbox"
                checked={intake.nisq_tolerance}
                onChange={(e) => patch({ nisq_tolerance: e.target.checked })}
              />
              Sample-based / good-enough solutions are acceptable
            </label>
          </>
        )}

        {step === 3 && (
          <>
            <h3>Review</h3>
            <dl className="review-dl">
              <dt>Industry</dt>
              <dd>{intake.industry}</dd>
              <dt>Problem type</dt>
              <dd>{intake.problem_type}</dd>
              <dt>Variables</dt>
              <dd>{intake.variable_count.toLocaleString()}</dd>
              <dt>Exact solution required</dt>
              <dd>{intake.needs_exact_solution ? "Yes" : "No"}</dd>
              <dt>QUBO structure</dt>
              <dd>
                {intake.has_qubo_structure === true ? "Yes" : "Unknown / No"}
              </dd>
            </dl>
            {intake.problem_description && (
              <p className="body-text">{intake.problem_description}</p>
            )}
          </>
        )}

        {error && <p className="error">{error}</p>}

        <div className="wizard-actions">
          {step > 0 && (
            <button
              type="button"
              className="btn secondary"
              onClick={() => setStep((s) => s - 1)}
            >
              Back
            </button>
          )}
          {step < STEPS.length - 1 ? (
            <button
              type="button"
              className="btn primary"
              onClick={() => setStep((s) => s + 1)}
            >
              Continue
            </button>
          ) : (
            <button
              type="button"
              className="btn primary"
              disabled={loading}
              onClick={analyze}
            >
              {loading ? "Analyzing…" : "Get recommendation"}
            </button>
          )}
        </div>
      </section>

      <p className="footer-note">
        Conservative bias: defaults to classical unless structure and scale clearly
        favor annealing or Leap hybrid. Not affiliated with D-Wave Systems.
      </p>
    </div>
  );
}
