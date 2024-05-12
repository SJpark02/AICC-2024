import os

# Define the directory containing the original files and the directory to store results
input_directory = '스크립트 완료한 data folder path'
output_directory = '타임스탬프 및 특수문자 제거한 data folder path'

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

        # Process the text to remove timestamps and special characters, then join them into a single paragraph
        processed_text = []
        current_sentence = []

        for line in lines:
            if line.strip() and ':' in line[:5]:
                text_part = line[line.index('\n') + 1:].strip()
            else:
                text_part = line.strip()

            # Remove unwanted characters
            text_part = text_part.replace('>>>', '').replace('>>', '').strip()
            
            if text_part:
                current_sentence.append(text_part)

        if current_sentence:
            processed_text.append(' '.join(current_sentence))

        final_text = ' '.join(processed_text)

        # Save the processed text to a new file in the output directory using utf-8 encoding
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(final_text)

print("Processing complete. Cleaned files are saved in", output_directory)
