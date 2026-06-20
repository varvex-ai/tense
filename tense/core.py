from dataclasses import dataclass
from datetime import datetime
from typing import Any, Callable


@dataclass(frozen=True)
class Fact:
    entity: str
    attr: str
    value: Any
    valid_time: datetime  # when the fact was true in the world
    tx_time: datetime     # when this version was recorded by the system


class Store:
    """Append-only bitemporal fact store. Derived facts are never stored — always re-projected."""

    def __init__(self) -> None:
        self._log: list[Fact] = []

    def assert_fact(
        self,
        entity: str,
        attr: str,
        value: Any,
        valid_time: datetime,
        tx_time: datetime,
    ) -> None:
        """Record a base fact (or a retroactive correction) into the append-only log."""
        self._log.append(Fact(entity, attr, value, valid_time, tx_time))

    def as_of(self, as_of_tx: datetime, as_of_valid: datetime) -> list[Fact]:
        """
        Return the believed set of facts at the bitemporal coordinate (as_of_tx, as_of_valid).

        For each (entity, attr, valid_time) triple, pick the latest tx_time <= as_of_tx.
        Then keep only facts whose valid_time <= as_of_valid.

        A retroactive correction is just a new log entry with the same (entity, attr,
        valid_time) but a later tx_time and a new value. Querying with as_of_tx before
        the correction's tx_time naturally excludes it — preserving the prior belief.
        """
        best: dict[tuple, Fact] = {}
        for f in self._log:
            if f.tx_time <= as_of_tx:
                key = (f.entity, f.attr, f.valid_time)
                if key not in best or f.tx_time > best[key].tx_time:
                    best[key] = f
        return [f for f in best.values() if f.valid_time <= as_of_valid]

    def derive(
        self,
        rule: Callable[[list[Fact]], Any],
        as_of_tx: datetime,
        as_of_valid: datetime,
    ) -> Any:
        """
        Re-project a user-supplied rule against the believed facts at (as_of_tx, as_of_valid).

        The cascade is automatic: derived facts are never stored. Every call to derive()
        recomputes from the believed base facts at that bitemporal coordinate.
        Retroactive corrections cascade for free — re-project at the new tx_time and
        the rule sees the corrected base, producing the corrected derived fact.
        Pre-correction beliefs are preserved: re-project at the old tx_time and the
        rule sees the original base.
        """
        return rule(self.as_of(as_of_tx, as_of_valid))
