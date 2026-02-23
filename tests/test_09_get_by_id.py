"""Test 09: Get Vectors by ID — Both platforms."""

import time

from core.clients import get_clients
from core.config import QDRANT_COLLECTION, S3V_BUCKET_NAME, S3V_INDEX_NAME, qdrant_id


def run():
    qc, sc = get_clients()

    print("=" * 60)
    print("TEST 09: Get Vectors by ID")
    print("=" * 60)

    test_id = "mov_01"  # Inception

    # Qdrant
    t0 = time.perf_counter()
    q_result = qc.retrieve(
        QDRANT_COLLECTION, ids=[qdrant_id(test_id)], with_payload=True
    )
    q_ms = (time.perf_counter() - t0) * 1000

    print(f"\nQdrant ({q_ms:.0f}ms):")
    if q_result:
        p = q_result[0].payload
        print(f"  ID: {q_result[0].id}")
        print(f"  Title: {p['title']}")
        print(f"  Genre: {p['genre']}, Year: {p['year']}, Rating: {p['rating']}")

    # S3 Vectors
    t0 = time.perf_counter()
    s_result = sc.get_vectors(
        vectorBucketName=S3V_BUCKET_NAME,
        indexName=S3V_INDEX_NAME,
        keys=[test_id],
        returnMetadata=True,
    )
    s_ms = (time.perf_counter() - t0) * 1000

    print(f"\nS3 Vectors ({s_ms:.0f}ms):")
    if s_result["vectors"]:
        v = s_result["vectors"][0]
        m = v["metadata"]
        print(f"  Key: {v['key']}")
        print(f"  Title: {m['title']}")
        print(f"  Genre: {m['genre']}, Year: {m['year']}, Rating: {m['rating']}")

    print(f"\n→ Qdrant: retrieve(ids=[...]) | S3 Vectors: get_vectors(keys=[...])")


if __name__ == "__main__":
    run()
