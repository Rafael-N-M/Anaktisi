import os
import json
import math
import string

def custom_word_tokenize(text):
    translator = str.maketrans('', '', string.punctuation.replace('-', ''))  # Removing punctuation except hyphens
    text = text.translate(translator)
    words = text.lower().split()
    return words

#Creating the Inverted Index

data_folder = 'data'
documents = {}
inverted_index = {}

# Read documents and create inverted index
for filename in os.listdir(data_folder):
    with open(os.path.join(data_folder, filename), 'r') as file:
        doc_text = file.read().lower()
        documents[filename] = doc_text
        words = custom_word_tokenize(doc_text)
        word_freq = {}
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1
        for word, freq in word_freq.items():
            if word not in inverted_index:
                inverted_index[word] = {}
            inverted_index[word][filename] = freq

# Store Inverted Index in a JSON File
with open('inverted_index_custom.json', 'w') as file:
    json.dump(inverted_index, file)

#Calculate TF-IDF Weights

N = len(documents)
tfidf_weights = {}

for term, docs in inverted_index.items():
    df = len(docs)
    idf = math.log(N / df) if df > 0 else 0
    tfidf_weights[term] = {}
    for doc, freq in docs.items():
        tfidf_weights[term][doc] = (1 + math.log(freq)) * idf

# Store TF-IDF Weights in a JSON File
with open('tfidf_weights_custom.json', 'w') as file:
    json.dump(tfidf_weights, file)

# Compute Cosine Similarity for Queries

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

queries_similarities_top_10 = {}

for query in queries:
    query_words = custom_word_tokenize(query)
    query_tfidf = {}
    for word in query_words:
        if word in inverted_index:
            df = len(inverted_index[word])
            idf = math.log(N / df) if df > 0 else 0
            tf = (query_words.count(word) / len(query_words))
            query_tfidf[word] = tf * idf

    similarities = {}
    for doc_id, doc in documents.items():
        dot_product = sum(query_tfidf[word] * tfidf_weights[word].get(doc_id, 0) for word in query_tfidf if doc_id in tfidf_weights[word])
        query_magnitude = math.sqrt(sum(val ** 2 for val in query_tfidf.values()))
        doc_magnitude = math.sqrt(sum(tfidf_weights[word].get(doc_id, 0) ** 2 for word in query_tfidf if doc_id in tfidf_weights[word]))
        similarity = dot_product / (query_magnitude * doc_magnitude) if (query_magnitude * doc_magnitude) > 0 else 0
        similarities[doc_id] = similarity

    # Get top 10 similar documents for the current query
    top_10 = {k: v for k, v in sorted(similarities.items(), key=lambda item: item[1], reverse=True)[:10]}
    queries_similarities_top_10[query] = top_10

# Save the top 10 similarities to a JSON file
with open('queries_similarities_top_10.json', 'w') as file:
    json.dump(queries_similarities_top_10, file, indent=4)
