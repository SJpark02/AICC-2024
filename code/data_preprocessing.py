import os
import re

def clean_text(text):
    # Regex pattern to remove special characters except periods (.)
    # It specifically targets musical note symbols (♪) and other unwanted non-alphanumeric symbols
    pattern = re.compile(r'[^\w\s\.]|[\u266A]', re.UNICODE)  # Keeps periods, removes musical notes and other non-word, non-space characters
    # Convert text to lowercase before removing unwanted characters
    cleaned_text = pattern.sub('', text.lower())
    return cleaned_text

# Define the directory containing the original files and the directory to store results
input_directory = '2024_stt'
output_directory = '2024_stt_result'

# Create the output directory if it does not exist
os.makedirs(output_directory, exist_ok=True)

# Process each file in the input directory
for filename in os.listdir(input_directory):
    if filename.endswith('.txt'):  # Ensure to process only text files
        file_path = os.path.join(input_directory, filename)
        output_file_path = os.path.join(output_directory, filename)

        # Read the content of the file with utf-8 encoding
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # Process the text to remove timestamps, special characters including musical notes, then join them into a single paragraph
        processed_text = []
        current_sentence = []

        for line in lines:
            if line.strip() and ':' in line[:5]:
                text_part = line[line.index('\n') + 1:].strip()
            else:
                text_part = line.strip()

            # Remove '>>>', '>>', and additional special characters including musical notes but preserve periods
            # Convert to lowercase
            text_part = clean_text(text_part.replace('>>>', '').replace('>>', '').strip())
            
            if text_part:
                current_sentence.append(text_part)

        if current_sentence:
            processed_text.append(' '.join(current_sentence))

        final_text = ' '.join(processed_text)

        # Save the processed text to a new file in the output directory using utf-8 encoding
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(final_text)

print("Processing complete. Cleaned files are saved in", output_directory)
