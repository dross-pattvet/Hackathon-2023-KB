def split_and_display_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        sections = content.split('\x0c')
        for section in sections:
            print(section)
            print('----------------------')  # Optional separator for clarity


# Example usage
split_and_display_text(r'IVUserManual/Table_of_contents.txt')