"""
Step 7 — Publish Lambda

Uploads the results summary JSON to S3 for CloudFront serving.

Input:  { ..., "summary": {...} }
Output: { ..., "published_url": "s3://..." }
"""

import logging

from ..storage.s3 import publish_results

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def handler(event: dict, context) -> dict:
    if event.get("tally_skipped") or event.get("summary") is None:
        logger.info("No summary to publish — skipping")
        return {**event, "published_url": None}

    summary: dict = event["summary"]
    url = publish_results(summary)
    logger.info("Published results to %s", url)

    return {**event, "published_url": url}
