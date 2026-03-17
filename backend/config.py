"""Application configuration from environment variables."""
import os


class Config:
    AWS_REGION: str = os.environ.get("AWS_REGION", "us-east-1")
    BULLETINS_TABLE: str = os.environ.get("BULLETINS_TABLE", "appuracao-bulletins")
    PARTIAL_QR_TABLE: str = os.environ.get("PARTIAL_QR_TABLE", "appuracao-partial-qrcodes")
    RESULTS_BUCKET: str = os.environ.get("RESULTS_BUCKET", "appuracao-results")
    RESULTS_KEY: str = os.environ.get("RESULTS_KEY", "results.json")
    TSE_PUBLIC_KEY_HEX: str = os.environ.get("TSE_PUBLIC_KEY_HEX", "")


config = Config()
