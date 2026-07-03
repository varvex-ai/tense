# Tense — Session State

Rolling snapshot. Update **every session**. First artifact anyone reads on the file bus.
Keep it short and current; the narrative log lives in `Tense — Research Log.md`.

---

## Now
<!-- Where the thesis actually stands today. -->
- **Toy proof is green** (`tests/test_cascade.py`): on a 2-fact toy with one user-supplied
  rule (`ownership > 50% = control`), a retroactive correction (40% → 60%) re-projects to
  "controls", and the pre-correction belief ("no-control" at the earlier `tx_time`) is still
  queryable. Cascade + history preservation demonstrated for the **single-hop** case.
- **Core** (`tense/core.py`): in-memory append-only `Store` with `assert_fact`,
  `as_of(as_of_tx, as_of_valid)` bitemporal filter, and `derive(rule, tx, valid)` by
  **re-projection** (derived facts never stored) — per ADR-003.
- **Decisions recorded:** ADR-001 (Python), ADR-002 (business rules live outside Tense),
  ADR-003 (re-projection over stored provenance edges, at ≤20 facts).
- **Repo hygiene note (uncommitted at last check):** modified `Tense — Open Questions.md`,
  untracked `AGENTS.md` and `tense.egg-info/`. Decide what to commit (see the governance-layer
  note under Blocked).

## In flight
<!-- Actively being worked on. -->
- Governance/agent layer landed: routing table, review protocol, this STATE file, plus the
  refreshed CLAUDE.md (model routing + loop) and AGENTS.md (now the independent ChatGPT
  reviewer role, not a builder clone). Pending: commit these to git and push.

## Blocked
<!-- Waiting, and on what. -->
- (nothing blocked)

## Open frontier
<!-- The live research tension. This is the point of the thesis. -->
- **[CENTRAL THESIS QUESTION]** Does re-projection have an *expressiveness* ceiling, not just a
  *cost* ceiling? Re-projection is cheap at 20 facts, but the audit/provenance use-case may
  require a derived belief to be a **stored, first-class bitemporal object** that other facts
  depend on and that carries its own valid/tx timeline. If so, re-projection cannot replace
  stored provenance edges at *any* scale — the limit would be architectural, not performance.
  (This is exactly the property that distinguishes Tense from Graphloom: Graphloom commits to
  pure projection forever; Tense is testing whether it must go beyond it.)
- Subsidiary open questions (from `Tense — Open Questions.md`): what happens to a derived
  fact's valid/tx time when a base fact's *valid* time is corrected; what precisely counts as
  a "dependency"; how a rule is registered so a later correction can re-fire it.

## Next
<!-- The single highest-priority next action. -->
- **The two-hop experiment: D → C → A.** Extend the toy from single-hop to a chain (D derived
  from C, C derived from A). Retroactively correct A and prove the correction cascades all the
  way to D **while every pre-correction belief along the chain stays queryable**. This is the
  first real stress test of non-oblivious retroactivity beyond one hop, and it is the most
  likely thing to force an answer on the central thesis question above.
