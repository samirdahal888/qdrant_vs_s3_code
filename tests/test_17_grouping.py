"""Test 17: Group By — Qdrant only."""

import time

from core.clients import get_qdrant
from core.config import QDRANT_COLLECTION
from core.embeddings import generate_query_embedding


def run():
    qc = get_qdrant()

    print("=" * 60)
    print("TEST 17: Grouping (group by genre, 1 best per genre) — Qdrant only")
    print("=" * 60)

    qvec = generate_query_embedding("great movies of all time")

    t0 = time.perf_counter()
    results = qc.query_points_groups(
        QDRANT_COLLECTION,
        query=qvec,
        group_by="genre",
        group_size=1,
        limit=10,
        with_payload=True,
    )
    ms = (time.perf_counter() - t0) * 1000

    print(f"\nTop movie per genre ({ms:.0f}ms):")
    for group in results.groups:
        genre = group.id
        for hit in group.hits:
            print(f"  [{genre}] {hit.payload['title']} (score={hit.score:.4f})")

    print(f"\nS3 Vectors: ❌ Not supported")
    print(f"  No group_by in QueryVectors API.")
    print(f"  You'd have to fetch all results and group client-side.")


if __name__ == "__main__":
    run()
