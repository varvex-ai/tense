# Tense — Open Questions

Running parking lot of "don't know yet." One line each. Check off and date when resolved;
move the reasoning into the Research Log or an ADR.

Format: `- [ ] <question> (raised YYYY-MM-DD)`

---

- [x] Re-projection from scratch vs. stored provenance edges — resolved 2026-06-20 → ADR-003: re-projection wins at ≤20 facts
- [ ] When a base fact's VALID time is corrected (not just its value), what exactly happens to a derived fact's valid time vs. its tx time? (raised 2026-06-20) — the genuinely subtle bitemporal-cascade question; expect the toy to force the answer
- [ ] What counts as a "dependency"? If a rule reads fact A but its output doesn't change when A changes, was C really derived from A? (raised 2026-06-20)
- [ ] How is a derivation rule registered/identified so a later correction can re-fire the same rule? (raised 2026-06-20)
