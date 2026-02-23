Amazon S3 Vectors primarily supports 32-bit floating point numbers (Float32) for vector data. Each vector stored in a single vector index must have the identical dimensions. 

For associated metadata, the following data types are supported: 

Strings (for titles, categories, or the vector's unique key)
Numbers (for timestamps or scores)
Booleans (for flags like "published")
Lists (for tags or multiple authors) 
S3 Vectors stores structured numerical arrays within "vector indexes". While it doesn't directly support traditional file formats (like PDF or image files), you can use integrated services such as Amazon Bedrock Knowledge Bases or the S3 Vectors Embed CLI to process unstructured data, generate the necessary vector embeddings, and store them. 
