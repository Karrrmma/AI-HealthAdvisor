import pandas as pd
import re
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss

# ================================
# 1. Load and Preprocess Data
# ================================
# Load CSV file
data = pd.read_csv("nhs_conditions_batch_data.csv")  # Replace with your CSV file path

# Function to preprocess text
def preprocess_text(text):
    text = re.sub(r'[^a-zA-Z\s]', '', str(text))  # Remove special characters
    return text.lower().strip()  # Convert to lowercase and remove extra spaces

# Preprocess the 'symptoms' column
data['symptoms'] = data['symptoms'].fillna('').apply(preprocess_text)

print('Data loaded and preprocessed:')
print(data.head())

# ================================
# 2. Semantic Chunking
# ================================
# Function for semantic chunking
def semantic_chunking(text, chunk_size=150, overlap=50):
    words = text.split()  # Split text into words
    chunks = []

    # Loop through the words with a step size of (chunk_size - overlap)
    for i in range(0, len(words), chunk_size - overlap):
        word_slice = words[i:i + chunk_size]  # Extract a slice of words
        chunk = " ".join(word_slice)  # Join words into a single string
        chunks.append(chunk)  # Add to chunks list
    
    return chunks

# Generate chunks for all rows in the dataset
all_chunks = []  # List to hold all chunks
condition_names = []  # List to hold corresponding condition names

for _, row in data.iterrows():
    condition = row['Condition Name']
    symptoms = row['symptoms']
    chunks = semantic_chunking(symptoms)  # Generate chunks
    for chunk in chunks:
        all_chunks.append(chunk)  # Add chunk to list
        condition_names.append(condition)  # Add corresponding condition name

print(f"Total Chunks Created: {len(all_chunks)}")

# ================================
# 3. Generate Embeddings
# ================================
# Load pre-trained Hugging Face embedding model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# Generate embeddings for all chunks
print("Generating embeddings...")
embeddings = embedding_model.encode(all_chunks, show_progress_bar=True)

# Convert embeddings to a numpy array
embeddings_array = np.array(embeddings).astype('float32')  
print(f"Embeddings generated with shape: {embeddings_array.shape}")

# ================================
# 4. Store Embeddings in FAISS
# ================================
# Initialize FAISS index
index = faiss.IndexFlatL2(embeddings_array.shape[1])  # L2 norm for similarity search
index.add(embeddings_array)  # Add embeddings to the FAISS index

print(f"FAISS index created with {index.ntotal} embeddings.")



# ================================
# Save FAISS Model and Data
# ================================
import faiss
import pickle

# Save FAISS index
faiss.write_index(index, "faiss_index.bin")

# Save condition names and chunks
with open("condition_names.pkl", "wb") as f:
    pickle.dump(condition_names, f)

with open("all_chunks.pkl", "wb") as f:
    pickle.dump(all_chunks, f)

print("Model and data saved successfully.")

# ================================
# 5. Retrieve Relevant Chunks
# ================================
# Function to retrieve relevant chunks based on a query
def retrieve_chunks(query, top_k=3):
    query_embedding = embedding_model.encode([query]).astype('float32')  # Embed the query
    distances, indices = index.search(query_embedding, k=top_k)  # Perform FAISS search
    
    results = [all_chunks[i] for i in indices[0]]  # Retrieve the corresponding chunks
    return results

# Example query
query = "What are the symptoms of abdominal pain?"
retrieved_chunks = retrieve_chunks(query)

# Print the top relevant chunks
print("\nTop Relevant Chunks:")
for i, chunk in enumerate(retrieved_chunks, start=1):
    print(f"{i}. {chunk}")
