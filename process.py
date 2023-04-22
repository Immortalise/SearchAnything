from pypdf import PdfReader
from utils import encode_text


def process_file(file_path, tokenizer, model):
    if file_path.endswith(".pdf"):
        return process_pdf(file_path, tokenizer, model)
    else:
        print("File type not supported.")


def process_pdf(pdf_file_path, tokenizer, model):
    line_list = []
  
    reader = PdfReader(pdf_file_path)
    meta = reader.metadata

    # All of the following could be None!
    pdf_title = meta.title
    pdf_author = meta.author
    pdf_subject = meta.subject
            
    for page_num, page in enumerate(reader.pages):

        text = page.extract_text()

        # Split text into lines and store them with their corresponding page number  
        raw_lines = text.splitlines()
        
        raw_lines = [raw_line.lower() for raw_line in raw_lines]

        contains_references = any(raw_line == 'references' for raw_line in raw_lines)

        if contains_references:
            raw_lines = raw_lines[:raw_lines.index('references')]
        
        concatenated_string = ' '.join(raw_lines)
        concatenated_string.replace("- ", "")


        lines = concatenated_string.split('\n')

        for line in lines:
            print(line)

            file_dict = {}
            file_dict['title'] = pdf_title
            file_dict['author'] = pdf_author
            file_dict['page'] = page_num + 1
            file_dict['content'] = line
            file_dict['embedding'] = encode_text(tokenizer, model, line)
            file_dict['file_path'] = pdf_file_path
            file_dict['subject'] = pdf_subject

            line_list.append(file_dict)

        if contains_references:
            break

    return line_list
