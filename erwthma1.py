import os
import csv
from collections import defaultdict

def create_inverted_index(folder_path):
    inverted_index = defaultdict(list)

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
                words = content.split()

                for word in words:
                    word = word.strip(".,")
                    if filename not in inverted_index[word]:
                        inverted_index[word].append(filename)
        except Exception as e:
            print(f"An error occurred while processing {file_path}: {e}")

    return inverted_index

def write_sorted_index_to_csv(sorted_inverted_index, output_file):
    with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Word", "Occurrences", "Filenames"])

        for word, filenames in sorted_inverted_index.items():
            csv_writer.writerow([word, len(filenames), ', '.join(filenames)])

# Specify the path to the "docs" folder
docs_folder_path = os.path.join("data", "docs")

# Create the inverted index
inverted_index = create_inverted_index(docs_folder_path)

# Sort the inverted index by the number of occurrences in descending order
sorted_inverted_index = dict(sorted(inverted_index.items(), key=lambda x: len(x[1]), reverse=True))

# Specify the output CSV file path
output_csv_file_path = "sorted_inverted_index.csv"

# Write the sorted inverted index to the output CSV file
write_sorted_index_to_csv(sorted_inverted_index, output_csv_file_path)

print(f"Sorted inverted index written to {output_csv_file_path}")