# S3 Vectors vs Qdrant — 25 Comparison Tests

Side-by-side comparison of **Amazon S3 Vectors** and **Qdrant** using a Semantic Movie Search use case.

## Structure

```
├── run_all.py                          # Entry point — run all or pick tests
├── setup.py                            # Shared setup for both platforms
├── core/
│   ├── config.py                       # URLs, bucket names, model config
│   ├── dataset.py                      # 50 movies + queries + filters
│   ├── embeddings.py                   # Embedding generation with cache
│   └── display.py                      # Rich output helpers
├── tests/
│   ├── test_01_semantic_search.py      # Common: top-K cosine search
│   ├── test_02_filter_exact_match.py   # Common: genre = "Sci-Fi"
│   ├── test_03_filter_numeric_range.py # Common: year >= 2010
│   ├── test_04_filter_combined_and.py  # Common: genre + year + rating
│   ├── test_05_filter_or.py            # Common: Drama OR Comedy
│   ├── test_06_filter_negation.py      # Common: language != English
│   ├── test_07_filter_set_membership.py# Common: genre IN [...]
│   ├── test_08_insert_batch.py         # Common: batch insert speed
│   ├── test_09_get_by_id.py            # Common: retrieve by ID
│   ├── test_10_update_metadata.py      # Common: partial vs full re-put
│   ├── test_11_delete.py               # Common: delete vectors
│   ├── test_12_hybrid_search.py        # Qdrant: dense + sparse fusion
│   ├── test_13_recommendation.py       # Qdrant: positive/negative recs
│   ├── test_14_scroll_paginate.py      # Qdrant: scroll with filter
│   ├── test_15_fulltext_match.py       # Qdrant: text search in payload
│   ├── test_16_geo_filter.py           # Qdrant: location-based search
│   ├── test_17_grouping.py             # Qdrant: group by field
│   ├── test_18_named_vectors.py        # Qdrant: multi-vector per point
│   ├── test_19_zero_setup.py           # S3: zero infrastructure
│   ├── test_20_iam_auth.py             # S3: native AWS IAM
│   ├── test_21_bedrock_integration.py  # S3: managed RAG pipeline
│   ├── test_22_topk_limit.py           # Limit: topK > 100
│   ├── test_23_consistency.py          # Limit: immediate vs eventual
│   ├── test_24_batch_limits.py         # Limit: batch size comparison
│   └── test_25_scale_constraints.py    # Limit: dimensions, RPS, etc.
├── docker-compose.yml
└── docs/                               # Reference documentation
```

## Quick Start

```bash
# Install
uv sync

# Start Qdrant
docker compose up -d

# Run all 25 tests
python run_all.py

# Run specific tests
python run_all.py 1              # Test 01 only
python run_all.py 1 2 3          # Tests 01, 02, 03
python run_all.py 12-18          # Qdrant-only tests
python run_all.py 19-21          # S3 strengths tests

# List all tests
python run_all.py --list

# Cleanup
python run_all.py --cleanup
```

## The 25 Tests

| # | Test | Platforms | Category |
|---|------|-----------|----------|
| 01 | Semantic search (top-K cosine) | Both | Common Ground |
| 02 | Filter: exact match | Both | Common Ground |
| 03 | Filter: numeric range | Both | Common Ground |
| 04 | Filter: combined AND | Both | Common Ground |
| 05 | Filter: OR logic | Both | Common Ground |
| 06 | Filter: negation | Both | Common Ground |
| 07 | Filter: set membership | Both | Common Ground |
| 08 | Insert vectors (batch) | Both | Common Ground |
| 09 | Get vectors by ID | Both | Common Ground |
| 10 | Update metadata | Both | Common Ground |
| 11 | Delete vectors | Both | Common Ground |
| 12 | Hybrid search (dense+sparse) | Qdrant only | Qdrant-Only |
| 13 | Recommendation (+/-) | Qdrant only | Qdrant-Only |
| 14 | Scroll/paginate with filter | Qdrant only | Qdrant-Only |
| 15 | Full-text match filter | Qdrant only | Qdrant-Only |
| 16 | Geo filtering | Qdrant only | Qdrant-Only |
| 17 | Grouping (group by field) | Qdrant only | Qdrant-Only |
| 18 | Named vectors (multi-vector) | Qdrant only | Qdrant-Only |
| 19 | Zero setup | S3 Vectors | S3 Strengths |
| 20 | AWS IAM native auth | S3 Vectors | S3 Strengths |
| 21 | Bedrock KB integration | S3 Vectors | S3 Strengths |
| 22 | TopK > 100 | Both | Limits |
| 23 | Consistency | Both | Limits |
| 24 | Batch size limits | Info | Limits |
| 25 | Scale constraints | Info | Limits |
