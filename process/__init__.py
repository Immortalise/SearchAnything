from pathlib import Path
from typing import Any, List
from .parser_base import BaseParser
from .pdfparser import PDFParser
from .docparser import WordParser
from .pptparser import PPTXParser

parsers: List[BaseParser] = [PDFParser, WordParser, PPTXParser]


def _get_parser(file_type: str) -> BaseParser:
    for parser in parsers:
        if parser.type == file_type:
            return parser
    return None


def process_file(file_path: str, file_type: Any, model: Any):
    fpath = Path(file_path)
    ftype = file_type if file_type is not None else fpath.suffix.strip('.')
    
    parser = _get_parser(ftype)
    if not parser:
        return None
    
    return parser(file_path, model, None).parse()