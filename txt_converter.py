import os

def convert_txt_to_tsv(input_file_path):
    # Extract the filename without extension (e.g., "00001")
    filename_without_extension = os.path.splitext(os.path.basename(input_file_path))[0]

    # Create the unique identifier (id_1, id_2, etc.)
    identifier = f'id_{filename_without_extension}'

    with open(input_file_path, 'r', encoding='utf-8') as input_file:
        lines = input_file.readlines()

    # Extract words from each line, handling errors
    data = [line.strip() for line in lines if line.strip()]

    # Return the identifier and data as a formatted string
    return f'{identifier}\t{"\t".join(data)}\n'

# Specify the input folder containing text files
input_folder_path = r'./data'

# Specify the output file path
output_file_path = './output.tsv'

# Open the output file in write mode
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    # Process each text file in the input folder
    for filename in os.listdir(input_folder_path):
        #if filename.endswith('.txt'):
        input_file_path = os.path.join(input_folder_path, filename)
            
        # Call the function and write the result to the output file
        output_file.write(convert_txt_to_tsv(input_file_path))

print(f'Concatenated TSV file created: {output_file_path}')
