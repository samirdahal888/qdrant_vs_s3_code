"""Test 16: Geo Filtering — Qdrant only (demo with synthetic data)."""

import time

from qdrant_client import QdrantClient, models

from core.config import EMBEDDING_DIM, QDRANT_URL, qdrant_id
from core.embeddings import generate_query_embedding

COLLECTION = "movies_geo"  # Separate collection — don't touch shared 'movies'

# Synthetic: movies with filming locations
MOVIES_WITH_LOCATION = [
    {"id": "geo_01", "title": "Inception (Paris)", "lat": 48.8566, "lon": 2.3522},
    {"id": "geo_02", "title": "Amélie (Montmartre)", "lat": 48.8867, "lon": 2.3431},
    {"id": "geo_03", "title": "Dark Knight (Chicago)", "lat": 41.8781, "lon": -87.6298},
    {
        "id": "geo_04",
        "title": "Lost in Translation (Tokyo)",
        "lat": 35.6762,
        "lon": 139.6503,
    },
    {"id": "geo_05", "title": "Gladiator (Rome)", "lat": 41.9028, "lon": 12.4964},
    {
        "id": "geo_06",
        "title": "Slumdog Millionaire (Mumbai)",
        "lat": 19.0760,
        "lon": 72.8777,
    },
    {
        "id": "geo_07",
        "title": "Midnight in Paris (Paris)",
        "lat": 48.8606,
        "lon": 2.3376,
    },
]


def run():
    print("=" * 60)
    print("TEST 16: Geo Filtering — Qdrant only")
    print("=" * 60)

    qc = QdrantClient(url=QDRANT_URL)
    qc.recreate_collection(
        COLLECTION,
        vectors_config=models.VectorParams(
            size=EMBEDDING_DIM, distance=models.Distance.COSINE
        ),
    )
    qc.create_payload_index(COLLECTION, "location", models.PayloadSchemaType.GEO)

    # Insert with geo locations
    points = []
    for m in MOVIES_WITH_LOCATION:
        vec = generate_query_embedding(m["title"])
        points.append(
            models.PointStruct(
                id=qdrant_id(m["id"]),
                vector=vec,
                payload={
                    "title": m["title"],
                    "location": {"lat": m["lat"], "lon": m["lon"]},
                },
            )
        )
    qc.upsert(COLLECTION, points)

    # Search: movies filmed within 50km of Paris center
    qvec = generate_query_embedding("movies filmed in France")
    t0 = time.perf_counter()
    results = qc.query_points(
        COLLECTION,
        query=qvec,
        limit=5,
        with_payload=True,
        query_filter=models.Filter(
            must=[
                models.FieldCondition(
                    key="location",
                    geo_radius=models.GeoRadius(
                        center=models.GeoPoint(lat=48.8566, lon=2.3522),
                        radius=50000,  # 50km
                    ),
                )
            ]
        ),
    )
    ms = (time.perf_counter() - t0) * 1000

    print(f'\nSearch: "Movies within 50km of Paris" ({ms:.0f}ms):')
    for p in results.points:
        loc = p.payload["location"]
        print(f"  {p.payload['title']} — lat={loc['lat']}, lon={loc['lon']}")

    print(f"\nS3 Vectors: ❌ Not supported")
    print(f"  No geo data type, no geo_radius/geo_bounding_box filters.")
    print(f"  Location-based search is impossible in S3 Vectors.")

    # Cleanup dedicated collection
    qc.delete_collection(COLLECTION)


if __name__ == "__main__":
    run()
