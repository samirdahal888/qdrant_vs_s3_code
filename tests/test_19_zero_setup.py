"""Test 19: Zero Setup (no Docker/server) — S3 Vectors strength."""


def run():
    print("=" * 60)
    print("TEST 19: Zero Infrastructure Setup — S3 Vectors strength")
    print("=" * 60)

    print("""
┌─────────────────────────────────────────────────────────────┐
│                    QDRANT SETUP                             │
├─────────────────────────────────────────────────────────────┤
│  1. Install Docker                                          │
│  2. Write docker-compose.yml:                               │
│       services:                                             │
│         qdrant:                                             │
│           image: qdrant/qdrant:latest                       │
│           ports: ["6333:6333", "6334:6334"]                 │
│           volumes: [./qdrant_storage:/qdrant/storage]       │
│  3. Run: docker compose up -d                               │
│  4. Wait for container to start                             │
│  5. Monitor health: docker ps / docker logs                 │
│  6. Manage storage volumes & backups yourself               │
│  7. Handle scaling: replicas, sharding, load balancing      │
│  8. Configure TLS for production                            │
│  9. Set up API key authentication                           │
│                                                             │
│  → You own ALL the infrastructure.                          │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                  S3 VECTORS SETUP                           │
├─────────────────────────────────────────────────────────────┤
│  1. pip install boto3                                       │
│  2. Two API calls:                                          │
│       client = boto3.client("s3vectors")                    │
│       client.create_vector_bucket(name="my-bucket")         │
│       client.create_vector_index(name="my-index", dim=384)  │
│  3. Done. AWS manages everything.                           │
│                                                             │
│  → Zero Docker, zero servers, zero scaling config.          │
│  → AWS handles storage, availability, scaling.              │
└─────────────────────────────────────────────────────────────┘
""")

    # Actually demonstrate: create a bucket + index in code
    import time

    import boto3

    from core.config import AWS_REGION

    demo_bucket = "demo-zero-setup"
    demo_index = "demo-index"
    sc = boto3.client("s3vectors", region_name=AWS_REGION)

    t0 = time.perf_counter()
    try:
        sc.create_vector_bucket(vectorBucketName=demo_bucket)
    except:
        pass
    try:
        sc.create_vector_index(
            vectorBucketName=demo_bucket,
            indexName=demo_index,
            dimension=384,
            distanceMetric="cosine",
        )
    except:
        pass
    ms = (time.perf_counter() - t0) * 1000

    print(f"  S3 Vectors: Created bucket + index in {ms:.0f}ms")
    print(f"  No Docker needed. No server to manage.\n")

    # Cleanup demo
    try:
        sc.delete_vector_index(vectorBucketName=demo_bucket, indexName=demo_index)
    except:
        pass
    try:
        sc.delete_vector_bucket(vectorBucketName=demo_bucket)
    except:
        pass


if __name__ == "__main__":
    run()
