# Tense — Open Questions

Running parking lot of "don't know yet." One line each. Check off and date when resolved;
move the reasoning into the Research Log or an ADR.

Format: `- [ ] <question> (raised YYYY-MM-DD)`

---

- [x] Re-projection from scratch vs. stored provenance edges — resolved 2026-06-20 → ADR-003: re-projection wins at ≤20 facts
- [ ] When a base fact's VALID time is corrected (not just its value), what exactly happens to a derived fact's valid time vs. its tx time? (raised 2026-06-20) — the genuinely subtle bitemporal-cascade question; expect the toy to force the answer
- [ ] What counts as a "dependency"? If a rule reads fact A but its output doesn't change when A changes, was C really derived from A? (raised 2026-06-20)
- [ ] How is a derivation rule registered/identified so a later correction can re-fire the same rule? (raised 2026-06-20)
- [ ] **[CENTRAL THESIS QUESTION]** Does re-projection have an expressiveness ceiling, not just a cost ceiling? Re-projection (O(facts×rules)) is cheap at 20 facts, but cost may not be the binding constraint: can re-projection represent a derived fact that is itself a stored, first-class bitemporal object — one that other facts depend on and that carries its own valid/tx timeline? The audit/provenance use-case may require the derived belief to be a persisted, queryable, depended-upon entity, not just a view. If so, re-projection cannot replace stored provenance edges at any scale; the limit is architectural, not performance. (raised 2026-06-21)
