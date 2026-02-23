"""Test 06: Filter — Negation (language != English) — Both."""

import time

from qdrant_client import models

from core.clients import get_clients
from core.config import QDRANT_COLLECTION, S3V_BUCKET_NAME, S3V_INDEX_NAME
from core.embeddings import generate_query_embedding


def run():
    qc, sc = get_clients()
    qvec = generate_query_embedding("great international films")

    print("=" * 60)
    print('TEST 06: Filter — Negation (language != "English")')
    print("=" * 60)

    # Qdrant: must_not
    t0 = time.perf_counter()
    q_res = qc.query_points(
        QDRANT_COLLECTION,
        query=qvec,
        limit=5,
        with_payload=True,
        query_filter=models.Filter(
            must_not=[
                models.FieldCondition(
                    key="language", match=models.MatchValue(value="English")
                ),
            ]
        ),
    )
    q_ms = (time.perf_counter() - t0) * 1000

    # S3 Vectors: $ne
    t0 = time.perf_counter()
    s_res = sc.query_vectors(
        vectorBucketName=S3V_BUCKET_NAME,
        indexName=S3V_INDEX_NAME,
        queryVector={"float32": qvec},
        topK=5,
        filter={"language": {"$ne": "English"}},
        returnDistance=True,
        returnMetadata=True,
    )
    s_ms = (time.perf_counter() - t0) * 1000

    print(f"\nQdrant ({q_ms:.0f}ms):")
    for p in q_res.points:
        print(
            f"  {p.payload['title']} — language={p.payload['language']}, score={p.score:.4f}"
        )

    print(f"\nS3 Vectors ({s_ms:.0f}ms):")
    for v in s_res["vectors"]:
        m = v["metadata"]
        print(f"  {m['title']} — language={m['language']}, score={v['distance']:.4f}")


if __name__ == "__main__":
    run()
