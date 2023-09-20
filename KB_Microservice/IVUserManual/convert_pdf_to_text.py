import os
import pdfplumber
import chardet


def save_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)



def convert_pdf2txt(src_dir, dest_dir):
    files = os.listdir(src_dir)
    files = [i for i in files if '.pdf' in i]
    for file in files:
        try:
            with pdfplumber.open(src_dir + file) as pdf:
                output = ''
                page_number = 1  # Initialize page number
                for page in pdf.pages:
                    text = page.extract_text()
                    print('text: ', text)
                    # if text is not None:
                        # # Detect and decode the encoding
                        # encoding = chardet.detect(text.encode())['encoding']
                        # print('encoding: ', encoding)
                        # decoded_text = text.encode(encoding).decode(encoding, errors='replace')
                        # output += decoded_text
                    output += text
                    output += f'\n\nNEW PAGE {page_number}\n\n'  # Include page number
                    page_number += 1  # Increment page number
                save_file(dest_dir + file.replace('.pdf', '.txt'), output.strip())
        except Exception as oops:
            print(oops, file)





if __name__ == '__main__':
    #convert_docx2txt('docx/', 'converted/')
    convert_pdf2txt('IVUserManual/', 'IVUserManual/converted/')
    
    
# import PyPDF2

# def convert_pdf_to_text(pdf_path, text_path):
    # with open(pdf_path, 'rb') as pdf_file:
        # pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        # with open(text_path, 'w', encoding='utf-8') as text_file:
            # print('pages: ', pdf_reader.pages)
            # for page_num in range(len(pdf_reader.pages)):
                # page = pdf_reader.pages[page_num]
                # print('page: ', page_num)
                # text_file.write(page.extract_text())

    # print('PDF converted to text successfully!')

# # Usage example
# pdf_path = r'C:\Users\dross\Documents\IntraVet Knowledge Base\IntraVet_Users_Manual_PROOFED_by_CB_8_20_2018.pdf'  # Replace with the path to your PDF file
# text_path = r'C:\Users\dross\Documents\IntraVet Knowledge Base\text\IntraVet_Users_Manual_PROOFED_by_CB_8_20_2018.txt'  # Replace with the desired path for the output text file

# if __name__ == "__main__":    
    # convert_pdf_to_text(pdf_path, text_path)