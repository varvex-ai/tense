# Tense

A bitemporal knowledge-graph primitive: facts that carry both their timelines and their
provenance, so a retroactive correction cascades to everything derived from it while
preserving every prior belief as a queryable historical state.

Status: pre-toy-proof. Building the smallest version that proves the cascade works.

## Repo

- `CLAUDE.md` — build frame + research-logging discipline (read every Claude Code session).
- `Tense — Research Log.md` — chronological lab notebook.
- `Tense — Decisions (ADR).md` — load-bearing architectural decisions.
- `Tense — Open Questions.md` — parking lot of unknowns.
- `src/` — the library (to be created, starting with the toy proof).

## One-time setup note

The three log files can live here in the repo, OR in the Obsidian vault under
`B2G/Track C — Tense/`. Pick one home and tell Claude Code the path so it logs there
automatically. If the vault is on the same machine, pointing Claude Code at the vault
folder means the research log and the Obsidian notes live together — preferred.

## First milestone

On a ~20-fact toy: a retroactive correction cascades correctly through derived facts AND
every pre-correction belief is still queryable. That proves the primitive.
