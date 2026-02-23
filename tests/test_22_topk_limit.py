"""Test 22: TopK > 100 — S3 Vectors hard limit."""

import time

from core.clients import get_clients
from core.config import QDRANT_COLLECTION, S3V_BUCKET_NAME, S3V_INDEX_NAME
from core.embeddings import generate_query_embedding


def run():
    qc, sc = get_clients()
    qvec = generate_query_embedding("popular movies")

    print("=" * 60)
    print("TEST 22: TopK Limit (S3 Vectors max = 100)")
    print("=" * 60)

    # Qdrant: topK=200 — no problem
    t0 = time.perf_counter()
    q_res = qc.query_points(QDRANT_COLLECTION, query=qvec, limit=200, with_payload=True)
    q_ms = (time.perf_counter() - t0) * 1000
    print(f"\nQdrant: topK=200 → returned {len(q_res.points)} results ({q_ms:.0f}ms) ✓")

    # S3 Vectors: topK=100 — works
    t0 = time.perf_counter()
    s_res = sc.query_vectors(
        vectorBucketName=S3V_BUCKET_NAME,
        indexName=S3V_INDEX_NAME,
        queryVector={"float32": qvec},
        topK=100,
        returnDistance=True,
        returnMetadata=True,
    )
    s_ms = (time.perf_counter() - t0) * 1000
    print(
        f"S3 Vectors: topK=100 → returned {len(s_res['vectors'])} results ({s_ms:.0f}ms) ✓"
    )

    # S3 Vectors: topK=101 — should fail
    print(f"\nS3 Vectors: topK=101 →", end=" ")
    try:
        sc.query_vectors(
            vectorBucketName=S3V_BUCKET_NAME,
            indexName=S3V_INDEX_NAME,
            queryVector={"float32": qvec},
            topK=101,
            returnDistance=True,
        )
        print("Unexpectedly succeeded ✗")
    except Exception as e:
        print(f"REJECTED ✓")
        print(f"  Error: {str(e)[:100]}")

    print(f"\n→ Qdrant: no hard topK limit (limited by data size)")
    print(f"→ S3 Vectors: hard max 100 per query")


if __name__ == "__main__":
    run()
