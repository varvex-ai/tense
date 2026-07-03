# Tense

A bitemporal knowledge-graph primitive: facts that carry both their timelines and their
provenance, so a retroactive correction cascades to everything derived from it while
preserving every prior belief as a queryable historical state.

**Status:** single-hop toy proof is green. On a small in-memory toy, a retroactive
correction re-projects to the corrected derived fact *and* the pre-correction belief stays
queryable at its earlier transaction time. Next up is the multi-hop cascade.

## The two timelines

- `valid_time` — when a fact was true in the world.
- `tx_time` — when the system recorded (or corrected) that fact.

A derived fact is not a stored value; it is a re-projection of a rule against what was
believed *as of* a chosen `(tx_time, valid_time)`. Correcting a base fact appends a new
belief; derived facts are re-projected rather than mutated. The unsolved core Tense is
chasing is **non-oblivious retroactivity** — cascading corrections that preserve every prior
belief as queryable state — which even XTDB explicitly punts on.

## Repo

- `tense/core.py` — the library: an append-only bitemporal `Store` with `as_of(tx, valid)`
  and `derive(rule, tx, valid)` by re-projection.
- `tests/test_cascade.py` — the toy proof (cascade + history preservation).
- `CLAUDE.md` — builder frame + research-logging discipline (read every Claude Code session).
- `AGENTS.md` — the independent ChatGPT reviewer role.
- `Tense — Research Log.md` — chronological lab notebook.
- `Tense — Decisions (ADR).md` — load-bearing decisions (through ADR-003).
- `Tense — Open Questions.md` — parking lot of unknowns, incl. the central thesis question.
- `docs/` — model routing and the review protocol.
- `sessions/STATE.md` — rolling session snapshot and primary handoff artifact.

## Run the proof

```bash
python -m pytest -q
```

## One-time setup note

The three log files can live here in the repo, OR in the Obsidian vault under
`B2G/Track C — Tense/`. Pick one home and tell Claude Code the path so it logs there
automatically. If the vault is on the same machine, pointing Claude Code at the vault folder
means the research log and the Obsidian notes live together — preferred.

## First milestone (done) and what's next

**Done:** on the toy, a retroactive correction cascades correctly through a derived fact and
every pre-correction belief is still queryable — single-hop. That proves the primitive in
the smallest case.

**Next: the two-hop experiment — D → C → A.** Extend the toy to a derivation chain,
retroactively correct A, and prove the correction cascades all the way to D while every
pre-correction belief along the chain stays queryable. This is the first real stress test of
non-oblivious retroactivity beyond one hop. See `sessions/STATE.md`.

The real validation later: one other engineer depends on it. Not market size. Dependency.
