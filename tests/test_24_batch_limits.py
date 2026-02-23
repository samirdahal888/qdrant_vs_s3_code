"""Test 24: Batch Size Limits."""


def run():
    print("=" * 60)
    print("TEST 24: Batch Size Limits")
    print("=" * 60)

    print("""
┌──────────────────────┬─────────────────┬──────────────────────┐
│ Operation            │ Qdrant          │ S3 Vectors           │
├──────────────────────┼─────────────────┼──────────────────────┤
│ Insert batch size    │ No hard limit   │ Max 500 per call     │
│ Delete batch size    │ No hard limit   │ Max 500 per call     │
│ Get by ID batch      │ No hard limit   │ Max 100 per call     │
│ Write RPS per index  │ No hard limit*  │ Max 1,000 RPS        │
│ Vectors/sec insert   │ No hard limit*  │ Max 2,500/sec        │
│ Request payload      │ No hard limit   │ Max 20 MiB           │
├──────────────────────┼─────────────────┼──────────────────────┤
│ * Qdrant is limited  │ by hardware     │ by AWS service quota │
│   (CPU, RAM, disk)   │                 │                      │
└──────────────────────┴─────────────────┴──────────────────────┘

Example: inserting 10,000 vectors
  Qdrant:     1 call  (or split into chunks for memory)
  S3 Vectors: 20 calls (10,000 / 500 = 20 batches)
              + must respect 1,000 RPS / 2,500 vectors-per-sec limits

For our 50-movie dataset: both handle it in a single call.
At scale, S3 Vectors requires pagination and rate limiting.
""")


if __name__ == "__main__":
    run()
