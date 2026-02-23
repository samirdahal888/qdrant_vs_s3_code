"""Test 15: Full-Text Match Filter — Qdrant only."""

import time

from qdrant_client import models

from core.clients import get_qdrant
from core.config import QDRANT_COLLECTION
from core.embeddings import generate_query_embedding


def run():
    qc = get_qdrant()

    print("=" * 60)
    print("TEST 15: Full-Text Match Filter — Qdrant only")
    print("=" * 60)

    # Create text index on description field
    qc.create_payload_index(
        QDRANT_COLLECTION,
        field_name="description",
        field_schema=models.TextIndexParams(
            type=models.TextIndexType.TEXT,
            tokenizer=models.TokenizerType.WORD,
            min_token_len=2,
            max_token_len=20,
        ),
    )

    qvec = generate_query_embedding("interesting movies")

    searches = ["robot", "war", "love"]
    for keyword in searches:
        t0 = time.perf_counter()
        results = qc.query_points(
            QDRANT_COLLECTION,
            query=qvec,
            limit=5,
            with_payload=True,
            query_filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="description", match=models.MatchText(text=keyword)
                    )
                ]
            ),
        )
        ms = (time.perf_counter() - t0) * 1000

        print(f'\nKeyword: "{keyword}" ({ms:.0f}ms):')
        for p in results.points:
            print(f"  {p.payload['title']} — ...{keyword}... in description")

    print(f"\nS3 Vectors: ❌ Not supported")
    print(f"  Metadata filters work on structured fields only (genre, year, etc.).")
    print(f"  No full-text search on content/description fields.")


if __name__ == "__main__":
    run()
