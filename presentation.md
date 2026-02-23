# Qdrant vs Amazon S3 Vectors
### A Hands-On Comparison of Two Vector Database Approaches

**Presented by:** Samir Dahal  
**Date:** February 2026

---

## Slide 1: What Problem Are We Solving?

Traditional databases search by **exact match**:
```sql
SELECT * FROM products WHERE category = 'shoes'
```

But modern AI needs **search by meaning**:
> "Find me comfortable running shoes" → should return "Nike Air Max"  
> even though the word "comfortable" never appears in the product data.

**Vector databases solve this.** They convert data into numbers (embeddings), then find items with similar numbers.

---

## Slide 2: How Does It Work?a

```
┌──────────────┐     ┌──────────────┐     ┌──────────────────┐
│  Your Data   │     │  AI Model    │     │  Vector Database  │
│              │────▶│ (Embedding   │────▶│                  │
│ "A sci-fi    │     │  Model)      │     │ [0.12, -0.45,    │
│  movie about │     │              │     │  0.78, 0.33, ... ]│
│  space"      │     │              │     │  (384 numbers)   │
└──────────────┘     └──────────────┘     └──────────────────┘
```

**Three simple steps:**
1. **Store:** Convert your data into vectors (numbers) using an AI model and store them
2. **Query:** Convert your search query into a vector using the same AI model
3. **Match:** The database finds stored vectors closest to your query vector

**Similar meaning = similar numbers = found by the database.**

---

## Slide 3: Why Does This Matter?

| Use Case | How Vector Databases Help |
|----------|--------------------------|
| **Semantic Search** | "budget-friendly laptops" finds "affordable notebooks" |
| **RAG (for LLMs)** | Feed relevant documents to ChatGPT-like systems for accurate answers |
| **Recommendations** | "Users who liked Movie A also liked..." — without manual rules |
| **Image Search** | Upload a photo → find visually similar products |
| **Anomaly Detection** | Find data points that are "far away" from normal patterns |

**Every major AI application today relies on vectors.**

---

## Slide 4: The Two Candidates

We evaluated two fundamentally different approaches:

```
┌─────────────────────────┐          ┌─────────────────────────┐
│        QDRANT            │          │    AMAZON S3 VECTORS     │
│                          │          │                          │
│  Purpose-built vector    │          │  S3 storage extended     │
│  database (open source)  │          │  with vector search      │
│                          │          │  (AWS serverless)        │
│  Think: Sports Car       │          │  Think: Cargo Ship       │
│  ● Fast (10–50 ms)      │          │  ● Massive scale (2B)    │
│  ● Feature-rich          │          │  ● Cheapest storage      │
│  ● Full control          │          │  ● Zero operations       │
│                          │          │                          │
│  Since: 2021 (mature)    │          │  Since: Dec 2025 (new)   │
│  License: Apache 2.0     │          │  License: Proprietary    │
└─────────────────────────┘          └─────────────────────────┘
```

---

## Slide 5: What We Built

A **hands-on testing framework** that runs the same operations on both platforms side-by-side.

**Setup:**
- 50 movies (title, description, genre, year, rating, director, language)
- Embedding model: `all-MiniLM-L6-v2` (384 dimensions, cosine distance)
- Qdrant: Docker container (localhost:6333)
- S3 Vectors: AWS cloud (us-east-1)

**25 tests across 4 categories:**

| Category | Tests | What We Tested |
|----------|-------|----------------|
| Common Ground (1–11) | Both platforms | Search, 6 filter types, insert, get, update, delete |
| Qdrant-Only (12–18) | Qdrant only | Hybrid search, recommendations, full-text, geo, grouping, multi-vector |
| S3 Strengths (19–21) | Informational | Zero infra, IAM auth, Bedrock integration |
| Limits (22–25) | Both | Top-K cap, consistency, batch limits, scale |

---

## Slide 6: Project Structure

```
s3_vs_qdrant/
├── core/
│   ├── clients.py       ← Lightweight client factory (Qdrant + S3)
│   ├── config.py        ← Shared constants (URLs, names, dimensions)
│   ├── dataset.py       ← 50 movies with full metadata
│   ├── embeddings.py    ← Embedding generation + disk caching
│   └── display.py       ← Rich terminal output helpers
├── tests/
│   ├── test_01 → 25     ← One file per comparison (25 total)
├── setup.py             ← Load data into both platforms (run once)
├── run_all.py           ← Run all/specific tests, save results
├── final_report.md      ← Written comparison report
└── docker-compose.yml   ← Qdrant container config
```

**Key design decisions:**
- One file per test — easy to read, easy to demo
- Clients are singletons — no data reloading between tests
- Output captured to `results/` folder automatically

---

## Slide 7: Common Ground — What Both Can Do

