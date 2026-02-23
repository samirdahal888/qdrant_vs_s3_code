"""Test 10: Update Metadata — Both platforms."""

import time

from core.clients import get_clients
from core.config import QDRANT_COLLECTION, S3V_BUCKET_NAME, S3V_INDEX_NAME, qdrant_id
from core.dataset import MOVIES
from core.embeddings import generate_movie_embeddings


def run():
    qc, sc = get_clients()
    embeddings = generate_movie_embeddings(MOVIES)

    print("=" * 60)
    print("TEST 10: Update Metadata (change rating of Shawshank Redemption)")
    print("=" * 60)

    target_id = "mov_05"
    original = next(m for m in MOVIES if m["id"] == target_id)
    new_rating = 9.5
    print(f"\n  Movie: {original['title']}")
    print(f"  Original rating: {original['rating']} → New rating: {new_rating}")

    # ── Qdrant: partial update (just the field) ───────────────
    t0 = time.perf_counter()
    qc.set_payload(
        QDRANT_COLLECTION, payload={"rating": new_rating}, points=[qdrant_id(target_id)]
    )
    q_ms = (time.perf_counter() - t0) * 1000

    q_verify = qc.retrieve(
        QDRANT_COLLECTION, ids=[qdrant_id(target_id)], with_payload=True
    )
    print(f"\nQdrant ({q_ms:.0f}ms): rating = {q_verify[0].payload['rating']}")
    print(f"  Method: set_payload() — partial update, send only changed field")

    # ── S3 Vectors: full re-put (vector + all metadata) ──────
    full_metadata = {
        k: original[k]
        for k in [
            "title",
            "description",
            "genre",
            "year",
            "rating",
            "director",
            "language",
        ]
    }
    full_metadata["rating"] = new_rating

    t0 = time.perf_counter()
    sc.put_vectors(
        vectorBucketName=S3V_BUCKET_NAME,
        indexName=S3V_INDEX_NAME,
        vectors=[
            {
                "key": target_id,
                "data": {"float32": embeddings[target_id]},
                "metadata": full_metadata,
            }
        ],
    )
    s_ms = (time.perf_counter() - t0) * 1000

    s_verify = sc.get_vectors(
        vectorBucketName=S3V_BUCKET_NAME,
        indexName=S3V_INDEX_NAME,
        keys=[target_id],
        returnMetadata=True,
    )
    s_rating = s_verify["vectors"][0]["metadata"]["rating"]
    print(f"\nS3 Vectors ({s_ms:.0f}ms): rating = {s_rating}")
    print(f"  Method: put_vectors() — must re-send vector + ALL metadata")

    print(f"\n→ Key difference:")
    print(f"  Qdrant: partial update — just send the field you want to change")
    print(f"  S3 Vectors: no patch API — must re-put entire vector + metadata")


if __name__ == "__main__":
    run()
