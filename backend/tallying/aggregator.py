"""
Vote aggregation — recomputes totals from all stored BUs.

Uses a full recompute strategy: idempotent and safe for the scale of a
single municipality (<500 sections).
"""

import json
from collections import defaultdict
from typing import Any

from ..storage.dynamodb import scan_all_bulletins


def aggregate_votes() -> dict[str, Any]:
    """
    Load all BUs from DynamoDB and aggregate votes per cargo per candidate.

    Returns a nested dict:
        {
          process_key: {
            cargo_code: {
              candidate_number: total_votes,
              ...
              "_blank": total_blank,
              "_null": total_null,
              "_total": grand_total,
              "_sections_counted": n,
            }
          }
        }
    """
    items = scan_all_bulletins()

    # process_key → cargo_code → candidate/special → int
    aggregated: dict[str, dict[str, dict[str, int]]] = defaultdict(
        lambda: defaultdict(lambda: defaultdict(int))
    )
    process_meta: dict[str, dict] = {}

    for item in items:
        pk = item.get("pk", "")
        elections_raw = item.get("elections", "[]")
        elections = json.loads(elections_raw) if isinstance(elections_raw, str) else elections_raw

        # Track turnout
        agg = aggregated[pk]
        agg["_meta"]["_eligible_voters"] += int(item.get("eligible_voters", 0))
        agg["_meta"]["_compared_voters"] += int(item.get("compared_voters", 0))
        agg["_meta"]["_absent_voters"] += int(item.get("absent_voters", 0))
        agg["_meta"]["_sections_counted"] += 1

        process_meta[pk] = {
            "process": item.get("process", ""),
            "plea": item.get("plea", ""),
            "turn": item.get("turn", ""),
            "state": item.get("state", ""),
        }

        for election in elections:
            cargo = election.get("cargo_code", "")
            agg[cargo]["_blank"] += election.get("blank_votes", 0)
            agg[cargo]["_null"] += election.get("null_votes", 0)
            agg[cargo]["_total"] += election.get("total_votes", 0)
            agg[cargo]["_sections_counted"] += 1

            for candidate in election.get("candidates", []):
                number = candidate.get("number", "")
                agg[cargo][number] += candidate.get("votes", 0)

    return {
        pk: {
            "meta": {**process_meta.get(pk, {}), **dict(aggregated[pk].get("_meta", {}))},
            "results": {
                cargo: dict(votes)
                for cargo, votes in aggregated[pk].items()
                if cargo != "_meta"
            },
        }
        for pk in aggregated
    }
