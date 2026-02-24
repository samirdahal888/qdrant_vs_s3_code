"""Test 18: Named Vectors (multi-vector per point) — Qdrant only."""

import time

from qdrant_client import QdrantClient, models

from core.config import EMBEDDING_DIM, QDRANT_URL, qdrant_id
from core.dataset import MOVIES
from core.embeddings import generate_query_embedding, get_model

COLLECTION = "movies_named"  # Separate collection — don't touch shared 'movies'


def run():
    print("=" * 60)
    print("TEST 18: Named Vectors (title + description embeddings) — Qdrant only")
    print("=" * 60)

    qc = QdrantClient(url=QDRANT_URL)
    model = get_model()

    # Collection with TWO named vectors per point
    qc.recreate_collection(
        COLLECTION,
        vectors_config={
            "title": models.VectorParams(
                size=EMBEDDING_DIM, distance=models.Distance.COSINE
            ),
            "description": models.VectorParams(
                size=EMBEDDING_DIM, distance=models.Distance.COSINE
            ),
        },
    )

    # Insert with separate embeddings for title and description
    points = []
    for m in MOVIES[:20]:  # use 20 for speed
        title_vec = model.encode(m["title"], normalize_embeddings=True).tolist()
        desc_vec = model.encode(m["description"], normalize_embeddings=True).tolist()
        points.append(
            models.PointStruct(
                id=qdrant_id(m["id"]),
                vector={"title": title_vec, "description": desc_vec},
                payload={"title": m["title"], "genre": m["genre"]},
            )
        )
    qc.upsert(COLLECTION, points)
    print(f"  Inserted {len(points)} movies with 2 vectors each (title + description)")

    # Search by title similarity
    query = "The Matrix"
    qvec = generate_query_embedding(query)

    print(f'\nSearch by TITLE vector: "{query}"')
    t0 = time.perf_counter()
    title_results = qc.query_points(
        COLLECTION,
        query=qvec,
        using="title",
        limit=5,
        with_payload=True,
    )
    ms = (time.perf_counter() - t0) * 1000
    for p in title_results.points:
        print(f"  {p.payload['title']} (score={p.score:.4f})")
    print(f"  ({ms:.0f}ms)")

    # Search by description similarity
    desc_query = "a computer hacker discovers reality is simulated"
    desc_vec = generate_query_embedding(desc_query)

    print(f'\nSearch by DESCRIPTION vector: "{desc_query}"')
    t0 = time.perf_counter()
    desc_results = qc.query_points(
        COLLECTION,
        query=desc_vec,
        using="description",
        limit=5,
        with_payload=True,
    )
    ms = (time.perf_counter() - t0) * 1000
    for p in desc_results.points:
        print(f"  {p.payload['title']} (score={p.score:.4f})")
    print(f"  ({ms:.0f}ms)")

    print(f"\nS3 Vectors:  Not supported")
    print(f"  One vector per key. To search by title AND description,")
    print(f"  you'd need two separate indexes.")

    # Cleanup dedicated collection
    qc.delete_collection(COLLECTION)


if __name__ == "__main__":
    run()
