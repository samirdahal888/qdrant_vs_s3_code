"""
Test 01: Semantic Search (top-K cosine) — Qdrant vs S3 Vectors
"""

import time
from typing import List, Tuple

from core.clients import get_clients
from core.config import QDRANT_COLLECTION, S3V_BUCKET_NAME, S3V_INDEX_NAME
from core.embeddings import generate_query_embedding

TOP_K = 5

QUERIES = [
    "space exploration and adventure movies",
    "romantic stories about love",
    "crime and gangster films",
]


def search_qdrant(
    client, query_vector: List[float]
) -> Tuple[List[Tuple[str, float]], float]:
    start = time.perf_counter()

    response = client.query_points(
        collection_name=QDRANT_COLLECTION,
        query=query_vector,
        limit=TOP_K,
        with_payload=True,
    )

    duration_ms = (time.perf_counter() - start) * 1000

    hits = [(point.payload["title"], point.score) for point in response.points]
    return hits, duration_ms


def search_s3_vectors(
    client, query_vector: List[float]
) -> Tuple[List[Tuple[str, float]], float]:
    start = time.perf_counter()

    response = client.query_vectors(
        vectorBucketName=S3V_BUCKET_NAME,
        indexName=S3V_INDEX_NAME,
        queryVector={"float32": query_vector},
        topK=TOP_K,
        returnDistance=True,
        returnMetadata=True,
    )

    duration_ms = (time.perf_counter() - start) * 1000

    hits = [
        (vector["metadata"]["title"], vector["distance"])
        for vector in response["vectors"]
    ]

    return hits, duration_ms


def print_header(query: str) -> None:
    print(f'\nQuery: "{query}"')
    print(f"{'#':<3} {'Qdrant':<35} {'Score':<8} {'S3 Vectors':<35} {'Score':<8}")
    print("-" * 90)


def print_results(q_hits, s_hits, q_ms, s_ms) -> None:
    max_len = max(len(q_hits), len(s_hits))

    for i in range(max_len):
        qt = q_hits[i][0] if i < len(q_hits) else "—"
        qs = f"{q_hits[i][1]:.4f}" if i < len(q_hits) else ""
        st = s_hits[i][0] if i < len(s_hits) else "—"
        ss = f"{s_hits[i][1]:.4f}" if i < len(s_hits) else ""

        print(f"{i + 1:<3} {qt:<35} {qs:<8} {st:<35} {ss:<8}")

    print(f"    Qdrant: {q_ms:.0f}ms | S3 Vectors: {s_ms:.0f}ms")


#
def run() -> None:
    qdrant_client, s3Vector_client = get_clients()

    print("=" * 60)
    print("TEST 01: Semantic Search (top-K, cosine similarity)")
    print("=" * 60)

    for query in QUERIES:
        query_vector = generate_query_embedding(query)

        print_header(query)

        q_hits, q_time = search_qdrant(qdrant_client, query_vector)
        s_hits, s_time = search_s3_vectors(s3Vector_client, query_vector)

        print_results(q_hits, s_hits, q_time, s_time)


if __name__ == "__main__":
    run()
