"""Test 21: Bedrock KB Integration — S3 Vectors strength."""


def run():
    print("=" * 60)
    print("TEST 21: Bedrock Knowledge Bases Integration — S3 Vectors strength")
    print("=" * 60)

    print("""
S3 Vectors integrates natively with the AWS ecosystem:

┌─────────────────────────────────────────────────────────────┐
│  Amazon Bedrock Knowledge Bases                             │
│  ─────────────────────────────────                          │
│  Fully managed RAG pipeline:                                │
│    1. Connect S3 data source (PDFs, docs, etc.)             │
│    2. Bedrock auto-chunks text                              │
│    3. Bedrock auto-generates embeddings                     │
│    4. Bedrock stores vectors in S3 Vectors                  │
│    5. Query with natural language → get grounded answers     │
│                                                             │
│  → Zero embedding code. Zero vector management.             │
│  → Just point to your docs and ask questions.               │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  S3 Vectors Embed CLI (open source)                         │
│  ──────────────────────────────────                         │
│  Command-line semantic search:                              │
│    $ s3vectors-embed search "space adventure" \\             │
│        --bucket my-bucket --index movies                    │
│                                                             │
│  → Handles embedding generation + query in one command.     │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  Other AWS Integrations                                     │
│  ──────────────────────                                     │
│  • AWS Lambda    — serverless query functions                │
│  • CloudWatch    — metrics and monitoring                    │
│  • CloudTrail    — API audit logging                         │
│  • IAM           — fine-grained access control               │
│  • VPC Endpoints — private network access                    │
└─────────────────────────────────────────────────────────────┘

Qdrant: Integrates via REST/gRPC API — works anywhere,
        but requires you to build the entire RAG pipeline yourself.
        No native AWS service integration.
""")


if __name__ == "__main__":
    run()
