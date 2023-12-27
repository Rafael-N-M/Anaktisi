import json
import math

# Your existing code for inverted index creation and other functions

# Load the existing inverted index
with open('sorted_inverted_index_pandas.json', 'r') as file:
    inverted_index_data = json.load(file)

# Assuming 'inverted_index_data' contains the inverted index created previously

# Define a function to calculate TF-IDF vectors for queries
def calculate_query_vectors(queries, inverted_index_data):
    total_files = 1209  # Assuming the total number of files

    query_vectors = {}
    for query in queries:
        query_words = query.lower().split()  # Split query into words
        query_vector = [0] * len(query_words)  # Initialize query vector

        for idx, word in enumerate(query_words):
            if word in inverted_index_data:
                idf = math.log(total_files / inverted_index_data[word]['total_occurrences'])

                # Calculate TF for the query word (assuming 1 occurrence per query)
                tf = 1

                # Calculate TF-IDF for the query word
                tf_idf = tf * idf
                query_vector[idx] = tf_idf

        query_vectors[query] = query_vector

    return query_vectors

# Define your queries
queries = [
    "What are the effects of calcium on the physical properties of mucus from CF patients",
"Can one distinguish between the effects of mucus hypersecretion and infection on the submucosal glands of the respiratory tract in CF",
"How are salivary glycoproteins from CF patients different from those of normal subjects",
"What is the lipid composition of CF respiratory secretions",
"Is CF mucus abnormal",
"What is the effect of water or other therapeutic agents on the physical properties viscosity elasticity of sputum or bronchial secretions from CF patients",
"Are mucus glycoproteins degraded differently in CF patients as compared to those from normal subjects",
"What histochemical differences have been described between normal and CF respiratory epithelia",
"What is the association between liver disease cirrhosis and vitamin A metabolism in CF",
"What is the role of Vitamin E in the therapy of patients with CF",
"What is the difference between meconium ileus and meconium plug syndrome",
"What abnormalities of amino acid transport have been described in the small bowel of CF patients",
"What are the clinical or biochemical features of pancreatitis in CF patients",
"What non-invasive tests can be performed for the evaluation of exocrine pancreatic function in patients with CF",
"What are the hepatic complications or manifestations of CF",
"What are the gastrointestinal complications of CF after the neonatal period exclude liver disease and meconium ileus",
"What is the most effective regimen for the use of pancreatic enzyme supplements in the treatment of CF patients",
"Is dietary supplementation with bile salts of therapeutic benefit to CF patients",
"What complications of pancreatic enzyme therapy have been reported in CF patients"
]

# Calculate TF-IDF vectors for the queries using the inverted index
query_vectors = calculate_query_vectors(queries, inverted_index_data)

# Save query vectors to a new JSON file
with open('query_vectors_tfidf.json', 'w') as file:
    json.dump(query_vectors, file, indent=4)