### Test 01: Semantic Search

Both platforms return relevant movies for the query **"space exploration and adventure"**:

```
Query: "space exploration and adventure movies"

#  Qdrant                             S3 Vectors
1  Interstellar (0.72)                Interstellar (0.72)
2  Gravity (0.61)                     Gravity (0.62)
3  The Martian (0.58)                 The Martian (0.57)
```

**Key insight:** Same results, same quality — the embedding model drives relevance, not the database.

### Tests 02–07: Metadata Filtering

Both platforms support filtering during vector search:

| Filter Type | Qdrant Syntax | S3 Vectors Syntax | Both Work? |
|-------------|---------------|-------------------|------------|
| Exact match | `MatchValue(value="Sci-Fi")` | `{"genre": "Sci-Fi"}` | Yes |
| Numeric range | `Range(gte=2010)` | `{"year": {"$gte": 2010}}` | Yes |
| Combined AND | `must=[cond1, cond2]` | `{"$and": [cond1, cond2]}` | Yes |
| OR logic | `should=[cond1, cond2]` | `{"$or": [cond1, cond2]}` | Yes |
| Negation (!=) | `must_not=[cond]` | `{"language": {"$ne": "English"}}` | Yes |
| Set membership | `should=[val1, val2]` | `{"genre": {"$in": ["Action"]}}` | Yes |

---

## Slide 8: Where Qdrant Pulls Ahead

### Test 12: Hybrid Search (Dense + Sparse Vectors)

Qdrant supports combining **semantic search** (what the text means) with **keyword matching** (exact words):

```
Query: "robot uprising"

Dense-only results:          Hybrid results (dense + sparse):
  1. The Matrix                1. I, Robot              ← keyword "robot" boosts this
  2. I, Robot                  2. The Matrix
  3. Blade Runner              3. Blade Runner
```

**S3 Vectors:** No sparse vectors, no hybrid search. Would need OpenSearch integration for this.

### Test 13: Recommendation API

Qdrant can recommend movies based on what you liked/disliked:

```python
# "Find movies like Inception and Interstellar, but NOT like Forrest Gump"
qc.query_points(
    query=models.RecommendQuery(
        recommend=models.RecommendInput(
            positive=[inception_id, interstellar_id],   # I liked these
            negative=[forrest_gump_id],                 # Not this kind
        )
    )
)
```

**S3 Vectors:** No recommendation API. You'd have to fetch vectors, average them manually, and can't handle negative examples.

### Test 18: Named Vectors (Multi-Signal Search)

Qdrant stores **multiple vectors per item** — search by title OR description independently:

```
Same movie → two embeddings:
  "title"       → [0.12, -0.45, ...]   ← captures the title's meaning
  "description" → [0.78, 0.33, ...]    ← captures the plot's meaning

Search by title:  "inception" → finds "Inception"
Search by plot:   "dream heist" → also finds "Inception"
```

**S3 Vectors:** One vector per item only. Need separate indexes for multiple embeddings.

---

## Slide 9: Where S3 Vectors Shines

### Test 19: Zero Infrastructure Setup

```
Qdrant setup (9 steps):              S3 Vectors setup (2 API calls):
─────────────────────                 ────────────────────────────────
1. Install Docker                     1. create_vector_bucket()
2. Write docker-compose.yml           2. create_index()
3. docker compose up -d                  ...done.
4. Wait for container
5. Install qdrant-client
6. Connect to localhost:6333
7. Create collection
8. Configure vector params
9. Create payload indexes
```

### Test 20: Security — IAM vs API Key

| Aspect | Qdrant | S3 Vectors |
|--------|--------|------------|
| Authentication | API key (optional, off by default) | AWS IAM (built-in) |
| Encryption at rest | Manual setup | Automatic (SSE) |
| Audit logging | None built-in | CloudTrail (automatic) |
| Network security | Manual firewall rules | VPC endpoints, PrivateLink |
| Access control | All-or-nothing API key | Fine-grained IAM policies |

### Test 21: Bedrock Integration (Managed RAG)

S3 Vectors plugs directly into Amazon Bedrock Knowledge Bases:

```
Your documents (S3) → Bedrock auto-chunks → auto-embeds → stores in S3 Vectors
                                                              ↓
User question → Bedrock retrieves relevant chunks → LLM generates answer
```

**No code needed** for the embedding + storage + retrieval pipeline.

---

## Slide 10: The Limits — Where Each Hits a Wall

### Test 22: Top-K Limit

```python
# Qdrant: no limit — works fine
qc.query_points(limit=200)    # ✅ Returns 200 results

# S3 Vectors: hard cap at 100
sc.query_vectors(topK=200)    # ❌ Error! Max is 100
```

### Test 10: Updating a Single Field

