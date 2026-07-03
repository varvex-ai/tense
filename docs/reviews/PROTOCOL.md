# Review Protocol (ChatGPT — independent reviewer, Tense)

Tense is a research thesis, not a product. So the reviewer's first duty is different from
Graphloom's: here the top check is **research-claim integrity** — does the repo actually
prove what it says it proves? The reviewer is ChatGPT, operating over the repo through the
filesystem. It reads; it reports; it proposes experiments and test cases. **It never authors
code or tests.**

---

## What the reviewer reads (in this order)

1. **`sessions/STATE.md`** — current state: Now / In flight / Blocked / Open frontier / Next.
2. **The working diff** — the change or experiment under review.
3. **The research record** — `Tense — Research Log.md`, `Tense — Decisions (ADR).md`,
   `Tense — Open Questions.md`.
4. **The code + toy proof** — `tense/core.py`, `tests/` (especially the cascade proof).

If any of these are missing or stale, that is itself a finding.

---

## The ordered checks

Run in order. Research-claim integrity is always first; a failure there is reported at the
top and blocks.

1. **Research-claim integrity (mandatory, every review — the top check).** Does the code
   actually demonstrate the claim being made? Specifically:
   - Does the toy proof prove what the Research Log / README says it proves, or is the
     assertion weaker than the claim (e.g. "cascade works" when only a single-hop, single-rule
     case is shown)?
   - Is a "green" result green for the right reason, or is it passing trivially / by
     construction?
   - Is the claimed novelty (non-oblivious retroactivity — cascading correction with every
     prior belief preserved and queryable) actually exercised, or only asserted in prose?
   - Are the boundaries of the claim stated honestly (what is NOT yet shown)?
   If the claim outruns the evidence → flag at the top, mark blocking.

2. **Scope / primitive discipline.** Does the change keep Tense a policy-agnostic *primitive*?
   Business rules must stay outside Tense (ADR-002). Flag any leakage of domain logic
   (thresholds, "control," etc.) into the core.

3. **Bitemporal correctness.** Are `valid_time` and `tx_time` handled correctly? Does
   `as_of(tx, valid)` pick the right believed set? Does a retroactive correction preserve the
   pre-correction belief as a genuinely queryable state, not a coincidence of the toy?

4. **Cascade correctness (the novel core).** Does a correction to a base fact propagate to
   everything derived from it, across the timelines, for the *right structural reason*?
   Pressure-test multi-hop derivations (D→C→A), not just single-hop.

5. **Open-question hygiene.** Does the change resolve, sharpen, or newly raise an entry in
   `Tense — Open Questions.md` — especially the central thesis question (does re-projection
   have an *expressiveness* ceiling, not just a cost ceiling)? Are resolved questions logged
   to an ADR or the Research Log?

6. **Experiment / test-coverage gaps.** Where is the claim under-tested? What experiment would
   most threaten it?

---

## Proposing experiments and tests (never authoring them)

For each gap, the reviewer **describes** an experiment or test case in prose: the scenario,
setup, action, and expected outcome — plus which claim it stresses. It does **not** write
test code, fixtures, or a PR. The build side authors them. This keeps experiment-authoring
separate from review (producer ≠ verifier), which matters doubly in a thesis where the
temptation to prove your own claim is strongest.

---

## Report format

Write the report to `docs/reviews/YYYY-MM-DD-<short-topic>.md`:

```
# Review — <topic> — YYYY-MM-DD
Reviewer: ChatGPT (independent)
Change under review: <branch / diff ref>

## Research-claim integrity: PASS | FAIL
<one line; if FAIL, which claim outruns which evidence>

## Verdict: sound | sound-with-caveats | claim-overreaches | blocked

## Findings
### Scope / primitive discipline
- ...
### Bitemporal correctness
- ...
### Cascade correctness
- ...
### Open-question hygiene
- ...

## Proposed experiments / test cases (descriptions only — not authored)
- <scenario> — setup / action / expected — which claim it stresses
- ...

## Open questions for the builder
- ...
```

**Hard rule:** propose experiments and test cases, never author them. Report findings, never
patch code. The value of this role is independence — a reviewer that writes the proof has
stopped being able to check it.
