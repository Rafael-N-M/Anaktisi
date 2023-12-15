import json
import pandas as pd
import math

# Load data from the JSON file
with open('sorted_inverted_index.json', 'r') as file:
    data = json.load(file)

# Create a DataFrame from the loaded JSON data
df = pd.DataFrame(data)

# Calculate IDF for each word
total_files = 1209
df['idf'] = df['total_occurrences'].apply(lambda x: math.log(total_files / x))

# Create a dictionary to store vectors for each file
file_vectors = {file: [] for file in df['frequencies_per_file'][0]}

# Loop through the data to create TF-IDF vectors for each file
for _, row in df.iterrows():
    word = row['word']
    frequencies_per_file = row['frequencies_per_file']
    idf = row['idf']

    # For each file, calculate TF-IDF for the word or 0 if absent
    for file in file_vectors:
        tf = frequencies_per_file.get(file, 0)
        tf_idf = tf * idf
        file_vectors[file].append(tf_idf)

# Save file vectors to a new JSON file
with open('file_vectors_tfidf_pandas.json', 'w') as file:
    json.dump(file_vectors, file, indent=4)
