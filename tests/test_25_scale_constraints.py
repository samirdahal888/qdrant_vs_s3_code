"""Test 25: Scale Constraints — RPS and dimension limits."""


def run():
    print("=" * 60)
    print("TEST 25: Scale Constraints")
    print("=" * 60)

    print("""
┌──────────────────────────┬──────────────────┬───────────────────┐
│ Constraint               │ Qdrant           │ S3 Vectors        │
├──────────────────────────┼──────────────────┼───────────────────┤
│ Max vectors per index    │ Billions*        │ 2 billion         │
│ Max dimensions           │ No hard limit    │ 4,096             │
│ Vector data types        │ float32/16/8/1   │ float32 only      │
│ Distance metrics         │ Cosine/Euclid/Dot│ Cosine/Euclidean  │
│ TopK per query           │ Unlimited*       │ 100 max           │
│ RPS per index            │ Hardware-bound   │ 1,000 combined    │
│ Metadata per vector      │ No strict limit  │ 40KB total        │
│ Filterable metadata      │ No strict limit  │ 2KB max           │
│ Non-filterable keys      │ N/A              │ 10 per index      │
│ Indexes per bucket       │ N/A              │ 10,000            │
│ Buckets per region       │ N/A              │ 10,000            │
│ Query consistency        │ Immediate        │ Eventual           │
│ Latency (cold)           │ Depends on HNSW  │ Sub-second         │
│ Latency (warm)           │ ~1-10ms          │ ~100ms             │
│ Recall                   │ 99%+ (tunable)   │ 90%+ (fixed)      │
├──────────────────────────┼──────────────────┼───────────────────┤
│ * Limited by server      │ hardware, not    │ service quota      │
│   software               │                  │                    │
└──────────────────────────┴──────────────────┴───────────────────┘

Key takeaways:
  • Qdrant gives you more control and fewer hard limits
  • S3 Vectors has fixed service quotas but zero ops burden
  • S3 Vectors recall is 90%+ (not tunable) vs Qdrant's HNSW tuning
  • S3 Vectors warm latency (~100ms) vs Qdrant (~1-10ms)
  • Choose based on your accuracy/latency/ops requirements
""")


if __name__ == "__main__":
    run()
