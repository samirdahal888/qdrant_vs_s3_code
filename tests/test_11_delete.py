"""Test 11: Delete Vectors — Both platforms."""

import time

from qdrant_client import models

from core.clients import get_clients
from core.config import QDRANT_COLLECTION, S3V_BUCKET_NAME, S3V_INDEX_NAME, qdrant_id


def run():
    qc, sc = get_clients()

    print("=" * 60)
    print("TEST 11: Delete Vectors")
    print("=" * 60)

    target = "mov_50"  # Everything Everywhere All at Once

    # Before counts
    q_before = qc.get_collection(QDRANT_COLLECTION).points_count
    s_before = len(
        sc.list_vectors(
            vectorBucketName=S3V_BUCKET_NAME, indexName=S3V_INDEX_NAME, maxResults=1000
        ).get("vectors", [])
    )

    # Qdrant delete
    t0 = time.perf_counter()
    qc.delete(
        QDRANT_COLLECTION,
        points_selector=models.PointIdsList(points=[qdrant_id(target)]),
    )
    q_ms = (time.perf_counter() - t0) * 1000

    q_after = qc.get_collection(QDRANT_COLLECTION).points_count

    # S3 Vectors delete
    t0 = time.perf_counter()
    sc.delete_vectors(
        vectorBucketName=S3V_BUCKET_NAME,
        indexName=S3V_INDEX_NAME,
        keys=[target],
    )
    s_ms = (time.perf_counter() - t0) * 1000

    s_after = len(
        sc.list_vectors(
            vectorBucketName=S3V_BUCKET_NAME, indexName=S3V_INDEX_NAME, maxResults=1000
        ).get("vectors", [])
    )

    print(f"\nQdrant ({q_ms:.0f}ms): {q_before} → {q_after} vectors")
    print(f"  Method: delete(points=[id])")

    print(f"\nS3 Vectors ({s_ms:.0f}ms): {s_before} → {s_after} vectors")
    print(f'  Method: delete_vectors(keys=[{{"key": id}}])')

    print(f"\n→ Both support batch delete. S3 Vectors max 500 per call.")


if __name__ == "__main__":
    run()
