"""S3 storage for publishing the results JSON."""

import json

import boto3

from ..config import config


def publish_results(summary: dict) -> str:
    """
    Upload the results summary JSON to S3 with public-read via CloudFront.

    Returns:
        S3 object URL (not CloudFront — use config.RESULTS_BASE_URL for public URL).
    """
    s3 = boto3.client("s3", region_name=config.AWS_REGION)
    key = config.RESULTS_KEY
    body = json.dumps(summary, ensure_ascii=False, indent=2)

    s3.put_object(
        Bucket=config.RESULTS_BUCKET,
        Key=key,
        Body=body.encode("utf-8"),
        ContentType="application/json",
        CacheControl="no-cache, no-store, must-revalidate",
    )

    return f"s3://{config.RESULTS_BUCKET}/{key}"