```python
# Qdrant: partial update — send only what changed
qc.set_payload(payload={"rating": 9.5}, points=[movie_id])

# S3 Vectors: must re-send EVERYTHING (vector + all metadata)
sc.put_vectors(vectors=[{
    "key": movie_id,
    "data": {"float32": full_embedding},      # Must re-send vector
    "metadata": { ... all 7 fields ... }      # Must re-send ALL metadata
}])
```

**No partial update API in S3 Vectors.**

### Full Limits Comparison

| Constraint | Qdrant | S3 Vectors |
|------------|--------|------------|
| Max vectors per index | Billions (hardware-bound) | 2 billion (hard limit) |
| Max dimensions | No hard limit | 4,096 |
| Vector data types | float32, float16, uint8, binary | float32 only |
| Distance metrics | Cosine, Euclidean, Dot Product, Manhattan | Cosine, Euclidean only |
| Top-K per query | Unlimited (hardware-bound) | 100 max |
| Write throughput | Hardware-bound | 2,500 vectors/sec |
| Metadata per vector | No strict limit | 40 KB total (2 KB filterable) |
| Metadata keys | No strict limit | 50 max |

---

## Slide 11: Performance Comparison

| Metric | Qdrant | S3 Vectors |
|--------|--------|------------|
| **Query latency (warm)** | 10–50 ms | ~100 ms |
| **Query latency (cold)** | Same as warm | 500–800 ms |
| **Recall** | 99%+ (tunable via HNSW) | 90%+ (fixed, not configurable) |
| **Insert throughput** | Hardware-bound (typically fast) | Max 2,500 vectors/sec per index |
| **Index tunability** | Full (m, ef_construct, ef_search) | None (internal, proprietary) |
| **Consistency** | Strong (immediate read-after-write) | Eventual (may miss on immediate read) |

**Key takeaway:** Qdrant is 2–10x faster for queries and gives you tuning knobs. S3 Vectors trades speed for simplicity and cost.

---

## Slide 12: Cost Comparison

### Scenario: 10 million vectors, 384 dimensions

**Qdrant (self-hosted):**
- ~15 GB RAM needed
- Cloud VM: ~$100–150/month
- Cost is **fixed** regardless of query volume

**Qdrant Cloud (managed):**
- Starting ~$25/month (small clusters)
- Scales with cluster size
- Always-on cost

**S3 Vectors (serverless):**
- Storage: ~$0.90/month (15 GB × $0.06/GB)
- Queries: $0.065 per 1M queries + $0.06 per TB scanned
- **Near-zero cost at rest** — you pay almost nothing if nobody queries

```
              Low traffic         High traffic (1M queries/day)
Qdrant:       $100/month          $100/month (same)
S3 Vectors:   ~$3/month           ~$100+/month (scales up)
```

**Crossover point:** S3 Vectors is cheaper below ~1M queries/month. Above that, Qdrant's fixed cost wins.

---

## Slide 13: The Feature Gap at a Glance

```
                            Qdrant    S3 Vectors
                            ──────    ──────────
Semantic search              ✅         ✅
Metadata filtering           ✅         ✅
Insert/Get/Delete            ✅         ✅
Batch operations             ✅         ✅
─────────────────────────────────────────────────
Hybrid search (dense+sparse) ✅         ❌
Recommendation API           ✅         ❌
Named vectors (multi-vector) ✅         ❌
Full-text search             ✅         ❌
Geo-spatial filtering        ✅         ❌
Group-by queries             ✅         ❌
Scroll/paginate (no vector)  ✅         ❌
Partial metadata update      ✅         ❌
─────────────────────────────────────────────────
Serverless (zero ops)        ❌         ✅
Bedrock KB integration       ❌         ✅
IAM/CloudTrail built-in      ❌         ✅
Pay-per-query pricing        ❌         ✅
```

---

## Slide 14: When to Use What

### Choose Qdrant When:

- You need **low latency** (<50 ms) for real-time applications
- You need **advanced features**: hybrid search, recommendations, geo-filters, multi-vector
- You want **full control** over indexing (HNSW tuning, quantization)
- You're building **complex RAG pipelines** or **AI agents** that need precision
- Your team can manage infrastructure (Docker/K8s) or use Qdrant Cloud
- You want **multi-cloud** or **on-premise** deployment

### Choose S3 Vectors When:

- You need **massive scale** (billions of vectors) at **minimal cost**
- Your queries are **infrequent** (archival, batch processing)
- You want **zero operations** — no servers to manage
- You only need **basic semantic search + simple filters**
- You're **already in the AWS ecosystem** (Bedrock, IAM, CloudTrail)
- **Cost at rest** matters more than query speed

### Consider Using Both:

