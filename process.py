import PyPDF2  


def process_pdf(file_path):
    # Open the PDF file  
    pdf_file = open(file_path, 'rb')  
    
    # Create a PDF reader object  
    pdf_reader = PyPDF2.PdfFileReader(pdf_file)  
    
    # Get the total number of pages in the PDF  
    num_pages = pdf_reader.numPages  
    print(f"Total pages: {num_pages}")  
    
    # Extract text from each page  
    for page in range(num_pages):  
        pdf_page = pdf_reader.getPage(page)  
        text = pdf_page.extractText()  
        print(f"Page {page + 1}:\n{text}\n")  
    
    # Close the PDF file  
    pdf_file.close()  
