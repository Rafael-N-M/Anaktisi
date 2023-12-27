import os
import re
import math
import numpy as np
from collections import defaultdict

# Function to read text from files in the 'data' folder
def read_documents(folder):
    documents = []
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        with open(file_path, 'r') as file:
            text = file.read()
            documents.append(text)
    return documents

# Function to preprocess text
def preprocess_text(text):
    text = text.lower()
    tokens = re.findall(r'\b\w+\b', text)
    return tokens

# Function to create term frequency dictionary
def create_term_frequency(documents):
    term_frequency = defaultdict(lambda: defaultdict(int))
    for idx, document in enumerate(documents):
        tokens = preprocess_text(document)
        for token in tokens:
            term_frequency[idx][token] += 1
    return term_frequency

# Function to create document-term matrix
def create_document_term_matrix(term_frequency, vocabulary):
    doc_term_matrix = np.zeros((len(term_frequency), len(vocabulary)), dtype=int)
    for doc_id, term_freq in term_frequency.items():
        for term, freq in term_freq.items():
            if term in vocabulary:
                term_index = vocabulary.index(term)
                doc_term_matrix[doc_id][term_index] = freq
    return doc_term_matrix


# Function to calculate TF-IDF
def calculate_tfidf(doc_term_matrix):
    doc_count = len(doc_term_matrix)
    doc_with_term = np.sum((doc_term_matrix > 0).astype(int), axis=0)
    idf = np.log(doc_count / (1 + doc_with_term))
    tfidf_matrix = doc_term_matrix * idf
    return tfidf_matrix

# Function to calculate cosine similarity
def cosine_similarity(query, docs):
    similarities = np.dot(query, docs.T)
    query_norm = np.linalg.norm(query, axis=1)
    docs_norm = np.linalg.norm(docs, axis=1)
    similarities /= np.outer(query_norm, docs_norm)
    return similarities

# Path to the 'data' folder containing documents
data_folder = 'data'

# Read documents from the 'data' folder
documents = read_documents(data_folder)

# Read queries from file
queries_file = 'Queries_20'
with open(queries_file, 'r') as file:
    queries = file.readlines()
queries = [str(query).strip() for query in queries]

# Concatenate documents and queries for term frequency calculation
all_texts = documents + queries

# Create term frequency dictionary
term_freq = create_term_frequency(all_texts)

# Create vocabulary from term frequency
vocabulary = list(set(term for doc in term_freq.values() for term in doc))

# Create document-term matrix
doc_term_matrix = create_document_term_matrix(term_freq, vocabulary)

# Calculate TF-IDF
tfidf_matrix = calculate_tfidf(doc_term_matrix)

# Process queries similarly
query_term_freq = create_term_frequency(queries)
query_vector = create_document_term_matrix(query_term_freq, vocabulary)
query_tfidf = calculate_tfidf(query_vector)

# Calculate Similarity Scores
similarities = cosine_similarity(query_tfidf, tfidf_matrix)

# Print relevant documents for each query
for i, query in enumerate(queries):
    print(f"Query: {query}")
    sim_scores = similarities[i]
    sorted_indices = np.argsort(sim_scores)[::-1]
    for idx in sorted_indices:
        print(f"Document {idx + 1}: {documents[idx]}")
    print("\n")

# Define the output file for storing results
output_file = 'query_results.txt'

# Open the output file in write mode
with open(output_file, 'w') as file:
    # Loop through queries and print relevant documents to the file
    for i, query in enumerate(queries):
        file.write(f"Query: {query}\n")
        sim_scores = similarities[i]
        sorted_indices = np.argsort(sim_scores)[::-1]
        for idx in sorted_indices:
            file.write(f"Document {idx + 1}: {documents[idx]}\n")
        file.write("\n")