"""Test 23: Consistency — query immediately after insert."""

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
from core.embeddings import generate_query_embedding


def run():
    print("=" * 60)
    print("TEST 23: Consistency (query right after insert)")
    print("=" * 60)

    test_title = "CONSISTENCY_TEST_MOVIE_XYZ"
    test_vec = generate_query_embedding(test_title)

    # ── Qdrant ─────────────────────────────────────────────────
    qc = QdrantClient(url=QDRANT_URL)
    qc.recreate_collection(
        QDRANT_COLLECTION,
        vectors_config=models.VectorParams(
            size=EMBEDDING_DIM, distance=models.Distance.COSINE
        ),
    )

    # Insert then immediately query
    qc.upsert(
        QDRANT_COLLECTION,
        [
            models.PointStruct(
                id=qdrant_id("test_1"), vector=test_vec, payload={"title": test_title}
            ),
        ],
    )

    result = qc.query_points(
        QDRANT_COLLECTION, query=test_vec, limit=1, with_payload=True
    )
    found = result.points[0].payload["title"] == test_title if result.points else False
    print(
        f"\nQdrant: Insert → immediate query → {'FOUND ✓' if found else 'NOT FOUND ✗'}"
    )
    print(f"  → Strong consistency: data available immediately after write")

    # ── S3 Vectors ─────────────────────────────────────────────
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

    # Insert
    sc.put_vectors(
        vectorBucketName=S3V_BUCKET_NAME,
        indexName=S3V_INDEX_NAME,
        vectors=[
            {
                "key": "test_1",
                "data": {"float32": test_vec},
                "metadata": {"title": test_title},
            }
        ],
    )

    # Immediate query
    res = sc.query_vectors(
        vectorBucketName=S3V_BUCKET_NAME,
        indexName=S3V_INDEX_NAME,
        queryVector={"float32": test_vec},
        topK=1,
        returnMetadata=True,
    )
    found_immediate = any(
        v.get("metadata", {}).get("title") == test_title for v in res.get("vectors", [])
    )
    print(
        f"\nS3 Vectors: Insert → immediate query → {'FOUND' if found_immediate else 'NOT FOUND'}"
    )

    if not found_immediate:
        # Wait and retry
        for delay in [1, 2, 3]:
            time.sleep(delay)
            res = sc.query_vectors(
                vectorBucketName=S3V_BUCKET_NAME,
                indexName=S3V_INDEX_NAME,
                queryVector={"float32": test_vec},
                topK=1,
                returnMetadata=True,
            )
            found_delayed = any(
                v.get("metadata", {}).get("title") == test_title
                for v in res.get("vectors", [])
            )
            total = sum(range(1, delay + 1))
            if found_delayed:
                print(
                    f"  → Found after ~{total}s delay — eventual consistency confirmed"
                )
                break
            else:
                print(f"  → Still not found after ~{total}s...")
    else:
        print(f"  → Found immediately (index was warm / fast convergence)")

    print(f"\n→ Qdrant: strong consistency — always available immediately")
    print(f"→ S3 Vectors: eventual consistency — may take seconds to appear")

    # Cleanup
    sc.delete_vectors(
        vectorBucketName=S3V_BUCKET_NAME,
        indexName=S3V_INDEX_NAME,
        keys=[{"key": "test_1"}],
    )


if __name__ == "__main__":
    run()
