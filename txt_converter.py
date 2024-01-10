import os

# Specify the name of the new folder
folder_name = 'output_tsv_files'

# Get the current working directory
current_directory = os.getcwd()

# Create the full path for the new folder
new_folder_path = os.path.join(current_directory, folder_name)

# Check if the folder already exists
if not os.path.exists(new_folder_path):
    # Create the new folder
    os.makedirs(new_folder_path)
    print(f'Folder "{folder_name}" created successfully in {current_directory}')



print("Script started")

def convert_txt_to_tsv(input_file_path, output_folder):
    # Extract the filename without extension (e.g., "00001")
    filename_without_extension = os.path.splitext(os.path.basename(input_file_path))[0]

    # Create the output TSV file path
    output_file_path = os.path.join(output_folder, f'{filename_without_extension}.tsv')

    with open(input_file_path, 'r', encoding='utf-8') as input_file:
        lines = input_file.readlines()

    # Extract words from each line, handling errors
    data = [line.strip() for line in lines if line.strip()]

    with open(output_file_path, 'w', encoding='utf-8') as tsv_file:
        # Write data to the TSV file in a single line
        tsv_file.write('\t'.join(data))

    #print(f'TSV file created: {output_file_path}')

# Specify the input folder containing text files
input_folder_path = r'./data'

# Specify the output folder for TSV files
output_folder_path = './output_tsv_files'

# Process each text file in the input folder
for filename in os.listdir(input_folder_path):
    #if filename.endswith('.txt'):
    input_file_path = os.path.join(input_folder_path, filename)
    convert_txt_to_tsv(input_file_path, output_folder_path)