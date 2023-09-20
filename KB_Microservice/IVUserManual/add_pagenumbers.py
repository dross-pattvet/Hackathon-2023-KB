import os

def replace_FF_with_page_number(filename):
    folder_name = "AddedPages"
    os.makedirs(folder_name, exist_ok=True)

    with open(filename, 'r', encoding='utf-8') as file:
        text = file.read()

    page_number = 3

    while '\x0C' in text:
        text = text.replace('\x0C', f'\n\n<<NEW PAGE {page_number}>>\n\n', 1)
        page_number += 1

    new_filename = os.path.join(folder_name, os.path.basename(filename))
    with open(new_filename, 'w', encoding='utf-8') as file:
        file.write(text)

# Example usage
replace_FF_with_page_number(r'IVUserManual/IntraVet_Users_Manual_PROOFED_by_CB_8_20_2018.txt')