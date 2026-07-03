# Model Routing & the File Bus (Tense)

Tense is a **research repo**. The routing here is tuned for that: the bottleneck is novel
reasoning about unsolved bitemporal semantics, not shipping features. Two things live in this
doc — which model does which work, and how the pieces talk (the filesystem, no orchestration
platform, no vector-DB memory layer).

---

## Model routing

| Model  | Use it for | Notes |
|--------|------------|-------|
| **Sonnet** | Code and execution — the toy proofs, test scaffolds, running experiments, mechanical edits. | The workhorse for turning a decided experiment into running code. |
| **Opus** | Architecture, ADRs, and the hard semantics calls — the bitemporal-cascade questions, whether re-projection has an expressiveness ceiling, what counts as a dependency. | Load-bearing research decisions get an ADR (continue the numbering in `Tense — Decisions (ADR).md`). |
| **Fable** | **Frontier reasoning — and here it earns its seat.** Tense is exactly the kind of unsolved, novel-semantics problem Fable is for: non-oblivious retroactivity is genuinely open research. Reach for it on the conceptual knots. | **Auto-fallback caveat:** Fable can silently fall back to another model, so never assume a given answer actually came from Fable, and don't rely on it for a reproducible or load-bearing step. Treat its output as a lead to verify by building, not a result to trust — which fits Tense's "resolve by building, not debating" discipline anyway. |

Rule of thumb for Tense: **Sonnet builds the toy, Opus decides the fork, Fable is pulled in
at the genuine frontier** — the semantics no one has cleanly solved. Unlike Graphloom (a
shippable product where Fable is frontier-only and rare), Tense *is* a frontier problem, so
Fable has a standing seat at the table here.

---

## The file bus (how everyone stays in sync)

The filesystem is the message bus. No orchestration platform, no hosted memory, no vector DB.
State is files on disk; every participant reads and writes the same files.

**Participants:**
- **Claude Code (terminal)** — the builder. Runs the toy proofs, writes core code, keeps the
  research logs and ADRs current.
- **Cowork / chat (Opus + Fable)** — semantics reasoning, ADR drafting, the frontier
  questions.
- **ChatGPT (reviewer)** — independent reviewer/adversary. Reads the repo and the research
  logs, produces review reports, proposes experiments and test cases. Never authors code or
  tests. See `AGENTS.md` and `docs/reviews/PROTOCOL.md`.

**Handoff artifacts (all on disk):**
- `sessions/STATE.md` — rolling snapshot (Now / In flight / Blocked / Open frontier / Next).
- `Tense — Research Log.md` — chronological lab notebook (tried / expected / got / decided /
  why).
- `Tense — Decisions (ADR).md` — load-bearing forks (continue numbering from ADR-003).
- `Tense — Open Questions.md` — the parking lot, including the central thesis question.
- **Working diff** — the change/experiment under review.
- `docs/reviews/*.md` — review reports.

**The loop, on the bus:** builder runs an experiment + updates STATE.md and the Research Log →
reviewer reads STATE.md + diff + logs and writes a review to `docs/reviews/` (research-claim
integrity first) → builder acts, logging results and any ADR. Producer never verifies its own
claim; experiment/test-authoring stays separate from review.
