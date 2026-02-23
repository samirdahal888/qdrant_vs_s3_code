"""Test 01: Semantic Search (top-K cosine) — Both platforms."""

import time

from core.clients import get_clients
from core.config import QDRANT_COLLECTION, S3V_BUCKET_NAME, S3V_INDEX_NAME
from core.embeddings import generate_query_embedding

QUERIES = [
    "space exploration and adventure movies",
    "romantic stories about love",
    "crime and gangster films",
]


def run():
    qc, sc = get_clients()

    print("=" * 60)
    print("TEST 01: Semantic Search (top-5, cosine similarity)")
    print("=" * 60)

    for query in QUERIES:
        qvec = generate_query_embedding(query)
        print(f'\nQuery: "{query}"')
        print(f"{'#':<3} {'Qdrant':<35} {'Score':<8} {'S3 Vectors':<35} {'Score':<8}")
        print("-" * 90)

        # Qdrant search
        t0 = time.perf_counter()
        q_res = qc.query_points(
            QDRANT_COLLECTION, query=qvec, limit=5, with_payload=True
        )
        q_ms = (time.perf_counter() - t0) * 1000

        # S3 Vectors search
        t0 = time.perf_counter()
        s_res = sc.query_vectors(
            vectorBucketName=S3V_BUCKET_NAME,
            indexName=S3V_INDEX_NAME,
            queryVector={"float32": qvec},
            topK=5,
            returnDistance=True,
            returnMetadata=True,
        )
        s_ms = (time.perf_counter() - t0) * 1000

        q_hits = [(p.payload["title"], p.score) for p in q_res.points]
        s_hits = [(v["metadata"]["title"], v["distance"]) for v in s_res["vectors"]]

        for i in range(max(len(q_hits), len(s_hits))):
            qt = f"{q_hits[i][0]}" if i < len(q_hits) else "—"
            qs = f"{q_hits[i][1]:.4f}" if i < len(q_hits) else ""
            st = f"{s_hits[i][0]}" if i < len(s_hits) else "—"
            ss = f"{s_hits[i][1]:.4f}" if i < len(s_hits) else ""
            print(f"{i + 1:<3} {qt:<35} {qs:<8} {st:<35} {ss:<8}")

        print(f"    Qdrant: {q_ms:.0f}ms | S3 Vectors: {s_ms:.0f}ms")


if __name__ == "__main__":
    run()
