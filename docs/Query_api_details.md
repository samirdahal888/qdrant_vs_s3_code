You can run a similarity query with the QueryVectors API operation, where you specify the query vector, the number of relevant results to return (the top K nearest neighbors), and the index ARN. Additionally, you can use metadata filters in a query, to search only the vectors that match the filter. If you make a request to filter on a non-filterable metadata field, the request will return a 400 Bad Request error. For more information about metadata filtering, see Metadata filtering.

In the response, the vector keys are returned by default. You can optionally include the distance and metadata in the response.

When generating the query vector, you should use the same vector embedding model that was used to generate the initial vectors that are stored in the vector index. For example, if you use the Amazon Titan Text Embeddings V2 model in Amazon Bedrock to generate vector embeddings of your documents, use the same embedding model to convert a question to a query vector. Additionally, Amazon Bedrock Knowledge Bases provides a fully managed end-to-end RAG workflow where Amazon Bedrock automatically fetches data from your S3 data source, converts content into text blocks, generates embeddings, and stores them in your vector index. You can then query the knowledge base and generate responses based on chunks retrieved from your source data. For more information about how to query vectors from an Amazon Bedrock knowledge base in the console, see (Optional) Integrate S3 Vectors with Amazon Bedrock Knowledge Bases.

Furthermore, the open-source Amazon S3 Vectors Embed CLI tool provides a simplified way to perform semantic searches from the command line. This open source tool streamlines the query process by handling both the vector embedding generation with Amazon Bedrock foundation models and executing semantic search operations against your S3 vector indexes. For more information about using this tool for querying your vector data, see Creating vector embeddings and performing semantic searches with s3vectors-embed-cli.

S3 Vectors delivers sub-second response times for cold queries, leveraging Amazon S3 elastic throughput to efficiently search across millions of vectors. This makes it highly cost-effective for workloads with infrequent queries. For warm queries, S3 Vectors can deliver response times as low as 100ms, benefiting workloads with repeated or frequent query patterns.

For performing similarity queries for your vector embeddings, several factors can affect average recall performance, including the vector embedding model, the size of the vector dataset (the number of vectors and dimensions), and the distribution of queries. S3 Vectors delivers 90%+ average recall for most datasets. Average recall measures the quality of query results. A 90% average recall means that the response contains 90% of the actual closest vectors (ground truth) that are stored in the vector index relative to the query vector. However, because actual performance may vary depending on your specific use cases, we recommend conducting your own tests with representative data and queries to validate that S3 Vectors meet your recall requirements.

``` python # Query a vector index with an embedding from Amazon Titan Text Embeddings V2.
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
    ```