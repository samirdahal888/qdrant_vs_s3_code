"""Lightweight client factory — returns ready-to-use clients without reloading data."""

import boto3
from qdrant_client import QdrantClient

from core.config import AWS_REGION, QDRANT_URL

# Module-level singletons (created once, reused across tests)
_qc = None
_sc = None


def get_qdrant() -> QdrantClient:
    """Return a Qdrant client (singleton)."""
    global _qc
    if _qc is None:
        _qc = QdrantClient(url=QDRANT_URL, timeout=120)
    return _qc


def get_s3v():
    """Return an S3 Vectors boto3 client (singleton)."""
    global _sc
    if _sc is None:
        _sc = boto3.client("s3vectors", region_name=AWS_REGION)
    return _sc


def get_clients():
    """Return (qdrant_client, s3v_client) — lightweight, no data loading."""
    return get_qdrant(), get_s3v()
