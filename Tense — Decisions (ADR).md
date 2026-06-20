# Tense — Architecture Decision Records

Load-bearing forks only. Rare (~10–15 over the whole thesis). Format:

```
## ADR-NNN — <decision title>  (YYYY-MM-DD)
- Context: <the fork, 1–2 lines>
- Options: <A vs B, briefly>
- Choice: <what we picked>
- Consequences: <what this commits us to / rules out>
```

---

## ADR-001 — Language: Python  (2026-06-20)
- Context: Choosing the implementation language for the Tense primitive.
- Options: Python (known, ecosystem fit, fast iteration) vs Rust (performance, "foundational" feel, unfamiliar).
- Choice: Python for the exploratory/semantics phase.
- Consequences: Optimises for iteration speed and reachability of first users (the
  GraphRAG/agent-memory crowd live in Python). A Rust performance core via Python bindings
  (pyo3/maturin) stays open as a LATER option, earned only once semantics are solved and
  adoption justifies it. Not now.

## ADR-002 — Business rules live outside Tense  (2026-06-20)
- Context: Where does a derivation rule ("ownership > 50% = control") live?
- Options: Built into Tense (knows thresholds) vs user-supplied black-box function Tense calls.
- Choice: User-supplied function. Tense records THAT a derivation happened and what it
  depended on — never what the rule means.
- Consequences: Keeps Tense a policy-agnostic substrate primitive, not a domain app. Tense
  stores provenance/derivation; the user owns business logic.

<!-- Likely next ADR: re-projection vs stored provenance edges. Resolve by building. -->