- **S3 Vectors** as the cold storage / archival layer (billions of vectors, low cost)
- **Qdrant** as the hot query layer (real-time search, advanced features)
- Sync between them based on access patterns

---

## Slide 15: What We Tested (25 Tests Summary)

| # | Test | Both? | Key Finding |
|---|------|-------|-------------|
| 01 | Semantic search (top-K cosine) | Both | Same results, Qdrant faster |
| 02 | Filter: exact match (genre) | Both | Both work, different syntax |
| 03 | Filter: numeric range (year >= 2010) | Both | Both work |
| 04 | Filter: combined AND (genre + year + rating) | Both | Both work |
| 05 | Filter: OR logic (Drama OR Comedy) | Both | Both work |
| 06 | Filter: negation (language != English) | Both | Both work |
| 07 | Filter: set membership ($in) | Both | Both work |
| 08 | Batch insert (50 movies) | Both | Qdrant: flexible; S3: max 500/call |
| 09 | Get by ID | Both | Both work |
| 10 | Update metadata | Both | Qdrant: partial update; S3: full re-put |
| 11 | Delete vector | Both | Both work |
| 12 | Hybrid search (dense + sparse) | Qdrant only | S3 can't do this |
| 13 | Recommendation (like A, not B) | Qdrant only | S3 can't do this |
| 14 | Scroll/paginate with filter | Qdrant only | S3 can't do this |
| 15 | Full-text keyword match | Qdrant only | S3 can't do this |
| 16 | Geo-spatial filter (radius, bbox) | Qdrant only | S3 can't do this |
| 17 | Group-by (best per genre) | Qdrant only | S3 can't do this |
| 18 | Named vectors (title + description) | Qdrant only | S3 can't do this |
| 19 | Zero infrastructure setup | Info | S3: 2 API calls vs Qdrant: 9 steps |
| 20 | IAM authentication | Info | S3: built-in vs Qdrant: manual |
| 21 | Bedrock Knowledge Bases | Info | S3: native RAG pipeline |
| 22 | Top-K > 100 | Both | Qdrant: unlimited; S3: capped at 100 |
| 23 | Consistency (insert → immediate read) | Both | Qdrant: strong; S3: eventual |
| 24 | Batch size limits | Info | S3: hard limits; Qdrant: hardware-bound |
| 25 | Scale constraints | Info | S3: documented caps; Qdrant: flexible |

---

## Slide 16: Final Verdict

```
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│   Neither solution is universally superior.                  │
│                                                              │
│   Qdrant = PERFORMANCE + FEATURES + CONTROL                 │
│   Best for: Real-time search, complex AI apps, RAG          │
│                                                              │
│   S3 Vectors = SCALE + COST + SIMPLICITY                    │
│   Best for: Massive storage, low-traffic, AWS-native apps   │
│                                                              │
│   The right choice depends on:                               │
│     1. How fast do you need answers?                         │
│     2. How complex are your queries?                         │
│     3. How much are you willing to manage?                   │
│     4. What's your budget model?                             │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## Slide 17: Deliverables

| Deliverable | Description |
|-------------|-------------|
| `final_report.md` | Detailed written comparison (7 sections) |
| `presentation.md` | This presentation |
| `tests/` (25 files) | One file per test — runnable, readable |
| `core/` | Shared framework (clients, config, embeddings, dataset) |
| `setup.py` | One-command data loading for both platforms |
| `run_all.py` | Test runner with output capture to `results/` |
| `docs/` | Official documentation references |

### How to Run

```bash
# 1. Start Qdrant
docker compose up -d

# 2. Load data into both platforms (run once)
python setup.py

# 3. Run all 25 tests
python run_all.py

# 4. Run specific tests
python run_all.py 1          # Just test 01
python run_all.py 1-11       # Common ground tests
python run_all.py 12-18      # Qdrant-only features
```

---

## Q&A

**Anticipated questions:**

**Q: Why not just use pgvector (PostgreSQL)?**  
A: pgvector is a solid middle ground but lacks Qdrant's advanced features (hybrid search, named vectors, quantization) and S3 Vectors' serverless scale. We focused on the two extremes of the spectrum.

**Q: Can S3 Vectors replace Qdrant for RAG?**  
A: For basic RAG (embed → store → retrieve), yes. For advanced RAG (hybrid search, re-ranking, multi-vector), Qdrant is significantly more capable.

**Q: What about Pinecone, Weaviate, or Milvus?**  
A: They sit between Qdrant and S3 Vectors on the spectrum. Qdrant and S3 Vectors were chosen because they represent the clearest contrast — purpose-built database vs. storage-layer extension.

**Q: Is S3 Vectors production-ready?**  
A: GA since December 2025. AWS reports 40+ billion vectors ingested during preview, but the ecosystem (third-party integrations, community resources) is still maturing.
