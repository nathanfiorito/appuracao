"""
Step 6 — Tally Lambda

Recomputes the full vote aggregation from all stored BUs.
Only runs if a new BU was actually stored (stored=True).

Input:  { ..., "stored": True/False }
Output: { ..., "summary": {...} }
"""

import logging

from ..tallying.summary import build_summary

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def handler(event: dict, context) -> dict:
    if not event.get("stored"):
        logger.info("No new BU stored — skipping tally")
        return {**event, "summary": None, "tally_skipped": True}

    logger.info("Recomputing vote totals...")
    summary = build_summary()
    logger.info(
        "Tally complete: %d elections, %d sections counted",
        len(summary.get("elections", [])),
        sum(e.get("sections_counted", 0) for e in summary.get("elections", [])),
    )

    return {**event, "summary": summary}
