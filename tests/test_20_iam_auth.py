"""Test 20: AWS IAM Native Auth — S3 Vectors strength."""


def run():
    print("=" * 60)
    print("TEST 20: AWS IAM Native Auth — S3 Vectors strength")
    print("=" * 60)

    print("""
┌─────────────────────────────────────────────────────────────┐
│                  QDRANT AUTH                                │
├─────────────────────────────────────────────────────────────┤
│  • API key auth (optional, off by default)                  │
│  • TLS must be configured manually for production           │
│  • Network security: manage firewall rules yourself         │
│  • No built-in audit logging                                │
│  • No built-in encryption at rest                           │
│  • Access control: all-or-nothing API key                   │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                S3 VECTORS AUTH                              │
├─────────────────────────────────────────────────────────────┤
│  • AWS IAM — same policies as S3, Lambda, DynamoDB          │
│  • Fine-grained: per-bucket, per-index permissions          │
│  • VPC endpoints supported (private network)                │
│  • Encryption at rest: enabled by default (SSE)             │
│  • CloudTrail: every API call is audit-logged               │
│  • Integrates with AWS Organizations, SCP, etc.             │
│  • No extra auth setup — uses your AWS credentials          │
└─────────────────────────────────────────────────────────────┘
""")

    # Demo: show that boto3 just works with existing credentials
    import boto3

    from core.config import AWS_REGION

    sc = boto3.client("s3vectors", region_name=AWS_REGION)
    sts = boto3.client("sts", region_name=AWS_REGION)

    identity = sts.get_caller_identity()
    print(f"  Current AWS Identity:")
    print(f"    Account: {identity['Account']}")
    print(f"    ARN: {identity['Arn']}")
    print(f"\n  S3 Vectors uses this identity automatically — no API keys to manage.")


if __name__ == "__main__":
    run()
