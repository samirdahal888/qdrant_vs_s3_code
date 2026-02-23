"""Test 14: Scroll/Paginate with Filters — Qdrant only."""

import time

from qdrant_client import models

from core.clients import get_qdrant
from core.config import QDRANT_COLLECTION


def run():
    qc = get_qdrant()

    print("=" * 60)
    print("TEST 14: Scroll/Paginate with Filter — Qdrant only")
    print("=" * 60)
    print("  Browse all Sci-Fi movies WITHOUT a query vector")
    print("  (filter-only retrieval, paginated)")

    # Page 1
    t0 = time.perf_counter()
    page1, next_offset = qc.scroll(
        QDRANT_COLLECTION,
        scroll_filter=models.Filter(
            must=[
                models.FieldCondition(
                    key="genre", match=models.MatchValue(value="Sci-Fi")
                )
            ]
        ),
        limit=5,
        with_payload=True,
    )
    ms1 = (time.perf_counter() - t0) * 1000

    print(f"\nPage 1 ({ms1:.0f}ms) — {len(page1)} results:")
    for p in page1:
        print(f"  {p.payload['title']} ({p.payload['year']})")

    # Page 2 (if more exist)
    if next_offset:
        t0 = time.perf_counter()
        page2, _ = qc.scroll(
            QDRANT_COLLECTION,
            scroll_filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="genre", match=models.MatchValue(value="Sci-Fi")
                    )
                ]
            ),
            limit=5,
            offset=next_offset,
            with_payload=True,
        )
        ms2 = (time.perf_counter() - t0) * 1000
        print(f"\nPage 2 ({ms2:.0f}ms) — {len(page2)} results:")
        for p in page2:
            print(f"  {p.payload['title']} ({p.payload['year']})")

    print(f"\nS3 Vectors: ❌ Not supported")
    print(f"  ListVectors exists but cannot apply filters.")
    print(f"  QueryVectors requires a query vector — no browse/scroll.")


if __name__ == "__main__":
    run()
