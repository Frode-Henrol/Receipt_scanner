import os

# Function to replace Danish characters and remove duplicates from a text file
def remove_duplicates_and_replace_chars(input_file, output_file):
    try:
        # Read the file and collect unique lines
        with open(input_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # Replace Danish characters and remove duplicates
        processed_lines = []
        for line in lines:
            line = line.lower()
            # Replace Danish characters
            replaced_line = (
                line.replace('æ', 'a')
                    .replace('ø', 'o')
                    .replace('å', 'a')
            )
            if replaced_line not in processed_lines:
                processed_lines.append(replaced_line)

        # Write the processed lines to the output file
        with open(output_file, 'w', encoding='utf-8') as file:
            file.writelines(processed_lines)

        print(f"Duplicates removed and Danish characters replaced. Cleaned content saved to '{output_file}'")

    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Specify input and output file paths
input_file = os.path.join(os.getcwd(), "data", 'madvarer_mk1.txt')  # Replace with your input file path
output_file = os.path.join(os.getcwd(), "data", 'madvarer_mk1_nodub.txt')  # Replace with your desired output file path

# Run the function
remove_duplicates_and_replace_chars(input_file, output_file)