https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-vectors.html
https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-vectors-getting-started.html
https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-vectors-buckets.html
https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-vectors-buckets-naming.html
https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-vectors-buckets-create.html
``import boto3

# Create a S3 Vectors client in the AWS Region of your choice. 
s3vectors = boto3.client("s3vectors", region_name="us-west-2")

#Create a vector bucket
s3vectors.create_vector_bucket(vectorBucketName="media-embeddings")``

https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-vectors-buckets-list.html
``import boto3

# Create a S3 Vectors client in the AWS Region of your choice. 
s3vectors = boto3.client("s3vectors", region_name="us-west-2")

#List vector buckets
response = s3vectors.list_vector_buckets()
buckets = response["vectorBuckets"]
print(buckets)``
https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-vectors-buckets-details.html
https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-vectors-buckets-delete.html
``import boto3

# Create a S3 Vectors client in the AWS Region of your choice. 
s3vectors = boto3.client("s3vectors", region_name="us-west-2")

#Delete a vector bucket
response = s3vectors.delete_vector_bucket(vectorBucketName="media-embeddings")
``
https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-vectors-bucket-policy.html
https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-vectors-tags.html
https://docs.aws.amazon.com/AmazonS3/latest/userguide/managing-tags-vector-buckets.html
https://docs.aws.amazon.com/AmazonS3/latest/userguide/creating-vector-buckets-with-tags.html
https://docs.aws.amazon.com/AmazonS3/latest/userguide/adding-tag-vector-bucket.html
https://docs.aws.amazon.com/AmazonS3/latest/userguide/viewing-vector-bucket-tags.html
https://docs.aws.amazon.com/AmazonS3/latest/userguide/deleting-tag-vector-bucket.html
https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-vectors-indexes.html
https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-vectors-create-index.html
``import boto3

# Create a S3 Vectors client in the AWS Region of your choice. 
s3vectors = boto3.client("s3vectors", region_name="us-west-2")

#Create a vector index "movies" in the vector bucket "media-embeddings" without non-filterable metadata keys
s3vectors.create_index(
    vectorBucketName="media-embeddings",
    indexName="movies",
    dimension=3,
    distanceMetric="cosine",
    dataType = "float32"
)


#Create a vector index "movies" in the vector bucket "media-embeddings" with non-filterable metadata keys
s3vectors.create_index(
    vectorBucketName="media-embeddings",
    indexName="movies",
    dimension=3,
    distanceMetric="cosine",
    dataType = "float32",
    metadataConfiguration= {"nonFilterableMetadataKeys": ["nonFilterableMetadataKey1"]}
)``
https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-vectors-index-list.html
``import boto3

# Create a S3 Vectors client in the AWS Region of your choice. 
s3vectors = boto3.client("s3vectors", region_name="us-west-2")

#List vector indexes in your vector bucket
response = s3vectors.list_indexes(vectorBucketName="media-embeddings")
indexes = response["indexes"]
print(indexes)``
https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-vectors-index-delete.html
``import boto3

# Create a S3 Vectors client in the AWS Region of your choice. 
s3vectors = boto3.client("s3vectors", region_name="us-west-2")

#Delete a vector index
response = s3vectors.delete_index(
    vectorBucketName="media-embeddings",
    indexName="movies")``
https://docs.aws.amazon.com/AmazonS3/latest/userguide/vector-index-tagging.html
https://docs.aws.amazon.com/AmazonS3/latest/userguide/managing-tags-vector-indexes.html
https://docs.aws.amazon.com/AmazonS3/latest/userguide/creating-vector-indexes-with-tags.html
https://docs.aws.amazon.com/AmazonS3/latest/userguide/adding-tag-vector-index.html
https://docs.aws.amazon.com/AmazonS3/latest/userguide/viewing-vector-index-tags.html
https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-vectors-vectors.html
https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-vectors-index-create.html
``# Populate a vector index with embeddings from Amazon Titan Text Embeddings V2.
import boto3
import json

# Create Bedrock Runtime and S3 Vectors clients in the AWS Region of your choice. 
bedrock = boto3.client("bedrock-runtime", region_name="us-west-2")
s3vectors = boto3.client("s3vectors", region_name="us-west-2")

# Texts to convert to embeddings.
texts = [
    "Star Wars: A farm boy joins rebels to fight an evil empire in space", 
    "Jurassic Park: Scientists create dinosaurs in a theme park that goes wrong",
    "Finding Nemo: A father fish searches the ocean to find his lost son"
]

