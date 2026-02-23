"""Test 12: Hybrid Search (dense + sparse) — Qdrant only."""

import time

from qdrant_client import QdrantClient, models

from core.config import EMBEDDING_DIM, QDRANT_COLLECTION, QDRANT_URL, qdrant_id
from core.dataset import MOVIES
from core.embeddings import generate_movie_embeddings, generate_query_embedding


def run():
    print("=" * 60)
    print("TEST 12: Hybrid Search (dense + sparse vectors) — Qdrant only")
    print("=" * 60)

    qc = QdrantClient(url=QDRANT_URL)
    embeddings = generate_movie_embeddings(MOVIES)

    # Create collection with BOTH dense and sparse vectors
    qc.recreate_collection(
        QDRANT_COLLECTION,
        vectors_config={
            "dense": models.VectorParams(
                size=EMBEDDING_DIM, distance=models.Distance.COSINE
            )
        },
        sparse_vectors_config={"sparse": models.SparseVectorParams()},
    )

    # Build simple sparse vectors from keywords (bag-of-words style)
    def make_sparse(text: str) -> tuple[list[int], list[float]]:
        words = set(text.lower().split())
        indices = [hash(w) % 10000 for w in words]
        values = [1.0] * len(indices)
        return indices, values

    # Insert with both vector types
    points = []
    for m in MOVIES:
        text = f"{m['title']} {m['description']} {m['genre']}"
        indices, values = make_sparse(text)
        points.append(
            models.PointStruct(
                id=qdrant_id(m["id"]),
                vector={
                    "dense": embeddings[m["id"]],
                    "sparse": models.SparseVector(indices=indices, values=values),
                },
                payload={"title": m["title"], "genre": m["genre"], "year": m["year"]},
            )
        )
    qc.upsert(QDRANT_COLLECTION, points)

    # Hybrid query: combine dense (semantic) + sparse (keyword)
    query_text = "space robots adventure"
    dense_vec = generate_query_embedding(query_text)
    sparse_idx, sparse_val = make_sparse(query_text)

    t0 = time.perf_counter()
    results = qc.query_points(
        QDRANT_COLLECTION,
        prefetch=[
            models.Prefetch(query=dense_vec, using="dense", limit=10),
            models.Prefetch(
                query=models.SparseVector(indices=sparse_idx, values=sparse_val),
                using="sparse",
                limit=10,
            ),
        ],
        query=models.FusionQuery(fusion=models.Fusion.RRF),  # Reciprocal Rank Fusion
        limit=5,
        with_payload=True,
    )
    ms = (time.perf_counter() - t0) * 1000

    print(f'\nQuery: "{query_text}"')
    print(f"Qdrant Hybrid Search — RRF Fusion ({ms:.0f}ms):")
    for i, p in enumerate(results.points):
        print(
            f"  {i + 1}. {p.payload['title']} (genre={p.payload['genre']}, score={p.score:.4f})"
        )

    print(f"\nS3 Vectors: ❌ Not supported")
    print(f"  S3 Vectors only supports dense (float32) vectors.")
    print(f"  No sparse vectors, no hybrid search, no fusion.")


if __name__ == "__main__":
    run()
