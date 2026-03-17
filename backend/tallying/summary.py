"""
Generates the public-facing results JSON from aggregated vote data.
"""

from datetime import datetime, timezone
from typing import Any

from .aggregator import aggregate_votes


def build_summary() -> dict[str, Any]:
    """
    Build the full results summary to be published to S3/CloudFront.

    Schema:
    {
      "generated_at": "ISO-8601",
      "elections": [
        {
          "process_key": "...",
          "process": "...",
          "plea": "...",
          "turn": "1",
          "state": "SP",
          "sections_counted": 42,
          "eligible_voters": 10000,
          "compared_voters": 8500,
          "cargos": [
            {
              "cargo_code": "11",
              "sections_counted": 42,
              "total_votes": 8500,
              "blank_votes": 200,
              "null_votes": 100,
              "candidates": [
                {"number": "11111", "votes": 4000},
                ...
              ]
            }
          ]
        }
      ]
    }
    """
    raw = aggregate_votes()
    elections = []

    for pk, data in raw.items():
        meta = data.get("meta", {})
        results = data.get("results", {})

        cargos = []
        for cargo_code, votes in results.items():
            candidates = [
                {"number": k, "votes": v}
                for k, v in votes.items()
                if not k.startswith("_")
            ]
            candidates.sort(key=lambda c: c["votes"], reverse=True)

            cargos.append({
                "cargo_code": cargo_code,
                "sections_counted": votes.get("_sections_counted", 0),
                "total_votes": votes.get("_total", 0),
                "blank_votes": votes.get("_blank", 0),
                "null_votes": votes.get("_null", 0),
                "candidates": candidates,
            })

        elections.append({
            "process_key": pk,
            "process": meta.get("process", ""),
            "plea": meta.get("plea", ""),
            "turn": meta.get("turn", ""),
            "state": meta.get("state", ""),
            "sections_counted": meta.get("_sections_counted", 0),
            "eligible_voters": meta.get("_eligible_voters", 0),
            "compared_voters": meta.get("_compared_voters", 0),
            "absent_voters": meta.get("_absent_voters", 0),
            "cargos": cargos,
        })

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "elections": elections,
    }
