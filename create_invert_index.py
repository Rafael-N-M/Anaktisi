import os
import json
from collections import defaultdict

def create_inverted_index(folder_path):
    inverted_index = defaultdict(lambda: defaultdict(int))
    word_count_per_file = defaultdict(int)

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
                words = content.split()
                word_count = len(words)  # Total words in this file
                word_count_per_file[filename] = word_count

                for word in words:
                    word = word.strip(".,")
                    inverted_index[word][filename] += 1  # Increment count for word in this filename

        except Exception as e:
            print(f"An error occurred while processing {file_path}: {e}")

    return inverted_index, word_count_per_file



def write_sorted_index_to_json(sorted_inverted_index, word_count_per_file, output_file):
    data_to_export = []

    for word, files_counts in sorted_inverted_index.items():
        total_occurrences = files_counts.__len__()

        filenames = list(files_counts.keys())
        frequencies = {filename: files_counts[filename] / word_count_per_file[filename] for filename in filenames}

        entry = {
            "word": word,
            "total_occurrences": total_occurrences,
            "frequencies_per_file": frequencies
        }

        data_to_export.append(entry)

    with open(output_file, "w", encoding="utf-8") as json_file:
        json.dump(data_to_export, json_file, indent=4)


# Specify the path to the "docs" folder
docs_folder_path = os.path.join("data")

# Create the inverted index and count of words per file
inverted_index, word_count_per_file = create_inverted_index(docs_folder_path)

# Sort the inverted index by the number of occurrences in descending order
sorted_inverted_index = dict(sorted(inverted_index.items(), key=lambda x: len(x[1]), reverse=True))

# Specify the output CSV file path
output_json_file_path = "sorted_inverted_index.json"

# Write the inverted index to the output CSV file
write_sorted_index_to_json(sorted_inverted_index, word_count_per_file, output_json_file_path)

print(f"Inverted index written to {output_json_file_path}")
