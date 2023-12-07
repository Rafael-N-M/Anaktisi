import json
import math

# Load the JSON file with word frequencies
with open('sorted_inverted_index.json', 'r') as file:
    data = json.load(file)

# Assuming 'data' is a list of dictionaries, each containing word frequencies
vectors = []

for record in data:
    word = record['word']
    frequencies = record['frequencies_per_file']
    n_i = record['total_occurrences']
    idf = math.log(1209/n_i, 2)  # Using the number of files as len(frequencies)

    word_vector = {
        'word': word,
        'vector': []
    }

    for file_name, value in frequencies.items():
        if value == 0:
            w = 0
        else:
            tf = 1 + math.log(value, 2)
            w = tf * idf
        word_vector['vector'].append(w)

    vectors.append(word_vector)

# Store vectors in a new JSON file
output_file = 'word_vectors.json'

with open(output_file, 'w') as file:
    json.dump(vectors, file)

print(f"Word vectors have been stored in {output_file}")
