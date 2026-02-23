"""Test 08: Insert Vectors (batch) — Both platforms."""

import time

from qdrant_client import QdrantClient, models

from core.config import (
    AWS_REGION,
    EMBEDDING_DIM,
    QDRANT_COLLECTION,
    QDRANT_URL,
    S3V_BUCKET_NAME,
    S3V_INDEX_NAME,
    qdrant_id,
)
from core.dataset import MOVIES
from core.embeddings import generate_movie_embeddings


def run():
    embeddings = generate_movie_embeddings(MOVIES)

    print("=" * 60)
    print("TEST 08: Insert Vectors (batch) — Compare speed & approach")
    print("=" * 60)

    # ── Qdrant ────────────────────────────────────────────────
    qc = QdrantClient(url=QDRANT_URL)
    qc.recreate_collection(
        QDRANT_COLLECTION,
        vectors_config=models.VectorParams(
            size=EMBEDDING_DIM, distance=models.Distance.COSINE
        ),
    )

    points = [
        models.PointStruct(
            id=qdrant_id(m["id"]),
            vector=embeddings[m["id"]],
            payload={
                k: m[k]
                for k in ["title", "genre", "year", "rating", "director", "language"]
            },
        )
        for m in MOVIES
    ]

    t0 = time.perf_counter()
    qc.upsert(QDRANT_COLLECTION, points)
    q_ms = (time.perf_counter() - t0) * 1000

    print(f"\nQdrant: Inserted {len(points)} vectors in {q_ms:.0f}ms")
    print(f"  Method: upsert() — no hard batch limit")
    print(f"  Supports: upsert (insert or update), flexible batch size")

    # ── S3 Vectors ────────────────────────────────────────────
    import boto3

    sc = boto3.client("s3vectors", region_name=AWS_REGION)
    try:
        sc.create_vector_bucket(vectorBucketName=S3V_BUCKET_NAME)
    except:
        pass
    try:
        sc.create_vector_index(
            vectorBucketName=S3V_BUCKET_NAME,
            indexName=S3V_INDEX_NAME,
            dimension=EMBEDDING_DIM,
            distanceMetric="cosine",
        )
    except:
        pass

    vectors = [
        {
            "key": m["id"],
            "data": {"float32": embeddings[m["id"]]},
            "metadata": {
                k: m[k]
                for k in ["title", "genre", "year", "rating", "director", "language"]
            },
        }
        for m in MOVIES
    ]

    t0 = time.perf_counter()
    sc.put_vectors(
        vectorBucketName=S3V_BUCKET_NAME, indexName=S3V_INDEX_NAME, vectors=vectors
    )
    s_ms = (time.perf_counter() - t0) * 1000

    print(f"\nS3 Vectors: Inserted {len(vectors)} vectors in {s_ms:.0f}ms")
    print(f"  Method: put_vectors() — max 500 per call")
    print(f"  Limit: 1,000 combined put+delete RPS per index")

    print(f"\n→ Speed: Qdrant {q_ms:.0f}ms vs S3 Vectors {s_ms:.0f}ms")


if __name__ == "__main__":
    run()
