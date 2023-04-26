from pypdf import PdfReader
import markdown  
from bs4 import BeautifulSoup 

from utils import encode_text


def process_file(file_path, file_type, tokenizer, model):
    if file_type == "pdf":
        return process_pdf(file_path, tokenizer, model)
    elif file_type == "md":
        return process_markdown(file_path, tokenizer, model)
    elif file_type == "txt":
        return process_text(file_path, tokenizer, model)
    else:
        print("File type not supported.")


def process_text(txt_file_path, tokenizer, model):  
    line_list = []  
  
    with open(txt_file_path, 'r', encoding='utf-8') as txt_file:  
        lines = txt_file.readlines()  
  
    for line_num, line in enumerate(lines):  
        print(line.strip())  
  
        file_dict = {}  
        file_dict['title'] = None  # Text files don't have built-in metadata like PDFs  
        file_dict['author'] = None  
        file_dict['page'] = None  
        file_dict['content'] = line.strip()  
        file_dict['embedding'] = encode_text(tokenizer, model, line.strip())  
        file_dict['file_path'] = txt_file_path  
        file_dict['subject'] = None  
  
        line_list.append(file_dict)  
  
    return line_list  

  
def process_markdown(md_file_path, tokenizer, model):  
    line_list = []  
  
    with open(md_file_path, 'r', encoding='utf-8') as md_file:  
        md_content = md_file.read()  
  
    html_content = markdown.markdown(md_content)  
    soup = BeautifulSoup(html_content, 'html.parser')  
    text = soup.get_text()  
  
    # Split text into lines  
    lines = text.splitlines()  
  
    for line_num, line in enumerate(lines):  
        print(line)  
  
        file_dict = {}  
        file_dict['title'] = None  # Markdown files don't have built-in metadata like PDFs  
        file_dict['author'] = None  
        file_dict['page'] = None  
        file_dict['content'] = line  
        file_dict['embedding'] = encode_text(tokenizer, model, line)  
        file_dict['file_path'] = md_file_path  
        file_dict['subject'] = None  
  
        line_list.append(file_dict)  
  
    return line_list  


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
            if raw_lines == "":
                break
        
        concatenated_string = ' '.join(raw_lines)
        concatenated_string = concatenated_string.replace("- ", "")
        words = concatenated_string.split(" ")

        max_length = 100

        lines = [words[i:i+max_length] for i in range(0, len(words), max_length)]

        for line in lines:
            if len(line) < 3:
                continue

            line = ' '.join(line)
            print(line)
            print()

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
