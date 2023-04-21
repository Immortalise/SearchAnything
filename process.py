import PyPDF2  
from pdfminer.high_level import extract_metadata  
from pdfminer.pdfparser import PDFParser  
from pdfminer.pdfdocument import PDFDocument  
from utils import encode_text


def process_file(file_path, tokenizer, model):
    if file_path.endswith(".pdf"):
        process_pdf(file_path, tokenizer, model)
    else:
        print("File type not supported.")


def process_pdf(pdf_file_path, tokenizer, model):
    line_list = []
  
    # Extract metadata  
    with open(pdf_file_path, 'rb') as file:  
        parser = PDFParser(file)  
        document = PDFDocument(parser)  
        metadata = extract_metadata(document)  
    
    pdf_title = metadata['title'] if 'title' in metadata else None  
    pdf_author = metadata['author'] if 'author' in metadata else None   
    
    # Extract text content and track the corresponding page for each line  
    with open(pdf_file_path, 'rb') as file:  
        reader = PyPDF2.PdfFileReader(file)  
        num_pages = reader.numPages  
        
        for page_num in range(num_pages):  
            page = reader.getPage(page_num)  
            text = page.extract_text()  

            # Split text into lines and store them with their corresponding page number  
            lines = text.splitlines()  
            for line in lines:
                file_dict = {}
                file_dict['title'] = pdf_title
                file_dict['author'] = pdf_author
                file_dict['page'] = page_num + 1 
                file_dict['content'] = line
                file_dict['embedding'] = encode_text(tokenizer, model, line)

                line_list.append(file_dict)
    
    return file_dict
