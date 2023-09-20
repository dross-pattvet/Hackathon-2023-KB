import os

def split_and_save_file_content(file_path, output_folder):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    split_content = content.split('\n\n\n')

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Save each segment as a new file
    for i, segment in enumerate(split_content, start=1):
        # Generate the new file name with a three-digit suffix
        new_file_name = f'{i:03}.txt'
        new_file_path = os.path.join(output_folder, new_file_name)
        
        with open(new_file_path, 'w', encoding='utf-8') as new_file:
            new_file.write(segment)


file_path = r'C:\Users\dross\Documents\IntraVet Knowledge Base\IntraVet_Users_Manual_PROOFED_by_CB_8_20_2018.txt'
output_folder = r'C:\Users\dross\Documents\IntraVet Knowledge Base\split'

split_and_save_file_content(file_path, output_folder)
