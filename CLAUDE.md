# Project Tense — Working Instructions

This file is read at the start of every Claude Code session. It defines (1) what we're
building, (2) how we build, and (3) how we log. Follow it without being re-asked.

---

## 1. What Tense Is

Tense is a **bitemporal knowledge-graph primitive**, built as an open-source Python
library. The core, in one sentence:

> A fact that carries both its timelines and its provenance, such that a retroactive
> correction cascades to everything derived from it while preserving every prior belief
> as a queryable historical state.

**The two timelines:**
- `valid_time`  — when a fact was true in the world
- `tx_time`     — when the system recorded (or corrected) that fact

**The key mental model:** a derived fact is NOT a stored value. It is a *re-projection* —
a re-computation of a rule against what was believed *as of* a chosen time. Correcting a
base fact does not mutate derived facts; it appends a new belief, and derived facts are
re-projected. This is event-sourcing lifted into two time dimensions.

**The unsolved core (the whole point):** cascading retroactive corrections. When a base
fact is corrected, the correction must ripple through everything derived from it, across
both timelines, while every prior belief stays queryable. Even XTDB (the production
leader) explicitly punts on this ("non-oblivious retroactivity"). That gap is Tense.

**Relationship to Graphloom (keep the boundary clean):** Graphloom is the shippable
sibling — it re-projects derived facts from an append-only log and never corrects them in
place. Tense is the research thesis that goes *past* re-projection: whether a derived fact
can be a stored, first-class bitemporal object that is corrected in place and cascades.
The one thing that must never happen is Graphloom silently absorbing Tense's
cascading-correction logic. In this repo we push the frontier; in Graphloom we do not.

---

## 2. How We Build

**Scope discipline — the MVP is brutally small:**
- ~20 facts. Not 20 million. Performance is irrelevant at this stage.
- 1–2 explicit derivation rules, user-supplied as plain Python functions.
- One retroactive correction that cascades and preserves history.
- In-memory only. No storage engine, no query language, no Neo4j, no scale.

**Build order — invert the natural temptation:**
1. Build the **cascade** first, even ugly. It is the hard, novel 20%. If it doesn't work,
   nothing else matters. Do NOT polish the fact representation to avoid the cascade.
2. Then the fact-with-two-timelines representation around it.
3. Then derivation tracking.
4. Then clean up.

**Business rules live OUTSIDE Tense.** The threshold ("ownership > 50% = control") is a
user-supplied function Tense calls as a black box. Tense never inspects what a rule
*means* — it only records *that* a derivation happened and what it depended on. Staying
policy-agnostic is what keeps Tense a foundational primitive, not a domain app.

**First design fork (resolve by building, not debating):** explicit provenance edges vs.
re-projection from scratch. Start with re-projection (simplest, always correct, fine at 20
facts). Only add stored edges when re-projection's cost is actually felt. Log the decision
when made (see below). [Resolved 2026-06-20 as ADR-003: re-projection — but see the CENTRAL
THESIS QUESTION in Open Questions on whether re-projection has an *expressiveness* ceiling.]

**Git from line one.** This is a real repo. Commit working increments with terse messages.

---

## 3. How We Log (research discipline — IMPORTANT)

This is a thesis. Every decision, try, failure, and result gets logged so reasoning is
never lost to memory or buried in chat. BUT the log serves the build — it must stay
lightweight and build-triggered, never become its own project.

**Three log files live in the Obsidian vault folder (path set per machine):**

- `Tense — Research Log.md` — chronological, append-only lab notebook. High frequency.
- `Tense — Decisions (ADR).md` — the big forks only. Rare (~10–15 over the whole thesis).
- `Tense — Open Questions.md` — running parking lot of "don't know yet."

### When to log (build-triggered, automatic — don't ask me each time)
- After a meaningful result (something worked / broke unexpectedly) → Research Log entry.
- After a real fork is decided (e.g. re-projection vs edges) → ADR entry.
- When a "don't know yet" surfaces → add to Open Questions (and remove when resolved).

### Format rules (keep it TERSE — if an entry takes >2 min to write, it's too long)

**Research Log entry** — one block, this shape:
```
### YYYY-MM-DD — <short title>
- Tried: <what>
- Expected: <what I thought would happen>
- Got: <what actually happened>
- Decided: <what I'm doing about it>
- Why: <one line>
```

**ADR entry** — only for load-bearing choices:
```
## ADR-NNN — <decision title>  (YYYY-MM-DD)
- Context: <the fork, 1–2 lines>
- Options: <A vs B, briefly>
- Choice: <what we picked>
- Consequences: <what this commits us to / rules out>
```

**Open Question** — one line: `- [ ] <question> (raised YYYY-MM-DD)`

### Logging boundary (the trap to avoid)
A healthy log is mostly "tried/broke/fixed/learned" entries — evidence of building. If the
log starts filling with structure, templates, or meta-notes about logging, STOP — that's
avoidance with footnotes. Entries are earned by building. Never refine the log's format
instead of adding entries.

---

## 4. Model Routing

Route work to the model that fits the job. Full table + the file-bus handoff live in
`docs/routing-table.md`.

- **Sonnet** — code and execution: the toy proofs, test scaffolds, running experiments,
  mechanical edits.
- **Opus** — architecture, ADRs, and the hard semantics calls: the bitemporal-cascade
  questions, the expressiveness-ceiling question, what counts as a dependency.
- **Fable** — **frontier reasoning, and here it earns its seat.** Tense is exactly the kind
  of unsolved, novel-semantics problem Fable is for — non-oblivious retroactivity is open
  research. Reach for it on the conceptual knots. **Auto-fallback caveat:** Fable can
  silently fall back to another model, so never assume an answer actually came from Fable
  and don't rely on it for a reproducible or load-bearing step. Treat its output as a lead
  to verify by building — which fits "resolve by building, not debating" anyway.

---

## 5. The Loop & the File Bus

- **Producer ≠ verifier.** The independent reviewer is ChatGPT — it reads the repo and
  research logs, writes review reports, and proposes experiments/tests. It never authors
  code or tests. See `AGENTS.md` and `docs/reviews/PROTOCOL.md`.
- **Experiment/test-authoring is separate from review.** The reviewer proposes; the build
  side authors.
- **Update `sessions/STATE.md` every session** — the rolling snapshot (Now / In flight /
  Blocked / Open frontier / Next) and the primary handoff artifact. The filesystem is the
  message bus; no orchestration platform, no vector-DB memory.

---

## 6. The Checkpoint

Done with the first milestone = on the 20-fact toy, a retroactive correction cascades
correctly through derived facts AND every pre-correction belief is still queryable. That
proves the primitive. **Single-hop is done (2026-06-20).**

**Next step: the two-hop experiment — D → C → A.** Extend the toy to a derivation chain
(D derived from C, C derived from A), retroactively correct A, and prove the correction
cascades all the way to D while every pre-correction belief along the chain stays
queryable. This is the first real stress test of non-oblivious retroactivity beyond one
hop, and the most likely thing to force an answer on the central thesis question.

The real validation later: one other engineer depends on it. Not market size. Dependency.
