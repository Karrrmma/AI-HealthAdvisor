# AI-HealthAdvisor
Retrieval-Augmented Generation (RAG) system using OpenAI GPT-3 and FAISS to recommend medical conditions based on user-reported symptoms.

# Overview

This project processes a dataset containing conditions and their associated symptoms. It performs text preprocessing, semantic chunking, embedding generation using a pre-trained model, and stores the embeddings in a FAISS index for fast retrieval. The system then allows for querying the most relevant chunks of symptoms based on the input query.

# Requirements

pandas (for data manipulation)

re (for text preprocessing)

sentence_transformers (for generating embeddings)

numpy (for handling arrays)

faiss (for efficient similarity search)

pickle (for saving the model and data)

Install these dependencies via pip:

pip install pandas sentence-transformers numpy faiss-cpu


# Install these dependencies via pip:
    pip install pandas sentence-transformers numpy faiss-cpu

1. Load and Preprocess Data

The dataset is loaded from a CSV file and the text data (symptoms) is preprocessed by:

Removing non-alphabetical characters.

Converting text to lowercase.

Stripping extra whitespace.

2. Semantic Chunking

The preprocessed symptoms text is divided into smaller chunks of words. Each chunk consists of a specified number of words, with an overlap between consecutive chunks. This allows for better representation and retrieval of information.

Chunking Parameters:

chunk_size: The maximum number of words per chunk (default: 150).

overlap: The number of words that overlap between consecutive chunks (default: 50).

3. Generate Embeddings

Embeddings are generated for each chunk using the pre-trained all-MiniLM-L6-v2 model from Sentence-Transformers. These embeddings are used to capture the semantic meaning of each chunk.

4. Store Embeddings in FAISS

The generated embeddings are added to a FAISS index, which allows for fast similarity search. FAISS uses a vector search algorithm to efficiently retrieve similar chunks based on query embeddings.

5. Save Model and Data

The FAISS index and associated data (condition names, chunks) are saved to disk using pickle and FAISS's native .bin format.

6. Retrieve Relevant Chunks

When a query is provided, it is embedded using the same model. The query's embedding is then compared to the embeddings stored in the FAISS index, and the most similar chunks are retrieved.

Retrieve Chunks Function Parameters:

query: The input query string.

top_k: The number of top results to retrieve (default: 3).

Example Usage

query = "What are the symptoms of abdominal pain?"
retrieved_chunks = retrieve_chunks(query)

print("\nTop Relevant Chunks:")
for i, chunk in enumerate(retrieved_chunks, start=1):
    print(f"{i}. {chunk}")


