from pathlib import Path
from typing import List
import sys
import io
import re
import fitz
import nltk
from nltk.tokenize import sent_tokenize

from parser import Parser

nltk.download("punkt")


class PDFParser(Parser):
    """
    Parser for PDF files
    """
    def __init__(self, file_path: str, out_path: str) -> None:
        super().__init__(file_path, out_path)
    
    def parse_to_text(self) -> List[str]:
        """
        Parse PDF file to text
        """
        if not self._check_format():
            self.parse_output = None
            return []

        pdf_doc: fitz.Document = fitz.open(self.file_path)
        raw_text: str = ""
        for page in pdf_doc:
            page: fitz.Page
            raw_text += page.get_text("text")
        # remove hyphens 
        raw_text = re.sub(r"-\n(\w+)", r"\1", raw_text)
        raw_text = raw_text.replace("\n", " ")

        sentences = sent_tokenize(raw_text)
        self.parse_output = sentences
        return sentences
        
    def _check_format(self) -> bool:
        f_path: Path = Path(self.file_path)
        return f_path.exists() and f_path.suffix == '.pdf'


if __name__ == "__main__":
    parser = PDFParser(sys.argv[1], None)
    parser.parse_to_text()
    print(parser.parse_output)