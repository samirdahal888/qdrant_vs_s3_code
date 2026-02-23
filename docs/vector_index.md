Creating a vector index in a vector bucket

``` python 
import boto3

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
)
```

listing vector index 

``` python 
import boto3

# Create a S3 Vectors client in the AWS Region of your choice. 
s3vectors = boto3.client("s3vectors", region_name="us-west-2")

#List vector indexes in your vector bucket
response = s3vectors.list_indexes(vectorBucketName="media-embeddings")
indexes = response["indexes"]
print(indexes)


```

deleting vector index

``` python   
import boto3

# Create a S3 Vectors client in the AWS Region of your choice. 
s3vectors = boto3.client("s3vectors", region_name="us-west-2")

#Delete a vector index
response = s3vectors.delete_index(
    vectorBucketName="media-embeddings",
    indexName="movies") 
    
    ```






Vector indexes are resources within vector buckets that store and organize vector data for efficient similarity search operations. When you create a vector index, you specify the distance metric (Cosine or Euclidean), the number of dimensions that a vector should have, and optionally a list of metadata fields that you want to exclude from filtering during similarity queries.

For more information about vector index limits per bucket, vector limits per index, and dimension limits per vector, see Limitations and restrictions.

Each vector index has a unique Amazon Resource Name (ARN). The ARNs of vector indexes follow the following format:


arn:aws:s3vectors:region:account-id:bucket/bucket-name/index/index-name
Vector index naming requirements

Vector index names must be unique within the vector bucket.

Vector index names must be between 3 and 63 characters long.

Valid characters are lowercase letters (a-z), numbers (0-9), hyphens (-), and dots (.).

Vector index names must begin and end with a letter or number.

Dimension requirements

A dimension is the number of values in a vector. All vectors added to the index must have exactly this number of values.

A dimension must be an integer between 1 and 4096.

A larger dimension requires more storage space.

Distance metric options

Distance metric specifies how similarity between vectors is calculated. When creating vector embeddings, choose your embedding model's recommended distance metric for more accurate results.

Cosine – Measures the cosine of the angle between vectors. Best for normalized vectors and when direction matters more than magnitude.

Euclidean – Measures the straight-line distance between vectors. Best when both direction and magnitude are important.

Non-filterable metadata keys

Metadata keys allow you to attach additional information to your vectors as key-value pairs during storage and retrieval. By default, all metadata is filterable, so you can use it to filter query results. However, you can designate specific metadata keys as non-filterable when you want to store information with vectors without using it for filtering.

Unlike default metadata keys, these keys can't be used as query filters. Non-filterable metadata keys can be retrieved but can't be searched, queried, or filtered. You can only access it after finding the index.

Non-filterable metadata keys allow you to enrich vectors with additional context that you want to retrieve with search results but don't need for filtering. A common example of a non-filterable metadata key is when you embed text into vectors and want to include the original text itself as non-filterable metadata. This allows you to return the source text alongside vector search results without increasing your filterable metadata size limits. Other examples include storing creation timestamps, source URLs, or descriptive information purely for reference. Non-filterable metadata keys can be accessed when retrieving vectors but, unlike default metadata keys, these keys can't be used as query filters.

Requirements for non-filterable metadata keys are as follows.

Non-filterable metadata keys must be unique within the vector index.

Non-filterable metadata keys must be 1 to 63 characters long.

Non-filterable metadata keys can't be modified after the vector index is created.

S3 Vectors support up to 10 non-filterable metadata keys per index.

For more information about non-filterable metadata keys, see Non-filterable metadata.

Topics
Creating a vector index in a vector bucket

Listing vector indexes

Deleting a vector index

Using tags with S3 vector indexes

You can add vectors to a vector index with the PutVectors API operation. Each vector consists of a key, which uniquely identifies each vector in a vector index. If you put a vector with a key that already exists in the index, it will overwrite the existing vector completely, which makes the previous vector no longer searchable. To maximize write throughput and optimize for costs, it's recommended that you insert vectors in large batches, up to the maximum batch size for PutVectors. However, for workloads that need to use smaller batches - such as when live, incoming vector data must become immediately searchable - you can achieve higher write throughput by using a higher number of concurrent PutVectors requests, up to the maximum allowed requests per second limit. For more information about the maximum batch size for PutVectors, which is the limit of vectors per PutVectors API call, and the maximum requests and vectors per second limit, see Limitations and restrictions. Additionally, you can attach metadata (for example, year, author, genre, location) as key-value pairs to each vector. By default, all metadata keys that are attached to vectors are filterable and can be used as filters in a similarity query. Only metadata keys that are specified as non-filterable during vector index creation are excluded from filtering. S3 vector indexes support string, number, boolean, and list types of metadata. For more information about the total metadata size limit per vector and the filterable metadata size limit per vector, see Limitations and restrictions. If the metadata size exceeds these limits, the PutVectors API operation will return a 400 Bad Request error.

Before adding vector data to your vector index with the PutVectors API operation, you need to convert your raw data into vector embeddings, which are numerical representations of your content as arrays of floating-point numbers. The vector embeddings capture the semantic meaning of your content, enabling similarity searches once they're stored in your vector index through the PutVectors operation. You can generate vector embeddings using various methods depending on your data type and use case. These methods include using machine learning frameworks, specialized embedding libraries, or AWS services such as Amazon Bedrock. For example, if you're using Amazon Bedrock, you can generate embeddings with the InvokeModel API operation and your preferred embedding model.

Additionally, Amazon Bedrock Knowledge Bases provides a fully managed end-to-end RAG workflow where Amazon Bedrock automatically fetches data from your S3 data source, converts content into text blocks, generates embeddings, and stores them in your vector index. You can then query the knowledge base and generate responses based on chunks retrieved from your source data.

Furthermore, the open-source Amazon S3 Vectors Embed CLI tool provides a simplified way to generate embeddings and perform semantic searches from the command line. For more information about this open source tool that automates both vector embedding generation with Amazon Bedrock foundation models and semantic search operations within your S3 vector indexes, see Creating vector embeddings and performing semantic searches with s3vectors-embed-cli.

``` python
# Populate a vector index with embeddings from Amazon Titan Text Embeddings V2.
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
)

```
Example: List vectors in a vector index

``` python 
import boto3

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

print(vectors)
```