# Generate vector embeddings.
embeddings = []
for text in texts:
    response = bedrock.invoke_model(
        modelId="amazon.titan-embed-text-v2:0",
        body=json.dumps({"inputText": text})
    )

    # Extract embedding from response.
    response_body = json.loads(response["body"].read())
    embeddings.append(response_body["embedding"])

# Write embeddings into vector index with metadata.
s3vectors.put_vectors(
    vectorBucketName="media-embeddings",   
    indexName="movies",   
    vectors=[
        {
            "key": "Star Wars",
            "data": {"float32": embeddings[0]},
            "metadata": {"source_text": texts[0], "genre":"scifi"}
        },
        {
            "key": "Jurassic Park",
            "data": {"float32": embeddings[1]},
            "metadata": {"source_text": texts[1], "genre":"scifi"}
        },
        {
            "key": "Finding Nemo",
            "data": {"float32": embeddings[2]},
            "metadata": {"source_text": texts[2], "genre":"family"}
        }
    ]
)``
https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-vectors-list.html
``import boto3

# Create a S3 Vectors client in the AWS Region of your choice. 
s3vectors = boto3.client("s3vectors", region_name="us-west-2")

#List vectors in your vector index 

response = s3vectors.list_vectors( 
    vectorBucketName="media-embeddings",
    indexName="movies",
    maxResults = 600,
    returnData = True,
    returnMetadata = True
)

vectors = response["vectors"]

print(vectors)``
``import boto3

# Create a S3 Vectors client in the AWS Region of your choice. 
s3vectors = boto3.client("s3vectors", region_name="us-west-2")

#List vectors in the 1st half of vectors in the index.
response = s3vectors.list_vectors( 
    vectorBucketName="media-embeddings",
    indexName="movies",
    segmentCount=2,
    segmentIndex=1,
    maxResults = 600,
    returnData = True,
    returnMetadata = True
)

vectors = response["vectors"]

#List vectors starting from the 2nd half of vectors in the index.
# This can be ran in parallel with the first `list_vectors` call.
response = s3vectors.list_vectors( 
    vectorBucketName="media-embeddings",
    indexName="movies",
    segmentCount=2,
    segmentIndex=1,
    maxResults = 600,
    returnData = True,
    returnMetadata = True
)

vectors = response["vectors"]

print(vectors)``
https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-vectors-query.html
``# Query a vector index with an embedding from Amazon Titan Text Embeddings V2.
import boto3 
import json 

# Create Bedrock Runtime and S3 Vectors clients in the AWS Region of your choice. 
bedrock = boto3.client("bedrock-runtime", region_name="us-west-2")
s3vectors = boto3.client("s3vectors", region_name="us-west-2") 

# Query text to convert to an embedding. 
input_text = "adventures in space"

# Generate the vector embedding.
response = bedrock.invoke_model(
    modelId="amazon.titan-embed-text-v2:0",
    body=json.dumps({"inputText": input_text})
) 

# Extract embedding from response.
model_response = json.loads(response["body"].read())
embedding = model_response["embedding"]

# Query vector index.
response = s3vectors.query_vectors(
    vectorBucketName="media-embeddings",
    indexName="movies",
    queryVector={"float32": embedding}, 
    topK=3, 
    returnDistance=True,
    returnMetadata=True
)
print(json.dumps(response["vectors"], indent=2))

# Query vector index with a metadata filter.
response = s3vectors.query_vectors(
    vectorBucketName="media-embeddings",
    indexName="movies",
    queryVector={"float32": embedding}, 
    topK=3, 
    filter={"genre": "scifi"},
    returnDistance=True,
    returnMetadata=True
)
print(json.dumps(response["vectors"], indent=2))
    ``

https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-vectors-delete.html
``import boto3

# Create a S3 Vectors client in the AWS Region of your choice. 
s3vectors = boto3.client("s3vectors", region_name="us-west-2")
https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-vectors-cli.html

#Delete vectors in a vector index
response = s3vectors.delete_vectors(
    vectorBucketName="media-embeddings",
    indexName="movies",
    keys=["Star Wars", "Finding Nemo"])``

https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-vectors-metadata-filtering.html
https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-vectors-limitations.html
https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-vectors-best-practices.html
https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-vectors-cli.html
https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-vectors-integration.html
https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-vectors-opensearch.html
https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-vectors-bedrock-kb.html
https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-vectors-regions-quotas.html
https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-vectors-security.html
https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-vectors-access-management.html
https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-vectors-iam-policies.html
https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-vectors-resource-based-policies.html
https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-vectors-data-encryption.html
https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-vectors-sectting-encryption.html
https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-vectors-viewing-encryption.html
https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-vectors-privatelink.html
https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-vectors-logging.html
https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-vectors-cloudtrail-log-example.html