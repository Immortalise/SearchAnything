from pathlib import Path
from typing import List, Tuple, Dict
from collections import defaultdict
import sys
import os
import io
import re
import fitz
import nltk
from nltk.tokenize import sent_tokenize

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from .parser_base import BaseParser
from utils import encode_text

nltk.download("punkt")


class PDFParser(BaseParser):
    """
    Parser for PDF files
    """
    type = 'pdf'
    def __init__(self, file_path: str=None, model=None, out_path: str=None) -> None:
        super().__init__(file_path, model, out_path)
        
    def parse(self) -> List[Dict]:
        page_sents = self._to_sentences()
        if not page_sents:
            return None
        
        self.parse_output = []
        for pageno, sents in page_sents:
            for sent in sents:
                file_dict = {}
                file_dict['title'] = self.metadata["title"]
                file_dict['author'] = self.metadata["author"]
                file_dict['page'] = pageno
                file_dict['content'] = sent
                file_dict['embedding'] = encode_text(self.model, sent)
                file_dict['file_path'] = self.file_path
                file_dict['subject'] = self.metadata["subject"]
                
                self.parse_output.append(file_dict)
        
        return self.parse_output

    def _to_sentences(self) -> List[Tuple[int, str]]:
        """
        Parse PDF file to text [(pageno, sentence)]
        """
        if not self._check_format():
            self.parse_output = None
            return []

        pdf_doc: fitz.Document = fitz.open(self.file_path)
        
        raw_text: str = ""
        page_text: List(int, str) = []
        for pageno, page in enumerate(pdf_doc):
            page: fitz.Page
            raw_text = page.get_text("text")
            # remove hyphens 
            raw_text = re.sub(r"-\n(\w+)", r"\1", raw_text)
            raw_text = raw_text.replace("\n", " ")
            page_text.append((pageno + 1, raw_text))

        page_sents = map(lambda x: (x[0], sent_tokenize(x[1])), page_text)
        return page_sents
    
    @property
    def metadata(self) -> defaultdict:
        if not self._metadata:
            metadata = defaultdict(str)
            pdf_doc: fitz.Document = fitz.open(self.file_path)

            for k in pdf_doc.metadata.keys():
                metadata[k] = pdf_doc.metadata[k]
            
            self._metadata = metadata
        
        return self._metadata


    def _check_format(self) -> bool:
        f_path: Path = Path(self.file_path)
        return f_path.exists() and f_path.suffix == '.pdf'


if __name__ == "__main__":
    parser = PDFParser(sys.argv[1], None)
    parser._to_sentences()
    # print(parser.parse_output)
    parser.parse()