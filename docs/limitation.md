Limitations and restrictions

Focus mode
Amazon S3 Vectors has certain limitations and restrictions that you should be aware of when planning your vector storage and search applications.

Vector buckets per AWS Region in an account: 10,000

Vector indexes per vector bucket: 10,000

Vectors per vector index: Up to 2 billion

Dimension value per vector: 1 to 4,096

Total metadata per vector: Up to 40 KB (filterable + non-filterable)

Total metadata keys per vector: Up to 50

Filterable metadata per vector: Up to 2 KB

Non-filterable metadata keys per vector index: Up to 10

Combined PutVectors and DeleteVectors requests per second per vector index: Up to 1,000

Combined vectors inserted and deleted per second per vector index: Up to 2,500

Request payload size: Up to 20 MiB

Vectors per PutVectors API call: Up to 500

Vectors per DeleteVectors API call: Up to 500

Vectors per GetVectors API call: Up to 100

Top-K results per QueryVectors request: Up to 100

Vectors listed per page in a ListVectors response: Up to 1,000

Vector buckets listed per page in a ListVectorBuckets response: Up to 500.

Vector indexes listed per page in a ListIndexes response: Up to 500.

Segment count for parallel listing in a ListVectors API call: Up to 16