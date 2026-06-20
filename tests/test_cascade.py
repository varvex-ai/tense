"""
Toy proof: bitemporal cascade with preserved history.

Scenario
--------
- Acme owns 40% of BetaCo (valid from 2020-01-01, recorded at T1).
- BetaCo revenue = $1M (valid from 2020-01-01, recorded at T1).
- Rule: Acme "controls" BetaCo if ownership > 50%.
- At T2, a retroactive correction is recorded: Acme actually owned 60% since 2020-01-01.

Assertions
----------
1. Before correction (as_of_tx=T1): derived fact is "no-control".
2. After correction  (as_of_tx=T2): derived fact is "controls"  (cascade worked).
3. Re-querying at T1 after the correction still returns "no-control" (history preserved).
"""

from datetime import datetime

from tense.core import Fact, Store

T1 = datetime(2024, 1, 1)   # original recording
T2 = datetime(2024, 6, 1)   # retroactive correction
VALID = datetime(2020, 1, 1)


def control_rule(facts: list[Fact]) -> str:
    """User-supplied rule: Acme controls BetaCo iff it owns > 50%."""
    for f in facts:
        if f.entity == "acme" and f.attr == "owns_pct_of_betaco" and f.value > 50:
            return "controls"
    return "no-control"


def test_cascade_and_history_preserved() -> None:
    store = Store()

    # --- T1: two base facts recorded ---
    store.assert_fact("acme",   "owns_pct_of_betaco", 40,        VALID, T1)
    store.assert_fact("betaco", "revenue",             1_000_000, VALID, T1)

    # 1. Pre-correction belief: 40% → no-control
    pre = store.derive(control_rule, as_of_tx=T1, as_of_valid=VALID)
    assert pre == "no-control", f"Expected no-control before correction, got {pre!r}"

    # --- T2: retroactive correction — Acme actually owned 60% since 2020 ---
    store.assert_fact("acme", "owns_pct_of_betaco", 60, VALID, T2)

    # 2. Post-correction re-projection: 60% → controls (cascade worked)
    post = store.derive(control_rule, as_of_tx=T2, as_of_valid=VALID)
    assert post == "controls", f"Expected controls after correction, got {post!r}"

    # 3. Pre-correction belief survives: querying at T1 still returns no-control
    pre_still = store.derive(control_rule, as_of_tx=T1, as_of_valid=VALID)
    assert pre_still == "no-control", (
        f"Pre-correction belief was destroyed! Got {pre_still!r}"
    )
