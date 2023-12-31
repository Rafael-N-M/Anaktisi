import os
import pandas as pd
from collections import defaultdict

def create_inverted_index(folder_path):
    inverted_index = defaultdict(lambda: defaultdict(int))
    word_count_per_file = defaultdict(int)

    all_files = [filename for filename in os.listdir(folder_path)]

    for filename in all_files:
        file_path = os.path.join(folder_path, filename)

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
                words = content.split()
                word_count = len(words)  # Total words in this file
                word_count_per_file[filename] = word_count

                for word in set(words):  # Use set to get unique words in file
                    word = word.strip(".,")
                    inverted_index[word][filename] += words.count(word)

        except Exception as e:
            print(f"An error occurred while processing {file_path}: {e}")

    return inverted_index, word_count_per_file

def write_sorted_index_to_json(sorted_inverted_index, word_count_per_file, output_file):
    data_to_export = []

    for word, files_counts in sorted_inverted_index.items():
        total_occurrences = sum(1 for filename in files_counts if files_counts[filename] > 0)

        filenames = list(files_counts.keys())
        frequencies = {filename: files_counts[filename] / word_count_per_file[filename] for filename in filenames}

        entry = {
            "word": word,
            "total_occurrences": total_occurrences,
            "frequencies_per_file": frequencies
        }

        data_to_export.append(entry)

    data_to_export_sorted = sorted(data_to_export, key=lambda x: x['total_occurrences'], reverse=True)

    df = pd.DataFrame(data_to_export_sorted)
    df.to_json(output_file, orient='records', indent=4)

# Specify the path to the "docs" folder
docs_folder_path = os.path.join("data")

# Create the inverted index and count of words per file
inverted_index, word_count_per_file = create_inverted_index(docs_folder_path)

# Specify the output JSON file path
output_json_file_path = "sorted_inverted_index_pandas.json"

# Write the inverted index to the output JSON file using Pandas DataFrame
write_sorted_index_to_json(inverted_index, word_count_per_file, output_json_file_path)

print(f"Inverted index written to {output_json_file_path}")
