import os
import json


def extract_sections(json_file, text_file):
    # Read the JSON file
    with open(json_file, 'r', encoding='utf-8') as f:
        toc = json.load(f)
    
    # Read the main text file
    with open(text_file, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Create a 'sections' folder if it doesn't exist
    if not os.path.exists('sections'):
        os.makedirs('sections')
    
    # Iterate over each section in the table of contents
    for i, section in enumerate(toc):
        content = section['content']
        page = section['page']
        
        # Find the start and end positions of the section in the text file
        start_marker = '<<NEW PAGE {}>>'.format(page)
        print("start_marker: ", start_marker)
        # Determine the end marker based on the next section page
        if i < len(toc) - 1:
            next_page = toc[i + 1]['page']
            if page == next_page:
                end_marker = '<<NEW PAGE'
            else:
                end_marker = '<<NEW PAGE {}>>'.format(next_page)
        else:
            end_marker = '<<NEW PAGE'
        
        print("end_marker: ", end_marker)
        
        start_pos = text.find(start_marker) + len(start_marker)
        end_pos = text.find(end_marker, start_pos)
        
        print('positions: ', start_pos, end_pos)
        
        # continue
        
        # Extract the section content
        section_content = text[start_pos:end_pos].strip()
        # print('section: ', section_content)
                
        
        # Save the section content to a new file in the 'sections' folder
        # filename = os.path.join('sections', content.replace('/', '_').replace(':', '_') + '.txt')
        # with open(filename, 'w', encoding='utf-8') as f:
            # f.write(section_content)
        
        # Save the section content to multiple files in the 'sections' folder
        chunk_size = 5000
        chunks = [section_content[i:i + chunk_size] for i in range(0, len(section_content), chunk_size)]
        
        for j, chunk in enumerate(chunks):
            # Create the filename with an increasing suffix number
            suffix = str(j + 1)
            filename = os.path.join('sections', '{}_{}.txt'.format(content.replace('/', '_').replace(':', '_'), suffix))
            
            # Save the chunk to a new file
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(chunk) 

# Usage example 
extract_sections(r'C:\KB_microservice\IVUserManual\Table_of_contents.json', r'C:\KB_microservice\AddedPages\IntraVet_Users_Manual_PROOFED_by_CB_8_20_2018.txt')
