"""Test 13: Recommendation (like A, not like B) — Qdrant only."""

import time

from qdrant_client import models

from core.clients import get_qdrant
from core.config import QDRANT_COLLECTION, qdrant_id


def run():
    qc = get_qdrant()

    print("=" * 60)
    print("TEST 13: Recommendation API — Qdrant only")
    print("=" * 60)

    # Test 1: Movies like Inception
    print('\n--- "Movies similar to Inception" ---')
    t0 = time.perf_counter()
    results = qc.query_points(
        collection_name=QDRANT_COLLECTION,
        query=models.RecommendQuery(
            recommend=models.RecommendInput(
                positive=[qdrant_id("mov_01")],  # Inception
                negative=[],
                strategy=models.RecommendStrategy.AVERAGE_VECTOR,
            )
        ),
        limit=5,
        with_payload=True,
    )
    ms = (time.perf_counter() - t0) * 1000

    print(f"Qdrant ({ms:.0f}ms):")
    for i, r in enumerate(results.points):
        print(
            f"  {i + 1}. {r.payload['title']} ({r.payload['genre']}, {r.payload['year']}) score={r.score:.4f}"
        )

    # Test 2: Like Interstellar + Matrix, NOT like Forrest Gump
    print('\n--- "Like Interstellar + Matrix, NOT like Forrest Gump" ---')
    t0 = time.perf_counter()
    results = qc.query_points(
        collection_name=QDRANT_COLLECTION,
        query=models.RecommendQuery(
            recommend=models.RecommendInput(
                positive=[
                    qdrant_id("mov_02"),
                    qdrant_id("mov_03"),
                ],  # Interstellar, The Matrix
                negative=[qdrant_id("mov_08")],  # Not like Forrest Gump
                strategy=models.RecommendStrategy.AVERAGE_VECTOR,
            )
        ),
        using='dense',
        limit=5,
        with_payload=True,
    )
    ms = (time.perf_counter() - t0) * 1000

    print(f"Qdrant ({ms:.0f}ms):")
    for i, r in enumerate(results.points):
        print(
            f"  {i + 1}. {r.payload['title']} ({r.payload['genre']}, {r.payload['year']}) score={r.score:.4f}"
        )

    print(f"\nS3 Vectors: ❌ Not supported")
    print(f"  No recommendation API. You'd need to fetch the embedding,")
    print(f"  compute an average, and query manually — no negative examples possible.")


if __name__ == "__main__":
    run()
